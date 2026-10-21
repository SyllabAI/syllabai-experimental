# Manifest — captures & provenance

**Capture session**: 2026-10-22 (UTC) · operator: SyllabAI experiment run
(automated capture via scripts, polite spacing, descriptive User-Agent
`SyllabAI-research-capture/0.1`).

All committed captures are **metadata-only**, from the site's public REST
API. No copyrighted content (question/solution bodies, PDFs, images, site
assets) is committed — see `../docs/IP-AND-COPYRIGHT-NOTES.md`.

## Committed captures

| File | Source endpoint | Captured | Rows | Notes |
|---|---|---|---|---|
| `api/stations.json` | `GET /api/stations` | 2026-10-22 | 29 | stations with guiding questions, tubemap positions, publish flags |
| `api/lines.json` | `GET /api/lines/detail` | 2026-10-22 | 5 | lines with colours, order, member stationIds |
| `api/pervasive-ideas.json` | `GET /api/pervasive-ideas` | 2026-10-22 | 6 | cross-cutting ideas |
| `api/resource-types.json` | `GET /api/resource-types/converted` | 2026-10-22 | 14 | types with official descriptions |
| `api/all-resources.json` | `GET /api/stations/{id}/resources/all` (24 live stations, looped; per-station responses retained locally, not committed) | 2026-10-22 | 855 | master inventory; each record stamped `_station`; wrapper records source + capture date + total |
| `api/key-questions.json` | `GET /api/stations/{id}/key-questions` (looped) | 2026-10-22 | 113 | per-station key questions; 4 under-construction stations return 401 (absent) |

## Local-only artifacts (analysis inputs, not committed)

| Artifact | Source | Why local-only |
|---|---|---|
| `home.html` | `GET /` | site shell (© markup) — used for stack/link analysis |
| `quadratics.html`, `discriminating.html`, `r5059.html` | `GET /quadratics`, `/quadratics/discriminating`, `/quadratics/r5059` | resource pages contain copyrighted question/solution bodies — HTML retained locally for structure analysis only |
| `about.html`, `about-website.txt` | `GET /about`, `/about/website` | prose pages; findings paraphrased into research notes rather than committed |
| `main.min.js`, `resource.min.js` | `/static/js/main.min.js`, `/static/js/public/resource.min.js` | site code (©) — endpoint strings catalogued in research notes |
| `sitemap.xml` probe | `GET /sitemap.xml` | 404 — no sitemap exists |
| per-station `station-*.json` | `/api/stations/{id}/resources/all` | superseded by `all-resources.json` aggregate; dropped from commit to avoid duplication |

## Capture method

1. Metadata pass: public API endpoints (curl / Python urllib), ~0.3–0.4 s
   spacing, three retries, no auth.
2. Page probes: HTTP GET of exemplar pages + targeted status-code probes to
   verify URL patterns (documented in
   `../research/2026-10-22-url-schemes.md`).
3. Client-bundle scan: endpoint strings extracted from served JS to map the
   API surface (215 endpoints; groups in
   `../research/2026-10-22-api-catalogue.md`).

## Re-capture

The endpoints above are stable and anonymous; any capture in this manifest
can be reproduced with a loop over `/api/stations` →
`/api/stations/{id}/resources/all` etc. If the site ever disappears, this
metadata capture + the Wayback Machine are the recovery paths (the corpus is
wayback-archived; verify before relying on it).
