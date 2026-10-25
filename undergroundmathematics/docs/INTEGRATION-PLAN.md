# UGM → SyllabAI integration plan

**Drafted**: 2026-10-22 · status: proposal (operator decision pending)
· upstream: `REVERSE-ENGINEERING-PLAN.md` phases 1–2 complete (855
resources, 2,181 section bodies extracted)

## 0. Objective

Decide and execute how Underground Mathematics (UGM) enriches SyllabAI
math courses — IGCSE and especially IAL — without violating rights and
without re-running UGM's own retrospective mistakes.

Standing constraints:

- UGM content is © University of Cambridge / © UCLES; site is dormant but
  live; no licence currently exists for content reuse of record.
- SyllabAI of-record surfaces: `syllabai-v2` (api + hub), `syllabai-resources`
  (RAG corpus, CIE lanes, exam-question corpus), `syllabai-pastpapers`
  (canonical exam corpus with SHA-256 provenance), Teacher Workbench.
- Integration graduates of record only via proper PRs/ADRs (repo ground
  rules).

## 1. The rights ladder — five integration modes

| Mode | What it is | Rights exposure | Available now? |
|---|---|---|---|
| **0. Research asset** | UGM corpus informs our design; nothing ships | none | ✅ done (phases 1–2) |
| **1. Taxonomy cross-map** | Map UGM stations/lines/key-questions onto CIE/IAL spines as *facts* (slugs, titles, relations) | facts/metadata only — low | ✅ phase 3 work |
| **2. Deep-link enrichment** | Hub lane pages show curated UGM links ("explore further") pointing at undergroundmathematics.org | linking = safe | needs hub change + ADR |
| **3. Licensed content import** | Import question bodies / pedagogy wrappers of record | requires licence from Cambridge Maths / CA Archives | needs conversation |
| **4. Pattern adoption** | Re-author our own content using UGM's *schemas and pedagogy patterns* | none (ideas, not text) | ✅ design work |

The plan below uses modes 1 → 4 immediately, proposes a Mode-2 pilot, and
keeps Mode 3 behind an operator decision + licensing conversation.

## 2. Integration surfaces — where UGM plugs into SyllabAI

| # | UGM asset | SyllabAI component | Mode | The move |
|---|---|---|---|---|
| S1 | **Provenance metadata** (board, QP code, year, question number on 569 review questions) | `syllabai-pastpapers` / Official-ExamQuestion corpus | **1** | **The provenance bridge** (see §2.1) — join key into our own corpus |
| S2 | **Stations & lines** (29/5) + key questions (113) | CIE/IAL spines & lanes (`syllabai-resources` lanes, `cie-phase1..4` registries) | **1** | Cross-map: every lane gets candidate UGM station alignments as an enrichment column |
| S3 | **Review questions as worked examples** (Q→Suggestion→Solution) | SmartChat grounded tutoring; Smart Mark feedback | **2/3** | Mode 2: deep links as "explore a similar challenge"; Mode 3: import as exemplar solutions |
| S4 | **Suggestion layer** (hint-before-solution) | SmartChat hint policy | **4** | Adopt the pattern: our tutor emits a Suggestion-class hint before any solution; hint authored per lane from UGM-style prompts |
| S5 | **MUST/MAY/CAN'T + task archetypes** (Many ways problem, Problem requiring decisions, Fluency exercise…) | Test Builder item archetypes; task taxonomy | **4** | Add task-archetype tags to item schema; author MUST/MAY/CAN'T generators per topic |
| S6 | **Pervasive ideas** (invariance, symmetry, limits…) | Paper A four-layer struggle model; misconception tagging | **4** | Second orthogonal tagging axis on items/lanes — misconception-oriented, matches our learner-model research |
| S7 | **Teacher support pages** (opportunities-for-learning prompt tables) | Teacher Workbench; teacher-facing materials | **2/4** | Mode 2: link from lane teacher view; Mode 4: re-author prompt tables per CIE lane |
| S8 | **Tubemap IA** (map positions as data, modal nav) | Hub navigation concepts | **4** | Future: subject-level "map view" of lanes/links; no commitment |

### 2.1 The provenance bridge (the highest-value, lowest-risk move)

UGM carries acknowledgements on 623 of 855 extracted records (the 569
review questions plus sourced teaching resources), e.g.
e.g. *"UCLES O level Additional Mathematics 2, QP 420/2, 1962, Q7(ii),
7(iii)"*. SyllabAI already owns a canonical exam-question corpus with
manifests (`syllabai-resources` Official-ExamQuestion, `syllabai-pastpapers`
SHA-256 ledgers).

**Move**: parse UGM acknowledgements into (board, qualification, paper code,
year, question numbers) tuples → join against our corpus → for every match we
get, for free:

1. **worked-solution alignment**: UGM's solution *design* (what a good
   solution does step-wise, what the Suggestion hint is) becomes an
   authoring guide for our own solution/marking of that same question —
   our content, their pedagogy as scaffold;
2. **difficulty/curriculum signal**: UGM's station + level (Introducing/
   Developing) for a question we already serve;
3. **gap census aid**: UGM stations with many review questions but no match
   in our corpus = candidate acquisition targets for `syllabai-pastpapers`.

This uses only *facts* from UGM (mode 1) — no licence required — and is
worth doing regardless of any Mode-3 outcome.

## 3. Syllabus fit (set expectations)

- UGM is **post-16 A level maths** → primary fit is **IAL Pure (P1–P4)**
  lanes: quadratics, polynomials, trig, calculus chain (9 stations),
  exponentials/logs, sequences, vectors, geometry of equations.
- **IGCSE** overlap is partial: algebra/quadratics/circles/trig/sequences
  stations and ~the easier review questions; calculus stations out of scope.
- Stations with **no** SyllabAI analogue (matrices, complex numbers,
  hyperbolics, differential equations — the 4 under-construction ones aside)
  map to **Further Maths / IAL Further Pure**, a future course line.
- Conclusion: cross-map produces an **IAL-first enrichment sheet**, IGCSE
  gets the algebra/trig subset. Document the non-overlap rather than force
  mappings.

## 4. Execution plan (phased, repo-conventions-aware)

### P3a — corpus cleanup (this repo, no dependencies) `[x]`
- [x] `qwell` dedup pass: strip re-displayed problem from
      suggestion/solution bodies into a shared `questionWell` field —
      done 2026-10-22: 2,204 re-displays stripped, 584 section-unique
      qwells kept (flagged), 791 canonical wells; substring rule handles
      multi-part resources
- [x] emit `ugm-clean/` per-station JSON (schema stable, bodies clean) —
      `resources/ugm-clean/{station}.json`, 24 files
- [x] parse all 569 acknowledgements into structured provenance tuples;
      publish `resources/derived/review-question-provenance.json` —
      done 2026-10-22: 623 acks processed, 572 parsed (569 review + 3),
      boards/years/labels structured; S1 join key ready

### P3b — enrichment data (this repo) `[x]`
- [x] station→line→key-question→pervasive-idea relation graph export
      (JSON, one node/edge table) — done 2026-10-22:
      `resources/derived/relation-graph.json` — 1,295 nodes / 7,783 edges
      across 8 node kinds (station 29, line 5, key-question 113,
      pervasive-idea 6, resource-type 14, tag 11, resource 855,
      keyphrase 262 unresolved) and 9 edge relations (passes-through 64,
      belongs-to 855, has-type 855, addresses 1,530, sits-on 1,272,
      illustrates 331, related-to 290 unique [Around/Back/Forward],
      tagged 300, keyphrased 2,286); GraphML twin
      `relation-graph.graphml`; raw per-axis captures in
      `resources/derived/relations/`. Key discovery: all six
      per-resource relation endpoints are anonymously readable
      (`/api/resources/{id}/…`, 5,130 calls, 0 failures)
- [x] per-station **enrichment sheet**: resource inventory with type,
      level, key questions, has-teacher-support, asset links — the
      catalog a course designer consumes — done 2026-10-22:
      `resources/derived/enrichment-sheets/{station}.json` (25 sheets,
      855 resources) + `INDEX.md`; each resource carries type, level,
      key questions, lines, pervasive ideas, tags, related resources,
      teacher-support presence+sections, question-well source, asset
      links, provenance tuple and interactivity labels; station-level
      counts include KQ coverage (111/113 key questions addressed corpus-
      wide). Consumes ugm-clean (wells), content (teacher support),
      content-assets, review-question-provenance, relation graph

### P3c — spine cross-map pilot (this repo + `syllabai-resources`) `[x]`
- [x] export lane list + item inventory for **one IAL Pure lane**
      (quadratics — UGM's richest station, 59 resources) and one
      CIE IGCSE lane for contrast — done 2026-10-22:
      `resources/derived/spine-export/cie-a-level-maths-20-pure-1.json`
      (9709 P1 Quadratics 1.1.1–1.1.5) +
      `cie-igcse-maths-25-extended.json` (0580 Extended quadratics-bearing
      points). Finding: item attachment in the of-record content map is
      sparse (10 items on 1.1.x of 1,728 course items) → UGM enrichment
      attaches at spec-point/lane level
- [x] produce `docs/cross-map-quadratics.md`: lane item ↔ UGM resource
      alignments with confidence + mode flags (S1 provenance matches
      highlighted) — done 2026-10-22: 56/59 aligned (95%), 3 explicit
      non-overlaps, mode-2 shortlists per spec point, S1 bridge status;
      machine-readable twin in `resources/derived/cross-map-quadratics.json`
- [x] review with operator; if useful, generalize (script + all-lane run)
      and graduate via PR to `syllabai-resources` (mode-1 artifacts are
      facts/links — safe to land) — **pilot ready for operator review**;
      generalisation proposal in the doc §8

### P4 — decision doc for operator `[x]`
- [x] draft ADR (in `syllabai-v2/docs/adr` style, content authored here
      first): **"UGM integration mode"** — recommend Mode 2 pilot + Mode 4
      adoption list; Mode 3 contingent on licensing — done 2026-10-22:
      `docs/ADR-UGM-0001-ugm-integration-mode.md` — adopts Option B
      (Mode 1 facts + Mode 4 doctrine baseline, Mode-2 "Explore further"
      pilot on the IAL P1 quadratics lane behind a feature flag with
      link-health job + Wayback fallback + CTR floor 1.0%/28d continue,
      3.0% generalise, below-floor kill), explicitly rejects shipping UGM
      body text of record in any mode; early-revisit triggers (site dark,
      floor missed, licensing opens, hub arch change); status **Accepted**
      — ratified by operator 2026-10-22, without amendments
- [x] the ADR records the licensing-ask scope if operator wants Mode 3
      (worked solutions + suggestion wrappers for matched provenance only —
      a narrow, grantable ask, not the whole corpus) — done 2026-10-22:
      ADR §Decision item 4 — provenance-matched questions only (S1 tuple
      match), non-exclusive, attribution in UI mirroring their
      acknowledgement strings, schema after their `copyright-licences`
      entity; outreach order Cambridge Mathematics → CA Group Archives;
      S1 match census = negotiation exhibit; conversation starts only
      after pilot CTR evidence exists

### P5 — conditional Mode-2 pilot in hub `[~]` *(DROPPED by operator directive 2026-10-22 — "don't need links to UGM"; ticket + pilot kit retained below as record; syllabai-v2#305 closed not_planned. Mode-1 data landing continues: quadratics facts PR = [syllabai-resources#55](https://github.com/SyllabAI/syllabai-resources/pull/55))*
- [x] author the implementation ticket + pilot kit — done 2026-10-22:
      `pilot/` = ticket (flag spec, render spec, health-job state machine,
      CTR instrumentation + floors, acceptance criteria, ADR conformance
      map) + `pilot-links-quadratics.json` (24-link pool, 5 primary) +
      `link-health-check.sh` (state-machine tested: SWAP/HIDE/alert,
      fail-closed) + `wayback-bootstrap.sh` + dry-run report (24/24 live
      200). **Launch gate G1 found: 0/24 resource pages have Wayback
      snapshots** (availability API + CDX verified 2026-10-22) →
      fail-closed render law added; bootstrap is blocking before enable
- [~] hub lane page: "Explore further" module rendering 3–5 curated UGM
      deep links per lane (from the cross-map), rel-nofollow, link-health
      check job (site is dormant — guard against rot, Wayback fallback) —
      **DROPPED with the P5 directive 2026-10-22**; superseded by the direct
      content-consumption surfaces (P7, live for lanes 1–4 via #308/#312/#321/#327)
- [~] measure: CTR on UGM links from lane pages — moot with the link module
      dropped; the direct surfaces' engagement measurement is operator-scoped

### P6 — conditional Mode-3 licensing track `[ ]` *(operator-gated)*
- [ ] outreach to Cambridge Mathematics (they host UGM; a preservation-
      minded reuse conversation is plausible)
- [ ] if granted: import pipeline lands of record via `syllabai-v2` PR
      with provenance + licence fields first-class (their own
      `copyright-licences` entity is the schema hint)
      *(note 2026-10-23: the text import below lands under the operator's
      permission attestation — P6 remains the optional track for formal
      licence instruments with Cambridge)*

### P7 — direct UGM text import of record `[~]` *(operator attestation 2026-10-23: "Continue and downloaded text can ship into SyllabAI. We have permission" — supersedes "Mode-3 only route" from the 2026-10-22 amendment; ADR Status Tracking 2026-10-23)*
- [x] licensing of record: **Amendment 2026-10-23** appended to
      `syllabai-resources` `LICENSE-DATA.md` (attestation verbatim, scope =
      downloaded UGM text, takedown/provenance law unchanged) — the exact
      path the `UGM-Enrichment/` README anticipated for text of record
- [x] first lane: **quadratics → CIE 9709 P1** — 59 resources imported as
      `UGM-Resources/pure-1-quadratics/` in `syllabai-resources` — **PR opened:
      [syllabai-resources#58](https://github.com/SyllabAI/syllabai-resources/pull/58)** (task
      **`T-UGM-IMPORT-1`**; text-only: images/PDF/GeoGebra recorded as
      front-matter refs, not fetched; math byte-true; MANIFEST.json sha256
      identity; spec points SUGGESTED with primaryPick cross-referenced to
      `UGM-Enrichment/` #55; 3 resources honestly unmapped) — **MERGED of
      record 2026-10-23 with #55** (`main@91eed732`; both LEDGER entries
      ordered; operator-delegated review + merge with evidence comments;
      self-approval impossible on the shared PAT)
- [x] hub consumption wiring (syllabai-v2 surfaces the corpus on lane
      pages — the content successor of the dropped #305 link module) —
      **PR opened: [syllabai-v2#308](https://github.com/SyllabAI/syllabai-v2/pull/308)**
      (task **`T-UGM-HUB-CONSUME-1`**; importer `import_ugm.py` with
      fail-closed audits → `content/cie-a-level-maths-20-pure-1/ugm-resources.json`;
      flag law `content/flags.json` absent=OFF per ADR-CLASS-0001 practice;
      hub card + spec-point index + reader behind `src/lib/ugm.ts`; math
      byte-true through the shared renderer; SUGGESTED + rights surfaces
      mandatory; tsc/eslint/prebuild gates green locally) — **MERGED of record
      2026-10-23** ([syllabai-v2#308](https://github.com/SyllabAI/syllabai-v2/pull/308) →
      merge `56db3b96`; branch pre-merged with main@18244e76 — worklog EOF
      conflict resolved in append-log order; operator-delegated eyeball +
      merge per instruction "eyeball PR #308 and merge it")
- [x] second lane: **Combining Functions → CIE 9709 P1 1.2 (1.2.1–1.2.5)** —
      cross-map of record `resources/derived/cross-map-functions.json` +
      `docs/cross-map-functions.md` (P3c lane 2, commit `e59276be`; spine
      export extended with the 1.2 rows `4a592ed0`; 27/38 aligned = 71.1%,
      50 rows, 11 honest non-overlaps incl. 2 honest-empty applet pages;
      sibling station `thinking-about-functions` declared out of scope);
      corpus + facts **merged of record 2026-10-23 as
      [syllabai-resources#61](https://github.com/SyllabAI/syllabai-resources/pull/61)**
      (`a32c6c0f`; tasks `T-UGM-MODE1-2` + `T-UGM-IMPORT-2`; MANIFEST bumped
      to **v2 multi-lane**, lane-1 rows re-verified byte-identical; no new
      license amendment — the 2026-10-23 attestation covers the corpus
      family); hub consumption **merged of record as
      [syllabai-v2#312](https://github.com/SyllabAI/syllabai-v2/pull/312)**
      (`635264b2`; task **`T-UGM-HUB-CONSUME-2`**; bundle schema 1.1
      multi-lane — 2 stations, 10 spec points, 97 resources, 111 candidate
      rows; runtime Zod+loader battery 44/44, tsc/eslint/prebuild green;
      PR #311 manifest conflict resolved preserving both sides)
- [x] third lane: **Geometry of Equations + Circles → CIE 9709 P1 1.3 Coordinate
      geometry (the first two-station lane)** — corpus + facts merged of record
      as [syllabai-resources#66](https://github.com/SyllabAI/syllabai-resources/pull/66)
      (tasks `T-UGM-MODE1-3` + `T-UGM-IMPORT-3`, MANIFEST v3, 85 bodies,
      61/85 aligned, 77 rows over folded codes 1.3.1/1.3.2, 24 honest
      non-overlaps); hub consumption **merged of record as
      [syllabai-v2#321](https://github.com/SyllabAI/syllabai-v2/pull/321)**
      (`f757c643`; task **`T-UGM-HUB-CONSUME-3`**; importer extended for
      multi-station lanes — stationScope-audited lane blocks, per-resource
      front-matter station; bundle 903 KB: 3 lanes / 4 stations, 12 spec
      points, 188 rows, 38 non-overlaps, 182 bodies; lanes 1-2 byte-identical
      through the regen; committed-bundle regression test added; tsc 0,
      packages 527/527)
- [x] fourth lane: **Circular-measure strand → CIE 9709 P1 1.4 Circular
      measure (the first strand lane; operator "extend channel 4" — overrides
      the #321 residual's "1.5 next" default)** — cross-map of record
      `cross-map-circular-measure.json` @ `b52cf1bf` (corpus sweep 855 → 62
      candidates resolved as 17 aligned — 3 new-text + 14 cross-lane
      circles-strand facts incl. 2 lane-3 1.3.2 extensions — plus 4
      non-overlaps and 41 routed to recorded homes; hub fragment 1.4.1a folded
      into 1.4.1; clause-a radian-definition gap recorded, never manufactured;
      primary pick r5534); corpus + facts **merged of record as
      [syllabai-resources#74](https://github.com/SyllabAI/syllabai-resources/pull/74)
      → `1585c4ff`** (tasks `T-UGM-MODE1-4` + `T-UGM-IMPORT-4`, MANIFEST v4, 5
      new-text bodies — strand-lane shape: cross-lane `ugmId` uniqueness law
      keeps one text body per resource, circles-strand mappings by
      `textOfRecordUnder` reference; converter byte-identical vs lane-1/3
      ground truths; full 4-lane importer audit green: 187 bodies, 0 dup ids);
      hub consumption **merged of record as
      [syllabai-v2#327](https://github.com/SyllabAI/syllabai-v2/pull/327) →
      `2684a8e4`** (task `T-UGM-HUB-CONSUME-4`; the fail-closed cross-lane
      join — 12 lane-3 non-overlaps flipped to aligned under 1.4.1, r8946/
      r9386 one-to-many, fleet 4 lanes / 8 stations / 13 spec points / 205
      rows / 187 bodies; bundle regression 18/18, hub tsc 0)
- [x] fifth lane: **Trigonometry: Triangles to Functions + Compound Angles →
      CIE 9709 P1 1.5 Trigonometry (the two-station lane; operator "lane 5";
      lanes 1–3 shape restored)** — cross-map of record
      `cross-map-trigonometry.json` @ `f3ef5745` (corpus sweep 855 → 299
      candidates resolved as 41 aligned — 36 TTF + 3 TCA substrate + 2
      cross-station strays r7912/r7184; 55 alignment rows — plus 36
      non-overlaps and 220 routed to recorded homes; NO fold fragments:
      1.5.1–1.5.5 verbatim into the spine export; compound-angles station's
      honest P3 2.3 mapping recorded — 24 non-overlaps, five of lane 4's
      routed-1.5 preview pool refined; 2 cross-lane fact joins r9924/r8411 →
      1.5.4 against lane-2 bodies; primary picks going-round-in-circles /
      trig-tables / inverse-or-not / r5269 / r6138); corpus + facts filed as
      **[syllabai-resources#79](https://github.com/SyllabAI/syllabai-resources/pull/79)**
      (tasks `T-UGM-MODE1-5` + `T-UGM-IMPORT-5`, MANIFEST v5, whole-substrate
      77 text bodies — station-lane corpus law: non-overlaps imported UNMAPPED
      with the coverage note; converter byte-identical vs lane-1/3 ground
      truths; full 5-lane importer audit green: 5 lanes / 12 stations / 18
      spec points / 262 rows / 63 non-overlaps / 264 bodies, 0 dup ids);
      hub consumption (`T-UGM-HUB-CONSUME-5`) pending on the syllabai-v2 side
- [x] sixth lane: **Sequences + Counting and Binomials →
      CIE 9709 P1 1.6 Series (the second two-station lane; operator "lane 6
      (CIE 9709 P1 1.6 Series)")** — cross-map of record
      `cross-map-series.json` @ `82964ce4` (corpus sweep 855 → 137
      candidates resolved as 49 aligned — 43 substrate + 6 cross-station
      strays r5640/r9404/r9916/r8260/r6592/r9312; 56 alignment rows — plus
      50 non-overlaps and 36 routed to recorded homes; NO fold fragments:
      1.6.1–1.6.4 verbatim into the spine export; findings of record:
      Sequences maps 31/42 onto 1.6.2–1.6.4, Counting and Binomials is
      combinatorics/logic-dominated (39 non-overlaps) around a binomial core
      (12/51), and the general-index binomial questions carry P3 Series
      bearings — the P3-lane substrate preview, mirroring lane 5's P3 2.3
      finding; 2 cross-lane fact joins r7553/r9527 → 1.6.3 against lane-2
      bodies; primary picks r7078 / sort-it-out / r8907 / square-spirals);
      corpus + facts filed as
      **[syllabai-resources#89](https://github.com/SyllabAI/syllabai-resources/pull/89)**
      (tasks `T-UGM-MODE1-6` + `T-UGM-IMPORT-6`, MANIFEST v6, whole-substrate
      99 text bodies — station-lane corpus law: non-overlaps imported UNMAPPED
      with the coverage note; converter byte-identical vs the full 77-file
      lane-5 of-record corpus); hub consumption (`T-UGM-HUB-CONSUME-6`) pending
      on the syllabai-v2 side
- [x] seventh lane: **Introducing Calculus + Calculus of Powers →
      CIE 9709 P1 1.7 Differentiation (the third two-station lane; operator
      "Proceed Lane 7")** — cross-map of record
      `cross-map-differentiation.json` @ `93575e69` (corpus sweep 855 → 195
      candidates resolved as 74 aligned — 40 substrate + 34 cross-station
      strays; 107 alignment rows — plus 32 non-overlaps (the
      trapezium-rule/kinematics cluster in Introducing Calculus; the
      trapezium rule is not in the 2023–2025 P1 spec) and 86 routed to
      recorded homes; NO fold fragments: 1.7.1–1.7.4 verbatim into the spine
      export; findings of record: Calculus of Powers is the P1 workhorse
      (31/48 aligned) while Introducing Calculus splits between
      gradient-concept building blocks and the non-overlap cluster; the
      chain-rule/product-rule/calculus-trig-log stations are P3-bearing and
      routed with bearings named; 3 cross-lane fact joins r5640/r7115/r8936;
      primary picks r7692 / r9942 / r8065 / r9260); corpus + facts filed as
      **[syllabai-resources#91](https://github.com/SyllabAI/syllabai-resources/pull/91)**
      (tasks `T-UGM-MODE1-7` + `T-UGM-IMPORT-7`, MANIFEST v7, whole-substrate
      106 text bodies — station-lane corpus law: non-overlaps imported UNMAPPED
      with the coverage note; converter byte-identical vs the full 99-file
      lane-6 of-record corpus); hub consumption (`T-UGM-HUB-CONSUME-7`) pending
      on the syllabai-v2 side
- [x] **eighth lane — CIE 9709 P1 1.8 Integration (operator: next lane
      per this plan; the Pure 1 spine is now complete of record)** — cross-map
      of record `cross-map-integration.json` @ `c04abfbd` (corpus sweep
      855 → 91 candidates resolved as 28 aligned — 10 new-text strand
      (calculus-meets-functions 7, chain-rule 2, product-rule 1) + 18
      cross-lane fact joins to `pure-1-differentiation/` bodies, 13 of them
      flipping the lane-7 Calculus-of-Powers non-overlaps of record with
      reasons retained; 28 alignment rows; 0 new non-overlaps; 32 routed
      (P3-technique honesty) + 31 rejected with reasons; NO fold fragments:
      1.8.1–1.8.4 verbatim into the spine export (33 rows — Pure 1 complete);
      findings of record: lane 7's integration-dressed deferral realised;
      1.8 coverage area/volume-dominated (12 of 28 rows 1.8.4) while
      reverse-process/constant-of-integration coverage is thin (2 + 4);
      primary picks r8716 / r7734 / r6067 / r9357); corpus + facts filed as
      **[syllabai-resources#96](https://github.com/SyllabAI/syllabai-resources/pull/96)**
      (tasks `T-UGM-MODE1-8` + `T-UGM-IMPORT-8`, MANIFEST v8, 10 new-text
      files — strand-lane corpus law: new text only, no unmapped imports,
      cross-lane 1.8 mappings by reference); hub consumption
      (`T-UGM-HUB-CONSUME-8`) pending on the syllabai-v2 side
- [x] **ninth lane — CIE 9709 **Pure 3** 3.1 Algebra (operator:
      "review+merge #357 then proceed with lane 9"; the first lane on the
      pure-3 course plane, beyond the completed Pure 1 spine)** — cross-map
      of record `cross-map-algebra.json` @ `3098d8eb` (corpus sweep
      855 → 90 candidates resolved as 47 aligned rows — 38 fresh rows over
      35 substrate resources (`inequalities`, `r5276`, `r6577` carry two
      codes each) + 9 cross-lane fact joins riding lanes 2/6/7/8 bodies:
      5 flips (r8427 from the lane-2 non-overlaps; r5245/r6295/r6340/r7477
      from the lane-6 non-overlaps whose recorded "P3 Series bearing"
      reasons predicted this landing) + 4 one-to-many (r5362, r9523, r9082,
      r9701); 16 fresh non-overlaps recorded by reference only
      (`bodyImported: false`, the lane-8 candidate-model law) + 30
      of-record candidates rejected with reasons — the integer-index
      binomial pool stays 1.6.1 of record, 3.1.6 being the rational-index
      `|x| < 1` expansion that realises the lane-6 P3 preview; NO fold
      fragments — 3.1.1–3.1.6 verbatim into the spine export (new pure-3
      file; the repaired hub parse rows of record,
      `T-SPECS-CIE-PARSE-REPAIR-1`); findings of record: UGM's polynomials
      station is the 3.1.4 workhorse (21 of 38 fresh rows), the modulus
      limb (3.1.1/3.1.2) is thin outside the thinking-about-functions
      scaffolded tasks, and partial fractions ride integration work in
      5 of 7 rows; primary picks absolutely / inequalities / whats-left /
      r6577 / r7792 / r7436); corpus + facts filed as
      **[syllabai-resources#114](https://github.com/SyllabAI/syllabai-resources/pull/114)**
      (tasks `T-UGM-MODE1-9` + `T-UGM-IMPORT-9`, MANIFEST v10, 35 new-text
      files — candidate-model corpus law: non-overlaps by reference, no
      unmapped imports); hub consumption (`T-UGM-HUB-CONSUME-9`, opening
      the pure-3 bundle plane) pending on the syllabai-v2 side
- [x] **tenth lane — CIE 9709 **Pure 3** 3.2 Logarithmic and exponential
      functions (operator: "merging #358 then proceed with lane 10"; the
      second lane on the pure-3 course plane, first by spine adjacency
      after 3.1)** — cross-map of record `cross-map-log-and-exp.json` @
      `980556af` (corpus sweep 855 → 71 candidates resolved as 39 aligned
      rows — 34 fresh rows over 34 substrate resources, all single-code,
      31 of them from the dedicated exp-and-log station plus 3 strays
      (to-the-limit, r7077, powerful-fractions — the last two lane-5
      pre-baked "2.2" routings) + 5 cross-course fact joins riding lanes
      2/5/6 bodies (r9824 → 3.2.2, r7607 → 3.2.1, r6137 → 3.2.1,
      r8260 → 3.2.3, r7184 → 3.2.1; all one-to-many, no flips); 26 fresh
      non-overlaps recorded by reference only (`bodyImported: false`) + 6
      of-record candidates rejected with reasons; NO fold fragments —
      3.2.1–3.2.4 verbatim into the spine export (the 3.2.2/3.2.3
      dropped-math title artifacts carried verbatim, no `T-SPECS` repair
      needed); findings of record: the exp-and-log station is the 3.2
      workhorse and was essentially untouched (2 of 40 of record before
      this lane — both now joined), the lane-5 pre-baked "2.2
      Logarithmic and exponential functions" bearings all landed (9 of 10
      aligned, 1 routed out honestly), and the 3.2.2 e/ln limb is
      structurally thin (2 fresh + 1 join — UGM's e/ln corpus rides the
      lane-7/8 recorded P3 3.4/3.5 bearings, which stand); primary picks
      proving-laws-of-logs / an-irrational-inequality /
      to-log-or-not-to-log (flipping the lane-9 nonOverlapByReference
      row) / how-far-did-the-earth-move); corpus + facts filed as
      **[syllabai-resources#119](https://github.com/SyllabAI/syllabai-resources/pull/119)**
      (tasks `T-UGM-MODE1-10` + `T-UGM-IMPORT-10`, MANIFEST v11, 34
      new-text files — converter pre-flight 45/45 byte-identity vs the
      lane-8 AND lane-9 of-record bodies); hub consumption
      (`T-UGM-HUB-CONSUME-10`, extending the pure-3 bundle plane) pending
      on the syllabai-v2 side
- [x] **eleventh lane — CIE 9709 **Pure 3** 3.3 Trigonometry (operator:
      "merge #363 then lane 11"; the third lane on the pure-3 course plane
      and the FIRST MOSTLY-MAPPING lane)** — the body-of-record audit found
      the dedicated compound-angles station and TTF whole-imported of record
      under lane 5 (the two-station lane law, 77 bodies), so the lane-5
      pre-baked "P3 2.3" pool maps by reference under the lane-9 flip law —
      cross-map of record `cross-map-p3-trigonometry.json` @ `4dbd50d5`
      (corpus sweep 855 → 103 candidates resolved as 28 aligned rows —
      1 fresh row (r7616, the 3.3.1 pick) + 27 cross-course rows by
      reference: 23 flips of the lane-5 pool rows + 4 one-to-many
      (going-round-in-circles, muddled-trig, trig-tables 3.3.1; r7021 3.3.2);
      no flips of pure-3 rows, nothing duplicated) + 42 fresh non-overlaps
      recorded by reference only (`bodyImported: false`; 9 riding prior
      bodies per the supersede law) + 33 of-record candidates rejected with
      reasons; primary picks r7616 (3.3.1, fresh) / r6018 (3.3.2 — rides a
      reference row, disclosed of record); corpus + facts filed as
      **[syllabai-resources#126](https://github.com/SyllabAI/syllabai-resources/pull/126)**
      (tasks `T-UGM-MODE1-11` + `T-UGM-IMPORT-11`, MANIFEST v12, 1 new-text
      file — converter pre-flight 79/79 byte-identity vs the lane-8 AND
      lane-9 AND lane-10 of-record bodies); hub consumption
      (`T-UGM-HUB-CONSUME-11`) pending on the syllabai-v2 side
- [x] **twelfth lane — CIE 9709 **Pure 3** 3.4 Differentiation (operator:
      "eyeball+merge of #371 then lane 12"; the fourth lane on the pure-3
      course plane and the LARGEST FRESH-TEXT LANE SINCE LANE 9)** — #371
      (T-UGM-HUB-CONSUME-11) verified already merged of record at arrival
      (`07b37c08`, r0-auto) with the fail-closed post-merge pipeline ALL
      GREEN (the #347 precedent) — the differentiation substrate
      concentrates on the chain-rule and product-rule stations, which
      lane 7 did NOT whole-import (only 7 + 2 stray alignments), so the
      lane inverts lane 11's shape: cross-map of record
      `cross-map-p3-differentiation.json` @ `506ea24f` (corpus sweep
      855 → 189 candidates resolved as 41 aligned rows — 40 fresh rows
      (13 × 3.4.1 standard derivatives, 12 × 3.4.2 product/quotient,
      15 × 3.4.3 parametric/implicit; 16 of them promotions of the
      lane-10/11 pre-baked "P3 3.4 Differentiation" bearing pool
      superseding their stale rows of record) + 1 cross-course flip by
      reference (r8931 riding its lane-7 body)) + 29 fresh non-overlaps
      recorded by reference only (`bodyImported: false`; 3 honest
      re-routings of lane-10 bearings) + 119 of-record candidates
      rejected with reasons (the lane-7 P1 alignments already hold the
      tangent/normal/optimisation embodiments — the 3.4.1 list boundary
      applied strictly); primary picks r6938 / r6530 / r8620 (all fresh);
      corpus + facts filed as
      **[syllabai-resources#134](https://github.com/SyllabAI/syllabai-resources/pull/134)**
      (tasks `T-UGM-MODE1-12` + `T-UGM-IMPORT-12`, MANIFEST v13, 40
      new-text files — converter pre-flight 80/80 byte-identity vs the
      lane-8 AND lane-9 AND lane-10 AND lane-11 of-record bodies); hub
      consumption (`T-UGM-HUB-CONSUME-12`) pending on the syllabai-v2 side
- [x] **thirteenth lane — CIE 9709 **Pure 3** 3.5 Integration (operator:
      "review+merge #373 then lane 13"; the fifth lane on the pure-3
      course plane and the FIRST LANE OF RECORD WITH AN HONEST EMPTY
      SPEC POINT)** — #373 (T-UGM-HUB-CONSUME-12) verified already merged
      of record at arrival (`bf3a7fbe`, r0-auto — the third interception
      after #347/#371) with the fail-closed post-merge pipeline ALL GREEN
      (4 blobs byte-identical head↔main; census exact; gates green) — the
      integration substrate concentrates on the calculus-trig-log,
      chain-rule and product-rule stations, so the lane-10/11/12
      pre-baked "P3 3.5 Integration" bearing pool converts or declines:
      cross-map of record `cross-map-p3-integration.json` @ `21845f3f`
      (corpus sweep 855 → 102 candidates resolved as 23 aligned rows —
      16 fresh rows (15 of them promotions of the bearing pool
      superseding their stale rows of record) + 1 cross-course flip by
      reference (circular-slice riding its lane-4 body) + 6 one-to-many
      joins beside standing alignments (r7616, r8774, r9312, r9701,
      r8694, r5126)) + 11 fresh non-overlaps by reference
      (`bodyImported: false`; 5 superseding stale bearing rows) + 68
      rejected with reasons (every one verified against its solution of
      record); **3.5.4 carries the honest zero** (no f′(x)/f(x) resource
      exists corpus-wide — rule 3); primary picks r8679 / r9297 / r5126
      (rides its lane-9 body — the r6018 convention disclosed) / r8134 /
      r8890; corpus + facts filed as
      **[syllabai-resources#140](https://github.com/SyllabAI/syllabai-resources/pull/140)**
      (tasks `T-UGM-MODE1-13` + `T-UGM-IMPORT-13`, MANIFEST v14, 16
      new-text files — converter pre-flight 120/120 byte-identity vs the
      lane-8/9/10/11/12 of-record bodies; plus the lane-12 LEDGER restore
      the #136 clobber had reverted); hub consumption
      (`T-UGM-HUB-CONSUME-13`) pending on the syllabai-v2 side
- [x] **fourteenth lane — CIE 9709 **Pure 3** 3.6 Numerical solution of equations (operator:
      "review+merge #377 then \"lane 14\""; the sixth lane on the pure-3 course plane)** — #377
      (T-UGM-HUB-CONSUME-13) reviewed 33/33 ALL GREEN and MERGED of record at `861250a1` BEFORE the lane
      opened (the eyeball gate stayed ours — the first un-intercepted review+merge order of the programme;
      lane-13 SERVED, hub pure-3 plane at 5 lanes); the lane inverts lane-13: NO pre-baked bearing pool
      exists (no prior lane ever routed rows to 'P3 3.6'), and the iteration content is scattered across
      nine stations — so the lane joins heavily: cross-map of record
      `cross-map-p3-iteration.json` @ `2d93dd7d` (corpus sweep 855 → 48 candidates of record resolved as
      11 aligned rows — 3 fresh rows (r8711 3.6.1 the purest sign-change search; r8013 3.6.1 graphical
      solution of 3^x=3x+2; staircase-sequences 3.6.2+3.6.3 the x = 1 + 1/x fixed point) + 1 cross-course
      flip by reference (r8404 riding its unmapped-by-design lane-6 body under pure-1-series — the
      circular-slice precedent, first flip whose prior body carried no spec assertion) + 7 one-to-many
      joins beside standing alignments (r8231 Newton-Raphson + trial-and-improvement to 3 d.p.; r8679 the
      numerical-canon survey on the lane-13 pick body; r7549; r5948 the chord-intercept
      linear-interpolation formula; to-log-or-not-to-log; see-the-power; r9082)) + 1 fresh non-overlap by
      reference (staircase-sequences-revisited, the companion disclosure) + 36 rejected with reasons
      (every one verified against its solution of record); **no honest gap this lane** (3.6.1 carries 8
      rows, 3.6.2 three, 3.6.3 four); primary picks r8711 (fresh) / r8404 (rides its lane-6 body — the
      r6018 convention disclosed) / r8231 (rides its lane-3 body — disclosed); corpus + facts filed as
      **[syllabai-resources#145](https://github.com/SyllabAI/syllabai-resources/pull/145)**
      (tasks `T-UGM-MODE1-14` + `T-UGM-IMPORT-14`, MANIFEST v14 → v15, 3 new-text files — converter
      pre-flight 136/136 byte-identity vs the lane-8..13 of-record bodies); #145 MERGED of
      record `8b3e57b9` (eyeballed ALL GREEN at `6d0719e9` — blob identity ×8, census recount,
      drift law); hub consumption `T-UGM-HUB-CONSUME-14` filed as
      [syllabai-v2#380](https://github.com/SyllabAI/syllabai-v2/pull/380) (head `4e824ff4` —
      pin advance + the twenty-station block + the cross-course pick normalization law, the
      r8404 string-form pick catch; bundle of record 6 lanes / 24 spec points / 201 rows /
      129 bodies; 54/54 GREEN; NOT self-merged)
- [ ] further lanes (the Pure 1 spine 1.1–1.8 is complete of record and
      lanes 9–14 opened the pure-3 plane at 3.1 Algebra, 3.2 Logarithmic
      and exponential functions, 3.3 Trigonometry, 3.4 Differentiation,
      3.5 Integration and 3.6 Numerical solution of equations; the recorded
      next substrate is 3.7 (then 3.8–3.9) per the spine's remaining SUB3.7–SUB3.9
      rows of record; ordering is the
      operator's call)
      lane-by-lane on operator ack — recipe of record:
      `scripts/ugm_import_build.py --lane <name>` + the multi-lane importer
      (`LANE_STATIONS` entry + expected census; multi-station and strand
      blocks now supported) + `ugm-resources.json` re-run at the new pin

## 5. Mode-4 pattern adoption — do these regardless (design tasks)

1. **Suggestion layer for SmartChat**: hint taxonomy per lane (nudge →
   strategy → scaffold), inspired by UGM suggestions; feeds the SmartChat
   spec's hint policy.
2. **Task archetypes in Test Builder**: add `archetype` enum to item
   authoring (fluency / many-ways / decision-required / investigation /
   MUST-MAY-CANT) — improves item diversity and Smart Mark rubric variety.
3. **Pervasive-idea tagging**: second axis on items (misconception/
   insight-oriented) feeding the Paper A learner model.
4. **Teacher prompt tables**: Workbench view showing per-lane "questions
   teachers could ask" (re-authored, UGM-patterned).

## 6. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Rights drift (someone ships UGM text of record) | Modes ladder is explicit in this doc + ADR gate before any of-record landing; provenance-bridge needs no text |
| Dormant site / link rot | Wayback mirror check in pilot; store archive.org fallback URL per enrichment row |
| Syllabus mismatch (UGM ≠ CIE ordering) | Cross-map reports confidence + non-overlap explicitly; never force mappings |
| Stale pedagogy (2016-era) | Treat UGM as design reference + supplement, never as the spine; our lanes own the sequence |
| Effort sink | Pilot is one lane; generalize only after operator review |

## 7. Success measures

- P3c pilot: ≥70% of pilot-lane items have a defensible UGM alignment or an
  explicit non-overlap note
- S1 bridge: % of UGM 569 acknowledgements parsed; % matching our corpus
- Mode-2 pilot (if run): lane-page UGM CTR ≥ some floor agreed at ADR time
- Mode-4: suggestion-layer + archetype tags land in the relevant of-record
  specs (SmartChat spec §, Test Builder schema)
