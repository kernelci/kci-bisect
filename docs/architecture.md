# Architecture

**Status:** Draft — to be discussed at follow-up meeting.

## Design Principles

1. **Generic first** — components should work without KernelCI
2. **Composable** — building blocks that can be assembled differently
3. **Pluggable backends** — swap build/test/storage backends
4. **Reproducible** — deterministic builds and tests across bisection steps

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
- **Result parser** — determines pass/fail from test output
  - Integration: logspec for error signature matching

### Reporting

- **Report generator** — produces bisection report (suspect commit,
  verification result, bisection log)
- **Recipient finder** — determines who to notify
  (get_maintainers.pl, commit trailers, Lore mbox lookup)
- **Report sender** — delivers the report (email, API, etc.)

### Verification

- **Verify step** — confirms the suspect commit by reverting and retesting

## Integration Points

These are KernelCI-specific and should be separate from the generic core:

- Maestro regression detection → bisection trigger
- Maestro /api/checkout → build + test execution
- KCIDB → historical result lookup
- kci-dev CLI → developer-facing interface

## Open Questions

- How to handle non-linear git history (merge commits)?
- How to handle flaky/intermittent test failures?
- What state needs to be persisted for resumable bisections?
- Align with Guillaume's Renelec/Vixie framework?
