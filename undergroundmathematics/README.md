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
  `T-UGM-HUB-CONSUME-7` served as `syllabai-v2#343` → `1db17c1b` — 7 lanes /
  27 stations / 26 spec points / 431 rows / 469 bodies served) and
  **lane 8 the calculus family → CIE 9709 P1 1.8 Integration** — the first
  strand lane on a spec section (operator: next lane per INTEGRATION-PLAN;
  cross-map `cross-map-integration.json` @ `c04abfbd`, 91 sweep candidates:
  28 aligned — 10 new-text strand + 18 cross-lane joins, 13 flipping the
  lane-7 CoP non-overlaps of record — plus 0 new non-overlaps + 32 routed +
  31 rejected with reasons; primary picks r8716 / r7734 / r6067 / r9357;
  enrichment + 10 new-text bodies filed as `syllabai-resources#96`,
  MANIFEST v8; **the Pure 1 spine 1.1–1.8 is now complete of record**;
  hub `T-UGM-HUB-CONSUME-8` pending). Mode-2 deep-link
  pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
  **lane 9 the algebra candidates → CIE 9709 Pure 3 3.1 Algebra** — the
  first lane on the pure-3 course plane (operator: "proceed with lane 9";
  cross-map `cross-map-algebra.json` @ `3098d8eb`, 90 sweep candidates:
  47 aligned rows — 38 fresh over 35 new-text resources + 9 cross-lane
  joins, 5 flipping the lane-2/lane-6 non-overlaps whose P3 bearings were
  recorded at lanes 2/6 — plus 16 fresh non-overlaps by reference
  (`bodyImported: false`, the lane-8 candidate-model law) + 30 rejected
  with reasons; primary picks absolutely / inequalities / whats-left /
  r6577 / r7792 / r7436; enrichment + 35 new-text bodies filed as
  `syllabai-resources#114`, MANIFEST v10 — 514 files corpus-wide;
  hub `T-UGM-HUB-CONSUME-9` (pure-3 bundle plane) pending). The image
  plane is of record: `T-UGM-ASSETS-1` (976 figures + figures-map) via
  `syllabai-resources#107`, served locally by `syllabai-v2#354`/`#357`
  (1,233 refs + 282 inline rewrites, zero external UGM image links in
  served bodies). Mode-2 deep-link
  pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
  **lane 10 the exp-and-log station → CIE 9709 Pure 3 3.2 Logarithmic
  and exponential functions** — the second lane on the pure-3 course
  plane (operator: "merging #358 then proceed with lane 10"; cross-map
  `cross-map-log-and-exp.json` @ `980556af`, 71 sweep candidates: 39
  aligned rows — 34 fresh over 34 new-text resources, 31 from the
  dedicated exp-and-log station, + 5 cross-course joins riding lanes
  2/5/6 bodies — plus 26 fresh non-overlaps by reference
  (`bodyImported: false`) + 6 rejected with reasons; primary picks
  proving-laws-of-logs / an-irrational-inequality / to-log-or-not-to-log
  (flipping the lane-9 by-reference row) / how-far-did-the-earth-move;
  enrichment + 34 new-text bodies filed as `syllabai-resources#119`,
  MANIFEST v11 — 548 files corpus-wide; hub `T-UGM-HUB-CONSUME-10`
  merged of record `2d3e082c` (post-merge verified ALL GREEN).
  **lane 11 the compound-angles plane → CIE 9709 Pure 3 3.3
  Trigonometry** — the third lane on the pure-3 course plane and the
  first mostly-mapping lane (operator: "merge #363 then lane 11";
  cross-map `cross-map-p3-trigonometry.json` @ `4dbd50d5`, 103 sweep
  candidates: 28 aligned rows — 1 fresh (r7616, the 3.3.1 pick) + 27
  cross-course rows by reference (23 flips of the lane-5 pre-baked
  pool + 4 one-to-many; the compound-angles station is whole-imported
  of record under lane 5) — plus 42 fresh non-overlaps by reference
  (`bodyImported: false`; 9 riding prior bodies) + 33 rejected with
  reasons; primary picks r7616 / r6018 (rides a reference row,
  disclosed of record);
  enrichment + 1 new-text body filed as `syllabai-resources#126`,
  MANIFEST v12 — 549 files corpus-wide; hub `T-UGM-HUB-CONSUME-11`
  merged of record `07b37c08` (r0-auto; post-merge verified ALL
  GREEN at `main@3c2ecfa4`).
  **lane 12 the differentiation plane → CIE 9709 Pure 3 3.4
  Differentiation** — the fourth lane on the pure-3 course plane and
  the largest fresh-text lane since lane 9 (operator:
  "eyeball+merge of #371 then lane 12"; cross-map
  `cross-map-p3-differentiation.json` @ `506ea24f`, 189 sweep
  candidates: 41 aligned rows — 40 fresh (13 × 3.4.1 / 12 × 3.4.2 /
  15 × 3.4.3; 16 promotions of the lane-10/11 pre-baked
  "P3 3.4 Differentiation" bearing pool superseding their stale rows
  of record) + 1 cross-course flip by reference (r8931 riding its
  lane-7 body under pure-1-differentiation) — plus 29 fresh
  non-overlaps by reference (`bodyImported: false`; 3 honest
  re-routings of lane-10 bearings) + 119 rejected with reasons (the
  lane-7 P1 alignments hold the tangent/normal/optimisation
  embodiments; the 3.4.1 list boundary applied strictly); primary
  picks r6938 / r6530 / r8620 (all fresh);
  enrichment + 40 new-text bodies filed as `syllabai-resources#134`,
  MANIFEST v13 — 589 files corpus-wide; hub `T-UGM-HUB-CONSUME-12`
  merged of record `bf3a7fbe` (r0-auto; post-merge verified ALL GREEN —
  4 blobs byte-identical head↔main, pin `main@bb78ae37`).
  **lane 13 the integration plane → CIE 9709 Pure 3 3.5
  Integration** — the fifth lane on the pure-3 course plane and the
  first lane of record with an honest empty spec point (operator:
  "review+merge #373 then lane 13"; cross-map
  `cross-map-p3-integration.json` @ `21845f3f`, 102 sweep
  candidates: 23 aligned rows — 16 fresh (15 promotions of the
  lane-10/11/12 pre-baked "P3 3.5 Integration" bearing pool
  superseding their stale rows of record) + 1 cross-course flip by
  reference (circular-slice riding its lane-4 body under
  pure-1-circular-measure) + 6 one-to-many joins beside standing
  alignments (r7616, r8774, r9312, r9701, r8694, r5126) — plus 11
  fresh non-overlaps by reference (`bodyImported: false`; 5
  superseding stale bearing rows) + 68 rejected with reasons;
  3.5.4 carries the honest zero of record; primary picks r8679 /
  r9297 / r5126 / r8134 / r8890;
  enrichment + 16 new-text bodies filed as `syllabai-resources#140`,
  MANIFEST v14 — 605 files corpus-wide; hub `T-UGM-HUB-CONSUME-13`
  merged of record `861250a1` — reviewed 33/33 ALL GREEN at `aa4eed74`
  and merged by the operator gate (the first un-intercepted
  review+merge order of the programme).
  **lane 14 the numerical-methods plane → CIE 9709 Pure 3 3.6
  Numerical solution of equations** — the sixth lane on the pure-3
  course plane (operator: "review+merge #377 then 'lane 14'");
  cross-map `cross-map-p3-iteration.json` @ `2d93dd7d`, 48 candidates
  of record: 11 aligned rows — 3 fresh (r8711, r8013,
  staircase-sequences) + 1 cross-course flip by reference (r8404
  riding its unmapped-by-design lane-6 body under pure-1-series:
  the circular-slice precedent) + 7 one-to-many joins beside
  standing alignments (r8231, r8679, r7549, r5948,
  to-log-or-not-to-log, see-the-power, r9082) — plus 1 companion
  non-overlap by reference (staircase-sequences-revisited) + 36
  rejected with reasons; no honest gap this lane (8/3/4 rows); picks
  r8711 / r8404 (rides its lane-6 body — disclosed) / r8231 (rides
  its lane-3 body — disclosed); enrichment + 3 new-text bodies filed
  as `syllabai-resources#145` and **MERGED of record `8b3e57b9`** —
  eyeballed ALL GREEN at `6d0719e9` (blob identity remote == local ==
  staged ×8, census recount 48 = 11 + 1 + 36 exact, drift law verified:
  base ancestor with zero net UGM/LEDGER traffic past `4d857c47`), the
  eyeball gate stayed ours on the resources side too, MANIFEST v15 —
  608 files corpus-wide; hub `T-UGM-HUB-CONSUME-14` filed as
  [`syllabai-v2#380`](https://github.com/SyllabAI/syllabai-v2/pull/380)
  (head `4e824ff4`, 4 files +600/−83: DEFAULT_REF → `main@8b3e57b9`, the
  twenty-station LANE_STATIONS block, the cross-course pick normalization
  law — the r8404 string-form pick catch, first corpus CLA row to NAME its
  pick — bundle of record 6 lanes / 24 spec points / 201 rows / 129
  bodies / memberships 151; gates 54/54 + scoped tsc clean; NOT
  self-merged; **SERVED of record on the Task-19 ack** — #380 found ALREADY
  MERGED by r0-auto at `85088b51` (the fourth interception of record
  after #347/#371/#373, 9m49s after open, head untouched), the full
  post-merge pipeline verifying the bytes 48/48 ALL GREEN: blob identity
  remote PR head == local == merged tree == live main ×4, census recount
  == of record (129 bodies / 201 rows / 24 spec points / memberships
  151), merge parents {c5f53c5a, 4e824ff4}, CI hub+verify success).
  **lane 15 the vector plane → CIE 9709 Pure 3 3.7 Vectors** — the
  seventh lane on the pure-3 course plane and the FIRST with zero
  cross-lane joins and zero flips (the vector stations were never mapped
  by lanes 1–14; CIE pure-1 carries no vectors) (operator:
  "review+merge #380 then lane 15"); cross-map
  `cross-map-p3-vectors.json` @ `16c5f802`, 136 candidates of record:
  20 aligned rows ALL fresh bodies (vector-geometry 15 +
  combining-vectors 5 — lots-of-vector-lines, three-lines, the
  position-vector ratio suite, the scalar-product trio r6493/r7272/r5813,
  the r8456 λ/μ exam question PROMOTED over its stale lane-3-algebra
  non-overlap row) + 6 companion non-overlaps (the plane class, r5089
  rejected BY the 3.7.7 exclusion note, r8828 vs the 3.7.5
  common-perpendicular exclusion) + 110 rejected with reasons; the
  DESIGNED honest gap: 3.7.7 is the spec's own exclusion row and carries
  zero rows by rule; picks hit-the-spot / r8215 / r9575 /
  lots-of-vector-lines / three-lines / r6493; enrichment + 20 new-text
  bodies filed as
  [`syllabai-resources#149`](https://github.com/SyllabAI/syllabai-resources/pull/149)
  (tasks `T-UGM-MODE1-15` + `T-UGM-IMPORT-15`, MANIFEST v15 → v16 —
  628 files corpus-wide; converter pre-flight 139/139; audits 22/22 ALL
  GREEN; NOT self-merged). Mode-2 deep-link
  pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
- Served of record: #149 reviewed ALL GREEN and merged at `b151f65a`; `T-UGM-HUB-CONSUME-15` = syllabai-v2#383 merged at `25615d68` (7 lanes / 149 bodies / 31 spec points / both honest gaps — 3.5.4 + 3.7.7 designed; the r8456 promotion supersede; picks all-fresh); corpus pin `main@b151f65a`; next 3.8 (then 3.9)
- **lane 16 the differential-equations substrate → CIE 9709 Pure 3 3.8 Differential equations** — the EIGHTH lane on the pure-3 course plane and the ZERO-FRESH-BODY lane of record (the mirror of lane 15; operator: "lane 16"): cross-map `cross-map-p3-differential-equations.json` @ `b3700b80`, 53 candidates of record closed exactly — 2 aligned rows BOTH cross-lane joins riding of-record pure-1 bodies (r6959 → 1.7.3 pure-1-differentiation; r7410 → 1.8.2 pure-1-integration; the lane-6 law) + 4 companion non-overlaps (picture-the-process-i/ii modelling-recognition; weight-pulling + from-parabolas-to-catenaries beyond-spec separable-DE machinery) + 47 rejections with reasons; the CORPUS-BOUNDARY DISCLOSURE: the site's own differential-equations station is EMPTY (0 resources, verified live; one of the four never-captured stations), raw-parity 855/855 fail-closed; enrichment filed as [`syllabai-resources#155`](https://github.com/SyllabAI/syllabai-resources/pull/155) (tasks `T-UGM-MODE1-16` + `T-UGM-IMPORT-16`, MANIFEST v16 → v17 — 628 files unchanged, zero body files; audits 36/36 ALL GREEN; NOT self-merged). #155 MERGED at `51630517`; the #157 amendment
  (shape-only, the lane-9 cross-course law) at `c8b80c6a`; hub `T-UGM-HUB-CONSUME-16` filed as
  syllabai-v2#391 (the zero-fresh importer law; bundle 8 lanes / 35 spec points / 232 rows /
  149 bodies unchanged; byref 97; regression law 54/54; CI hub+verify success; NOT
  self-merged). Mode-2 deep-link pilot remains **dropped by operator directive 2026-10-22** (ADR amended;
  kit retained in `pilot/` as record); Mode-3 licensing remains
  operator-gated (its evidence source is now the S1 census).
  further lanes by operator ordering (lanes 9–16 opened the pure-3
  plane — 3.9 Complex numbers is the natural lane 17 per the spine's
  remaining SUB3.9 row, with lane 16's corpus-boundary caution applying
  in advance: the site's complex-numbers stations are among the
  never-captured four) — recipe of record in `docs/INTEGRATION-PLAN.md`
  P7; S1-bridge census run still pending.
