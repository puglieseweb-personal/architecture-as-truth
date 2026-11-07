# The reference site can be verified by Google and tells Bing when it changes

**Date:** 2026-11-07
**Actor:** Claude, at Emanuele Pugliese's request

## Merged
| PR | Title |
|---|---|
| https://github.com/puglieseweb-personal/architecture-as-truth/pull/3 | The reference site can be verified by Google and tells Bing when it changes |

## What changed
The site gains Google's verification file, so the address can be confirmed as a Search Console property, and an IndexNow key file. Each deploy now submits the sitemap to IndexNow, which reaches Bing and the other engines that use it. Nothing a reader sees changes, and the page still loads nothing from a third party.

## Documents reconciled
- `.github/workflows/pages.yml` — updated: the IndexNow step after the deploy
- `site/index.html`, `site/sitemap.xml`, `site/llms.txt` — unchanged: no page or address changes
- `ARCHITECTURE-AS-TRUTH.md` — unchanged: no definition, principle or rule changed
- `CHANGELOG.md`, `CITATION.cff` — unchanged: the wording's version is still 1.0
