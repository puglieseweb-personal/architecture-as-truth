# The checks

Two of the four rules for an AI agent can be enforced by a pipeline. These two scripts enforce them. Both are plain Python with no dependencies, so they run on a developer's machine and in CI with no install step. Apache-2.0.

| Script | Rule | What it refuses |
|---|---|---|
| `approved_guard.py` | 2. Build what was approved | A change that edits, renames or deletes a document under `docs/contracts/` or `docs/behaviours/` (configurable with `--guard`) unless the change is declared an amendment with `--amendment`. The one edit a build may make to a `.feature` file is a tag line, such as `@proposed` becoming `@built`. Adding a new document is always allowed. |
| `record_check.py` | 4. Leave the truth true | A record under `docs/records/` that cannot serve as the record of a change (no date, no actor, no pull request, no documents named), and, with `--require-record BASE`, a change that adds no record at all. A change that touches only records is the record of an earlier change and passes. |

The other two rules, *read before writing* and *stop, do not patch*, cannot be checked by a pipeline. They are asked of the agent in [`agent/AGENTS.md`](../agent/AGENTS.md), and the record is what makes a breach visible afterwards.

## Run them

```sh
python checks/approved_guard.py --base origin/main --head HEAD
python checks/record_check.py --root . --require-record origin/main
```

In CI, see [`starter/.github/workflows/aat.yml`](../starter/.github/workflows/aat.yml): it fetches this repository at a tagged release and runs both on every pull request, passing `--amendment` when the pull request carries the `amendment` label.

## Test them

```sh
python -m pip install pytest
python -m pytest checks -q
```

## A record

```markdown
# Reminders go out before an appointment

**Date:** 2026-11-06
**Actor:** Claude (session `abc123`)

## Merged
- https://github.com/example/product/pull/40

## What changed
The booking service sends a text 24 hours before an appointment.

## Documents reconciled
- `docs/decisions/ADR-0003-reminders-before-an-appointment.md` — unchanged: built as decided
- `docs/behaviours/reminders.feature` — updated in this change: two scenarios flipped to @built
- `docs/plan.md` — updated in this change: stories 2 and 3 done
```

The filename is the date and a slug: `docs/records/2026-11-06-reminders-before-an-appointment.md`. `## Documents reconciled` lists every document the change relied on, each updated or marked unchanged with the reason, or says exactly `None affected — <reason>`.
