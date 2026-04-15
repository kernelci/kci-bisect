VIXI Standalone Bisection
=========================

This is a snapshot of the
[VIXI](https://gitlab.com/gtucker.io/vixi/-/tree/5f998928f1a80aa9f99f306dee2b1cf6f3074981)
bisection feature to allow it to run as a standalone package.  It relies on a
Renelick API instance to be available with the test data as well as the
relevant schedulers to replay the tasks that produced the results in the first
place.  For more context, see the introductory [blog
post](https://gtucker.io/posts/2026-02-02-vixi-and-renelick/) about the VIXI
bisection feature in particular.

The Renelick config files need to have been adjusted to provide the API URL and
user account details.  Please refer to the [Renelick Quick-Start
Guide](https://renelick-gtucker-7b1c5d7d50ce51f57b4ff6327302e38a0a8f8c72d652a5.gitlab.io/quickstart/)
to set up a local instance.

## Sample run

The easiest way is to start an interactive shell in a container with Renelick
installed:

```
docker run -it \
  -v $HOME/.config/renelick:/home/renelick/.config/renelick \
  -v $PWD/contrib/vixi:/home/renelick/vixi \
  --entrypoint=bash \
  registry.gitlab.com/gtucker.io/renelick:main
```

Then check that it's all set up correctly:

```
renelick@2f71c29d6723:~$ rk hello
Connecting to https://renelick.gtucker.io
Renelick API 0.23.0
renelick@2f71c29d6723:~$ rk whoami
Connecting to https://renelick.gtucker.io (gtucker.io) as gtucker
Authentication method: Persistent API key
User profile:
  id             681dd2ff409e63a6dfd1f212
  username       gtucker
  email          <hidden>
  full_name      Guillaume Tucker
  is_superuser   False
  is_verified    True
```

To start a bisection, run the `vixi.main` module with the node ID containing
the regression data (here a build failure):

```
renelick@2f71c29d6723:~$ python -m vixi.main 69ae9d03b5f0d51ab9db9886
Delta node: 69ae9d03b5f0d51ab9db9886
Test:     kunit:exec:break
Tree:     next
URL:      https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
Revision: 44982d352c33767cd8d19f8044e7e1161a587ff7
Path:     workspace/src/next.git
New checkout, mirror: mirror/next.git
Cloning into bare repository 'workspace/src/next.git'...
info: Could not add alternate for 'mirror/next.git': reference repository 'mirror/next.git' is not a local repository.
POST git-upload-pack (175 bytes)
POST git-upload-pack (gzip 50002 to 25100 bytes)
remote: Enumerating objects: 11731152, done.
remote: Counting objects: 100% (9936/9936), done.
remote: Compressing objects: 100% (3468/3468), done.
remote: Total 11731152 (delta 7738), reused 7842 (delta 6457), pack-reused 11721216 (from 1)
Receiving objects: 100% (11731152/11731152), 3.26 GiB | 36.73 MiB/s, done.
Resolving deltas: 100% (9643384/9643384), done.
Checking objects: 100% (33554432/33554432), done.
User:     VIXI
Email:    <hidden>
Remote repositories:
origin	https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git (fetch)
origin	https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git (push)
From https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next
 * branch                      44982d352c33767cd8d19f8044e7e1161a587ff7 -> FETCH_HEAD
3.7G	workspace/src/next.git
Checking bad revision: next-20260219
Checking good revision: v6.19-418-gd08008f19610
Good revision check failed, aborting
```

In this case, the check for the "good" revision failed as this was an
intermittent failure so it stopped before starting the actual bisection.  This
is a random example for illustrative purposes, the VIXI demos and blog posts
showcase the whole bisection process.

The Delta node looks like this:

```
$ rk node get 69ae9d03b5f0d51ab9db9886
```
``` json
{
  "id": "69ae9d03b5f0d51ab9db9886",
  "name": "exec:break",
  "lineage": [
    "69ae9b54b5f0d51ab9db986b",
    "69ae9bbdb5f0d51ab9db9879",
    "69ae9cf3b5f0d51ab9db987e",
    "69ae9cfab5f0d51ab9db9882",
    "69ae9cfab5f0d51ab9db9885",
    "69ae9d03b5f0d51ab9db9886"
  ],
  "path": [
    "next:next-20260219:checkout",
    "next:next-20260219:build",
    "next:next-20260219:exec",
    "kunit",
    "exec",
    "exec:break"
  ],
  "created": "2026-03-09T10:12:19.417000",
  "owner": {
    "email": "<hidden>",
    "username": "vixi",
    "full_name": "VIXI Service Account"
  },
  "parent": "69ae9cfab5f0d51ab9db9885",
  "kind": "vixi.delta",
  "data": {
    "category": "break",
    "root": "kunit",
    "path": [
      "kunit",
      "exec"
    ],
    "old": {
      "id": "69ade539b5f0d51ab9db9869",
      "revision": {
        "sha1": "d08008f196107a80c4e88b866d594b88a56ceaa9",
        "describe": "v6.19-418-gd08008f19610",
        "subject": "Merge tag 'asoc-fix-v7.0-merge-window' of https://git.kernel.org/pub/scm/linux/kernel/git/broonie/sound into for-linus",
        "tree": "next",
        "url": "https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
        "digest": "c6d8a2ecc49764634ae62adef983f1da60daa442016826b82e39364ac4135ec1",
        "patches": []
      },
      "params": {
        "arch": "x86_64",
        "defconfig": "defconfig",
        "opts": "",
        "cc": "gcc",
        "ccver": "15.2",
        "ccarch": "-x86"
      },
      "result": "skip"
    },
    "new": {
      "id": "69ae9cfab5f0d51ab9db9885",
      "revision": {
        "sha1": "44982d352c33767cd8d19f8044e7e1161a587ff7",
        "describe": "next-20260219",
        "subject": "Add linux-next specific files for 20260219",
        "tree": "next",
        "url": "https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git",
        "digest": "dea66623c706f5ceec19b272d0e7d684c57674e8d1d3e758ac595550180df546",
        "patches": []
      },
      "params": {
        "arch": "x86_64",
        "defconfig": "defconfig",
        "opts": "",
        "cc": "gcc",
        "ccver": "15.2",
        "ccarch": "-x86"
      },
      "result": "fail"
    }
  },
  "task": {
    "name": "delta",
    "attributes": {
      "parent": "69ae9cfab5f0d51ab9db9882",
      "orch": "vixi"
    },
    "scheduler": "inline-vixi",
    "id": "97de1b1f-0c29-4c3d-82e8-5add613d9691",
    "timeout": "2026-03-09T10:42:18.182000"
  }
}
```

The monitor log shows all the individual steps with each task run in Tekton,
the nodes with artifacts that have been uploaded to storage and test results:

```
I  2026-04-15T09:20:01.003075+00:00 VIXI   bisect        next-20260219                         check:bad           44982d352c33767cd8d19f8044e7e1161a587ff7
I  2026-04-15T09:20:01.495026+00:00 TASK   add           6da4069b-8c28-46e5-b873-68898859f72c  tekton              kunit
I  2026-04-15T09:20:01.499106+00:00 TASK   receive       6da4069b-8c28-46e5-b873-68898859f72c  tekton              kunit
I  2026-04-15T09:20:01.581683+00:00 TASK   ack           6da4069b-8c28-46e5-b873-68898859f72c  tekton              kunit
I  2026-04-15T09:20:46.725729+00:00 NODE   add           69df586e439e6d2244db1b54              vixi.kunit.step     next:next-20260219:checkout
I  2026-04-15T09:20:47.447791+00:00 NODE   add           69df586f439e6d2244db1b55              artifact-v1         checkout-script
I  2026-04-15T09:20:47.507896+00:00 NODE   add           69df586f439e6d2244db1b56              artifact-v1         checkout-log.txt
I  2026-04-15T09:23:08.490707+00:00 NODE   add           69df58fc439e6d2244db1b57              vixi.kunit.step     next:next-20260219:build
I  2026-04-15T09:23:09.232046+00:00 NODE   add           69df58fd439e6d2244db1b58              artifact-v1         defconfig
I  2026-04-15T09:23:09.503245+00:00 NODE   add           69df58fd439e6d2244db1b59              artifact-v1         bzImage
I  2026-04-15T09:23:09.660611+00:00 NODE   add           69df58fd439e6d2244db1b5a              artifact-v1         build-log.txt
I  2026-04-15T09:23:09.819542+00:00 NODE   add           69df58fd439e6d2244db1b5b              artifact-v1         build-script
I  2026-04-15T09:23:19.587216+00:00 NODE   add           69df5907439e6d2244db1b5c              vixi.kunit.step     next:next-20260219:exec
I  2026-04-15T09:23:20.232559+00:00 NODE   add           69df5908439e6d2244db1b5d              artifact-v1         exec-log.txt
I  2026-04-15T09:23:20.375474+00:00 NODE   add           69df5908439e6d2244db1b5e              artifact-v1         exec-script
I  2026-04-15T09:23:20.523697+00:00 NODE   add           69df5908439e6d2244db1b5f              artifact-v1         kunit.json
I  2026-04-15T09:23:26.412852+00:00 NODE   populate      69df590e439e6d2244db1b60              batch:1             kunit
I  2026-04-15T09:23:26.444230+00:00 TASK   complete      6da4069b-8c28-46e5-b873-68898859f72c  tekton              kunit
I  2026-04-15T09:23:27.284802+00:00 VIXI   bisect        next-20260219                         check:good          d08008f196107a80c4e88b866d594b88a56ceaa9
I  2026-04-15T09:23:27.758078+00:00 TASK   add           6eab2ea0-e74d-4cfb-bf25-0d7c24ad38ea  tekton              kunit
I  2026-04-15T09:23:27.762268+00:00 TASK   receive       6eab2ea0-e74d-4cfb-bf25-0d7c24ad38ea  tekton              kunit
I  2026-04-15T09:23:27.839841+00:00 TASK   ack           6eab2ea0-e74d-4cfb-bf25-0d7c24ad38ea  tekton              kunit
I  2026-04-15T09:23:56.136467+00:00 NODE   add           69df592c439e6d2244db1b64              vixi.kunit.step     next:v6.19-418-gd08008f19610:checkout
I  2026-04-15T09:23:56.904493+00:00 NODE   add           69df592c439e6d2244db1b65              artifact-v1         checkout-script
I  2026-04-15T09:23:57.016209+00:00 NODE   add           69df592d439e6d2244db1b66              artifact-v1         checkout-log.txt
I  2026-04-15T09:26:12.604086+00:00 NODE   add           69df59b4439e6d2244db1b67              vixi.kunit.step     next:v6.19-418-gd08008f19610:build
I  2026-04-15T09:26:13.291168+00:00 NODE   add           69df59b5439e6d2244db1b68              artifact-v1         defconfig
I  2026-04-15T09:26:13.742882+00:00 NODE   add           69df59b5439e6d2244db1b69              artifact-v1         bzImage
I  2026-04-15T09:26:13.901978+00:00 NODE   add           69df59b5439e6d2244db1b6a              artifact-v1         build-log.txt
I  2026-04-15T09:26:14.043943+00:00 NODE   add           69df59b6439e6d2244db1b6b              artifact-v1         build-script
I  2026-04-15T09:26:23.785862+00:00 NODE   add           69df59bf439e6d2244db1b6c              vixi.kunit.step     next:v6.19-418-gd08008f19610:exec
I  2026-04-15T09:26:24.515347+00:00 NODE   add           69df59c0439e6d2244db1b6d              artifact-v1         exec-log.txt
I  2026-04-15T09:26:24.683307+00:00 NODE   add           69df59c0439e6d2244db1b6e              artifact-v1         exec-script
I  2026-04-15T09:26:24.821468+00:00 NODE   add           69df59c0439e6d2244db1b6f              artifact-v1         kunit.json
I  2026-04-15T09:26:29.619191+00:00 NODE   populate      69df59c5439e6d2244db1b70              batch:1             kunit
I  2026-04-15T09:26:29.653359+00:00 TASK   complete      6eab2ea0-e74d-4cfb-bf25-0d7c24ad38ea  tekton              kunit
```
