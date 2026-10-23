# Cross-map lane 4: UGM circular-measure strand → CIE 9709 Pure 1 Circular measure

**Status**: lane 4 of the P3c generalisation (operator instruction **"extend channel 4"** — overriding the #321 residual's "1.5 next" default; per §8 of `cross-map-coordinate-geometry.md` and `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-23 · machine-readable twin: `resources/derived/cross-map-circular-measure.json`

## 1. What this is

Lanes 1–3 mapped the quadratics, Combining Functions, and Geometry-of-Equations + Circles stations onto CIE 9709 Pure 1 subtopics 1.1–1.3, and lane 3 §8 pre-identified the substrate for this lane: *"the `circles` station's radian-mensuration strand (20 non-overlaps recorded there) is the natural substrate for a future 1.4 Circular measure lane"*. The operator now directs exactly that lane. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.4 Circular measure**, which the hub spine parse carries as **two rows**: 1.4.1 and 1.4.1a.

**Fold decision (of record).** Hub-spine rows 1.4.1 and 1.4.1a are one CIE syllabus bullet split by the curriculum parser (dupCodePolicy synthetic suffix). Per the lane-3 fold law the cross-map aligns against the parent code 1.4.1 and folds the fragment in; the spine export keeps both rows verbatim. Within the folded code, clause (a) is the radian definition/degrees relationship and clause (b) is the s = rθ / A = ½r²θ arc-and-sector mensuration.

**Strand-lane scope (new lane shape).** First strand lane (no dedicated UGM station): substrate = the circles station's radian-mensuration strand parked as '1.4 territory' by lane 3, plus a corpus-wide sweep of all 25 stations for radians/arc/sector/segment content. Resources whose home is another lane (1.2/1.5/1.7/1.8/P3/IGCSE) are routed, never forced. This is the first lane of the series without a dedicated UGM station: CIE 1.4 is a small, self-contained topic and UGM's circular-measure content is distributed as strands inside stations whose primary homes are other lanes. Method: (i) the circles strand is taken from lane 3's recorded non-overlaps and re-verdicted against 1.4; (ii) all 25 stations are swept for radian/arc/sector/segment content (62 keyword candidates from the 855-resource corpus); (iii) every candidate is aligned, non-overlap-noted, or **routed to its recorded home** — never forced (AGENT.md rule 3). Resources whose tested skill lives in 1.2/1.5/1.7/1.8/P3/IGCSE are excluded from this lane's rows by the scope law; they are listed in §5 so the routing is auditable.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| Corpus screened | 855 resources (25 stations) |
| Sweep candidates verdicted | 62 |
| Aligned to CIE 9709 P1 1.4.1 | 17 (3 new-text + 14 cross-lane) |
| Explicit non-overlap notes | 4 (2 new-text + 2 cross-lane) |
| Routed to recorded home with reason | 41 |
| Aligned resources with provenance tuple (S1 bridge) | 15 of 17 |
| Circles substrate resolution | 16/16 (14 aligned incl. 2 extensions + 2 non-overlaps) |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** — every candidate resolved: aligned, non-overlap-noted, or routed with a recorded reason |

Station facts of record (P3b enrichment sheets): Circles — 47 resources, 35 review questions, 5/5 key questions, 36 with parsed provenance; Thinking about Geometry — 43/22/4-4/27; Introducing Calculus — 27/11/4-4/15; Product Rule & Integration by Parts — 28/24/4-4/25; Chain Rule & Integration by Substitution — 49/32/5-5/33. Of-record item attachment: **both 1.4.1 and 1.4.1a sit in the hub content map's `uncoveredSpineCodeList` — zero course items are attached** (sparser than the pilot's 1.1.x, which had 10 items). The UGM enrichment therefore attaches at spec-point/lane level, as in every lane so far. The hub-facing new-text subset is small by design (39 sweep candidates outside the already-of-record circles station → 3 aligned + 2 boundary non-overlaps imported); the lane's mass is the cross-lane mapping of the circles strand, whose text of record already exists under `pure-1-coordinate-geometry/` — the corpus importer forbids duplicate `ugmId`s across lanes, so lane 4 records those mappings as facts (§4) without re-importing bodies.

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **verbatim from the of-record spine** (hub curriculum parse); the CIE spec parse carries known text artifacts (interleaved example text) — codes are authoritative. The 1.4.1 working text covers two clauses: **(a)** radian definition and the radians↔degrees relationship; **(b)** the formulae s = rθ and A = ½r²θ for arc length and sector area.

### 1.4.1 — understand the definition of a radian, and use the relationship between radians and degrees

**Clause (a) gap, recorded:** No UGM resource teaches radian definition/conversion as its tested skill — the clause-a statement is a GCSE-bridge skill the A-level corpus assumes. Closest touchpoint: sector-spirals' 45° = π/4 conversion. Recorded, never manufactured (AGENT.md rule 3).

**Clause (b)** — 17 UGM resources (primary pick **r5534** ⭐); new-text rows marked `[this lane]`, cross-lane rows marked `[x-lane: pure-1-coordinate-geometry]`:

- [review-question] Can we find a formula for an island's territorial waters? (`r5534`, confidence high, modes 1) `pure-1-circular-measure` ⭐
- [food-for-thought] Problem areas (`problem-areas`, confidence medium, modes 1,4) `pure-1-circular-measure`
- [review-question] When will the arclength $QR$ take a maximum value? (`r8936`, confidence medium, modes 1) `pure-1-circular-measure`
- [food-for-thought] Belt (`belt`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] What's the area of this square if it sits in this sector? (`r6164`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] What's the shared area for these two circles? (`r6838`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] How much of this log is below the surface? (`r7385`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] What's the area inside both the circle $C$ and the triangle $T$? (`r7495`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] Can we find the ratio of the areas of these two sectors? (`r7816`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] What area do these intersecting circles share? (`r7937`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] When does a circle touch a parabola twice? (`r7979`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] Can we find the area between three touching circles? (`r8225`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] When does this area within a circle have a maximum value? (`r9028`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] If we know the difference in their areas, how big are these sectors? (`r9423`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [fluency-exercise] Sector spirals (`sector-spirals`, confidence high, modes 1) `pure-1-coordinate-geometry`
- [review-question] Can we find the areas enclosed between a circle and its tangent? (`r8946`, confidence medium, modes 1) `pure-1-coordinate-geometry`
- [review-question] Can we find the area bounded by these two graphs? (`r9386`, confidence medium, modes 1) `pure-1-coordinate-geometry`

## 4. Full alignment table

| UGM resource | Station | Type | CIE P1 spec | Conf | Modes | Provenance | Text of record | Note |
|---|---|---|---|---|---|---|---|---|
| Can we find a formula for an island's territorial waters? | thinking-about-geometry | review-question | 1.4.1 | high | 1 | {"board": "Cambridge Colleges", "paper": "Examination for… | this lane | Territorial waters around a convex polygon: rectangle strips (pr) plus vertex sectors whose angles sum to a full turn (πr²) — sector-area mensuration is the proof core (clause b).
| Problem areas | introducing-calculus | food-for-thought | 1.4.1 | medium | 1,4 |  | this lane | Card (a): the area under (4−x²)^½ between 1 and 2 is a circular segment (sector − triangle) found by circle geometry before any calculus (clause b); the paired calculus card makes this a methods-contrast exemplar (Mode-4: compare-before-compute).
| When will the arclength $QR$ take a maximum value? | product-rule | review-question | 1.4.1 | medium | 1 | {"board": "UCLES", "paper": "Additional Mathematics 2", "… | this lane | Arc QR of a circle centred at P with radius PQ (itself a chord length of circle X): arc length s = rθ is the modelled object; the maximisation rides 1.7 (clause b; calculus extension recorded).
| Belt | circles | food-for-thought | 1.4.1 | medium | 1 | {"board": "NRICH", "paper": null, "paperCode": null, "yea… | pure-1-coordinate-geometry | Common tangents plus the wrapped arc pieces around two cylinders: arc lengths via s = rθ with wrapped angles π/2 ± α (clause b); the tangent-length part rides lane 3.
| What's the area of this square if it sits in this sector? | circles | review-question | 1.4.1 | medium | 1 | {"board": "O&C (Oxford & Cambridge SEG)", "paper": "Gener… | pure-1-coordinate-geometry | Square inscribed symmetrically in a 60° sector: sector/arc geometry constrains the square (clause b); chord-end reasoning rides trigonometry.
| What's the shared area for these two circles? | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Mathematics A 1 and Pure Mat… | pure-1-coordinate-geometry | Shared area of two circles: segment areas via ½r²(θ − sin θ) in radians — canonical clause-b mensuration.
| How much of this log is below the surface? | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Additional Mathematics 1", "… | pure-1-coordinate-geometry | Floating log: submerged cross-section area and arc pieces by sector/segment mensuration in radians (clause b).
| What's the area inside both the circle $C$ and the triangle  | circles | review-question | 1.4.1 | medium | 1 | {"board": "Oxford (MAT)", "paper": "University Mathematic… | pure-1-coordinate-geometry | Area inside circle C and triangle T (MAT): the circle part is sector/segment mensuration in radians (clause b) at MAT depth.
| Can we find the ratio of the areas of these two sectors? | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Additional Mathematics 1", "… | pure-1-coordinate-geometry | Ratio of areas of two sectors with π/4 and π/3 angles: A = ½r²θ applied twice (clause b).
| What area do these intersecting circles share? | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Additional Mathematics 1", "… | pure-1-coordinate-geometry | Intersecting circles' shared area: the common angle is found, then sector/segment areas in radians (clause b).
| When does a circle touch a parabola twice? | circles | review-question | 1.4.1 | medium | 1 | {"board": "Oxford (MAT)", "paper": "University Mathematic… | pure-1-coordinate-geometry | Circle resting on a parabola (MAT): tangency plus sector area with inverse-trig angles (clause b) — extension depth recorded.
| Can we find the area between three touching circles? | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Mathematics C", "paperCode":… | pure-1-coordinate-geometry | Area between three touching circles: equilateral triangle plus three 60° sectors (clause b).
| When does this area within a circle have a maximum value? | circles | review-question | 1.4.1 | medium | 1 | {"board": "Oxford (MAT)", "paper": "University Mathematic… | pure-1-coordinate-geometry | Chords meeting at angle θ: maximal shaded region as sector/segment area in radians (clause b, MAT MCQ).
| If we know the difference in their areas, how big are these  | circles | review-question | 1.4.1 | high | 1 | {"board": "UCLES", "paper": "Additional Mathematics 1", "… | pure-1-coordinate-geometry | Concentric sectors with ¾ radian given: s = rθ and A = ½r²θ used together (clause b, canonical).
| Sector spirals | circles | fluency-exercise | 1.4.1 | high | 1 |  | pure-1-coordinate-geometry | Arc length and sector area fluency across similar sectors; carries the 45° = π/4 conversion (clause a) plus canonical clause-b fluency — the lane's purest drill.
| Can we find the areas enclosed between a circle and its tang | circles | review-question | 1.4.1 | medium | 1 | {"board": "Oxford (MAT)", "paper": "University Mathematic… | pure-1-coordinate-geometry | Areas enclosed between a circle and its tangent: segment areas needing the tangent's angle (clause b) — extension recorded here; the lane-3 alignment (1.3.2) is not collapsed.
| Can we find the area bounded by these two graphs? | circles | review-question | 1.4.1 | medium | 1 | {"board": "Oxford (MAT)", "paper": "University Mathematic… | pure-1-coordinate-geometry | Area bounded by an arc of x²+y²=2 and a line = sector − triangle = π/4 − 1/√2 (clause b); the lane-3 alignment (1.3.2) is not collapsed.

Cross-lane rows were re-verdicted from lane 3's recorded non-overlaps (the parked "1.4 territory" strand) plus the corpus sweep; their text bodies are **not** duplicated — the corpus importer's cross-lane `ugmId` uniqueness law keeps one body of record per resource, and this lane's facts point at it. The two `extension` rows (r8946, r9386) are one-to-many alignments across lanes: their 1.3.2 alignments of record in lane 3 stand; lane 4 adds the sector/segment reading without collapsing either.

## 5. Non-overlaps, boundary cases and sweep routing (never forced)

**Non-overlaps (4):**

- **circular-slice** (chain-rule) — NON-OVERLAP for this lane: Tested skill is integration by the substitution x = cos θ (a P3 technique): the integral of √(1−x²) evaluates exactly the clause-b sector/segment area, but no radian-mensuration skill is asked — recorded as this lane's calculus boundary.
- **r7115** (chain-rule) — NON-OVERLAP for this lane: Tested skill is constrained optimisation of a cone's volume (1.7): the sheet-metal development is a circle sector whose arc length becomes the base circumference (clause-b vocabulary), but the ask is the maximum — recorded, never forced.
- **cones** (circles) — NON-OVERLAP for this lane: Frustum volume — 3D mensuration beyond P1 1.4, which is circle arc/sector only.
- **cutting-spheres** (circles) — NON-OVERLAP for this lane: Sphere-zone surface area — 3D mensuration beyond P1 1.4.

**Sweep routing — every remaining sweep candidate resolves to its recorded home** (41 resources; the routing is the lane boundary drawn in the open):

- **1.5 Trigonometry (radians used as units; the trig skill is the object) — the natural substrate preview for lane 5** (11): `big-trig`, `can-you-find-trigonometry-edition`, `have-a-sine`, `proving-half-angle-formulae`, `r6039`, `r6589`, `r7021`, `r7184`, `r8557`, `sine-ing-the-way`, `slices-of-pi`
- **1.7 Differentiation (radians as units; the calculus is the object)** (4): `estimating-gradients`, `r8399`, `rotating-derivatives`, `similar-derivatives`
- **1.8 Integration (area/locus work)** (2): `r7444`, `r9184`
- **1.2 Functions (graphs/mapping)** (3): `mapping-a-function`, `picture-the-process-i`, `r9130`
- **Pure 3 (arc length of curves, parametric/hyperbolic work)** (5): `from-parabolas-to-catenaries`, `parametric-preliminaries`, `rolling-parabolas`, `square-wheels`, `weight-pulling`
- **IGCSE-bearing scale-drawing work** (1): `r7368`
- **3D mensuration/centre of gravity, beyond P1** (1): `r7628`
- **keyword false positives (curve/line *segments*, mapping segments — no circular-measure content; already aligned in lanes 1–3)** (14): `a-limiting-circle-theorem`, `all-about-ratios`, `finding-circles`, `look-before-you-leap`, `perfect-fit`, `proving-pythag`, `r5717`, `r5737`, `r5903`, `r5948`, `r6583`, `r6638`, `r8573`, `r9259`

## 6. Primary pick of record

As lanes 2–3 record: the Mode-2 shortlist section is retired (deep-link pilot dropped by operator directive 2026-10-22; text ships directly under ADR-UGM-0001 as amended 2026-10-23). One **primaryPick** of record for the folded spec point — starred on the hub index once lane 4 is served:

- **1.4.1**: Can we find a formula for an island's territorial waters? (`r5534`, review-question, Thinking about Geometry) — the sector-sum proof (vertex sectors totalling a full turn) is clause-b mensuration at its most structural: low-threshold diagram, high-ceiling proof, provenance of record (Cambridge Colleges Examination for Entrance Scholarships, 1952).

Pattern/doctrine exemplars of this lane (Mode-4 candidates for the owning specs): `problem-areas` (compare-before-compute card pair — geometric vs calculus area of the same region), `sector-spirals` (describe-the-image reconstruction fluency over similar sectors), `r8936` (arc-length model inside an optimisation).

## 7. S1 provenance bridge status for this lane

15 of 17 aligned resources carry provenance tuples parsed in the P3b enrichment sheets: UCLES (Additional Mathematics 1, Mathematics A 1/Pure Mathematics 1, O level Mathematics C, A level Mathematics 1), O&C O level General Mathematics, Oxford MAT (2007/2010/2012/2013), Cambridge Colleges Entrance Scholarships 1952, and NRICH-derived attribution (`belt`). As in lanes 1–3, the old UCLES series and MAT/entrance-paper rows do not collide with the CIE 9709 paper series — the S1 join against `syllabai-pastpapers` remains pending fleet-wide.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record** — enrichment #55, text #58 (main@91eed732), hub #308 (merged).
- Lane 2 (functions, 1.2.1–1.2.5): **of record** — enrichment + text #61 (a32c6c0f, MANIFEST v2), hub #312 (merged).
- Lane 3 (coordinate geometry, 1.3.1–1.3.2 with fragments folded): **of record** — cross-map @ cb947595, enrichment + text #66 (MANIFEST v3), hub #321 (merged; bundle serves 1.1.x–1.3.x).
- Lane 4 (this lane, 1.4.1 with 1.4.1a folded — **first strand lane**): cross-map of record here; corpus + enrichment filed as [syllabai-resources#74](https://github.com/SyllabAI/syllabai-resources/pull/74) (tasks `T-UGM-MODE1-4` / `T-UGM-IMPORT-4`, MANIFEST v4). Strand-lane corpus shape: `pure-1-circular-measure/` carries only new-text resources (3 aligned + 2 boundary non-overlaps); the circles strand's 14 alignments + 2 non-overlaps are recorded as facts with `textOfRecord` pointers, keeping the corpus importer's cross-lane `ugmId` uniqueness law intact. Hub consumption awaits operator order as `T-UGM-HUB-CONSUME-4` on the syllabai-v2 side: the importer's lane-4 block is a 4-station strand block (thinking-about-geometry, introducing-calculus, product-rule, chain-rule; expected census 5 resources / 3 rows / 3 aligned / 2 non-overlap) plus a new cross-lane join so the circles-strand mappings serve against their existing bodies.
- Next hops by spine adjacency: **1.5 Trigonometry** (`trigonometry-triangles-to-functions` + `trigonometry-compound-angles` stations — this lane's routed 1.5 pool is the substrate preview), then 1.6 Series (`sequences` + `counting-and-binomials`), then 1.7/1.8 (calculus stations, where of-record item attachment is densest: 51 + 14 parts).

Corpus sweep provenance: candidates from the keyword sweep over `resources/ugm-clean/*` (radian / arc / sector / segment patterns, 855 resources screened, 2026-10-23); verdicts read against question wells and solutions; machine-readable twin `resources/derived/cross-map-circular-measure.json`.
