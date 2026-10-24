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
  `syllabai-v2#321` → `f757c643` — first multi-station lane served, bundle
  1.1: 4 stations, 12 spec points, 182 resources) and
  **lane 4 Circular-measure strand → CIE 9709 P1 1.4 Circular measure** —
  the first strand lane (operator "extend channel 4"; cross-map
  `cross-map-circular-measure.json` @ `b52cf1bf`, 62 sweep candidates:
  17 aligned — 3 new-text + 14 cross-lane circles-strand facts — + 4
  non-overlaps + 41 routed; hub fragment 1.4.1a folded into 1.4.1;
  enrichment + 5 new-text bodies merged of record as `syllabai-resources#74`
  → `1585c4ff`, MANIFEST v4; hub `syllabai-v2#327` → `2684a8e4` — first strand
  lane served via the cross-lane join, bundle 1.1: 4 lanes / 8 stations /
  13 spec points / 187 resources) and
  **lane 5 Trigonometry: Triangles to Functions + Compound Angles → CIE 9709
  P1 1.5 Trigonometry** — the two-station lane (operator "lane 5"; cross-map
  `cross-map-trigonometry.json` @ `f3ef5745`, 299 sweep candidates: 41
  aligned — 36 TTF + 3 TCA substrate + 2 cross-station strays, 55 rows —
  plus 36 non-overlaps (the compound-angles station's honest P3 2.3
  mapping) + 2 cross-lane fact joins (r9924/r8411 → 1.5.4 vs lane-2
  bodies) + 220 routed; primary picks going-round-in-circles /
  trig-tables / inverse-or-not / r5269 / r6138; enrichment + whole-
  substrate 77 text bodies merged of record as `syllabai-resources#79`
  → `cf79ecd2`, MANIFEST v5; hub `syllabai-v2#330` → `16bef479` — 5 lanes /
  12 stations / 18 spec points / 262 rows / 264 bodies served) and
  **lane 6 Sequences + Counting and Binomials → CIE 9709 P1 1.6 Series** —
  the second two-station lane (operator "lane 6 (CIE 9709 P1 1.6 Series)";
  cross-map `cross-map-series.json` @ `82964ce4`, 137 sweep candidates: 49
  aligned — 43 substrate + 6 cross-station strays, 56 rows — plus 50
  non-overlaps (combinatorics/logic dominance in Counting and Binomials;
  general-index binomial questions carry P3 Series bearings) + 2 cross-lane
  fact joins (r7553/r9527 → 1.6.3 vs lane-2 bodies) + 36 routed; primary
  picks r7078 / sort-it-out / r8907 / square-spirals; enrichment +
  whole-substrate 99 text bodies filed as `syllabai-resources#89`,
  MANIFEST v6; hub `syllabai-v2#337` → `cdd7fcfc` — 6 lanes /
  20 stations / 22 spec points / 320 rows / 363 bodies served) and
  **lane 7 Introducing Calculus + Calculus of Powers → CIE 9709 P1 1.7
  Differentiation** — the third two-station lane (operator "Proceed Lane 7";
  cross-map `cross-map-differentiation.json` @ `93575e69`, 195 sweep
  candidates: 74 aligned — 40 substrate + 34 cross-station strays, 107 rows —
  plus 32 non-overlaps (the trapezium-rule/kinematics cluster in Introducing
  Calculus; the trapezium rule is not in the 2023–2025 P1 spec) + 3
  cross-lane fact joins (r5640 vs lane 6; r7115/r8936 vs lane 4) + 86 routed;
  primary picks r7692 / r9942 / r8065 / r9260; enrichment + whole-substrate
  106 text bodies filed as `syllabai-resources#91`, MANIFEST v7; hub
  `T-UGM-HUB-CONSUME-7` pending). Mode-2 deep-link
  pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
- Next: #91 review/merge on operator ack; further lanes by spine adjacency
  (1.8 Integration: the integration stations — the final Pure 1 subtopic) —
  recipe of record in `docs/INTEGRATION-PLAN.md` P7; S1-bridge census run
  still pending.
