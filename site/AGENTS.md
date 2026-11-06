# How an agent works in this repository: Architecture as Truth

This repository is built the Architecture as Truth (AAT) way. The architecture documents are the single source of truth about the product: the decisions, the contracts, the behaviours and the plan. People decide by changing those documents. You build from them. Everything that ships is reconciled back into them.

## Where the truth is

| Kind | Where | What it holds |
|---|---|---|
| Decisions | `docs/decisions/ADR-NNNN-<slug>.md` | What was decided, why, and what was turned down |
| Contracts | `docs/contracts/` | What the system promises: OpenAPI or AsyncAPI documents, or a plain `*.contract.md` |
| Behaviours | `docs/behaviours/*.feature` | Given/When/Then scenarios. They are also the tests |
| The plan | `docs/plan.md` | The stories, one pull request each, and their order |
| Records | `docs/records/YYYY-MM-DD-<slug>.md` | One dated record per change: what merged, what changed, which documents it touched |

A document on the default branch has been approved by a person. The merge was the approval.

## The four rules

1. **Read before writing.** Before it changes anything, the agent fetches the decisions, the contracts and the behaviours that govern what it is about to touch.
2. **Build what was approved.** It may not edit a contract, or the wording of a scenario, to make its own work pass.
3. **Stop, do not patch.** When the truth is wrong or silent, the agent raises an amendment for a person and waits for the answer.
4. **Leave the truth true.** Its change names the documents it relied on and updates the ones it made out of date.

## What the rules mean in practice

**Before the first edit.** List the decisions, contracts and behaviours that govern the files you are about to touch, and read them in full. If the task names a feature, read its scenarios before its code. Working from the code alone is guessing.

**While building.** Build what the scenarios assert and nothing more. A scenario tagged `@proposed` runs as an expected failure; when your change makes it pass, change its tag to `@built`. That tag is the only edit you may make to a feature file. Do not touch a contract. Do not reword a scenario. Do not weaken, skip or delete a test to get a green run.

**When the truth is wrong or silent.** Stop building. Open an amendment: a pull request that changes only the document or documents in question, says what is wrong or missing and proposes the answer. Wait for a person to merge it, then build from the merged text. Do not build through the gap with a confident guess, and do not leave the gap for a reviewer to find.

**With your change.** Add a record at `docs/records/YYYY-MM-DD-<slug>.md` with three sections: `## Merged` (the pull request URL), `## What changed` (in plain words) and `## Documents reconciled` (every document you relied on, each updated in this change or marked unchanged with the reason). Update the plan and any document your change made out of date. The pipeline refuses a change that edits an approved contract or scenario without an amendment, and a change that names no documents.

**Always.** Say in your pull request which documents you read and which you changed. If you made a judgement a person should have made, say so there.

---

Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth · Standing reference: https://architectureastruth.org/ · This file: CC BY 4.0, © 2026 PuglieseWeb LTD.
