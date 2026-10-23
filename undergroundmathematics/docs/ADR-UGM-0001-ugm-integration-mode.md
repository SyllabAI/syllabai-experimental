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
