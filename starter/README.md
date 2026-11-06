# Architecture as Truth: the starter

[![Architecture as Truth](https://architectureastruth.org/badge.svg)](https://architectureastruth.org/)

A repository shaped for Architecture as Truth (AAT), with nothing to install. Copy it, write down one part of your product, and let your AI agent build from the documents. The standing reference for the practice is https://architectureastruth.org/.

## The shape

```
AGENTS.md                      the four rules, as the file your agent reads (CLAUDE.md imports it)
docs/
  decisions/                   one record per decision: what, why, what was turned down
    ADR-0001-adopt-architecture-as-truth.md
    TEMPLATE.md
  contracts/                   what the system promises: OpenAPI, AsyncAPI, or plain contract.md
    TEMPLATE.openapi.yaml
    TEMPLATE.contract.md
  behaviours/                  Given/When/Then scenarios; they are also the tests
    example-appointment-reminders.feature
    TEMPLATE.feature
  plan.md                      the stories, one pull request each, in order
  records/                     one dated record per change
    2026-11-06-adopt-architecture-as-truth.md
    TEMPLATE.md
.github/workflows/aat.yml      runs the two checks on every pull request
```

A document on the default branch has been approved. The merge was the approval.

## In an hour

1. **Copy this folder** into a new repository, or `docs/`, `AGENTS.md`, `CLAUDE.md` and the workflow into an existing one. Delete the example feature file and the example record when you have your own.
2. **Pick one part of your product.** Write its decision from `docs/decisions/TEMPLATE.md`: what it promises, why, and what you considered and turned down. Keep it short enough for the analyst, the tester and the founder to read.
3. **Write the contract** if the part has an interface: an OpenAPI document for HTTP, AsyncAPI for events, or `TEMPLATE.contract.md` for anything else. By hand, before any code.
4. **Write the behaviours** as scenarios in a `.feature` file, each tagged `@proposed`. Bind them to your test runner (Cucumber, pytest-bdd, vitest-cucumber, SpecFlow, or any other) so that a `@proposed` scenario runs as an expected failure.
5. **Write the plan**: the stories, one pull request each, which scenarios each one makes pass, and the order.
6. **Merge the documents.** That is the first approval, and it is a person's.
7. **Ask your agent for the first story.** It reads `AGENTS.md`, reads the documents, builds, flips the scenarios it made pass from `@proposed` to `@built`, and adds a record under `docs/records/`.
8. **Open the pull request.** The workflow refuses an edit to an approved contract or scenario without an `amendment` label, and a change that adds no record.
9. **Read the record,** not the code. If the agent made a judgement a person should have made, amend the decision and let it build again.

## The two checks

`.github/workflows/aat.yml` fetches the checks from the main repository at a tagged release and runs them on every pull request:

- **Rule 2, build what was approved.** `approved_guard.py` refuses a change that edits, renames or deletes anything under `docs/contracts/` or `docs/behaviours/`, except a tag line in a feature file. A pull request labelled `amendment` is allowed through: that label is a person's.
- **Rule 4, leave the truth true.** `record_check.py` refuses a change that adds no record, and a record that names no documents.

Rules 1 and 3 are asked of the agent in `AGENTS.md`. Its record is how you see whether it kept them.

---

Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth · CC BY 4.0, © 2026 PuglieseWeb LTD.
