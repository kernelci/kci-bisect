# SPDX-License-Identifier: MIT
#
# Copyright (C) 2025-2026 Guillaume Tucker

"""Simplified vixi.base module to provide dependencies for vixi.bisect"""

import os
import subprocess

TORVALDS = 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git'


def sh(cmd, cwd=None, **kwargs):
    """Run a shell command and return stdout

    The output of the command is returned in a string with any trainling
    newline stripped.  Any extra kwargs are passed on as Popen constructor
    arguments.  Raise a CalledProcessError if the command fails.
    """
    return subprocess.check_output(
        cmd.split(), cwd=cwd, **kwargs
    ).decode('utf-8').strip()


def shx(cmd, cwd=None, retcode=False, **kwargs):
    """Run a shell command and return stdout

    As a simpler version of sh(), run a command and raise a CalledProcessError
    if it fails or return the exit code if retcode is True.  Any extra kwargs
    are passed on as Popen constructor arguments.  The output is printed on
    stdout as-is.
    """
    return (
        subprocess.call(cmd.split(), cwd=cwd, **kwargs) if retcode
        else subprocess.check_call(cmd.split(), cwd=cwd, **kwargs)
    )


def checkout(sandbox, mirror, path, revspec, clean=False, gitonly=False):
    """Initialise or update a kernel checkout"""
    tree, url, rev = (revspec[key] for key in ('tree', 'url', 'rev'))
    print(f"Tree:     {tree}")
    print(f"URL:      {url}")
    print(f"Revision: {rev}")
    cwd = os.path.join(sandbox, path, tree)
    if gitonly is True:
        cwd += '.git'
    print(f"Path:     {cwd}", flush=True)
    if clean is True:
        print("Deleting any existing checkout", flush=True)
        shx(f'rm -rf {cwd}')
    if not os.path.exists(cwd):
        shx(f'mkdir -p {cwd}')
        mirror = os.path.join(mirror, f'{tree}.git')
        print(f"New checkout, mirror: {mirror}", flush=True)
        opts = '--bare' if gitonly else ''
        shx(f'git clone -v --reference-if-able={mirror} {opts} {url} {cwd}')
    print("User:     ", end='', flush=True)
    if shx('git config user.name', cwd, retcode=True) != 0:
        shx('git config user.name VIXI', cwd)
    print("Email:    ", end='', flush=True)
    if shx('git config user.email', cwd, retcode=True) != 0:
        shx('git config user.email vixi@renelick.org', cwd)
    print("Remote repositories:", flush=True)
    shx('git remote -v', cwd)
    shx(f'git fetch --tags --force origin {rev}', cwd)
    if not gitonly:
        shx('git reset --hard', cwd)
        if os.path.exists(os.path.join(cwd, '.git/rebase-apply')):
            print("Aborting previous mailbox patch")
            shx('git am --abort', cwd)
        shx('git checkout FETCH_HEAD', cwd)
        shx(f'git fetch --tags {TORVALDS}', cwd)
        print(sh('git log -n1', cwd), flush=True)
    shx(f'du -hs {cwd}')
    return cwd
