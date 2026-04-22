# Bisection Data Model

Reference data model for the State store (see [architecture.md](./architecture.md)).

Each bisection campaign fixes a set of dimensions so that the kernel commit is the only changing variable.
Which dimensions matter depends on the failure type:

| Failure type | Fixed-scope dimensions |
|---|---|
| Build | arch, defconfig, toolchain, compiler version |
| Boot | arch, defconfig, toolchain, device/VM |
| Config | arch, base defconfig, toolchain |
| Unit-test | arch, defconfig, toolchain, test suite, test case |
| Performance | SUT profile, workload config, measured workload, metric, repetition structure |

The model below uses "campaign-scope fields" to refer to whichever set of dimensions applies 
to the campaign's failure type.

## Records

Bisection defines the records used after regression detection to isolate the kernel change
that caused an observed regression. Bisection tests builds within a fixed comparability scope
until the regression is isolated to one culprit commit, narrowed to a range, or judged unresolved.

A `build` is a compiled snapshot of the kernel source at a specific commit with a specific
configuration and toolchain. Bisection tests builds, not source; the kernel commit is the only
intended changing variable across builds in one campaign.

### Bisection Campaigns

Bisection Campaign represents one bounded investigation for isolating a detected regression.

One bisection campaign starts from already detected and classified regression evidence or 
grouped case built from classified regressions.
This entry is the durable record of one bisection workflow, linking the triggering evidence,
the fixed scope, and the steps performed.

A bisection campaign may conclude in different ways. It may isolate one culprit build,
narrow the regression to a smaller commits range, remain unresolved because the evidence is 
inconsistent or incomplete, or end with the conclusion that the originally suspected regression
could not be reproduced under the fixed campaign scope.

The entry contains:

- `Bisection-campaign record ID`: one regression-isolation workflow.
- `Evidence links`: the records that caused the bisection campaign to start.
- `Campaign-scope fields`: the fixed dimensions for this campaign's failure type that must remain constant.
- `Search-boundary fields`: the known-good boundary, the known-bad boundary, and the search method.
- `Lifecycle fields`: the campaign status, start/end times, and the actor responsible for compaign.
- `Final-outcome fields`: the final conclusion of the campaign, including the outcome category (single culprit
    identified, narrowed range, unresolved, or original regression not confirmed), the culprit kernel reference
    when a single kernel is identified, and the narrowed good and bad boundary references when the outcome 
    is a narrowed range.
- `Bisection-step links`: the ordered tested steps that belong to that campaign.

### Bisection Steps

Bisection Step represents one tested build inside one bisection campaign.

Each step records the build that was tested (commit plus configuration
and toolchain), the evidence produced, and the decision derived from
that evidence. Steps form the ordered audit trail of one campaign.

A step does not have to end with a clean good-or-bad decision. Some steps are `skip` because the build
failed or could not run, and some are `weak` because the evidence is too noisy or incomplete.

The entry contains:

- `Bisection-step record ID`: one tested build inside one bisection campaign.
- `Bisection-campaign reference`: the campaign this step belongs to.
- `Step-order fields`: the order of the step inside the workflow and the position of the
   tested commit relative to the current search boundaries.
- `Kernel reference`: the kernel commit tested at that step.
- `Build reference`: the concrete build provenance (commit, arch, defconfig,
   toolchain) used for that tested step.
- `Step-evidence links`: the comparison and analysis records between the tested build and a reference build.
- `Step-decision result`: the step result: `good`, `bad`, `skip`, or `weak`.
- `Step-rationale fields`: why that result was recorded — which evidence supported `good`/`bad`,
   which failure caused `skip`, or which uncertainty caused `weak`.
