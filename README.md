# kci-bisect

A generic toolbox for automated Linux kernel bisection.

This project provides composable building blocks for bisecting kernel
regressions — build failures, boot failures, and test failures. The
components are designed to be usable standalone or integrated into CI
systems such as [KernelCI](https://kernelci.org).

## Status

**Early development.** We are collecting existing bisection scripts and
tools from multiple organisations and refactoring them into reusable
components. Contributions are welcome.

## Goals

- Generic bisection framework not tied to any single CI system
- Composable building blocks: build, test, cache, result parsing, reporting
- Support for reproducible builds ([TuxMake](https://tuxmake.org)) and
  tests ([TuxRun](https://tuxrun.org))
- Pluggable backends for build and test execution
- Usable both as a CLI tool and as a library

## Repository structure

```
kci-bisect/
├── contrib/           # Existing scripts from contributors (as-is)
├── docs/              # Design documents and architecture notes
└── COPYING            # LGPL-2.1
```

## Contributing

We are actively looking for existing bisection scripts, wrappers, and
tools. Please drop them into `contrib/` with a short README describing
what they do and how they work.

See the [GitHub issues](../../issues) for the current roadmap and
discussion topics.

## Licence

LGPL-2.1 — see [COPYING](COPYING).
