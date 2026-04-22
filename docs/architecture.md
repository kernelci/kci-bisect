# Architecture

**Status:** Draft — to be discussed at follow-up meeting.

## Design Principles

1. **Generic first** — components should work without KernelCI
2. **Composable** — building blocks that can be assembled differently
3. **Pluggable backends** — swap build/test/storage backends
4. **Reproducible** — deterministic builds and tests across bisection steps
5. **Reuse over reinvention** — wrap existing open-source tools
   (TuxMake, TuxRun, LAVA, git-bisect, logspec, ...) behind the
   component interfaces rather than reimplementing them. Define the
   interface first so tool choice stays swappable; contribute upstream
   over forking.

## Proposed Building Blocks

These are the components identified from existing implementations. The
interfaces and boundaries are TBD.

### Core

- **Bisection loop** — drives git bisect (or n-bisect), manages state,
  handles good/bad/skip decisions
- **Commit selector** — given a range, selects which commit(s) to test
  next (single midpoint for standard bisect, N evenly-spaced for n-bisect)

### Build

- **Build step** — triggers a kernel build for a given commit
  - Backends: TuxMake (local/container), Maestro /api/checkout, custom
- **Build cache** — checks whether a build already exists before building
  - Cache key: (commit, arch, defconfig, toolchain, config_full)

### Test

- **Test step** — runs a test against a built kernel
  - Backends: TuxRun (QEMU), LAVA (hardware), custom
- **Result parser** — extracts structured signals from test output
  (pass/fail flags, error signatures, measured metrics). Deterministic
  extraction only; no verdict.
  - Integration: logspec for error signature matching

### Decision Engine

- **Decision Engine** — maps parsed signals to a bisection verdict:
  `good` / `bad` / `skip` / `weak`. Separated from `Result parser` so that policy (thresholds, confidence, etc) can evolve independently of signal extraction.
  - Strategies:
    - **binary** — presence/absence of an error signature
      (build, boot, config, unit-test failures)
    - **threshold / statistical** — regression decision on a continuous
      metric, possibly over multiple repetitions (performance)
  - `skip` (cannot test at this commit, e.g. build broken pre-existing)
    is distinct from `weak` (tested but evidence uncertain)

### Reporting

- **Report generator** — produces bisection report (suspect commit,
  verification result, bisection log)
- **Recipient finder** — determines who to notify
  (get_maintainers.pl, commit trailers, Lore mbox lookup)
- **Report sender** — delivers the report (email, API, etc.)

### Verification

- **Verify step** — confirms the suspect commit by reverting and retesting

### State

- **State store** — persists bisection progress for auditability and
  resumability. Data model:
  - **Campaign** — one bisection investigation, bounded by a fixed
    scope and known good/bad boundaries
  - **Step** — one tested commit inside a campaign; records tested
    commit, build and test evidence, decision
    (`good` / `bad` / `skip` / `weak`), and rationale.
  - Backends: local file (JSON, SQLite), KCIDB, custom

## Integration Points

These are KernelCI-specific and should be separate from the generic core:

- [Maestro](https://docs.kernelci.org/components/maestro/) regression detection -> bisection trigger
- Maestro /api/checkout -> build + test execution
- KCIDB -> historical result lookup
- kci-dev CLI-> developer-facing interface

## Open Questions

List of open questions is tracked in [../oq.md](../oq.md).
