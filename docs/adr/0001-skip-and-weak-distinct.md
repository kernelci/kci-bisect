# ADR-0001: Keep `skip` and `weak` as distinct step decisions

## Status

Proposed — 2026-05-04

## Context

A bisection step records a decision derived from build and test signals. `git bisect` defines three values: `good`, `bad`, `skip`. This project also needs to represent *tested but uncertain* results, which are common in performance bisection where measurement noise is intrinsic.

The question is whether "untestable at this commit" and "tested but uncertain" share one outcome (`skip`) or are kept separate (`skip` + `weak`).
The two states drive different follow-ups: 

- `skip` advances the search to a different commit,
- `weak` suggests re-testing the same commit before deciding.

## Decision

Use four step decisions: `good`, `bad`, `skip`, `weak`. 

`skip` and `weak` are distinct.

## Consequences

- Decision engine output type carries one extra value over `git bisect`.
- Step records must distinguish the two for audit and replay.
- Commit selector treats `skip` as "advance to a different commit"; retry policy treats `weak` as "re-run before deciding".
- Diverges from `git bisect` vocabulary; documented in `terms.md`.
- A retry-then-skip policy can be layered on top later without changing the decision vocabulary.
