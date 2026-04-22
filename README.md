# kci-bisect

A generic toolbox for automated Linux kernel bisection.

This project provides composable building blocks for bisecting kernel issues of
the different types, for example:

- build failures
- boot failures
- configuration failures
- unit test failures
- performance regressions

The components are designed to be usable standalone or integrated into CI
systems such as [KernelCI](https://kernelci.org).

## Status

**Early development.** We are collecting existing bisection tools and
approaches from multiple organisations and refactoring them into reusable
components. Contributions are welcome.

## Goals

- Generic bisection framework
- Composable building blocks: 
  - build
  - test
  - cache
  - results parsing
  - results verification
  - results analysis
  - reporting
- Support for reproducible builds ([TuxMake](https://tuxmake.org)) and
  tests ([TuxRun](https://tuxrun.org))
- Pluggable backends for build and test execution
- Pluggable frontends for reporting
- Usable both as a CLI tool(s) and as a library

## Repository structure

```
kci-bisect/
├── contrib/           # Existing scripts from contributors (as-is)
├── docs/              # Design documents and architecture notes
└── COPYING            # LGPL-2.1
```

## Contributing

We are actively looking for existing bisection tools.
Please drop them into `contrib/` with a short README describing
what they do and how they work.

See the [GitHub issues](../../issues) for the current roadmap and
discussion topics. Design sketch in
[docs/architecture.md](docs/architecture.md); unresolved design
questions in [oq.md](oq.md).

## Licence

LGPL-2.1 — see [COPYING](COPYING).
