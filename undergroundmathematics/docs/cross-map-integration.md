# Cross-map lane 8: the UGM calculus family → CIE 9709 Pure 1 Integration (strand lane)

**Status**: lane 8 of the P3c generalisation (operator order: the next lane per `docs/INTEGRATION-PLAN.md` §4 — *“further lanes (next by spine adjacency: 1.8 Integration …)”*, closing the Pure 1 spine) · generated 2026-10-24 · machine-readable twin: `resources/derived/cross-map-integration.json`

## 1. What this is

Lanes 1–7 mapped CIE 9709 Pure 1 subtopics 1.1–1.7; lane 7 §8 pre-identified this lane: *“1.8 Integration (the final Pure 1 subtopic — the integration stations and the 1.8-bearing pools recorded across lanes 6–7)”*. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.8 Integration**, carried by the hub spine parse as **four rows** — 1.8.1 through 1.8.4 — with **no fold fragments**.

**Strand-lane scope (lane-4 shape).** UGM has **no dedicated integration station**: integration lives across the seven-station calculus family (introducing-calculus, calculus-of-powers, calculus-meets-functions, chain-rule, product-rule, calculus-trig-log, power-series). Lanes 5–7 already carry the whole dedicated-calculus substrate as text of record (Introducing Calculus 27/27, Calculus of Powers 48/48 — lane 7 imported the latter as 1.7-dressed text precisely because its tested skill was differentiation, with the integration honesty deferred). The lane-8 **new-text universe is therefore the 10 unrecorded family resources whose tested skill is 1.8.x** — all 10 ship mapped under `pure-1-integration/` (a strand lane imports new text only), and every further 1.8 alignment is a **cross-lane fact join** to an already-of-record body under `pure-1-differentiation/` with `textOfRecordUnder` pointers — the lane-4 corpus-importer law, unchanged.

A corpus-wide keyword sweep of all 855 resources (integral signs, integrate/integration vocabulary, area-under/definite-integral/indefinite/trapezium/volume-of-revolution/constant-of-integration patterns) produced **91 candidates**; every one is resolved below as aligned, cross-lane-joined, routed, or rejected with a recorded reason — never forced (AGENT.md rule 3).

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| Corpus screened | 855 resources (25 stations) |
| Sweep candidates verdicted | 91 |
| New-text universe (strand) | 10 unrecorded family resources — all imported mapped |
| Aligned to CIE 9709 P1 1.8.x | 28 resources / 28 alignment rows — 10 new-text + 18 cross-lane joins |
| Cross-lane fact joins | 18 (13 flip the lane-7 Calculus-of-Powers non-overlaps of record; 5 add one-to-many rows beside standing 1.7 alignments) |
| Explicit non-overlap notes | 0 new (the lane-7 non-overlap pool is the join source; the 19 unmapped stay of record) |
| Routed to recorded home with reason | 32 |
| Rejected with reason | 31 (marker false positives, trapezium-rule resources with no spine home, teacher-supports) |
| Aligned rows with exam provenance (S1 bridge) | 12 of 28 |
| Success threshold (plan §7) | **yes** — every candidate resolved; nothing forced |

**Fleet arithmetic of record (post-lane-8):** 479 resources / 348 aligned / 131 non-overlap fleet-wide; 459 candidate rows corpus-wide; cross-lane joined {aligned: 40, nonOverlap: 2}. MANIFEST advances v7 → **v8** (479 files).

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are the of-record hub spine parse titles (codes authoritative; the machine twin carries them verbatim). ⭐ = primary pick (modes 1,4).

### 1.8.1 — understand integration as the reverse process of differentiation, and integrate ( ax + b ) (for any rational n except –1), together with constant multiples, sums and differences

2 UGM resources (primary pick **r8716** ⭐; 1 new-text here + 1 cross-lane joins):

- [review question] What happens if we integrate, then differentiate? (`r8716`, calculus-of-powers, confidence medium, modes [1, 4], join ← UGM-Resources/pure-1-differentiation) ⭐
- [review question] Can we find $\int 1/(\sqrt{x+2} - \sqrt{x+1}) dx$? (`r9701`, chain-rule, confidence medium, modes [1], new-text)

### 1.8.2 — solve problems involving the evaluation of a constant of integration

4 UGM resources (primary pick **r7734** ⭐; 2 new-text here + 2 cross-lane joins):

- [review question] Can we find a curve from its gradient function? (`r5768`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] If $dy/dx$ is inversely proportional to $x^2$, can we find $y$? (`r7410`, product-rule, confidence medium, modes [1], new-text)
- [review question] Given three clues, can we find the equation of the curve? (`r7734`, calculus-of-powers, confidence high, modes [1, 4], join ← UGM-Resources/pure-1-differentiation) ⭐
- [building blocks] Thinking constantly (`thinking-constantly`, calculus-meets-functions, confidence medium, modes [1], new-text)

### 1.8.3 — evaluate definite integrals

10 UGM resources (primary pick **r6067** ⭐; 6 new-text here + 4 cross-lane joins):

- [package of problems] Additional integrals (`additional-integrals`, calculus-meets-functions, confidence high, modes [1], new-text)
- [fluency exercise] Integral chasing (`integral-chasing`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] What does it mean if a function $f(x)=f(2\alpha-x)$? (`r5090`, calculus-meets-functions, confidence medium, modes [1], new-text)
- [review question] If we know $f(x)$, can we find $\int_{-1}^1 f(x^2-1) \:dx$? (`r5549`, calculus-meets-functions, confidence medium, modes [1], new-text)
- [review question] Can we find the area under a parabola? (`r6067`, calculus-of-powers, confidence high, modes [1, 4], join ← UGM-Resources/pure-1-differentiation) ⭐
- [review question] When does this definite integral have a minimum? (`r7236`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] If $f(x)$ always satisfies this equation, what is $\int_{-1}^1 f(x)\: dx$? (`r8105`, calculus-meets-functions, confidence medium, modes [1], new-text)
- [building blocks] Slippery areas (`slippery-areas`, chain-rule, confidence medium, modes [1], new-text)
- [food for thought] Stretch the function (`stretch-the-function`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [food for thought] What else do you know? (`what-else-do-you-know`, calculus-meets-functions, confidence medium, modes [1], new-text)

### 1.8.4 — use definite integration to find lines parallel to the axes, or between a curve and a line or between two curves: • the area of a region bounded by a curve and • a volume of revolution about one of the axes.

12 UGM resources (primary pick **r9357** ⭐; 1 new-text here + 11 cross-lane joins):

- [investigation] Meaningful areas (`meaningful-areas`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] What volume is generated when $y = ax - x^2$ is rotated about the x-axis? (`r5007`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] Can we find the centre of mass of a solid hemisphere? (`r5584`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] Can we sketch the graph of $y^2 = x^3$? (`r6372`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] What's the area enclosed by $y=x(x-3)^2$ and a tangent? (`r7386`, calculus-meets-functions, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] Can we find the area inside a straight line, a parabola and the x-axis? (`r7444`, calculus-of-powers, confidence high, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] If we take a slice from this sphere, where is its centre of gravity? (`r7628`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] When does a cubic curve have two turning points? (`r7861`, calculus-meets-functions, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] What's the area between $f_k(x) = x(x-k)(x-2)$ and the $x$-axis? (`r8130`, calculus-meets-functions, confidence high, modes [1], new-text)
- [review question] When is the area of this region bigger than the area of this one? (`r8350`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] Can we find the area enclosed by this quadratic and the $x$-axis? (`r9138`, calculus-of-powers, confidence medium, modes [1], join ← UGM-Resources/pure-1-differentiation)
- [review question] Can we find the area between a parabola and a line? (`r9357`, calculus-of-powers, confidence high, modes [1, 4], join ← UGM-Resources/pure-1-differentiation) ⭐

## 4. Cross-lane joins — the lane-7 hand-off, realised

Lane 7 imported the whole Calculus of Powers substrate as 1.7-dressed text and recorded 17 of its non-overlaps as *“integration-dressed honesty”* — resources whose tested skill is integration, deliberately left unmapped pending this lane. **13 of those 17 flip here** to 1.8.x alignments with the lane-7 reasons retained (`flipOfPriorNonOverlap: true`); the corpus importer's join law moves their bundle flag exactly as it did for r7115 in lane 7. The other four Calculus-of-Powers non-overlaps (calculus-of-variations, newton-and-leibniz, queen-dido, rectangles-in-triangles) are excerpt/title-only bigger-picture captures and stay unmapped, as do the 15 Introducing-Calculus non-overlaps (trapezium-rule and kinematics honesty — the trapezium rule is not in the 9709 P1 spine at all). The five remaining joins add one-to-many rows beside standing 1.7 alignments (r5768, r7734, r9138, r7386, r7861), mirroring the r5640/r8936 law from lanes 6–7.

## 5. Verdict honesty — the P1 boundary

CIE 9709 P1 1.8 covers exactly: reverse-process integration, (ax+b)^n for rational n ≠ −1, the constant of integration, definite integrals, areas bounded by curves and lines, and volumes of revolution about an axis. **Trig/log/exp antiderivatives, non-linear substitution, integration by parts and partial fractions are P3 technique** — the 32 routed candidates say so explicitly (19 carry standing lane-6/7 routing records that this lane resolves rather than re-litigates). The trapezium-rule family (r5324, r5642, r7903, r8140, underneath-the-arches, serpentine-lake, approximating-areas, r6592, r7912, r6841, r9586, problem-areas) is **not in the 9709 P1 spine at all**; those stay recorded non-overlaps of record. 31 further candidates are marker false positives or non-integration resources, rejected with reasons in `sweepRouting`.

## 6. Corpus law for this lane

`UGM-Resources/pure-1-integration/` carries **10 files** (MANIFEST v8, 479 corpus-wide): the 10 aligned new-text resources, all mapped. No unmapped files ship (the substrate is exhausted; there are no lane-8 non-overlaps). The 18 join rows reference bodies under `pure-1-differentiation/` via `textOfRecordUnder` — no text is duplicated, per the corpus importer's `ugmId` uniqueness law (lane-4 precedent).

## 7. Primary picks of record

| Code | Pick | Why |
|---|---|---|
| 1.8.1 | r8716 | the cleanest single-skill statement of integration as the reverse process of differentiation (dI/da = f(a)); r9701 carries the (ax+b)^n technique work |
| 1.8.2 | r7734 | reconstruct a curve from its gradient ax+b with the constant fixed from a point — the canonical constant-of-integration question |
| 1.8.3 | r6067 | I(c) = ∫((x−c)²+c²)dx evaluated and minimised — canonical polynomial definite integral |
| 1.8.4 | r9357 | area between y=x² and y=x+2 — the canonical curve-line area question |

## 8. Next hops by spine adjacency

**The Pure 1 spine (1.1–1.8) is now complete of record** — seven lanes, one per subtopic. The natural next substrates are the recorded P3 preview pools (real-index binomial + power series from lane 6; product/chain-rule and trig/exp/log derivative pools from lane 7; the 32 lane-8 P3-integration routings recorded here) and the P2/P3 spine sections beyond Pure 1 — operator's call on ordering. The ADR Status Tracking rows (S1 census, 28-day CTR readout) remain gated on their own instruments.

Corpus sweep provenance: candidates from the keyword sweep over `resources/ugm-clean/*` (855 resources screened, 2026-10-24); verdicts read against question wells and solutions; machine-readable twin `resources/derived/cross-map-integration.json`.
