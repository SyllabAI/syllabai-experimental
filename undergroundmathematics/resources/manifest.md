# Manifest — captures & provenance

**Capture session**: 2026-10-22 (UTC) · operator: SyllabAI experiment run
(automated capture via scripts, polite spacing, descriptive User-Agent
`SyllabAI-research-capture/0.1`).

Committed captures: **metadata** from the site's public REST API and, since
the Phase 2 operator decision of 2026-10-22, **extracted content bodies**
from the full crawl (see `../docs/IP-AND-COPYRIGHT-NOTES.md` for the recorded
decision and its conditions). Site binaries/assets remain excluded.

## Committed captures

### Metadata (public API)

| File | Source endpoint | Captured | Rows | Notes |
|---|---|---|---|---|
| `api/stations.json` | `GET /api/stations` | 2026-10-22 | 29 | stations with guiding questions, tubemap positions, publish flags |
| `api/lines.json` | `GET /api/lines/detail` | 2026-10-22 | 5 | lines with colours, order, member stationIds |
| `api/pervasive-ideas.json` | `GET /api/pervasive-ideas` | 2026-10-22 | 6 | cross-cutting ideas |
| `api/resource-types.json` | `GET /api/resource-types/converted` | 2026-10-22 | 14 | types with official descriptions |
| `api/all-resources.json` | `GET /api/stations/{id}/resources/all` (24 live stations, looped; per-station responses retained locally, not committed) | 2026-10-22 | 855 | master inventory; each record stamped `_station`; wrapper records source + capture date + total |
| `api/key-questions.json` | `GET /api/stations/{id}/key-questions` (looped) | 2026-10-22 | 113 | per-station key questions; 4 under-construction stations return 401 (absent) |

### Content (Phase 2 crawl + extraction — see operator decision in `../docs/IP-AND-COPYRIGHT-NOTES.md`)

| File | Source | Captured | Rows | Notes |
|---|---|---|---|---|
| `content/{station}.json` (24 files) | HTML crawl of all 855 resource pages + section + teacher-support pages (2,486 pages, 0 failures) | 2026-10-22 | 855 resources / 2,181 sections | per-resource records with full section bodies (`html` + `text`): Question/Problem, Suggestion, Solution, Interactive graph; teacher-support sections merged; acknowledgement + last-updated + ref preserved; canonical URL on every record |
| `content-assets.json` | discovered PDF/asset links during crawl | 2026-10-22 | — | asset URLs only; binaries not crawled |

### Derived artifacts (Phase 3a/3c — computed from the captures above)

| File | Derived from | Generated | Rows | Notes |
|---|---|---|---|---|
| `ugm-clean/{station}.json` (24 files) | `content/{station}.json` qwell dedup pass | 2026-10-22 | 855 resources / 1,101 sections cleaned | re-displayed question wells stripped into a shared `questionWell` field (791 resources); 2,204 duplicate qwells removed; 584 section-unique qwells preserved (flagged in `extraction.qwellVariantsKept`); schema otherwise stable |
| `derived/review-question-provenance.json` | `content/*.json` acknowledgements | 2026-10-22 | 623 records | structured tuples (board, qualification, paper, paperCode, year, question labels, permission); 572 parsed (569 review questions + 3), 45 non-exam provenance, 6 provenance-missing; boards: UCLES 360, Oxford MAT 147, O&C 37, NRICH 35, UKMT 20, Cambridge Colleges 6, MEI 1, TMUA 1; years 1951–2016; S1 join key for `syllabai-pastpapers` |
| `derived/spine-export/cie-a-level-maths-20-pure-1.json` | `syllabai-v2` apps/hub spines + content maps (read-only) | 2026-10-22 | 5 spec points | Quadratics lane (1.1.1–1.1.5) spec points + item attachment inventory (IDs/counts only, no item text) |
| `derived/spine-export/cie-igcse-maths-25-extended.json` | `syllabai-v2` apps/hub spines + content maps (read-only) | 2026-10-22 | 10 spec points | IGCSE 0580 Extended quadratics-bearing spec points (contrast lane) |
| `derived/cross-map-quadratics.json` | ugm-clean + provenance + spine export + authored alignments | 2026-10-22 | 59 alignments | pilot cross-map; twin of `../docs/cross-map-quadratics.md` |

## Local-only artifacts (analysis inputs, not committed)

| Artifact | Source | Why local-only |
|---|---|---|
| `home.html` | `GET /` | site shell (© markup) — used for stack/link analysis |
| `quadratics.html`, `discriminating.html`, `r5059.html`, `discriminating-ts.html` | `GET` exemplar pages | superseded by the full crawl (raw store local) |
| `about.html`, `about-website.txt` | `GET /about`, `/about/website` | prose pages; findings paraphrased into research notes rather than committed |
| `main.min.js`, `resource.min.js` | `/static/js/main.min.js`, `/static/js/public/resource.min.js` | site code (©) — endpoint strings catalogued in research notes |
| `sitemap.xml` probe | `GET /sitemap.xml` | 404 — no sitemap exists |
| per-station `station-*.json` | `/api/stations/{id}/resources/all` | superseded by `all-resources.json` aggregate; dropped from commit to avoid duplication |
| Phase-2 raw crawl store (`ugm-crawl/raw/`, 2,486 HTML files, ~46 MB) | full site crawl 2026-10-22 | raw © markup retained locally for verification; the committed canonical form is `content/{station}.json` |

## Capture method

1. Metadata pass: public API endpoints (curl / Python urllib), ~0.3–0.4 s
   spacing, three retries, no auth.
2. Page probes: HTTP GET of exemplar pages + targeted status-code probes to
   verify URL patterns (documented in
   `../research/2026-10-22-url-schemes.md`).
3. Client-bundle scan: endpoint strings extracted from served JS to map the
   API surface (215 endpoints; groups in
   `../research/2026-10-22-api-catalogue.md`).
4. Phase 2 content crawl (2026-10-22): resumable crawler, ~0.4 s spacing,
   descriptive UA, menu-driven section discovery, 3× retry with backoff —
   2,486 pages / 0 failures; extraction via BeautifulSoup into
   `content/{station}.json` (method + schema in
   `../research/2026-10-22-phase2-crawl-and-extraction.md`).

## Re-capture

The endpoints above are stable and anonymous; any capture in this manifest
can be reproduced with a loop over `/api/stations` →
`/api/stations/{id}/resources/all` etc. If the site ever disappears, this
metadata capture + the Wayback Machine are the recovery paths (the corpus is
wayback-archived; verify before relying on it).
