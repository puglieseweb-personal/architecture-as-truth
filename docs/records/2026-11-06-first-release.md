# The first release: the wording, the agent file, the starter, two checks and the reference site

**Date:** 2026-11-06
**Actor:** Claude (session `9e786f8b-1e20-4dfd-8f04-f8ccd18598db`), at Emanuele Pugliese's request

## Merged
| PR | Title |
|---|---|
| https://github.com/puglieseweb-personal/architecture-as-truth/pull/1 | Architecture as Truth 1.0: the wording, the agent file, the starter, two checks and the reference site |

## What changed
The repository opens with everything a team needs to try Architecture as Truth with no product: the fixed wording, version 1.0; the four rules as an agent file; a starter repository with templates, a worked example and a workflow; two pipeline checks, for rules 2 and 4, with their tests; a checklist for people who build AI coding tools; a list of implementations and adopters; and the reference site for https://architectureastruth.org/, published by GitHub Pages. The text is CC BY 4.0, © PuglieseWeb LTD, crediting Emanuele Pugliese; the code is Apache-2.0.

The record check is derived from the merge-changelog checker PuglieseWeb has run on its own decision repository since September 2026. The approved-file guard is new: the article said a pipeline can refuse a change that edits an approved file, and nothing published did.

## Documents reconciled
- `ARCHITECTURE-AS-TRUTH.md` — added: the fixed wording 1.0, quoted verbatim from the author's approved text of 2026-11-05; a script compared every passage before the merge
- `agent/AGENTS.md` and `site/AGENTS.md` — added: the four rules quoted verbatim; CI keeps the two copies identical
- `site/index.html` and `site/llms.txt` — added: the definition, the principles and the rules quoted verbatim
- `CITATION.cff`, `CHANGELOG.md` — added: version 1.0, dated 2026-11-05, the article's date
