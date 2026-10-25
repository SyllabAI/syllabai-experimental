# ADR-UGM-0001: UGM integration mode — Mode-1/4 baseline now, Mode-2 pilot gated, Mode 3 deferred with a narrow licensing ask

| | |
|---|---|
| **Status** | **Accepted** — ratified by the operator on 2026-10-22, without amendments (acceptance of record for this experiment; graduates into `syllabai-v2/docs/adr/` under a hub-scoped number when P5 lands of record) |
| **Deciders** | SyllabAI operator; authored by the undergroundmathematics reverse-engineering track |
| **Date** | 2026-10-22 |
| **Evidence base** | Phases 1–3 of this repo: 855 resources crawled (0 failures), 791 canonical question wells (`resources/ugm-clean/`), 623 structured provenance tuples (`resources/derived/review-question-provenance.json`), relation graph 1,295 nodes / 7,783 edges (`resources/derived/relation-graph.json`), 25 enrichment sheets (`resources/derived/enrichment-sheets/`), quadratics cross-map pilot 56/59 = 95% (`docs/cross-map-quadratics.md`) |
| **Conformance** | `docs/INTEGRATION-PLAN.md` §1 rights ladder + §4 P4 · `docs/IP-AND-COPYRIGHT-NOTES.md` (operator decision appendix) · syllabai-v2 repo ground rules (integration graduates of record only via proper PRs/ADRs) |
| **Style note** | Mirrors `syllabai-v2/docs/adr/ADR-*` structure (Status/Deciders/Context/Options/Decision/Consequences/Status Tracking); graduates into that directory under a hub-scoped number when P5 lands of record |

## Context

Underground Mathematics (UGM) is a dormant-but-live Cambridge resource site
for post-16 A level maths: 855 public resources (569 of them review questions
sourced from UCLES papers back to 1951), organised by an orthogonal taxonomy
(29 stations × 5 lines × 113 key questions × 6 pervasive ideas), with a
pedagogy structure (Problem → Suggestion → Solution, MUST/MAY/CAN'T proof
classification, low-threshold high-ceiling task design) that matches
SyllabAI's tutoring and item-authoring goals unusually well.

SyllabAI wants that value. The constraints that shape every option:

- **Rights**: UGM content is © University of Cambridge; exam questions are
  © UCLES. No licence for content reuse exists today. Linking and facts
  (slugs, titles, relations, provenance metadata) are safe; shipping text
  of record is not. The phase-2 operator decision allows corpus bodies to
  live in *this research repo* with attribution — it does **not** authorise
  any of-record SyllabAI surface to serve them. **(Amended 2026-10-23:**
  the operator attests that permission for the downloaded UGM text to ship
  into SyllabAI is granted and directs the direct text import — recorded of
  record as the Amendment 2026-10-23 in `syllabai-resources`
  `LICENSE-DATA.md` and in Status Tracking; the "text of record is not
  authorised" position is overridden by that attestation.**)**
- **Dormancy**: content frozen ~2016–17; the site is live but unmaintained.
  Any deep-link surface needs rot guarding (health checks + Wayback
  fallback).
- **Fit**: UGM is A-level maths — IAL-first fit, partial IGCSE overlap,
  Further-Mathics analogue for the remainder. Cross-mapping must report
  confidence and explicit non-overlap, never force alignment.
- **Effort discipline**: SyllabAI's own lanes own the learning sequence;
  UGM is a supplement and a design reference, never the spine.
- **Governance**: any of-record landing (hub module, corpus fields, spec
  changes) goes through proper PRs; this ADR is the gate.

The question: **which integration modes does SyllabAI adopt, in what
order, and what exactly would we ask Cambridge for if we ever want Mode 3?**

## Options

### Option A — Mode 1 + 4 only (facts and patterns, no surface change)

Keep everything at the fact level: the provenance bridge (S1), cross-map
enrichment columns on lanes (S2), and the pedagogy patterns adopted into
our own specs (S4–S6: suggestion-class hints, task archetypes,
pervasive-idea second axis, MUST/MAY/CAN'T generators). No learner-facing
UGM presence; nothing to click; zero hub work.

- **For**: absolutely rights-safe; no dormant-site dependency; no hub
  change.
- **Against**: learners never see the best curated maths problem set on
  the web; the 95%-confidence quadratics alignment (and its per-spec-point
  shortlists) goes unused.

### Option B — Mode 1 + 4 baseline, plus a **gated Mode-2 pilot** on one lane *(recommended)*

Everything in A, plus: hub lane pages get an **"Explore further" module**
rendering 3–5 curated UGM deep links per lane (from the P3c cross-map
shortlists), feature-flagged, `rel="nofollow"`, with a link-health job and
per-link Wayback fallback; pilot scoped to the IAL P1 quadratics lane
where the cross-map is strongest (56/59 aligned, per-spec-point mode-2
shortlists already authored); CTR measured against a floor agreed here.

- **For**: learner-visible value at near-zero rights exposure (linking);
  pilot evidence upgrades any future Mode-3 ask; kill switch is trivial.
- **Against**: needs a hub change; dormant-site rot must be engineered
  against (mitigated: health job + fallback URLs).

### Option C — pursue Mode 3 licensing now

Start the Cambridge Mathematics / CA Archives conversation immediately and
plan for imported question bodies + suggestion wrappers of record.

- **For**: richest learner experience if granted.
- **Against**: premature — an ask without pilot evidence and without the
  S1 match census is weaker and wider than it needs to be; licensing
  timelines are outside our control; blocks nothing if deferred (Mode 2
  links deliver learner value meanwhile).

### Option D — stop at research (Mode 0)

Declare phases 1–3 sufficient; archive the corpus; adopt nothing.

- **For**: zero further effort.
- **Against**: discards paid-for work with proven, quantified alignment
  (95% on the pilot lane); the provenance bridge alone (569 sourced exam
  questions with parsed board/paper/year/Q tuples) has direct value to
  `syllabai-pastpapers`.

## Decision (ratified by operator 2026-10-22)

**Adopt Option B.** Specifically, all of:

1. **Mode 1 (adopt now, of-record-eligible as facts)** — the relation
   graph, enrichment sheets, provenance tuples and the quadratics
   cross-map are *facts/metadata* and may land in `syllabai-resources` /
   lane records via normal PRs, one lane at a time, starting with the
   quadratics pilot artifacts. UGM text bodies stay out of all of-record
   repos (research-repo-only, per the IP notes) — **amended 2026-10-23**:
   under the operator's permission attestation, UGM text bodies land in
   `syllabai-resources` as the `UGM-Resources/` corpus family (text-only
   import, task `T-UGM-IMPORT-1`; see Status Tracking).
2. **Mode 4 (adopt as design doctrine; lands via the owning specs' own
   PRs)** — the four patterns from INTEGRATION-PLAN §5:
   - suggestion-layer hint taxonomy (nudge → strategy → scaffold) into the
     SmartChat spec hint policy;
   - `archetype` enum in Test Builder item schema (fluency / many-ways /
     decision-required / investigation / MUST-MAY-CAN'T);
   - pervasive-idea-style second tagging axis on items (misconception/
     insight-oriented) feeding the learner model;
   - teacher prompt tables in the Workbench (re-authored per CIE lane,
     UGM-patterned — never copied verbatim).
3. **Mode 2 (approved as a one-lane pilot, gated)** — "Explore further" on
   the IAL P1 quadratics lane only, behind a feature flag (class-toggle
   style per `syllabai-v2` ADR-CLASS-0001 practice), links
   `rel="nofollow"`, a weekly link-health job (three consecutive failures
   ⇒ auto-fallback to stored Wayback URLs, alert to owner), and a CTR
   floor: **pilot continues only if ≥1.0% of lane-page uniques click ≥1
   UGM link in any 28-day window after a 2-week learning grace; ≥3.0% is
   a strong-generalise signal; below floor ⇒ module is killed by the flag
   and the ADR is amended, not argued**. Generalisation to further lanes
   requires: floor met + cross-map for that lane completed + operator
   ack.

   > **Amended 2026-10-22 (operator directive):** Mode-2 is **dropped before
   implementation** — "don't need links to UGM; you already downloaded the
   resources". Hub ticket syllabai-v2#305 closed not_planned; the prepared
   pilot kit stays in `pilot/` as record. Mode-1/4 continue; Mode-3 remains
   the only route for UGM content of record. See Status Tracking.
4. **Mode 3 (deferred, operator-gated — but the ask is now scoped)** — the
   licensing-ask scope, if and when the operator wants it, is **narrow and
   grantable**: worked-solution bodies + suggestion wrappers **only for
   provenance-matched questions** (questions already in
   `syllabai-pastpapers` whose UCLES board/paper/year/Q tuple matches a
   UGM review question's acknowledgement tuple), non-exclusive, with
   attribution to Cambridge/UCLES in our UI mirroring their
   acknowledgement strings, schema after their own `copyright-licences`
   entity. **Not** the whole corpus, **not** the pedagogy wrappers for
   unmatched questions, **not** teacher-support content. Outreach targets
   in order: Cambridge Mathematics (hosts UGM; preservation-minded reuse
   is their stated interest), then Cambridge Assessment Group Archives
   (permission holder for UCLES papers). The S1 match census produced by
   the provenance bridge becomes the negotiation exhibit — the ask scales
   with the census, and we do not start the conversation before the pilot
   has produced CTR evidence.

**Explicitly rejected for now**: Option C (premature — evidence first);
shipping any UGM body text of record in any mode (rights violation — this
is a hard line, not a preference); forcing cross-map alignments where
confidence is low (the 3 explicit non-overlaps in the pilot are the
pattern to keep).

**Early-revisit triggers (any one forces the decision back to the
operator):**

1. Link-health job reports the UGM origin unreachable past fallback grace
   — deep links pivot to Wayback permanently or the Mode-3 ask accelerates.
2. CTR floor missed in the pilot window — kill the module, keep Mode 1/4
   gains, amend this ADR with the measured number.
3. A licensing conversation opens on the Cambridge side — Mode-3 scope
   re-ratified with the census + pilot data in hand before any import
   pipeline is built.
4. Hub lane-page architecture changes in a way that affects deep-link
   rendering or flag mechanics.

## Consequences

**Positive.** Learner-visible enrichment with no rights exposure; authoring
doctrine upgrades that outlive the pilot (hint layer, archetypes, second
axis); the provenance bridge gives `syllabai-pastpapers` a worked-solution
alignment aid and a gap census for acquisition; a clean, evidence-producing
path exists toward Mode 3 without asking anyone to bet on it now.

**Costs / obligations.** One hub change (flagged module + CTR event) and a
weekly link-health job to own; cross-map generalisation is one lane at a
time (each lane = alignment pass + operator ack); Mode-4 adoption touches
three of-record specs (SmartChat, Test Builder schema, Workbench) — each
lands via its own PR on its own timeline, and none of them copies UGM
text; this repo keeps carrying the research corpus under the phase-2
operator decision and its attribution conditions.

**Neutral.** UGM remains supplement-never-spine; our lanes own sequencing,
and the dormant 2016-era content is treated as a design reference with an
explicit staleness note in every consuming artifact.

**Reversibility.** Mode 2 is a flag kill. Mode 1 facts are additive
columns that can be dropped. Mode 4 patterns are our own schema/spec
changes, owned by us. Nothing adopted here creates a removal hazard
except the links — and those have a job watching them.

## Status Tracking

| When | What |
|---|---|
| 2026-10-22 | Drafted from phases 1–3 evidence; proposed to operator for ratification |
| 2026-10-22 | **Ratified by operator** — Option B accepted as drafted (Mode-1/4 baseline, gated Mode-2 pilot on IAL P1 quadratics, CTR floors 1.0%/28d continue · 3.0% generalise, Mode 3 deferred-and-scoped); no amendments requested; `INTEGRATION-PLAN.md` P4 → `[x]` |
| 2026-10-22 | P5 **implementation ticket + pilot kit authored** (`pilot/TICKET-P5-ugm-explore-further.md` + link set + tested health-job script + bootstrap script + 24/24-live dry-run), **filed as [syllabai-v2#305](https://github.com/SyllabAI/syllabai-v2/issues/305)** — hub implementation pending; **G1 finding: 0/24 resource pages Wayback-archived** ⇒ fail-closed render law + bootstrap as blocking launch gate (ticket §8) |
| pending | Hub implementation of TICKET-P5 in `syllabai-v2` (flag + module + health job + CTR event) → enable → first CTR readout — **VOIDED, see amendment below** |
| 2026-10-22 | **Amended by operator directive**: Mode-2 deep-link pilot **dropped before implementation** ("don't need links to UGM; you already downloaded the resources — create them in syllabai"); syllabai-v2#305 closed not_planned; pilot kit retained in `pilot/` as historical record. Mode-1/4 continue; Mode-3 unchanged |
| 2026-10-22 | Mode-1 first landing: **[syllabai-resources PR #55](https://github.com/SyllabAI/syllabai-resources/pull/55)** — new `UGM-Enrichment/` domain, `syllabai.ugm-spec-enrichment/1.0`, quadratics cross-map as facts-only SUGGESTED enrichment (61 rows over 1.1.1–1.1.5, 3 non-overlaps recorded, 5 primary picks; no UGM text bodies); repo LEDGER entry appended; review/promotion gate = operator |
| pending | First S1-bridge census run against `syllabai-pastpapers` (exhibit for any future Mode-3 ask) |
| pending | 28-day CTR readout → generalise / kill decision — **VOIDED with Mode-2 (amendment 2026-10-22)** |
| 2026-10-23 | **Operator attestation — TEXT IMPORT AUTHORIZED.** Operator: "Continue and downloaded text can ship into SyllabAI. We have permission." This supersedes the 2026-10-22 amendment's "Mode-3 is the only route for UGM text of record" statement: the text lands under the operator's attestation, recorded of record as **Amendment 2026-10-23** in `syllabai-resources` `LICENSE-DATA.md`. First lane executed as **task `T-UGM-IMPORT-1`**: 59 quadratics-station resources → `syllabai-resources` `UGM-Resources/pure-1-quadratics/` (**[PR #58](https://github.com/SyllabAI/syllabai-resources/pull/58)**; text-only import; math byte-true `\( \)`/`\[ \]`; front-matter per corpus law; spec points SUGGESTED + primaryPick cross-referenced to `UGM-Enrichment/` #55; MANIFEST sha256 identity). Mode-3 (formal licence instruments, Cambridge outreach) remains open as an optional separate track; takedown/provenance law unchanged |
| 2026-10-23 | **P3c generalisation lanes 2–3 of record (operator: "extend to the next UGM lane" → lane 3).** Lane 2 (Combining Functions → CIE 9709 P1 1.2 Functions, 27/38 aligned): enrichment + 38 text bodies landed via **[syllabai-resources#61](https://github.com/SyllabAI/syllabai-resources/pull/61)** (MANIFEST v2, multi-lane; hub consumption **[syllabai-v2#312](https://github.com/SyllabAI/syllabai-v2/pull/312)** → `635264b2`). Lane 3 (Geometry of Equations + Circles → CIE 9709 P1 1.3 Coordinate geometry — **first two-station lane**: 34/38 + 27/47 = 61/85 aligned, 77 alignment rows over folded of-record codes 1.3.1/1.3.2 with hub-spine parse fragments 1.3.1a/1.3.2a folded (spine export keeps all four rows verbatim); 24 honest non-overlaps with recorded reasons — the circles station's radian-mensuration / circle-theorem strands serve CIE 1.4 / IAL lanes; primary picks straight-line-pairs + teddy-bear): cross-map of record `cross-map-coordinate-geometry.json` @ `cb947595` (syllabai-experimental, with spine export 1.3 rows); enrichment (T-UGM-MODE1-3) + 85 text bodies (T-UGM-IMPORT-3, math byte-true `\( \)`/`\[ \]`, build audits 85/85 balanced + census-equal) filed as **[syllabai-resources#66](https://github.com/SyllabAI/syllabai-resources/pull/66)** (MANIFEST v3); hub consumption (`T-UGM-HUB-CONSUME-3`) pending on the syllabai-v2 side |
| 2026-10-23 | **Hub consumption complete for all three lanes (operator: "hub consumption T-UGM-HUB-CONSUME-3 on syllabai-v2").** **[syllabai-v2#321](https://github.com/SyllabAI/syllabai-v2/pull/321)** merged of record → `f757c643` (task `T-UGM-HUB-CONSUME-3`): the importer learned multi-station lanes (stationScope-audited lane blocks; per-resource front-matter station; stations[] from the stationScope of record) and regenerated the bundle at pin `main@7e11a74c` — **3 lanes / 4 stations, 12 spec points (incl. folded 1.3.1/1.3.2), 188 candidate rows, 38 non-overlaps, 182 bodies**, `counts.ugmResources` 182; lanes 1-2 proven **byte-identical** through the regen; lane-3 id sets EQUAL the cross-map of record with reasons verbatim; committed-bundle regression test added (`ugm.bundle.test.ts` 13/13); hub `tsc` 0, packages 527/527; course flag already ON (per-course law — lane additions are data). The UGM corpus is now SERVED on the pure-1 hub behind the existing gate for 1.1.x, 1.2.x and 1.3.x. Residuals: lanes 4+ by spine adjacency (1.5 Trigonometry next); S1-bridge census run pending |
| 2026-10-23 | **P3c generalisation lane 4 of record (operator: "extend channel 4" — overrides the #321 residual's "1.5 next" default).** Lane 4 (Circular-measure strand → CIE 9709 P1 1.4 Circular measure — **first strand lane**, no dedicated UGM station): cross-map of record `cross-map-circular-measure.json` @ `b52cf1bf` (syllabai-experimental, with spine export 1.4 rows); hub parse fragment 1.4.1a folded into parent code 1.4.1 (fold law per lane 3); corpus-wide sweep of all 25 stations (855 resources → 62 candidates) resolved as 17 aligned (3 new-text + 14 cross-lane circles-strand facts re-verdicted from lane 3's parked "1.4 territory" non-overlaps, incl. 2 one-to-many extensions of lane-3 1.3.2 rows) + 4 non-overlaps + 41 routed to recorded homes — never forced; clause-a (radian definition/conversion) corpus gap recorded, never manufactured; primary pick r5534 (Cambridge Colleges 1952 Q7); enrichment (T-UGM-MODE1-4) + 5 new-text bodies (T-UGM-IMPORT-4, converter verified byte-identical vs lane-1/3 ground truths belt/r6164/sector-spirals/r6638; full 4-lane importer audit green: 187 bodies joined, cross-lane ugmId uniqueness holds) filed as **[syllabai-resources#74](https://github.com/SyllabAI/syllabai-resources/pull/74)** (MANIFEST v4; strand-lane corpus shape: new-text subset only, cross-lane mappings by `textOfRecordUnder` reference — the corpus importer forbids duplicate `ugmId`s across lanes); hub consumption (`T-UGM-HUB-CONSUME-4`) pending on the syllabai-v2 side |
| 2026-10-23 | **Lane 4 corpus merged + hub consumption complete (operator: "eyeball+merge #74, T-UGM-HUB-CONSUME-4").** [syllabai-resources#74](https://github.com/SyllabAI/syllabai-resources/pull/74) merged of record → `1585c4ff` (T-UGM-MODE1-4 + T-UGM-IMPORT-4; MANIFEST v4; eyeball evidence: 10-file diff verified vs the audited landing, MANIFEST lanes 1-3 deep-equal base-vs-head, no CI configured, base churn unrelated domains). **[syllabai-v2#327](https://github.com/SyllabAI/syllabai-v2/pull/327) merged of record → `2684a8e4`** (task `T-UGM-HUB-CONSUME-4`): the importer learned the strand-lane block (expected census 5/3/3/2) and the fail-closed cross-lane join (joined-ugmId existence, textOfRecordUnder supplier audit, folded-code audit, no double-claim, ≤1 primaryPick) — **12 lane-3 non-overlaps flipped to aligned under 1.4.1** (their recorded reason was "serves 1.4"), r8946/r9386 gain a second spec row, cones/cutting-spheres stay non-overlap; the fleet census reflects the merged serve (4 lanes / 8 stations / 13 spec points / 205 rows / 28 non-overlaps / 187 bodies, `crossLaneJoined` {aligned 14, nonOverlap 2}); 1.4.1 serves 17 resources, primaryPick r5534. The UGM corpus is now SERVED on the pure-1 hub for 1.1.x–1.4.x behind the existing gate (lane additions are data — course flag already ON). Gates: bundle regression 18/18 (reader schema learned the additive cross-lane fields), hub tsc 0, root typecheck clean, eslint clean. Residuals: lanes 5+ by spine adjacency (1.5 Trigonometry next); S1-bridge census run pending |
| 2026-10-23 | **P3c generalisation lane 5 of record (operator: "lane 5").** Lane 5 (Trigonometry: Triangles to Functions + Compound Angles → CIE 9709 P1 1.5 Trigonometry — **the two-station lane**, lanes 1–3 shape restored): cross-map of record `cross-map-trigonometry.json` @ `f3ef5745` (syllabai-experimental, with spine export 1.5 rows verbatim — no fold fragments); corpus-wide sweep of all 25 stations (855 resources → 299 candidates) resolved as 41 aligned (36 TTF + 3 TCA substrate + 2 cross-station strays r7912/r7184; 55 alignment rows) + 36 non-overlaps + 2 cross-lane fact joins (r9924/r8411 → 1.5.4 against lane-2 bodies via `textOfRecordUnder` — the lane-4 join law reused) + 220 routed to recorded homes — never forced; **finding of record: the compound-angles station maps almost entirely to P3 2.3 (24 non-overlaps)** — the 2019 CIE revision moved compound/double-angle work out of Pure 1, and five of lane 4's routed-1.5 preview pool are refined to non-overlaps (preview was a substrate pointer, never a verdict); primary picks going-round-in-circles (1.5.1) / trig-tables (1.5.2) / inverse-or-not (1.5.3) / r5269 (1.5.4) / r6138 (1.5.5); enrichment (T-UGM-MODE1-5) + whole-substrate 77 text bodies (T-UGM-IMPORT-5 — station-lane corpus law: non-overlaps imported UNMAPPED with the coverage note; converter byte-identical vs lane-1/3 ground truths; full 5-lane importer audit green: 5 lanes / 12 stations / 18 spec points / 262 rows / 63 non-overlaps / 264 bodies, 0 dup ids) filed as **[syllabai-resources#79](https://github.com/SyllabAI/syllabai-resources/pull/79)** (MANIFEST v5); hub consumption (`T-UGM-HUB-CONSUME-5`) pending on the syllabai-v2 side |
| 2026-10-23 | **P3c generalisation lane 6 of record (operator: "lane 6 (CIE 9709 P1 1.6 Series)").** Lane 6 (Sequences + Counting and Binomials stations → CIE 9709 P1 1.6 Series — **the second two-station lane**, lane-5 shape): cross-map of record `cross-map-series.json` @ `82964ce4` (syllabai-experimental, with spine export 1.6 rows verbatim — no fold fragments); corpus-wide sweep of all 25 stations (855 resources → 137 candidates) resolved as 49 aligned (43 substrate — 31 Sequences + 12 Counting-and-Binomials — plus 6 cross-station strays r5640/r9404/r9916/r8260/r6592/r9312; 56 alignment rows) + 50 non-overlaps + 2 cross-lane fact joins (r7553/r9527 → 1.6.3 against lane-2 bodies via `textOfRecordUnder` — the lane-4/-5 join law reused) + 36 routed to recorded homes — never forced; **findings of record: the Sequences station maps 31/42 onto 1.6.2–1.6.4 while Counting and Binomials is dominated by combinatorics/logic (39 non-overlaps) around a tight binomial-expansion core (12/51); the general-index binomial questions (r6295/r6340/r7477 + routed power-series pair) carry P3 Series bearings — the natural substrate preview for a future P3 lane**, mirroring lane 5's P3 2.3 finding; primary picks r7078 (1.6.1) / sort-it-out (1.6.2) / r8907 (1.6.3) / square-spirals (1.6.4); enrichment (T-UGM-MODE1-6) + whole-substrate 99 text bodies (T-UGM-IMPORT-6 — station-lane corpus law: non-overlaps imported UNMAPPED with the coverage note; converter verified **byte-identical against all 77 lane-5 of-record files** before generation) filed as **[syllabai-resources#89](https://github.com/SyllabAI/syllabai-resources/pull/89)** (MANIFEST v6); hub consumption (`T-UGM-HUB-CONSUME-6`) pending on the syllabai-v2 side |
| 2026-10-24 | **P3c generalisation lane 7 of record (operator: "Proceed Lane 7").** Lane 7 (Introducing Calculus + Calculus of Powers stations → CIE 9709 P1 1.7 Differentiation — **the third two-station lane**, lane-5/6 shape): cross-map of record `cross-map-differentiation.json` @ `93575e69` (syllabai-experimental, with spine export 1.7 rows verbatim — no fold fragments); corpus-wide sweep of all 25 stations (855 resources → 195 candidates) resolved as 74 aligned (40 substrate — 9 Introducing-Calculus + 31 Calculus-of-Powers — plus 34 cross-station strays; 107 alignment rows; primary picks r7692 (the chord-limit derivation of the power rule, modes [1,4]) / r9942 / r8065 / r9260) + 32 non-overlaps (the honest trapezium-rule/kinematics cluster — the trapezium rule is not in the 2023–2025 P1 spec) + 3 cross-lane fact joins (r5640 vs lane 6; r7115 — whose lane-4 non-overlap row explicitly names 1.7 as the tested skill — and r8936 vs lane 4, via `textOfRecordUnder` — the lane-4/-5/-6 join law reused) + 86 routed to recorded homes — never forced; **findings of record: Calculus of Powers is the P1 workhorse (31/48 aligned — power rule with rational indices, tangents/normals, stationary points, canonical optimisations) while Introducing Calculus splits between gradient-concept building blocks and the non-overlap cluster; the chain-rule, product-rule and calculus-trig-log stations are P3-bearing (general chain rule, product/quotient rule, trig/exp/log derivatives, parametric and implicit differentiation) — the natural substrate preview for future P3 lanes**; lane 6's four 1.7 routing pointers all resolved (r7692/r6509/r6920 aligned, r5348/r9484 routed with P3 bearings); enrichment (T-UGM-MODE1-7) + whole-substrate 106 text bodies (T-UGM-IMPORT-7 — station-lane corpus law: non-overlaps imported UNMAPPED with the coverage note; converter verified **byte-identical against all 99 lane-6 of-record files** before generation) filed as **[syllabai-resources#91](https://github.com/SyllabAI/syllabai-resources/pull/91)** (MANIFEST v7); hub consumption (`T-UGM-HUB-CONSUME-7`) pending on the syllabai-v2 side |
| 2026-10-24 | **P3c generalisation lane 8 of record (operator: next lane per INTEGRATION-PLAN).** Lane 8 (the seven-station calculus family → CIE 9709 P1 1.8 Integration — **the first strand lane on a spec section**, lane-4 shape: UGM has no dedicated integration station and the dedicated calculus stations were already fully of record via lanes 5–7): cross-map of record `cross-map-integration.json` @ `c04abfbd` (syllabai-experimental, with spine export 1.8 rows verbatim — no fold fragments — completing the Pure 1 spine export); corpus-wide integration sweep of all 25 stations (855 resources → 91 candidates) resolved as 28 aligned (10 new-text strand — 7 calculus-meets-functions + 2 chain-rule + 1 product-rule — plus 18 cross-lane fact joins to `pure-1-differentiation/` bodies via `textOfRecordUnder`: 13 flipping the lane-7 Calculus-of-Powers non-overlaps of record with reasons retained — the integration-dressed honesty lane 7 deferred to this lane — and 5 one-to-many beside standing 1.7 alignments; 28 alignment rows; primary picks r8716 / r7734 / r6067 / r9357) + 0 new non-overlaps + 32 routed (P3-technique honesty) + 31 rejected with reasons — never forced; **findings of record: the lane-7 deferral realised (13/17 CoP non-overlaps flip; the 15 Introducing-Calculus trapezium-rule/kinematics non-overlaps stay unmapped — the trapezium rule is not in the 2023–2025 P1 spec); 1.8 coverage is area/volume-dominated (12 of 28 rows are 1.8.4) while reverse-process/constant-of-integration coverage is thin (2 + 4)**; enrichment (T-UGM-MODE1-8) + 10 new-text bodies (T-UGM-IMPORT-8 — strand-lane corpus law: new text only, no unmapped imports) filed as **[syllabai-resources#96](https://github.com/SyllabAI/syllabai-resources/pull/96)** (MANIFEST v8, 479 files corpus-wide); hub consumption (`T-UGM-HUB-CONSUME-8`) pending on the syllabai-v2 side |
| 2026-10-25 | **The image plane of record (operator: "Did you download all the figures/diagrams from UGM and saved it in github? I want the syllabai frontend to use those images then. Currently not showing any images, just links to ugm" → "Localize them" → "merge #107 first, then merge #354" → "review+merge #357").** Answer of record: the text-only corpus (Amendment 2026-10-23) deliberately carried no binaries; the answer shipped as three merged landings — [syllabai-resources#107](https://github.com/SyllabAI/syllabai-resources/pull/107) (`T-UGM-ASSETS-1`: 976 static figures, 37.7 MB, under `UGM-Assets/` + `figures-map.json` 1,233 section-anchored refs across 275 resources, text bodies byte-untouched) → [syllabai-v2#354](https://github.com/SyllabAI/syllabai-v2/pull/354) (`T-UGM-HUB-CONSUME-8a`: the importer copies referenced binaries to `apps/hub/public/ugm-assets/` and injects `![alt](/ugm-assets/…)` figures at deterministic section anchors; per-resource `figures` counts ride the rows) → [syllabai-v2#357](https://github.com/SyllabAI/syllabai-v2/pull/357) (`T-UGM-HUB-CONSUME-8b`, the "Localize them" seam: the converter's 282 inline figure placeholders — the only remaining external UGM image links — rewritten in place to local `/ugm-assets/` renders; bundle census 479 resources / 1,233 figures / **282 inlineRewritten exact**; regression 46 pass / 5,364 expect() incl. the "no external UGM image links remain in any served body" test). #357 verified merged of record at arrival (`4a72e109df`, R0-auto) — fail-closed full verification, no re-merge. Rights posture unchanged: binaries + map live under the 2026-10-23 operator attestation, © Cambridge retained on every plane |
| 2026-10-25 | **P3c generalisation lane 9 of record (operator: "review+merge #357 then proceed with lane 9").** Lane 9 (corpus-wide candidate sweep → CIE 9709 **Pure 3** 3.1 Algebra — **the first lane on the pure-3 course plane**, beyond the completed Pure 1 spine): cross-map of record `cross-map-algebra.json` @ `3098d8eb` (syllabai-experimental, with the new pure-3 spine export 3.1.1–3.1.6 verbatim — the repaired hub-parse rows of record, `T-SPECS-CIE-PARSE-REPAIR-1`; no fold fragments); sweep 855 → 90 candidates resolved as 47 aligned rows (38 fresh rows over 35 substrate resources + 9 cross-lane joins riding lanes 2/6/7/8 bodies: 5 flips — r8427 (lane 2) and r5245/r6295/r6340/r7477 (lane 6, whose "P3 Series bearing" reasons predicted this landing) — plus 4 one-to-many r5362/r9523/r9082/r9701; primary picks absolutely / inequalities / whats-left / r6577 / r7792 / r7436) + 16 fresh non-overlaps recorded by reference only (`bodyImported: false`, the lane-8 candidate-model law) + 30 of-record candidates rejected with reasons (the integer-index binomial pool stays 1.6.1 of record; 3.1.6 is the rational-index `|x| < 1` expansion — the lane-6 P3 preview realised); enrichment (T-UGM-MODE1-9) + 35 new-text bodies (T-UGM-IMPORT-9 — converter pre-flight 10/10 byte-identity vs the lane-8 of-record bodies) filed as [syllabai-resources#114](https://github.com/SyllabAI/syllabai-resources/pull/114) (MANIFEST v10, 514 files corpus-wide); hub consumption (`T-UGM-HUB-CONSUME-9`, opening the pure-3 bundle plane) pending on the syllabai-v2 side |
| 2026-10-25 | **P3c generalisation lane 10 of record (operator: "merging #358 then proceed with lane 10").** #358 (T-UGM-HUB-CONSUME-9) verified merged of record at arrival (`7cf01690`, R0-auto) — fail-closed post-merge verification ALL GREEN (pure-3 bundle census 35/15/6 exact at `main@fafd008d`, CI verify+hub green) — then lane 10 (corpus-wide candidate sweep → CIE 9709 **Pure 3** 3.2 Logarithmic and exponential functions — the second lane on the pure-3 course plane, first by spine adjacency): cross-map of record `cross-map-log-and-exp.json` @ `980556af` (syllabai-experimental, with the pure-3 spine export extended 3.2.1–3.2.4 verbatim; no fold fragments); sweep 855 → 71 candidates resolved as 39 aligned rows (34 fresh rows over 34 substrate resources — 31 from the dedicated exp-and-log station + 3 strays — plus 5 cross-course one-to-many joins riding lanes 2/5/6 bodies: r9824, r7607 (lane 2), r6137, r8260 (lane 6), r7184 (lane 5); no flips) + 26 fresh non-overlaps recorded by reference only (`bodyImported: false`, the lane-8 candidate-model law) + 6 of-record candidates rejected with reasons; the lane-9 `to-log-or-not-to-log` nonOverlapByReference row flips to aligned (3.2.3 pick) with a fresh body; primary picks proving-laws-of-logs / an-irrational-inequality / to-log-or-not-to-log / how-far-did-the-earth-move; findings of record: the exp-and-log station essentially untouched before this lane (2 of 40), the lane-5 pre-baked "2.2" bearings all landed (9 of 10), and the 3.2.2 e/ln limb is structurally thin (UGM's e/ln corpus rides the lane-7/8 recorded P3 3.4/3.5 bearings, which stand); enrichment (T-UGM-MODE1-10) + 34 new-text bodies (T-UGM-IMPORT-10 — converter pre-flight 45/45 byte-identity vs the lane-8 AND lane-9 of-record bodies) filed as [syllabai-resources#119](https://github.com/SyllabAI/syllabai-resources/pull/119) (MANIFEST v11, 548 files corpus-wide); hub consumption (`T-UGM-HUB-CONSUME-10`) pending on the syllabai-v2 side |
| 2026-10-25 | **P3c generalisation lane 11 of record (operator: "merge #363 then lane 11").** #363 (T-UGM-HUB-CONSUME-10) verified merged of record at arrival (`2d3e082c`, CI verify+hub green) — then lane 11 (CIE 9709 **Pure 3** 3.3 Trigonometry — the third lane on the pure-3 course plane and the first mostly-mapping lane): the body-of-record audit found the dedicated compound-angles station and TTF whole-imported of record under lane 5 (77 bodies — the two-station lane law), so the lane-5 pre-baked "P3 2.3" pool maps by reference under the lane-9 flip law: cross-map of record `cross-map-p3-trigonometry.json` @ `4dbd50d5` (syllabai-experimental, with the pure-3 spine export extended 3.3.1–3.3.2 verbatim; no fold fragments); sweep 855 → 103 candidates resolved as 28 aligned rows (1 fresh row — r7616, the 3.3.1 pick — plus 27 cross-course rows by reference: 23 flips of the lane-5 pool rows + 4 one-to-many; no flips of pure-3 rows, nothing duplicated) + 42 fresh non-overlaps recorded by reference only (`bodyImported: false`; 9 riding prior bodies per the supersede law) + 33 of-record candidates rejected with reasons; primary picks r7616 (3.3.1, fresh) / r6018 (3.3.2, rides a reference row — disclosed of record); enrichment (T-UGM-MODE1-11) + 1 new-text body (T-UGM-IMPORT-11 — converter pre-flight 79/79 byte-identity vs the lane-8/9/10 of-record bodies) filed as [syllabai-resources#126](https://github.com/SyllabAI/syllabai-resources/pull/126) (MANIFEST v12, 549 files corpus-wide); hub consumption (`T-UGM-HUB-CONSUME-11`) pending on the syllabai-v2 side |
| 2026-10-25 | **P3c generalisation lane 12 of record (operator: "eyeball+merge of #371 then lane 12").** #371 (T-UGM-HUB-CONSUME-11) verified ALREADY MERGED of record at arrival (`07b37c08`, r0-auto 14:02:02Z, receipt `e152e41d`) — fail-closed post-merge verification ALL GREEN (head `63ab1ac5` CI hub+verify green; post-merge main gates green; bundle of record re-validated on main: schema keys, pin `main@3c2ecfa4` = the #126 merge sha, census 114/70/12/21(17) exactly as claimed, crossCourse {41, flips 28, oneToMany 13} intact; importer patches read — no law changes) — then lane 12 (CIE 9709 **Pure 3** 3.4 Differentiation — the fourth lane on the pure-3 course plane and the largest fresh-text lane since lane 9; named by this file's lane-11 next pointer): cross-map of record `cross-map-p3-differentiation.json` @ `506ea24f` (syllabai-experimental, with the pure-3 spine export extended 3.4.1–3.4.3 verbatim; no fold fragments); sweep 855 → 189 candidates resolved as 41 aligned rows (40 fresh rows over 40 substrate resources — 13 × 3.4.1 / 12 × 3.4.2 / 15 × 3.4.3, incl. 16 promotions of the lane-10/11 pre-baked "P3 3.4 Differentiation" bearing pool superseding their stale rows of record — plus 1 cross-course flip by reference: r8931 riding its lane-7 body under pure-1-differentiation; no one-to-many joins — the lane-7 P1 alignments already hold the tangent/normal/optimisation embodiments) + 29 fresh non-overlaps recorded by reference only (`bodyImported: false`; 3 honest re-routings of lane-10 bearings) + 119 of-record candidates rejected with reasons; primary picks r6938 (3.4.1, fresh) / r6530 (3.4.2, fresh) / r8620 (3.4.3, fresh); enrichment (T-UGM-MODE1-12) + 40 new-text bodies (T-UGM-IMPORT-12 — converter pre-flight 80/80 byte-identity vs the lane-8/9/10/11 of-record bodies) filed as [syllabai-resources#134](https://github.com/SyllabAI/syllabai-resources/pull/134) (MANIFEST v13, 589 files corpus-wide); hub consumption (`T-UGM-HUB-CONSUME-12`) pending on the syllabai-v2 side |