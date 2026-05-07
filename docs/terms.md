# Terms

Foundation of the documentation. Every other document in this repository uses these terms with the meanings defined here.

## Core

- **Regression** — a change in observed kernel behaviour from passing to failing, or from a known metric baseline to a worse value. Detected before bisection starts.
- **Bisection** — binary search applied to kernel commits to identify the change that introduced a regression.
- **Culprit** — the commit identified by bisection as introducing the regression.
- **Bisection campaign** (campaign) — one attempt to identify the culprit by bisection.
- **Bisection step** (step) — one tested build inside a campaign.
- **Triggering evidence** — the record(s) that justify starting a campaign: a detected regression, a first bad build, a filed bug.
- **Verification** — re-confirming a campaign's conclusion, typically by reverting the culprit and retesting.

## Git history

- **git bisect** — the binary-search command provided by `git` over commit history.
- **n-bisect** — generalisation that tests N evenly-spaced commits per iteration instead of a single midpoint, trading parallel resources for fewer iterations.
- **Midpoint** — the commit selected to test next in standard bisect workflow.
- **Commit range** — the commits between the current _good_ and _bad_ boundaries, exclusive of the good boundary.
- **Linear history** — a commit history _without merge commits_; the case bisect assumes.
- **Non-linear history** — a commit history _containing merge commits_ or _cherry-picks_, which complicate commit selection.

## Search boundaries

- **Good boundary** — the most recent commit known to behave correctly under the campaign scope. Equivalent to `git bisect good`.
- **Bad boundary** — the earliest commit known to exhibit the regression under the campaign scope. Equivalent to `git bisect bad`.
- **Narrowed range** — the narrower commit range a campaign converges to when it cannot pin a single culprit.

## Scope

- **Campaign scope** — the fixed dimensions held constant across all steps of one campaign so the *kernel commit is the only changing variable*. The applicable dimensions depend on the failure type.
- **Build provenance** — the concrete (commit, arch, defconfig, toolchain, compiler version) tuple identifying one build.
- **SUT** (system under test) — the hardware or VM profile a test runs on. Part of campaign scope for boot, test, and performance failures.
- **Workload** — the program or benchmark exercised during a performance test; part of campaign scope for performance.
- **Repetition structure** — how many times a measurement is repeated and how repeats are aggregated; part of campaign scope for performance.

## Evidence and decision

- **Signal** — a structured fact extracted from build or test output (pass/fail flag, error signature, measured metric). Carries no judgement.
- **Decision strategy** — how a step decision is derived from signals:
  - **binary** — presence or absence of an error signature.
  - **threshold / statistical** — comparison of a continuous metric, typically over repetitions.
- **Step decision** — the result recorded for a step. One of:
  - `good` — tested build does not exhibit the regression.
  - `bad` — tested build exhibits the regression.
  - `skip` — cannot test at this commit (e.g. pre-existing build break). Advances the search to a different commit.
  - `weak` — tested but evidence uncertain (noise, partial data). Suggests re-test rather than skipping.
- **Rationale** — the recorded reason for a step decision: which signals supported `good`/`bad`, which failure caused `skip`, which uncertainty caused `weak`.

## Outcomes

A campaign concludes in one of these categories:

- **Single culprit identified** — one culprit found.
- **Narrowed range** — campaign produced a narrowed range without pinning a culprit.
- **Unresolved** — evidence inconsistent or incomplete.
- **Not confirmed** — the originally suspected regression was not reproduced under the fixed campaign scope.

## Building blocks

- **Bisection loop** — drives the search and step lifecycle.
- **Commit selector** — chooses the next commit(s) to test.
- **Build step** — produces a kernel build for a given commit.
- **Build cache** — checks whether a build already exists before building.
- **Test step** — runs a test against a built kernel.
- **Result parser** — extracts signals from raw output. Produces no decision.
- **Decision engine** — applies a decision strategy to map signals to a step decision. Separated from the Result parser so decision rules can evolve independently of signal extraction.
- **Verify step** — confirms a campaign's culprit by an independent check, typically reverting the culprit and retesting.
- **Report generator** — produces a bisection report (culprit, verification, log, etc).
- **Recipient finder** — determines who to notify.
- **Report sender** — delivers the report.
- **State store** — persists campaigns and steps.

## External tools

- **TuxMake** — reproducible kernel build tool; one Build step backend.
- **TuxRun** — QEMU-based test runner; one Test step backend.
- **LAVA** — hardware test lab; one Test step backend.
- **logspec** — error-signature matching library used by the Result parser.
- **KernelCI** — CI ecosystem this toolbox can integrate with.
- **Maestro** — KernelCI's pipeline service; integration point for build/test execution and regression triggers.
- **KCIDB** — KernelCI's results database; possible State store backend and source of historical results.
- **kci-dev** — developer-facing CLI in the KernelCI ecosystem.
