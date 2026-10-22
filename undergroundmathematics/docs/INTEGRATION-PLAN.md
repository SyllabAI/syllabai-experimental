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
- [ ] hub lane page: "Explore further" module rendering 3–5 curated UGM
      deep links per lane (from the cross-map), rel-nofollow, link-health
      check job (site is dormant — guard against rot, Wayback fallback)
- [ ] measure: CTR on UGM links from lane pages

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
      `UGM-Enrichment/` #55; 3 resources honestly unmapped)
- [ ] hub consumption wiring (syllabai-v2 surfaces the corpus on lane
      pages — the content successor of the dropped #305 link module)
- [ ] further lanes (other UGM stations ↔ spine exports) lane-by-lane on
      operator ack — reuse `scripts/ugm_import_build.py` (builder kept in
      the agent workspace; re-emit per lane with a new task id)

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
