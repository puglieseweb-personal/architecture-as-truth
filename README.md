# Architecture as Truth (AAT)

[![Architecture as Truth](https://architectureastruth.org/badge.svg)](https://architectureastruth.org/)

> **Architecture as Truth (AAT)** is a way of building software in which the architecture documents (the decisions, the contracts, the behaviours and the plan) are the single source of truth about the product. People decide by changing those documents, AI agents build from them, and everything that ships is reconciled back into them.

Set out by **Emanuele Pugliese** in 2026. The standing reference is **https://architectureastruth.org/**. The article that introduced it is [*AI Promoted Everybody. Architecture as Truth (AAT) Is the New Job.*](https://www.puglieseweb.com/blog/architecture-as-truth)

AAT is a practice, not a product. It needs a Git repository, plain text files, a test runner and an AI agent held to four rules. This repository holds everything a team needs to try it, with no product.

## What is here

| Path | What it is |
|---|---|
| [`ARCHITECTURE-AS-TRUTH.md`](ARCHITECTURE-AS-TRUTH.md) | The fixed wording, version 1.0: the definition, the five principles, the four rules for an AI agent. Quote it as it stands. |
| [`agent/AGENTS.md`](agent/AGENTS.md) | The four rules as an agent instruction file. Copy it into your repository; `agent/CLAUDE.md` imports it for Claude Code. |
| [`starter/`](starter/) | A starter repository: the four kinds of document as templates with one worked example, the agent file, and a workflow that runs the two checks on every pull request. Try AAT in an hour. |
| [`checks/`](checks/) | Two pipeline checks, plain Python, no dependencies: `approved_guard.py` (rule 2) and `record_check.py` (rule 4). |
| [`checklist/TOOL-BUILDERS.md`](checklist/TOOL-BUILDERS.md) | Four questions for the people who build AI coding tools, and how to test each. |
| [`IMPLEMENTATIONS.md`](IMPLEMENTATIONS.md) | Tools that implement part of it and teams that practise it, as they report. |
| [`site/`](site/) | The reference site, published at https://architectureastruth.org/ by GitHub Pages. |
| [`CITATION.cff`](CITATION.cff), [`CHANGELOG.md`](CHANGELOG.md) | How to cite, and the versions of the wording. |

## The four rules for an AI agent

1. **Read before writing.** Before it changes anything, the agent fetches the decisions, the contracts and the behaviours that govern what it is about to touch.
2. **Build what was approved.** It may not edit a contract, or the wording of a scenario, to make its own work pass.
3. **Stop, do not patch.** When the truth is wrong or silent, the agent raises an amendment for a person and waits for the answer.
4. **Leave the truth true.** Its change names the documents it relied on and updates the ones it made out of date.

A pipeline can enforce the second and the fourth today; the scripts in [`checks/`](checks/) do. The first and the third can only be asked for, and the agent's record is what makes a breach visible.

## Try it in an hour

1. Copy [`starter/`](starter/) into a new repository, or its `docs/`, `AGENTS.md` and workflow into an existing one.
2. Pick one part of your product. Write down what it promises and why: one decision, one contract, one feature file of scenarios, and the plan.
3. Point your AI agent at the repository. It reads `AGENTS.md`. Ask it for a change.
4. Open the pull request. The workflow refuses a change that edits an approved contract or scenario without an amendment, and a change that names no documents.
5. Read the record it wrote. Then keep the documents true.

## Contributing

- **The wording** is versioned and changes only by the author, with a date, in [`CHANGELOG.md`](CHANGELOG.md). Open an issue to argue for a change; a quiet edit is never merged.
- **Translations** of the wording are welcome as pull requests under `translations/<language>/`, with the credit line kept.
- **The checks, the starter and the site** take ordinary pull requests. The checks are tested; run `python -m pytest checks -q`.
- **Implementations and adopters** add a row to [`IMPLEMENTATIONS.md`](IMPLEMENTATIONS.md).

This repository practises what it describes: every change adds a record under [`docs/records/`](docs/records/) and CI checks it.

## Licence and credit

The text (the wording, the agent file, the templates, the checklist and the site's prose) is © 2026 PuglieseWeb LTD and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use it, adapt it and teach it, crediting Emanuele Pugliese and linking to the article. The code (`checks/` and the workflows) is licensed under the [Apache License 2.0](LICENSE). See [LICENSE-TEXT.md](LICENSE-TEXT.md).

Credit line: *Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth*

Interest declared: the author's company builds [SystemDox](https://www.systemdox.com), one implementation of AAT. Nothing here needs it.
