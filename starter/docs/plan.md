# The plan

**Decision:** [ADR-0001](decisions/ADR-0001-adopt-architecture-as-truth.md)
**Updated:** 2026-11-06

The plan is the fourth document: the stories, one pull request each, which scenarios each one makes pass, and the order. A story is done when its scenarios are `@built` and its record is written. The agent updates this file with its change; that is part of leaving the truth true.

## Stories

| # | Story | Repository | Scenarios it flips to @built | Depends on | State |
|---|---|---|---|---|---|
| 1 | Adopt Architecture as Truth: the documents, the agent file and the workflow | this one | none | | done |
| 2 | <the first story of your first change> | | <scenario names from docs/behaviours/> | 1 | proposed |
| 3 | | | | 2 | proposed |

## Release order

1. Story 1 (done with the first merge).
2. Stories 2 and 3 together, once their scenarios are built.

## Not planned

What was asked for and deliberately left out, and why, so that nobody builds it by accident.

- ...
