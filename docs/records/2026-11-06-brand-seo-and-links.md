# The reference site takes the AAT brand, search metadata and links to its companions

**Date:** 2026-11-06
**Actor:** Claude, at Emanuele Pugliese's request

## Merged
| PR | Title |
|---|---|
| https://github.com/puglieseweb-personal/architecture-as-truth/pull/PRNUM | The reference site takes the AAT brand, search metadata and links to its companions |

## What changed
The site moves to the Architecture as Truth brand: the mark, the hero, the share banner, the Blueprint Signal palette, and JetBrains Mono with Inter. The fonts are served from the site, so it still loads nothing from a third party and the footer's "no tracking" stays true. The title and description are rewritten for search, and the structured data gains keywords, the article and the questions. A new Questions section answers what people search for: spec-driven development, domain-driven design, docs-as-code, architecture as code, vibe coding, architectural drift, which agents, and whether a product is needed. Most of its answers are the article's words or the fixed wording. A new Pass it on section holds share links and a README badge, and the starter and this README carry the badge. SystemDox's row and the footer's interest note link to the page about that implementation. The long citation link no longer widens the page on a phone.

## Documents reconciled
- `ARCHITECTURE-AS-TRUTH.md` — unchanged: no definition, principle or rule changed, and a script compared the page with it
- `agent/AGENTS.md` and `site/AGENTS.md` — unchanged: the four rules are not touched
- `site/index.html` — updated: the brand, the metadata, the Questions and Pass it on sections, and the links; the definition, the principles and the rules quoted as they stand
- `site/llms.txt` — updated: a How it compares block and the link to the SystemDox page
- `site/404.html` — updated: the brand
- `README.md`, `starter/README.md` — updated: the badge
- `IMPLEMENTATIONS.md`, `CITATION.cff`, `CHANGELOG.md` — unchanged: nobody new has reported, and the wording's version is still 1.0
