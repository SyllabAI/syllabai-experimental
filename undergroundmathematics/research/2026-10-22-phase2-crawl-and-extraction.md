# Phase 2 — full-content crawl + section extraction

**Date**: 2026-10-22 · method: resumable crawler (`scripts/ugm_crawl.py` in the
local workspace; polite ~0.4 s spacing, descriptive UA, 0 failures), extractor
(`scripts/ugm_extract.py`)

## Crawl stats

| Measure | Value |
|---|---|
| Resources crawled | **855 / 855** (0 failures) |
| Raw HTML pages saved | **2,486** (main pages + section pages + teacher-support pages) |
| Sections extracted with HTML bodies | **2,181** |
| Resources with teacher-support content merged | 12 (the `Resource-in-action`-type records) |
| Resources with linked PDF assets recorded | (see `../resources/content-assets.json`) |
| Raw store size | ~46 MB local (not committed; extraction committed instead) |

Per-station extracted JSON (committed): `../resources/content/{station}.json` —
~10.8 MB total, one record per resource with full section bodies.

## How sections actually render (the discovery of this phase)

1. **One section per URL.** A resource page renders exactly one section's
   body inside `<div id="resource-section-content" class="resource-section-content
   cm-content" data-cm-content data-ng-non-bindable>`. The
   `resource-sections-menu` lists every section with its own URL
   (`/{station}/{slug}`, `.../suggestion`, `.../solution`,
   `.../interactive-graph`, …). So a full-content crawl must follow the menu
   — the landing page alone is only the first section.
2. **Section titles** come from `<h2 class="resource-section-title">` on each
   section page; menu labels match (`Question`, `Suggestion`, `Solution`,
   `Problem`, `Interactive graph`, …).
3. **The `qwell` pattern**: `Suggestion`/`Solution`/`Teacher notes` pages
   re-display the original problem inside
   `<div data-cm-element="qwell">` before their own content — the site
   duplicates the question well into each wrapper section so the reader never
   loses context. Extraction captures this verbatim (dedup is a downstream
   concern).
4. **Teacher support** is a sibling *resource* at
   `/{station}/{slug}-teacher-support` with its own section menu — for
   `discriminating`: `Outline`, `Opportunites for learning` (their typo in the
   URL slug: `opportunites-for-learning`), `Preliminary and Follow-up tasks`,
   `Sample work`.
5. **Review questions** (`r####`) have `Question` → `Suggestion` → `Solution`
   sections; the acknowledgement block (`.resource-acknowledgement`) carries
   the UCLES provenance string and sits in `.resource-footer` next to
   `.resource-last-updated`.
6. **Assets** (card PDFs, teacher-notes PDFs) are linked as
   `/{station}/{slug}/components/*.pdf` and `/{station}/{slug}/download/*.pdf`;
   URLs recorded in `../resources/content-assets.json`, binaries not crawled.
7. Page furniture selectors worth remembering: `.resource-type` (label, e.g.
   "Review question"), `.resource-heading-main h1` (title — contains raw TeX
   like `$12x^2+7x-10$`), `.resource-ref` (`Ref: R5059`),
   `.resource-related-wrapper` (related resources rail).

## Extraction schema (per resource record)

```
friendlyName, url, title, description, resourceTypeId, resourceLevel,
ref, oldSiteId, acknowledgement, station{id,friendlyId,title},
crawl{captured, mainPage},
pageMeta{typeLabel, title, ref, acknowledgement, lastUpdated},
sections[ {name, url, title, html, text} ],
teacherSupport{url, meta, sections[...]},     # when present
assets[urls]                                   # when present
```

`html` preserves the served markup (incl. `<span class="math inline">\(...\)</span>`
TeX); `text` is the tag-stripped plain version.

## Rights note for this phase

Operator instruction (2026-10-22): commit extracted question/solution bodies
to this repo. Recorded in `../docs/IP-AND-COPYRIGHT-NOTES.md` — attribution
and provenance travel with every record (`acknowledgement`, `station`,
`ref`, canonical `url`); all rights remain University of Cambridge / UCLES;
no platform adoption without a licensing conversation.
