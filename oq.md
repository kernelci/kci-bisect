# Open Questions

Design questions that are not yet resolved. Each should either become a
decision recorded in `docs/<file>` or be closed as out-of-scope.

## Scope & Semantics

1. What are the "fixed scope" dimensions of a bisection campaign for each failure type?
   Performance regressions need SUT profile, workload, metric, and repetition structure held constant.
   Build failures need arch, defconfig, toolchain.
   What is the minimum common set, and what is type-specific?

2. Shared Decision Engine interface for binary signals (build/boot/test failures)
  and continuous metrics (performance), or two strategies behind one interface?

3. Keep `skip` and `weak` as distinct step outcomes, or collapse to `git bisect`'s single `skip`?
   They drive different follow-ups: skip advances the search; weak suggests re-test.

4. What counts as "triggering evidence" generically? A regression classification, a first-red build,
   a user-filed bug?

## Git & Commit Selection

1. How to handle non-linear git history (merge commits)?
2. Cherry-picks and rebases: the "same" change has different SHAs across trees. How does the cache disambiguate?
3. What is the source-tree state for the cache key — commit alone, or commit plus applied patches / reverts?

## Flakiness & Reliability

1. How to handle flaky / intermittent test failures? N-of-M retry, statistical test, re-run on different hardware?
2. Who owns flakiness mitigation — Decision Engine, Scheduler, or Test step?
3. What timeout and resource-budget policy per build, per test, and per bisection campaign?

## State & Resumability

1. Which backend(s) to support first — local JSON, SQLite, KCIDB?
2. How is a step represented when the process crashes mid-run?

## Concurrency

1. N-bisect implies parallel build+test; who schedules, reconciles partial failures, and decides when
   enough evidence is in?
2. Upper bound on parallelism and interaction with cache warming?

## Verification

1. Is "revert and retest" the only strategy?
   Candidates: re-test on different hardware, statistical re-test for flakes, apply-on-known-good 
   to confirm the change introduces the failure.

## Integration

1. How are credentials / secrets for backend APIs (LAVA, Maestro, KCIDB, mail servers) handled?
2. What is the minimal generic input contract (good commit, bad commit, build command, test command,
   decision engine config) that works without KernelCI?

## Reporting

1. Is the kernel-specific recipient resolution (`get_maintainers.pl`, commit trailers, Lore mbox) part
   of the core or an integration plugin?
