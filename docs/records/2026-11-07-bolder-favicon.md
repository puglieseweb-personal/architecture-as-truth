# The browser icon can be read at tab size

**Date:** 2026-11-07
**Actor:** Claude, at Emanuele Pugliese's request

## Merged
| PR | Title |
|---|---|
| PR_URL | The browser icon can be read at tab size |

## What changed
The browser icon is drawn again from the mark's own outline. The old `favicon.svg` placed the mark on the full logo canvas, so it filled about 60% of the icon, and its lines were under one pixel wide in a 16-pixel tab. The mark now fills a dark rounded square to about 80%, with every edge thickened by 16 units. `favicon.svg`, `favicon-32.png` and `apple-touch-icon.png` are replaced, and `favicon.ico` (16, 32 and 48 pixels) is added for the tools and search results that still ask for it. Both pages link the new file. The mark's shape and colours are unchanged, and the page still loads nothing from a third party.

## Documents reconciled
- `site/index.html`, `site/404.html` — updated: one icon link each
- `site/aat-logo-mark.svg` — unchanged: the icons are drawn from it
- `ARCHITECTURE-AS-TRUTH.md` — unchanged: no definition, principle or rule changed
- `CHANGELOG.md`, `CITATION.cff` — unchanged: the wording's version is still 1.0
