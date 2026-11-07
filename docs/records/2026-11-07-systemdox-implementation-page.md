# The implementations list links SystemDox to the page that maps it to AAT

**Date:** 2026-11-07
**Actor:** Claude, at Emanuele Pugliese's request

## Merged
| PR | Title |
|---|---|
| https://github.com/puglieseweb-personal/architecture-as-truth/pull/6 | The implementations list links SystemDox to the page that maps it to AAT |

## What changed
SystemDox's page saying which principles and rules it implements, and which it does not, went live on 2026-11-07: https://www.systemdox.com/architecture-as-truth. The site already linked there. The SystemDox row in `IMPLEMENTATIONS.md` still linked to the SystemDox home page and now links to that page too, so a reader can check the claim. Nothing in the practice needs SystemDox.

## Documents reconciled
- `IMPLEMENTATIONS.md` — updated: the SystemDox row links to its AAT page
- `site/index.html` — unchanged: its implementations table and footer already link to the page
- `README.md`, `site/llms.txt` — unchanged: the interest-declared lines name SystemDox without claiming what it implements
- `ARCHITECTURE-AS-TRUTH.md` — unchanged: no definition, principle or rule changed
- `CHANGELOG.md`, `CITATION.cff` — unchanged: the wording's version is still 1.0
