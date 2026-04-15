# SPDX-License-Identifier: MIT
#
# Copyright (C) 2025-2026 Guillaume Tucker

"""Entry point to run vixi.bisect as a standalone tool"""

import argparse
import os
from datetime import datetime, timedelta

import renelick
import renelick.client

from .bisect import Bisection


class ExtendedClient(renelick.client.Client):
    """Extended client features based on the Renelick API"""

    def __init__(self, *args, verbose=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._verbose = verbose

    def run_and_wait(self, **kwargs):
        """Schedule a Task with provided kwargs and wait for it to complete"""
        sub = self.api.event.subscribe('task')
        task = self.api.task.schedule(renelick.client.Task(**kwargs))
        task_id = str(task.id)
        if self._verbose:
            print(f"{task_id}  {task.name}  {task.scheduler}")
        status = None
        while status is None:
            ev = self.api.event.receive(sub)
            if ev.data['id'] == task_id:
                op = ev.data['op']
                if self._verbose:
                    print(f"{ev['time']}  {op}")
                if op == 'complete':
                    status = True
                elif op in {'abort', 'timeout'}:
                    status = False
        self.api.event.unsubscribe(sub)
        if status is not True:
            raise renelick.client.RenelickError("Task failed to run")
        return task

    def find_single_node(self, *fields):
        """Find a single node matching the provided fields"""
        found = self.api.node.find(fields)
        if len(found) != 1:
            raise renelick.client.RenelickError(
                f"Failed to find single node: {fields}, found: {len(found)}"
            )
        return found[0]

    def find_latest_node(self, *fields, do_raise=True):
        """Find the latest node matching the provided fields"""
        found = self.api.node.find(fields + ('created__sort=down',), limit=1)
        if len(found) == 1:
            return found[0]
        if do_raise is True:
            raise renelick.client.RenelickError(
                f"Failed to find latest node: {fields}"
            )
        return None

    def get_tasks_history(self, node):
        """Reconstruct the history of Tasks that were run to produce a node"""
        tasks = [current := node.task]
        while node.parent:
            node = self.api.node.get(node.parent)
            if node.task.id != current.id:
                tasks.append(current := node.task)
        return list(reversed(tasks))

    def replay_tasks(self, node, patch):
        """Replay the tasks that were required to produce a node

        The history of tasks from the lineage of the ``node`` object will be
        run with the same schedulers and attributes, relying on 'input-nodes'
        to find data nodes produced by the previous task in the chain.  Each
        task should also have a 'timeout-spec' attribute, otherwise the default
        is 90 minutes.

        Any attribute may be overridden using the provided ``patch``
        dictionary.  This only applies to attributes that already exist in a
        task to avoid adding additional ones which may lead to unexpected
        results.
        """
        replay = []
        run = None
        for task in self.get_tasks_history(node):
            attrs = task.attributes.to_dict()
            for key, value in patch.items():
                orig = attrs.get(key)
                if orig is not None:
                    attrs[key] = value
            timeout_spec = attrs.get('timeout-spec', {'minutes': 90})
            if run and (input_data := attrs.get('input-nodes')):
                for _, input_fields in input_data.items():
                    search_fields = input_fields.copy()
                    search_fields.pop('id')
                    search_fields['task.id'] = run.id
                    input_fields['id'] = self.find_single_node(tuple(
                        '='.join((str(key), str(value)))
                        for key, value in search_fields.items()
                    )).id
            run = self.run_and_wait(name=task.name,
                scheduler=task.scheduler,
                timeout=datetime.now() + timedelta(**timeout_spec),
                attributes=renelick.client.TaskAttributes.from_dict(attrs),
            )
            replay.append(run)
        return replay


if __name__ == '__main__':
    parser = argparse.ArgumentParser("VIXI standalone bisection")
    parser.add_argument(
        'delta',
        help="ID of the Delta with the regression"
    )
    parser.add_argument(
        '--workspace', default='workspace',
        help="Path to the inline runtime workspace"
    )
    parser.add_argument(
        '--mirror', default='mirror',
        help="Path to the Git kernel mirrors directory"
    )
    args = parser.parse_args()
    print(f"Delta node: {args.delta}")
    for dir_path in [args.workspace, args.mirror]:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    client = ExtendedClient()
    bisect = Bisection(client, args.delta, None)
    result = bisect.run(args.workspace, args. mirror)
    if result:
        revision = result.data['revision']
        print(f"Found commit: {revision['sha1']}  {revision['subject']}")
