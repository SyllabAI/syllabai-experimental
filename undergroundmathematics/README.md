# undergroundmathematics

Experiment workspace inside `syllabai-experimental`. Target of study:
[undergroundmathematics.org](https://undergroundmathematics.org/) — free
web-based resources for teaching post-16 (A level) mathematics, built at the
University of Cambridge (2012–, originally the Cambridge Mathematics Education
Project, now hosted by Cambridge Mathematics).

Goal: **reverse engineer the site** — its information architecture, content
model, pedagogy layer, authoring/rendering pipeline and public API — to inform
SyllabAI's content platform design (stations/lines vs CIE/Edexcel spines,
review-question corpus model, teacher-support layer, resource taxonomies).

## Layout

```
undergroundmathematics/
  research/    # dated research notes — site analysis, architecture, API findings
  resources/   # scraped metadata captures (public API JSON) + manifest
  docs/        # working docs — plan, IP/copyright policy
```

## Conventions

Inherited from the repo ground rules plus [`exam-mate/`](../exam-mate/README.md):

- **Provenance first**: every capture in `resources/` is documented in
  [`resources/manifest.md`](./resources/manifest.md) with source URL, capture
  date and method. Captured API payloads are metadata-only (see IP notes).
- **Research notes are dated**: `YYYY-MM-DD-topic.md`, chronological trail.
- **Docs record decisions**: plan, phase status, and the IP/copyright policy
  live in `docs/`.
- **Nothing here is of record** — scratch space; graduations to the platform
  go through proper PRs against the receiving repo.

## Key findings (TL;DR)

- **Scale**: 855 public resources across 29 "stations" (24 live, 4 under
  construction); 569 of them (66%) are **review questions** digitised from
  historical UCLES/Cambridge exam papers going back to the 1960s; 113 station
  key questions; 6 pervasive ideas; 5 lines; 14 resource types.
- **Information architecture**: a London-tube-map metaphor — stations
  (topics) joined by coloured lines (Number, Algebra, Geometry, Functions,
  Calculus), with cross-cutting "pervasive ideas". Not tied to any syllabus.
- **Content model**: every resource = markdown + embedded LaTeX source in
  MySQL, sections like Problem → Suggestion → Solution, with teacher notes,
  key questions, interactivity labels (GeoGebra), related resources, and
  printable PDF generated via Pandoc → LaTeX.
- **Tech stack**: AngularJS 1.4 SPA with server-side pre-rendering, MySQL +
  a public REST API (`/api/*`, 215 endpoints in the client bundle), MathJax
  2.7, Pandoc-based print pipeline, ServiceWorker offline cache.
- **The site self-documents its pipeline** on `/about/website` — including a
  retrospective regret about Markdown-with-significant-whitespace.

## Status

- 2026-10-22: **Phase 1** — site identification, taxonomy + inventory capture
  (metadata), content model and technical architecture analysis.
- 2026-10-22: **Phase 2** — polite full-content crawl (2,486 pages, 0
  failures) + section extraction: 855 resources / 2,181 section bodies
  committed under `resources/content/` per operator decision (see
  `docs/IP-AND-COPYRIGHT-NOTES.md`). Discovery notes in
  `research/2026-10-22-phase2-crawl-and-extraction.md`.
- 2026-10-22: **Integration plan** — rights ladder (modes 0–4), eight
  integration surfaces, phased P3a–P6: `docs/INTEGRATION-PLAN.md`.
- 2026-10-22: **Phase 3a (corpus cleanup)** — qwell dedup into a shared
  `questionWell` field (2,204 duplicates stripped, 584 section-unique
  preserved) → `resources/ugm-clean/`; all 623 acknowledgements parsed into
  structured provenance tuples →
  `resources/derived/review-question-provenance.json`.
- 2026-10-22: **Phase 3c (spine cross-map pilot)** — UGM quadratics ↔
  CIE 9709 Pure 1 Quadratics (1.1.1–1.1.5): 56/59 resources aligned (95%),
  mode-2 deep-link shortlists per spec point, S1 provenance-bridge status;
  `docs/cross-map-quadratics.md` + machine-readable twin. Ready for
  operator review; generalisation to all lanes proposed (doc §8).
- 2026-10-22: **Phase 3b (enrichment data)** — captured all six per-resource
  relation axes anonymously (855×6 API calls, 0 failures; GETs on
  `/api/resources/{id}/…` are public — phase-1 grouping corrected);
  canonical relation graph 1,295 nodes / 7,783 edges →
  `resources/derived/relation-graph.json` + `.graphml`; per-station
  enrichment sheets (25 stations, 855 resources: type, level, key
  questions, lines, pervasive ideas, tags, related resources,
  teacher support, question wells, assets, provenance) →
  `resources/derived/enrichment-sheets/` + `INDEX.md`.
- 2026-10-22: **Phase 4 (ADR)** — `docs/ADR-UGM-0001-ugm-integration-mode.md`:
  adopt Mode 1 (facts of-record-eligible via PRs) + Mode 4 (hint layer,
  archetypes, second tagging axis, teacher prompt tables — via owning
  specs), gated Mode-2 "Explore further" pilot on IAL P1 quadratics
  (feature flag, link-health job, Wayback fallback, CTR floor 1.0%/28d —
  3.0% generalise, below-floor kill), Mode 3 deferred with a narrow
  provenance-matched licensing ask (Cambridge Mathematics first, census +
  pilot evidence before conversation). Status **Accepted** — ratified by
  operator 2026-10-22, without amendments.
- Lanes of record (operator attestation 2026-10-23, direct text import):
  **lane 1 quadratics** (`syllabai-resources` #55 facts + #58 text →
  `main@91eed732`; hub consumption `syllabai-v2#308` → `56db3b96`) and
  **lane 2 Combining Functions → CIE 9709 P1 1.2** (cross-map
  `cross-map-functions.json` @ `e59276be`, 27/38 aligned; corpus #61 →
  `a32c6c0f`, MANIFEST v2 multi-lane; hub `syllabai-v2#312` → `635264b2`,
  bundle 1.1: 2 stations, 10 spec points, 97 resources) and
  **lane 3 Geometry of Equations + Circles → CIE 9709 P1 1.3 Coordinate
  geometry** — the first two-station lane (cross-map
  `cross-map-coordinate-geometry.json` @ `cb947595`, 61/85 aligned = 71.8%,
  77 rows over folded codes 1.3.1/1.3.2 with hub-spine fragments
  1.3.1a/1.3.2a folded of record; 24 honest non-overlaps; enrichment + 85
  text bodies filed as `syllabai-resources#66`, MANIFEST v3; hub
  `T-UGM-HUB-CONSUME-3` pending on the syllabai-v2 side). Mode-2 deep-link
  pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
- Next: hub consumption for lane 3 (`T-UGM-HUB-CONSUME-3`, mirrors #308/#312);
  further lanes by spine adjacency on operator ack (1.5 Trigonometry:
  `trigonometry-triangles-to-functions` + `trigonometry-compound-angles`) —
  recipe of record in `docs/INTEGRATION-PLAN.md` P7; S1-bridge census run
  still pending.
