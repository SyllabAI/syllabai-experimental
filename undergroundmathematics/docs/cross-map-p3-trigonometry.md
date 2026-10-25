# Cross-map lane 11: the UGM compound-angles plane → CIE 9709 Pure 3, 3.3 Trigonometry

## 1. What this is

Lane 11 of the P3c generalisation, and the **third lane on the pure-3 course plane**: the Pure 1 spine closed of record at 33 rows (1.1–1.8) with lane 8, lane 9 opened the pure-3 plane at 3.1 Algebra, lane 10 landed 3.2 Logarithmic and exponential functions, and both the INTEGRATION-PLAN P7 next pointer and lane 10's cross-map §8 pre-embeds ("**3.3 Trigonometry** is the natural lane 11 — the pool is pre-baked: the lane-5 compound-angles station recorded 24 non-overlaps pointing at 'P3 2.3' = today's 3.3, plus TTF residuals") make **Pure 3 subtopic 3.3** the natural lane 11. Target of record: `cie-a-level-maths-20-pure-3`, spec points 3.3.1–3.3.2, verbatim from the hub spine parse (`apps/hub/spines/cie-a-level-maths-20-pure-3.json`; the parse artifacts in the 3.3.2 title — dropped math runs in the R-form/Pythagorean bullets and the mid-sentence truncation after 'the expression of a sin θ + b cos θ in the' — are carried verbatim, no `T-SPECS` repair needed, no fold fragments). Operator order (trace `1a172dd01cdcc525`): *"merge #363 then lane 11"* — #363 (T-UGM-HUB-CONSUME-10) was already merged of record at arrival (`2d3e082c`, CI verify+hub green) → lane 10 verified ALL GREEN post-merge → lane 11 built per the P3c rhythm.

**The body-of-record discovery that shapes this lane**: the dedicated Trigonometry: Compound Angles station and Triangles to Functions were WHOLE-IMPORTED of record by lane 5 (77 bodies under `pure-1-trigonometry/` — the two-station lane law that predates the lane-8 candidate model). The lane-5 pre-baked pool therefore cannot be re-imported: it maps **by reference** under the lane-9 flip law, and lane 11 is the first mostly-mapping lane of the generalisation (1 fresh body + 27 by-reference rows), the pure-3 mirror of lane 8's 10-fresh + 18-join shape on the pure-1 plane.

## 2. Lane coverage — headline numbers

| measure | value |
|---|---|
| corpus screened | 855 resources / 25 stations |
| raw hits → candidates | 110 → **103** (17 pass-1 title/description sweep + 93 pass-2 body-text sweep; 102 unique regex candidates + 1 pre-baked bearing `r9740` the regex cannot reach) |
| aligned rows | **28** = 1 fresh row (r7616, new text) + **27 cross-course rows by reference** |
| cross-course joins | **27 = 23 flips + 4 one-to-many** — the 23 lane-5 pre-baked pool rows flip from lane-5 non_overlap to 3.3.2 by reference (their whole-station bodies of record stay under `pure-1-trigonometry/`; lane-9 flip law, nothing duplicated); going-round-in-circles, muddled-trig, trig-tables (3.3.1) and r7021 (3.3.2) join beside standing 1.5.x alignments; **no flips of pure-3 rows** |
| fresh non-overlaps | **42 recorded by reference only** (`bodyImported: false`); 9 of them ride prior bodies of record (`textOfRecordUnder` set per the supersede law) |
| of-record candidates rejected | **33 with reasons** — their prior lane alignments stand |
| substrate stations | the fresh text substrate is r7616 alone (Calculus of Trigonometry & Logarithms); the mapping substrate is the compound-angles station (23 of 27 resources flip or join) plus 3 TTF rows |

**Primary picks of record:** `r7616` (3.3.1, fresh) / `r6018` (3.3.2). The 3.3.2 pick rides a body of record under `pure-1-trigonometry/` — disclosed of record: no fresh 3.3.2 body exists this lane because the dedicated station is whole-imported of record, and the fresh-pick convention (lanes 5–10) cannot apply; the pick designates the strongest 3.3.2 embodiment of record (the exact-evaluation-plus-equation-solving showcase).

## 3. Per-spec-point detail

### 3.3.1 — understand the relationship of the secant, cosecant and cotangent functions to cosine, sine and tangent, and use propert…

4 rows (1 fresh + 3 cross-course):

- `r7616` (calculus-trig-log, Review question, medium) **PICK (fresh)** — the sign of (∫cos)(∫sin over [π,2π])(∫dx/cos3x over [0,π/8]) decided from the properties of the six functions: sin negative on [π,2π] and 1/cos3x positive and finite on the range (cos3x≥cos(3π/8)>0) - properties and graphs for angles of any magnitude, no computation needed
- `going-round-in-circles` (trigonometry-triangles-to-functions, Building blocks, high) (cross-course — via crossLaneAligned) — the reciprocal-triangles derivation: 1/cosθ=secθ, 1/sinθ=cosecθ, 1/tanθ=cotθ relabelled on the three triangles, with Pythagoras giving cot^2+1=cosec^2 and 1+tan^2=sec^2 - the canonical relationship resource for the sec/cosec/cot limb
- `muddled-trig` (trigonometry-triangles-to-functions, Building blocks, high) (cross-course — via crossLaneAligned) — graphs and domains/ranges of 1/sin x, 1/cos x, 1/tan x sketched and named cosec, sec, cot - the graphs-of-all-six limb
- `trig-tables` (trigonometry-triangles-to-functions, Fluency exercise, medium) (cross-course — via crossLaneAligned) — a multiplication table of the six functions completed without calculators - the reciprocal relationships sec=1/cos, cosec=1/sin, cot=1/tan in use at special angles

### 3.3.2 — identities for simplification, exact evaluation and equation solving (spine title truncated of record)

24 rows (1 pick + 23 cross-course, all by reference):

- `equation-or-identity-ii` (trigonometry-compound-angles, Package of problems, high) — seven triangle statements decided identity-vs-equation and the identities proved with compound/double-angle formulae - the sibling of (I) whose P1-accessible core lane-5 recorded; the full compound-angle version is 3.3.2 work
- `inspecting-identities` (trigonometry-compound-angles, Many ways problem, high) — the half-angle identities cos^2(θ/2)=(1+cosθ)/2 and sin^2(θ/2)=(1-cosθ)/2 inspected and used - the double-angle derivations the lane-5 bearing recorded
- `proving-half-angle-formulae` (trigonometry-compound-angles, Scaffolded task, high) — derives cos^2(θ/2)=(1+cosθ)/2 from the double-angle identity (geometric and algebraic proofs) - half-angle formulae are 3.3.2 derivations
- `r5113` (trigonometry-compound-angles, Review question, high) — 2sinx-3cosx=1 solved by writing the left side as R sin(x-α) via the compound-angle identity - the R-form expression of a sinx + b cosx in the solving course
- `r5129` (trigonometry-compound-angles, Review question, high) — arctan addition evaluated via tan(P+Q)=(tanP+tanQ)/(1-tanPtanQ) from the compound-angle formula - exact evaluation through the tan(A±B) expansion
- `r5723` (trigonometry-compound-angles, Review question, high) — three trig equations solved: tan(x+60°)=1 (compound translation), 8siny+3secy=0 (sec as reciprocal of cos, then sin2y), 3sin^2z-8sinzcosz-3cos^2z=0 (identity reduction to quadratic) - identities in the course of solving equations
- `r6018` (trigonometry-compound-angles, Review question, high) **PICK (by reference)** — cos3θ=sin2θ expanded via the double/compound-angle formulae into 4x^2+2x-1=0 - sin 18° extracted as a surd plus all solutions 0-360°: the exact-evaluation-plus-equation-solving showcase for the identities limb
- `r6039` (trigonometry-compound-angles, Review question, high) — tanθtan(θ+α)=k proved equivalent to (k+1)cos(2θ+α)=(1-k)cosα via product-to-sum identities, then tanθtan(θ+π/3)=2 solved - compound-angle manipulation for exact results
- `r6120` (trigonometry-compound-angles, Review question, high) — cosθ-2cos3θ+cos5θ=2sinθ(sin2θ-sin4θ) proved by compound-angle products, then 3sec^2x=tanx+5 solved via sec^2=1+tan^2 - the Pythagorean identity in the course of solving equations
- `r6696` (trigonometry-compound-angles, Review question, high) — sinθ and cosθ expressed in terms of t=tan(θ/2) via the double-angle formulae - the half-angle t-substitution identities
- `r6807` (trigonometry-compound-angles, Review question, high) — cos3θsin2θ-cos4θsinθ=cos2θsinθ proved from sin(A±B)/cos(A±B), and tan(A+B) obtained from the compound-angle relations - simplification and derivation of the tan form
- `r7050` (trigonometry-compound-angles, Review question, high) — sin 15°=(√6-√2)/4 obtained by expanding sin(45°-30°) - the exact-evaluation limb via the compound-angle expansion
- `r7581` (trigonometry-compound-angles, Review question, high) — y=cosx-sinx+2 rewritten as R cos(x+θ)+2 via the compound-angle identity before sketching - the R-form expression
- `r7604` (trigonometry-compound-angles, Review question, high) — 3cos^2x+2cos^2y=4 with 3sin2x-2sin2y=0 solved for cos2x, cos2y via the double-angle formulae, then four solution pairs to the nearest degree - identities solving simultaneous equations
- `r7021` (trigonometry-compound-angles, Review question, high) — cos(π/5) extracted exactly via the cosine double-angle formula cos2θ=2cos^2θ-1 reducing the pentagon relation to 4γ^2-2γ-1=0 - exact evaluation through the double-angle identity
- `r8525` (trigonometry-compound-angles, Review question, high) — sin a sin b ≤ sin^2((a+b)/2) proved via the product-to-sum identities 2sinAsinB=cos(A-B)-cos(A+B) - identity selection for an inequality
- `r8557` (trigonometry-compound-angles, Review question, high) — tower height h sin(α+β)cosec(β-α) evaluated by expanding sin(α+β) and using the reciprocal relation for cosec - compound-angle work is the solution engine
- `r8648` (trigonometry-compound-angles, Review question, high) — general solutions of 2sin3θ-7cos2θ+sinθ+1=0 and cosθ-sin2θ+cos3θ-sin4θ=0 via sum-to-product and double-angle identities - multi-angle equation solving
- `r8709` (trigonometry-compound-angles, Review question, high) — 3cosθ+4sinθ>2 solved for 0°<θ<500° by writing the left side as r cos(θ-α) - the R-form plus general solutions the lane-5 bearing pre-recorded
- `r9740` (trigonometry-compound-angles, Review question, high) — cos(α+β) evaluated from sinα=3/5, cosβ=12/13 by the compound-angle expansion - the canonical expansion exercise the lane-5 bearing pre-recorded
- `r9782` (trigonometry-compound-angles, Review question, high) — cosθ+cos(θ+2π/3)+cos(θ+4π/3)=0 proved by deriving cos(A+B)=cosAcosB-sinAsinB and the three-cosine sum identity - identity derivation and use
- `t-for-tan` (trigonometry-compound-angles, Building blocks, high) — tan2θ=2t/(1-t^2), sin2θ=2t/(1+t^2), cos2θ=(1-t^2)/(1+t^2) obtained geometrically - the double-angle formulae in the t-substitution form
- `transformation-or-not` (trigonometry-compound-angles, Investigation, high) — y=3sinx+4cosx identified as R sin(x+α) with sinα=4/5 - the R-form recognition task the lane-5 bearing pre-recorded
- `lost-but-lovely-the-haversine` (trigonometry-triangles-to-functions, Bigger picture, high) — the haversine navigation formula derivation rides the half-angle/compound identities (hav θ=(1-cosθ)/2) - the lane-5 P3-2.3 bearing pre-recorded this piece into the pool

## 4. Cross-course rows (27 by reference, bodies of record under pure-1-trigonometry)

| slug | station | 3.3 code | kind | prior of record |
|---|---|---|---|---|
| `going-round-in-circles` | trigonometry-triangles-to-functions | 3.3.1 | one_to_many | lane-trigonometry 1.5.1 |
| `muddled-trig` | trigonometry-triangles-to-functions | 3.3.1 | one_to_many | lane-trigonometry 1.5.1/1.5.3 |
| `trig-tables` | trigonometry-triangles-to-functions | 3.3.1 | one_to_many | lane-trigonometry 1.5.1/1.5.2 |
| `equation-or-identity-ii` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `inspecting-identities` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `proving-half-angle-formulae` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r5113` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r5129` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r5723` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r6018` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r6039` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r6120` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r6696` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r6807` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r7050` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r7581` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r7604` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r7021` | trigonometry-compound-angles | 3.3.2 | one_to_many | lane-trigonometry 1.5.2 |
| `r8525` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r8557` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r8648` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r8709` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r9740` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `r9782` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `t-for-tan` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `transformation-or-not` | trigonometry-compound-angles | 3.3.2 | flip | lane-5 non_overlap (flips) |
| `lost-but-lovely-the-haversine` | trigonometry-triangles-to-functions | 3.3.2 | flip | lane-5 non_overlap (flips) |

## 5. Non-overlaps of record (42 by reference)

Recorded with reasons and routings (`bodyImported: false`); routing vocabulary of record: P3 3.4 Differentiation (9), P3 3.5 Integration (9), extended sine/cosine-rule work (4), beyond spec (14), false positive (5), one 3.4/1.7 mix. Nine rows ride prior bodies of record (`textOfRecordUnder`: r5988, r6589, r7756 under pure-1-trigonometry; circular-slice under pure-1-circular-measure; cones under pure-1-coordinate-geometry; approximating-areas, r5642 under pure-1-differentiation; r9798 under pure-1-functions; sum-estimating under pure-1-series).

## 6. Of-record candidates rejected (33)

Every rejected candidate is aligned of record elsewhere with a body of record; the prior homes stand unchanged: 12 under lane-5 pure-1 trigonometry (the TTF sweep residuals), 3 under lanes 9/10 on the pure-3 plane, 2 under lane-7, 2 under lane-8, and 14 across lanes 1/2/3/4/6/10. Reasons are carried in `sweepRouting` with `priorAlignmentOfRecord` pointers.

## 7. Findings of record

1. **The lane-5 pre-baked pool landed as flips, verbatim**: 22 of the 23 pool rows carrying 'P3 2.3' bearings map to 3.3.2 by reference (r5988 keeps its extended-sine-rule bearing and routes out) — the compound-angles station is UGM's dedicated 3.3.2 station, exactly as the lane-5 sweep reasons predicted, and the whole-station import law of record makes the mapping free.
2. **The 3.3.1 substrate is thin by construction**: UGM teaches the reciprocal functions inside the triangles-to-functions station (going-round-in-circles, muddled-trig, trig-tables — all lane-5 bodies of record), so 3.3.1 takes 3 cross-course joins plus one fresh stray (r7616, the sec-sign/definedness review question — the only fresh text of the lane). The pick rides the fresh row; the 3.3.2 pick necessarily rides a reference row, disclosed of record.
3. **R-form and general solutions are pure-3 work**: the lane-5 rows for r5113/r7581/r8709/transformation-or-not explicitly deferred R-form and general-solution work beyond P1 — all four flip to 3.3.2 this lane with the deferrals discharged.
4. **The mixed-skill discipline held**: the sinx/sin2x pair (r7074, r9184) carries a genuine 3.3.2 limb (the double-angle intersection step) but the area/integration limb dominates, so both route to P3 3.5 with the 3.3.2∩3.5.2 mix recorded in their reasons — mirroring lane-9's r9312 treatment.
5. **Figure-plane honesty**: the lane's only fresh body is text-only and the figures-map of record (T-UGM-ASSETS-1) predates the pure-3 lanes — figures=0 honestly, pending the T-UGM-ASSETS-2 amendment noted at lane 9.

## 8. Next hops by spine adjacency

Pure 3 continues in syllabus order: **3.4 Differentiation** is the natural lane 12 — the pool is pre-baked (this lane's non-overlaps carry 9 P3-3.4 routings: rotating-derivatives, similar-derivatives, r6938, r5251, r9413, r6843, r8939, odd-one-out, parametric-points) and the lane-8 integration-side finds already carry 3.5 bearings for the lane after. The 9 P3-3.5 routings (r7074, r9184, trigsy-integrals, circular-slice, r8778, r8836, r9297, constant-consistency, integral-chasing-2) are the integration lane's substrate preview, mirroring lane 6's P3-series finding.
