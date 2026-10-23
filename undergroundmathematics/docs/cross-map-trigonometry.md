# Cross-map lane 5: UGM trigonometry stations → CIE 9709 Pure 1 Trigonometry

**Status**: lane 5 of the P3c generalisation (operator instruction **“lane 5”**; per §8 of `cross-map-circular-measure.md` and `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-23 · machine-readable twin: `resources/derived/cross-map-trigonometry.json`

## 1. What this is

Lanes 1–4 mapped the Quadratics, Combining Functions, Geometry-of-Equations + Circles stations and the circles radian-mensuration strand onto CIE 9709 Pure 1 subtopics 1.1–1.4; lane 4 §8 pre-identified this lane's substrate: *“1.5 Trigonometry (`trigonometry-triangles-to-functions` + `trigonometry-compound-angles` stations — this lane's routed 1.5 pool is the substrate preview)”*. The operator now directs exactly that lane. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.5 Trigonometry**, carried by the hub spine parse as **five rows** — 1.5.1 through 1.5.5 — with **no fold fragments** (unlike lanes 3–4, no `a`-suffix rows exist, so no fold decision is required).

**Station-lane scope (lanes 1–3 shape).** UGM has two dedicated trigonometry stations — **Trigonometry: Triangles to Functions** (48 resources) and **Trigonometry: Compound Angles** (27 resources) — so this is a full-station lane, not a strand lane: the substrate is all 75 station resources, plus a corpus-wide sweep of all 25 stations for trigonometry content (\sin/\cos/\tan, inverse trig, sine/cosine rule, identities) so that cross-station strays whose tested skill is 1.5.x are caught and everything else is routed to its recorded home — never forced (AGENT.md rule 3). The two dedicated stations plus the two stray-home stations (Introducing Calculus for r7912, Exponentials & Logarithms for r7184) give a multi-station lane in the lane-3 shape.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| Corpus screened | 855 resources (25 stations) |
| Sweep candidates verdicted | 299 |
| Substrate resources considered | 75 (48 + 27 across the two trigonometry stations) |
| Aligned to CIE 9709 P1 1.5.x | 41 resources / 55 alignment rows — 36 TTF + 3 TCA substrate + 2 cross-station strays |
| Explicit non-overlap notes | 36 (12 TTF + 24 TCA) |
| Cross-lane fact joins (already-of-record bodies) | 2 (r9924, r8411 — lane-2 text untouched) |
| Routed to recorded home with reason | 220 |
| Aligned resources with provenance tuple (S1 bridge) | 23 of 41 |
| Hub content-map attachment | 1.5.1–1.5.5 all sit in `uncoveredSpineCodeList` — zero course items attached (spec-point/lane-level attachment, as in every lane) |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** — every candidate resolved: aligned, non-overlap-noted, cross-lane-joined, or routed with a recorded reason; substrate alignedShare 0.52 (39/75) reflects the compound-angles station's honest P3 verdict (§5) |

Station facts of record (P3b enrichment sheets): Trigonometry: Triangles to Functions — 48 resources; Trigonometry: Compound Angles — 27 resources. Of-record item attachment: **all five 1.5.x codes sit in the hub content map's `uncoveredSpineCodeList` — zero course items are attached**. The UGM enrichment therefore attaches at spec-point/lane level, as in every lane so far. Text import law: the lane's res dir `pure-1-trigonometry/` carries the 41 aligned resources' text (36 TTF + 3 TCA + 2 strays — of which 8 are excerpt/title-only captures per the of-record bigger-picture/teacher-support law, e.g. `cartesian-coordinates` in lane 3); no body text of any non-aligned resource is imported.

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **working texts** of the of-record spine rows; the CIE spec parse carries known text artifacts (interleaved example text) — codes are authoritative, and the machine twin plus the imported front-matter carry each row's **verbatim** parse title.

### 1.5.1 — sketch and use graphs of the sine, cosine and tangent functions (for angles of any size, and using either degrees or radians)

23 UGM resources (primary pick **going-round-in-circles** ⭐; stations: Exponentials & Logarithms + Introducing Calculus + Trigonometry: Compound Angles + Trigonometry: Triangles to Functions):

- [building-blocks] Going round in circles (`going-round-in-circles`, trigonometry-triangles-to-functions, confidence high, modes 1,4) ⭐
- [food-for-thought] Big trig (`big-trig`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [bigger-picture] Calculating latitude (`calculating-latitude`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [many-ways-problem] Can you find... trigonometry edition (`can-you-find-trigonometry-edition`, trigonometry-triangles-to-functions, confidence high, modes 1,4)
- [resource-in-action] Can you find...trigonometry edition - teacher support (`can-you-find-trigonometry-edition-teacher-support`, trigonometry-triangles-to-functions, confidence medium, modes 4)
- [bigger-picture] Catching waves (`catching-waves`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [bigger-picture] From stars to waves (`from-stars-to-waves`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [food-for-thought] Have a sine (`have-a-sine`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [food-for-thought] How high am I? (`how-high-am-i`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [building-blocks] Muddled trig (`muddled-trig`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] When is $\sin x$ or $\sin 2x$ larger than a half? (`r5199`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] How are these three angles connected? (`r5497`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] If $\sin X$ and $\cos Y$ are both negative, what can we say about $X + Y$? (`r7000`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] Which of these log and trig expressions is the largest? (`r7184`, exp-and-log, confidence medium, modes 1)
- [review-question] Which points in the $x$-$y$ plane satisfy $\sin y=\sin x$? (`r7374`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] What's the result when we reflect $y=\sin x$ twice? (`r7577`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] Can we approximate the area under this sine curve? (`r7912`, introducing-calculus, confidence high, modes 1)
- [review-question] Are any of these four trig expressions equal to each other? (`r7973`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] How many solutions does $\cos (\sin x)=\frac{1}{2}$ have? (`r8386`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] When is $\sin\theta > \sin 3\theta$? (`r8713`, trigonometry-compound-angles, confidence medium, modes 1)
- [many-ways-problem] Slices of $\pi$ (`slices-of-pi`, trigonometry-triangles-to-functions, confidence high, modes 1,4)
- [resource-in-action] Slices of $\pi$ - teacher support (`slices-of-pi-teacher-support`, trigonometry-triangles-to-functions, confidence medium, modes 4)
- [fluency-exercise] Trig tables (`trig-tables`, trigonometry-triangles-to-functions, confidence high, modes 1)

### 1.5.2 — use the exact values of the sine, cosine and tangent of 30°, 45°, 60°, and related angles

6 UGM resources (primary pick **trig-tables** ⭐; stations: Introducing Calculus + Trigonometry: Compound Angles + Trigonometry: Triangles to Functions):

- [fluency-exercise] Trig tables (`trig-tables`, trigonometry-triangles-to-functions, confidence high, modes 1) ⭐
- [review-question] Using angles in a pentagon... (`r7021`, trigonometry-compound-angles, confidence medium, modes 1)
- [review-question] Can we approximate the area under this sine curve? (`r7912`, introducing-calculus, confidence high, modes 1)
- [review-question] Which of these area and perimeter statements is true? (`r8330`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [fluency-exercise] Trig countdown (`trig-countdown`, trigonometry-compound-angles, confidence medium, modes 1)
- [resource-in-action] Trig tables - teacher support (`trig-tables-teacher-support`, trigonometry-triangles-to-functions, confidence medium, modes 4)

### 1.5.3 — use the notations sin⁻¹x, cos⁻¹x, tan⁻¹x to denote the principal values of the inverse trigonometric functions

3 UGM resources (primary pick **inverse-or-not** ⭐; stations: Trigonometry: Triangles to Functions):

- [food-for-thought] Inverse or not? (`inverse-or-not`, trigonometry-triangles-to-functions, confidence high, modes 1,4) ⭐
- [bigger-picture] Inverse trigonometric functions (`inverse-trig-functions`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [building-blocks] Muddled trig (`muddled-trig`, trigonometry-triangles-to-functions, confidence high, modes 1)

### 1.5.4 — use the identities tan θ ≡ sin θ / cos θ and sin²θ + cos²θ ≡ 1

12 UGM resources (primary pick **r5269** ⭐; stations: Trigonometry: Triangles to Functions):

- [review-question] Can we prove this trig identity to solve this equation? (`r5269`, trigonometry-triangles-to-functions, confidence high, modes 1) ⭐
- [package-of-problems] Equation or identity? (I) (`equation-or-identity-i`, trigonometry-triangles-to-functions, confidence medium, modes 1,4)
- [review-question] How many solutions does $\sin^2x+3\sin x\cos x+2\cos^2 x=0$ have? (`r6138`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] How many solutions do these simultaneous trig equations have? (`r7370`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] When does this equation in $x, y$ and $\theta$ represent a circle? (`r7378`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] How many solutions does this equation involving $\sin^8x$ have? (`r8136`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] Can we show this polynomial has roots $1$, $\cos\theta$ and $\sin\theta$? (`r8923`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] How many solutions does $2 \cos^2x + 5\sin x = 4$ have? (`r9491`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] As $\theta$ varies, what's the largest this ratio of areas can be? (`r9770`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] When is $\sin^8 x+\cos^6 x$ equal to $1$? (`r9817`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] How many solutions does $7\sin x +2\cos ^2 x =5$ have? (`r9837`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [many-ways-problem] Slices of $\pi$ (`slices-of-pi`, trigonometry-triangles-to-functions, confidence high, modes 1,4)

### 1.5.5 — find all the solutions of simple trigonometrical equations lying in a specified interval (general forms of solution are not included)

11 UGM resources (primary pick **r6138** ⭐; stations: Trigonometry: Compound Angles + Trigonometry: Triangles to Functions):

- [review-question] How many solutions does $\sin^2x+3\sin x\cos x+2\cos^2 x=0$ have? (`r6138`, trigonometry-triangles-to-functions, confidence high, modes 1) ⭐
- [food-for-thought] General solutions (`general-solutions`, trigonometry-triangles-to-functions, confidence medium, modes 1,4)
- [review-question] When is $\sin x$ or $\sin 2x$ larger than a half? (`r5199`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] Can we prove this trig identity to solve this equation? (`r5269`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] If $\sin X$ and $\cos Y$ are both negative, what can we say about $X + Y$? (`r7000`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] Which points in the $x$-$y$ plane satisfy $\sin y=\sin x$? (`r7374`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] How many solutions does this equation involving $\sin^8x$ have? (`r8136`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] How many solutions does $\cos (\sin x)=\frac{1}{2}$ have? (`r8386`, trigonometry-triangles-to-functions, confidence medium, modes 1)
- [review-question] When is $\sin\theta > \sin 3\theta$? (`r8713`, trigonometry-compound-angles, confidence medium, modes 1)
- [review-question] How many solutions does $2 \cos^2x + 5\sin x = 4$ have? (`r9491`, trigonometry-triangles-to-functions, confidence high, modes 1)
- [review-question] How many solutions does $7\sin x +2\cos ^2 x =5$ have? (`r9837`, trigonometry-triangles-to-functions, confidence high, modes 1)

## 4. Full alignment table

| UGM resource | Station | Type | CIE P1 spec | Conf | Modes | Provenance | Note |
|---|---|---|---|---|---|---|---|
| Big trig | trigonometry-triangles-to-functions | food-for-thought | 1.5.1 | medium | 1 | Based on this | compare sin(cos x) and cos(sin x): range and behaviour reasoning over sine and cosine for angles of any size |
| Calculating latitude | trigonometry-triangles-to-functions | bigger-picture | 1.5.1 | medium | 1 |  | triangles and trigonometry helped sailors use the sun and stars to navigate — applied sine/cosine use (excerpt-only capture, per the of-record bigger-picture law) |
| Can you find... trigonometry edition | trigonometry-triangles-to-functions | many-ways-problem | 1.5.1 | high | 1,4 |  | find sine/cosine/tangent graphs under constraints — stretches, reflections, translations of y=sin x and the behaviour that follows |
| Can you find...trigonometry edition - teacher support | trigonometry-triangles-to-functions | resource-in-action | 1.5.1 | medium | 4 |  | teacher-support twin of can-you-find... trigonometry edition (excerpt-only capture) |
| Catching waves | trigonometry-triangles-to-functions | bigger-picture | 1.5.1 | medium | 1 |  | how sine and cosine describe real waveforms — graph behaviour in context (excerpt-only capture) |
| Equation or identity? (I) | trigonometry-triangles-to-functions | package-of-problems | 1.5.4 | medium | 1,4 |  | identity-vs-equation discipline on triangle-angle statements: complementary/supplementary symmetry (sin(pi/2−A)=cos A, sin(pi−A)=sin B) and sin^2+cos^2 work; the reciprocal (sec^2−tan^2=1) and compound (tan(A+B)=−tan C) statements ride P3/0606 — recorded |
| From stars to waves | trigonometry-triangles-to-functions | bigger-picture | 1.5.1 | medium | 1 |  | right-angled triangles and circles give the sine and cosine waves (excerpt-only capture) |
| General solutions | trigonometry-triangles-to-functions | food-for-thought | 1.5.5 | medium | 1,4 |  | if tan A = tan B, what are A and B? — structure of trig solution sets; extends beyond P1's specified interval to general solutions (extension recorded) |
| Going round in circles | trigonometry-triangles-to-functions | building-blocks | 1.5.1 | high | 1,4 |  | unit-circle definitions: similar right triangles give sinθ, cosθ, tanθ and the point (cosθ, sinθ) on the circle — the canonical 1.5.1 foundation |
| Have a sine | trigonometry-triangles-to-functions | food-for-thought | 1.5.1 | medium | 1 |  | tangent obtained from sine and cosine; historic auxiliary functions; reciprocals (sec/cosec/cot) recorded beyond P1 |
| How high am I? | trigonometry-triangles-to-functions | food-for-thought | 1.5.1 | high | 1 |  | Ferris-wheel rider height as a cosine/sine model of the turned angle — graph use in context |
| Inverse or not? | trigonometry-triangles-to-functions | food-for-thought | 1.5.3 | high | 1,4 |  | one graph is y=arctan(tan x), another y=tan(arctan x) — inverse trig notation and principal values made visible |
| Inverse trigonometric functions | trigonometry-triangles-to-functions | bigger-picture | 1.5.3 | high | 1 |  | principal value ranges of inverse trigonometric functions via domain restriction (excerpt-only capture) |
| Muddled trig | trigonometry-triangles-to-functions | building-blocks | 1.5.1,1.5.3 | high | 1 |  | match plotted graphs to sin x, sin^2 x, sin(sin x), sin 2x, arcsin(sin x)... — graph recognition including inverse notation |
| When is $\sin x$ or $\sin 2x$ larger than a half? | trigonometry-triangles-to-functions | review-question | 1.5.1,1.5.5 | high | 1 | Oxford University Mathematics Aptitude Te… | fraction of 0≤x≤2π for which sin x ≥ 1/2 and sin 2x ≥ 1/2 — graph reading plus solution sets |
| Can we prove this trig identity to solve this equation? | trigonometry-triangles-to-functions | review-question | 1.5.4,1.5.5 | high | 1 | O&C O level Additional Mathematics 1, 196… | prove sinA/(1+cosA) + (1+cosA)/sinA = 2/sinA using sin^2+cos^2=1, then solve the resulting equation in 0°–360° |
| How are these three angles connected? | trigonometry-triangles-to-functions | review-question | 1.5.1 | medium | 1 | Oxford University Mathematics Aptitude Te… | circle-with-tangent diagram: choose the correct relation among cos α = sin(β+γ) etc. — complementary-angle structure read from a diagram |
| How many solutions does $\sin^2x+3\sin x\cos x+2\cos^2 x=0 | trigonometry-triangles-to-functions | review-question | 1.5.4,1.5.5 | high | 1 | Oxford University Mathematics Aptitude Te… | sin^2x + 3sinx cosx + 2cos^2x = 0 solution count: divide by cos^2x, use tan x = sin x/cos x, solve the quadratic in tan |
| If $\sin X$ and $\cos Y$ are both negative, what can we sa | trigonometry-triangles-to-functions | review-question | 1.5.1,1.5.5 | high | 1 | UCLES O level Additional Mathematics 1, Q… | count values of z with sin 3z° = k in 0–360; quadrant signs of sin X and cos Y — graph/behaviour reasoning |
| Using angles in a pentagon... | trigonometry-compound-angles | review-question | 1.5.2 | medium | 1 | UCLES A level Mathematics 1, QP 180, 1954… | regular pentagon projection: cos(π/5) − cos(2π/5) = 1/2 — exact-value derivation beyond the standard 30/45/60 set (extension recorded) |
| Which of these log and trig expressions is the largest? | exp-and-log | review-question | 1.5.1 | medium | 1 | Oxford University Mathematics Aptitude Te… | largest of tan(5π/4), sin^2(5π/4), log values — tan's period π and sin(π−x)=sinx symmetry with exact values; the log comparison rides 2.2 — recorded |
| How many solutions do these simultaneous trig equations ha | trigonometry-triangles-to-functions | review-question | 1.5.4 | medium | 1 | Oxford University Mathematics Aptitude Te… | simultaneous (cosθ)x − (sinθ)y = 2, (sinθ)x + (cosθ)y = 1: determinant cos^2θ + sin^2θ = 1 is why the system is solvable for every θ |
| Which points in the $x$-$y$ plane satisfy $\sin y=\sin x$? | trigonometry-triangles-to-functions | review-question | 1.5.1,1.5.5 | high | 1 | Oxford University Mathematics Aptitude Te… | the graph of all points with sin y = sin x — solution-set structure as a picture |
| When does this equation in $x, y$ and $\theta$ represent a | trigonometry-triangles-to-functions | review-question | 1.5.4 | medium | 1 | Oxford University Mathematics Aptitude Te… | x^2+y^2+4x cosθ+8y sinθ+10=0 represents a circle iff 4cos^2θ+16sin^2θ>10 — the deciding sin^2θ range comes from the identity (circle-equation carrier rides 1.3.2) |
| What's the result when we reflect $y=\sin x$ twice? | trigonometry-triangles-to-functions | review-question | 1.5.1 | high | 1 | Oxford University Mathematics Aptitude Te… | reflect y = sin x in x = π then in y = 2 — the result is y = cos x; transformations of trig graphs |
| Can we approximate the area under this sine curve? | introducing-calculus | review-question | 1.5.1,1.5.2 | high | 1 | O&C O level SMP Additional Mathematics 1,… | plot y = sin x at π/6 intervals using exact values (1/2, √3/2, 1), then trapezium-area approximation of ∫sin — the area work rides 1.8 (recorded) |
| Are any of these four trig expressions equal to each other | trigonometry-triangles-to-functions | review-question | 1.5.1 | medium | 1 | UKMT Senior Mathematical Challenge, 2006,… | how many distinct values among sinα sinβ, sinα cosβ, cosα sinβ, cosα cosβ — ratio definitions and ordering |
| How many solutions does this equation involving $\sin^8x$  | trigonometry-triangles-to-functions | review-question | 1.5.4,1.5.5 | medium | 1 | Oxford University Mathematics Aptitude Te… | (3+cos x)^2 = 4 − 2sin^8x solution count via sin^2+cos^2=1 and range bounds (sin^8 depth recorded) |
| Which of these area and perimeter statements is true? | trigonometry-triangles-to-functions | review-question | 1.5.2 | medium | 1 | Oxford University Mathematics Aptitude Te… | equilateral triangle on a circle of circumference 10: area via (1/2)r^2 sin(2π/3) with exact sin(2π/3)=√3/2 |
| How many solutions does $\cos (\sin x)=\frac{1}{2}$ have? | trigonometry-triangles-to-functions | review-question | 1.5.1,1.5.5 | medium | 1 | Oxford University Mathematics Aptitude Te… | cos(sin x) = 1/2 solution count — composite range reasoning over sin and cos |
| When is $\sin\theta > \sin 3\theta$? | trigonometry-compound-angles | review-question | 1.5.1,1.5.5 | medium | 1 | UCLES A level Pure Mathematics 3, QP 447/… | sinθ > sin 3θ: sketch both curves on 0–2π (solution suggested); triple-angle alternative rides P3 — recorded |
| Can we show this polynomial has roots $1$, $\cos\theta$ an | trigonometry-triangles-to-functions | review-question | 1.5.4 | medium | 1 | Oxford University Mathematics Aptitude Te… | cubic with roots 1, cosθ, sinθ — factorisation closes with the sin^2+cos^2=1 identity (polynomial carrier rides 1.1.4) |
| How many solutions does $2 \cos^2x + 5\sin x = 4$ have? | trigonometry-triangles-to-functions | review-question | 1.5.4,1.5.5 | high | 1 | Oxford University Mathematics Aptitude Te… | 2cos^2x + 5sin x = 4 solution count: substitute cos^2x = 1 − sin^2x, solve the quadratic in sin |
| As $\theta$ varies, what's the largest this ratio of areas | trigonometry-triangles-to-functions | review-question | 1.5.4 | medium | 1 | Oxford University Mathematics Aptitude Te… | half-disc regions with −cosθ ≤ x ≤ sinθ: area comparison powered by (sinθ−cosθ)^2; the rational sketch rides 1.2 and the optimisation extension 1.7 — recorded |
| When is $\sin^8 x+\cos^6 x$ equal to $1$? | trigonometry-triangles-to-functions | review-question | 1.5.4 | high | 1 | Oxford University Mathematics Aptitude Te… | sin^8x + cos^6x = 1 solution count — identity plus bounding argument |
| How many solutions does $7\sin x +2\cos ^2 x =5$ have? | trigonometry-triangles-to-functions | review-question | 1.5.4,1.5.5 | high | 1 | Oxford University Mathematics Aptitude Te… | 7sin x + 2cos^2x = 5 solution count via sin^2+cos^2=1 |
| Slices of $\pi$ | trigonometry-triangles-to-functions | many-ways-problem | 1.5.1,1.5.4 | high | 1,4 |  | semicircle divided by inequalities in sinθ, cosθ, tanθ — exact values and identities read off graphs |
| Slices of $\pi$ - teacher support | trigonometry-triangles-to-functions | resource-in-action | 1.5.1 | medium | 4 |  | teacher-support twin of slices of pi (excerpt-only capture) |
| Trig countdown | trigonometry-compound-angles | fluency-exercise | 1.5.2 | medium | 1 |  | card game pairing function cards with value cards against targets — evaluating trig functions at chosen angles (title-only capture; teacher notes on source page) |
| Trig tables | trigonometry-triangles-to-functions | fluency-exercise | 1.5.2,1.5.1 | high | 1 |  | complete tables of sinθ, cosθ, tanθ values — exact-value fluency at 30°/45°/60° and related angles |
| Trig tables - teacher support | trigonometry-triangles-to-functions | resource-in-action | 1.5.2 | medium | 4 |  | teacher-support twin of trig tables (excerpt-only capture) |

Cross-station strays (`r7912` from Introducing Calculus, `r7184` from Exponentials & Logarithms) are imported as lane-5 text because their tested skill is 1.5.x; their station provenance is carried in the front-matter and the machine twin. Two **cross-lane fact joins** (`r9924`, `r8411`) add 1.5.4 rows to resources whose text of record lives under `pure-1-functions/` — the corpus importer's cross-lane `ugmId` uniqueness law keeps one body per resource, so these are recorded as facts with `textOfRecordUnder` pointers, exactly as lane 4 served the circles strand; the recorded lane-2 alignments stand (one-to-many, not collapsed).

## 5. Non-overlaps, boundary cases and sweep routing (never forced)

**Non-overlaps (36)** — substrate resources whose tested skill is elsewhere; recorded with the reason, never forced:

- **equation-or-identity-ii** (trigonometry-compound-angles) — All seven statements need compound/double-angle identities — P3 2.3 bearing (sibling of Equation or identity? (I), whose P1-accessible core is recorded in this lane).
- **inspecting-identities** (trigonometry-compound-angles) — Half-angle identities and their graph-sketching use — the identities are P3 2.3 derivations (the sketching application is 1.5.1-adjacent, recorded).
- **lost-but-lovely-the-haversine** (trigonometry-triangles-to-functions) — Haversine navigation formula: derivation rides half-angle/compound identities — P3 2.3 bearing; put Have a sine in context.
- **proving-half-angle-formulae** (trigonometry-compound-angles) — Derives cos^2(θ/2)=(1+cosθ)/2 from the double-angle identity — P3 2.3 bearing. (Refines lane 4's routed-1.5 preview.)
- **r5113** (trigonometry-compound-angles) — Recorded solution rewrites 2sinx − 3cosx as R sin(x−α) — R-form is P3 2.3; a P1-viable squaring route (13cos^2x+6cosx−3=0) is recorded as an alternative.
- **r5129** (trigonometry-compound-angles) — arctan addition identity via tan(A+B) expansion — P3 2.3 bearing.
- **r5533** (trigonometry-triangles-to-functions) — Tested skill is right-angle/Pythagoras modelling of a hanging picture (cos 15° vocabulary touches 1.5.2) — triangle work is IGCSE/0606 bearing; recorded, never forced.
- **r5723** (trigonometry-compound-angles) — tan(x+60°)=1 is P1-viable by translation, but the recorded solutions use general-solution forms (excluded from P1 1.5.5) and sec y reciprocal work — 0606/P3 bearing (the tan-quadratic part is P1-viable, recorded).
- **r5988** (trigonometry-compound-angles) — Proves a/sinA = 2R for the circumradius — extended sine rule, IGCSE/0606 bearing.
- **r6018** (trigonometry-compound-angles) — sin 18° as a surd via cos3θ = sin2θ — triple/compound angle work, P3 2.3 bearing.
- **r6039** (trigonometry-compound-angles) — tanθ·tan(θ+α)=k ⇒ (k+1)cos(2θ+α)=(1−k)cosα — compound-angle product work, P3 2.3 bearing. (Refines lane 4's routed-1.5 preview.)
- **r6049** (trigonometry-triangles-to-functions) — Two ships observed from a coastline: tested skill is the triangle solution (sine/cosine rules) — IGCSE/0606 bearing, not in P1 1.5 of record.
- **r6120** (trigonometry-compound-angles) — cosθ − 2cos3θ + cos5θ = 2sinθ(sin2θ − sin4θ) — sum-to-product compound identities, P3 2.3 bearing.
- **r6144** (trigonometry-triangles-to-functions) — Roof geometry: lengths and angles in a 3D diagram — 3D triangle trig is IGCSE/0606 bearing.
- **r6589** (trigonometry-triangles-to-functions) — Pyramid altitudes and angles: 3D right-angle trig — IGCSE/0606 bearing. (Refines lane 4's routed-1.5 preview, which never claimed a final verdict.)
- **r6696** (trigonometry-compound-angles) — t = tan(θ/2) half-angle substitution for sinθ and cosθ — P3 2.3 bearing.
- **r6807** (trigonometry-compound-angles) — cos3θ sin2θ − cos4θ sinθ = cos2θ sinθ — compound-angle products, P3 2.3 bearing.
- **r7050** (trigonometry-compound-angles) — sin 15° = (√6−√2)/4 without tables — derivation needs compound/half-angle identities — P3/0606 bearing (15° sits beyond the P1 related-angle set).
- **r7581** (trigonometry-compound-angles) — Sketch y = cosx − sinx + 2: recorded solution uses R cos(x+θ) — P3 2.3 bearing (a value-table sketch is 1.5.1-adjacent, recorded).
- **r7596** (trigonometry-triangles-to-functions) — Swimmers crossing a river: bearings/velocity triangle — IGCSE/0606 bearing.
- **r7604** (trigonometry-compound-angles) — x = 1+2cosθ ⇒ x^3−3x^2+1 = 2cos3θ−1 — triple-angle identity, P3 2.3 bearing.
- **r7756** (trigonometry-triangles-to-functions) — Mountain elevation from three points on a road: triangle solution — IGCSE/0606 bearing.
- **r8525** (trigonometry-compound-angles) — sin a sin b ≤ sin^2((a+b)/2) — product-to-sum compound identities, P3 2.3 bearing.
- **r8557** (trigonometry-compound-angles) — Tower height via reflection: recorded solution uses sin(α+β) and cosec(β−α) — compound-angle work, P3 2.3 bearing. (Refines lane 4's routed-1.5 preview.)
- **r8648** (trigonometry-compound-angles) — General solutions of multi-angle equations (sin3θ, cos2θ, sin2θ mixes) — P3 2.3 bearing.
- **r8658** (trigonometry-triangles-to-functions) — Pedal triangle area: tested skill is extended sine-rule triangle work — IGCSE/0606 bearing.
- **r8709** (trigonometry-compound-angles) — 3cosθ + 4sinθ = r cos(θ−α), then solutions to 500° — R-form plus general solutions, P3 2.3 bearing.
- **r9200** (trigonometry-triangles-to-functions) — Tree bearing from two points 500 yd apart: triangle solution — IGCSE/0606 bearing.
- **r9702** (trigonometry-triangles-to-functions) — Perpendicular distance to the line x cosα + y sinα = p: tested skill is line geometry (1.3.1 bearing); the trig enters as a parameterisation.
- **r9740** (trigonometry-compound-angles) — cos(α+β) from sinα=3/5, cosβ=12/13 — compound-angle expansion, P3 2.3 bearing.
- **r9782** (trigonometry-compound-angles) — Proves cos(A+B)=cosAcosB−sinAsinB, then the three-cosine sum identity — P3 2.3 bearing.
- **sine-ing-the-way** (trigonometry-triangles-to-functions) — Derives the extended sine rule (a/sinA = 2R) from an inscribed triangle — triangle rules are IGCSE/0606 bearing; the circle-sine connection is recorded. (Refines lane 4's routed-1.5 preview.)
- **t-for-tan** (trigonometry-compound-angles) — Double-angle formulae in t = tanθ — the t-substitution building block is P3 2.3 bearing.
- **the-great-circle-distance** (trigonometry-compound-angles) — Spherical great-circle navigation — beyond P1 1.5.
- **the-longitude-problem** (trigonometry-triangles-to-functions) — Navigation history: the longitude problem rides spherical/astronomical methods beyond P1 1.5.
- **transformation-or-not** (trigonometry-compound-angles) — y = 3sinx + 4cosx described as R sin(x+α) — R-form, P3 2.3 bearing (the transformation reading is 1.5.1-adjacent, recorded).

The compound-angles finding of record: **UGM's Trigonometry: Compound Angles station maps almost entirely to P3 2.3 (compound/double/half-angle, R-form, t-substitution), not to P1 1.5** — the 2019 CIE syllabus revision moved those techniques out of Pure 1. The station's P1-tested residue is small (r7021's exact-value projection, trig-countdown's value fluency, r8713's graph-first inequality), and 5 of lane 4's routed-1.5 preview pool are here refined to non-overlaps (`proving-half-angle-formulae`, `r6039`, `r6589`, `r8557`, `sine-ing-the-way`) — the preview was a substrate pointer, never a final verdict (never forced). The station-level consequence for the future P3 lane is recorded in §8.

**Sweep routing — every remaining sweep candidate resolves to its recorded home** (220 resources; the routing is the lane boundary drawn in the open):

- **1.3 (circle theorems; tangent-line vocabulary false positive)** (1): `a-limiting-circle-theorem`
- **1.7 Differentiation (the calculus is the object; radians/degrees are units)** (53): `a-tangent-is`, `average-turning-points`, `can-you-find-chain-rule-edition`, `discussing-distance`, `estimating-gradients`, `gradient-spotting`, `how-does-your-rectangle-grow`, `i-can-see-u`, `keep-your-distance`, `producing-a-rule`, `r5251`, `r5376`, `r5584`, `r5678`, `r5703`, `r5854`, `r5990`, `r6067`, `r6345`, `r6352`, `r6530`, `r6546`, `r6584`, `r6877`, `r7386`, `r7433`, `r7734`, `r7750`, `r7833`, `r7839`, `r8130`, `r8286`, `r8287`, `r8387`, `r8399`, `r8543`, `r8931`, `r9085`, `r9297`, `r9312`, `r9325`, `r9599`, `r9815`, `r9942`, `rotating-derivatives`, `similar-derivatives`, `sine-stretching`, `slippery-slopes-another-derivative`, `speed-vs-velocity`, `tangent-or-normal`, `to-the-limit`, `two-way-calculus`, `two-way-calculus-teacher-support`
- **1.1/Algebra (quadratics/indices/proof; trig incidental)** (8): `absurder`, `r6299`, `r6797`, `r7991`, `r8682`, `r8701`, `r8779`, `whats-left`
- **1.2 Functions (graph transformations/composition; trig graphs as carriers)** (11): `approaching-asymptotes`, `can-you-find-asymptote-edition`, `choose-your-families`, `odd-one-out`, `picture-the-process-i`, `r8079`, `r8625`, `r9072`, `slippery-slopes`, `two-way-functions-teacher-support`, `worth-1000-words`
- **1.8 Integration (trig integrals/areas; the integration is the object)** (21): `approximating-areas`, `constant-consistency`, `integral-chasing-2`, `integral-sorting`, `inverse-integrals`, `inverse-integrals-teacher-support`, `r5126`, `r6620`, `r6622`, `r7074`, `r7616`, `r8134`, `r8152`, `r8694`, `r8778`, `r8890`, `r9184`, `r9701`, `sine-on-the-dotted-line`, `stretch-the-function`, `trigsy-integrals`
- **already of record under pure-1-coordinate-geometry — the trigonometry content is incidental to its recorded alignment (false-positive keyword hit)** (29): `belt`, `cones`, `cutting-spheres`, `pairs-of-circles`, `r5717`, `r5754`, `r5903`, `r6100`, `r6164`, `r6645`, `r6838`, `r7171`, `r7385`, `r7495`, `r7656`, `r7816`, `r7937`, `r7979`, `r8225`, `r8419`, `r8946`, `r9028`, `r9045`, `r9386`, `r9423`, `r9768`, `sector-spirals`, `teddy-bear-teacher-support`, `the-circle-of-apollonius-coordinate-edition`
- **1.6 Series (binomial/sequences; trig terms incidental)** (9): `binomials-are-the-answer`, `r5245`, `r5640`, `r5875`, `r6102`, `r8260`, `r9404`, `sort-it-out`, `sum-estimating`
- **Vectors & mechanics (bearings, components, resultant — not P1 1.5)** (21): `bouncing-to-nothing`, `frictional-story`, `make-it-equal`, `make-it-stop`, `one-windy-day`, `r5813`, `r6009`, `r6449`, `r6670`, `r7187`, `r7272`, `r7678`, `r7982`, `r8071`, `r8115`, `r8335`, `r8456`, `r8836`, `r9586`, `r9794`, `where-did-it-land`
- **2.2 Logarithmic and exponential functions** (10): `changing-bases`, `log-lineup`, `plotting-planets`, `powerful-fractions`, `r5080`, `r7077`, `r9747`, `r9976`, `reach-for-the-stars`, `see-the-power`
- **already of record under pure-1-circular-measure — the trigonometry content is incidental to its recorded alignment (false-positive keyword hit)** (4): `circular-slice`, `problem-areas`, `r5534`, `r8936`
- **Pure 3 (compound/double-angle, R-form, parametric, hyperbolic, arcsin integral)** (19): `from-parabolas-to-catenaries`, `how-long-is-a-piece-of-string`, `implicit-circles`, `parametric-paths`, `parametric-points`, `parametric-preliminaries`, `r5237`, `r6549`, `r6710`, `r6843`, `r6938`, `r7042`, `r8051`, `r8679`, `r8939`, `r9413`, `rolling-parabolas`, `weight-pulling`, `which-substitution`
- **already of record under pure-1-quadratics — the trigonometry content is incidental to its recorded alignment (false-positive keyword hit)** (10): `geogebra-constructions-quadratic`, `r5138`, `r6638`, `r6804`, `r6864`, `r7328`, `r7520`, `r7588`, `r8045`, `r9742`
- **already of record under pure-1-functions — the trigonometry content is incidental to its recorded alignment (false-positive keyword hit)** (13): `invertibles`, `making-inverse-functions`, `picture-the-process-ii`, `r5362`, `r5646`, `r5966`, `r6656`, `r6735`, `r7553`, `r7607`, `r8749`, `r9798`, `r9824`
- **1.3 (angle-bisector geometry)** (1): `look-before-you-leap`
- **1.3/IGCSE (incircle construction)** (1): `perfect-fit`
- **1.3 (line/angle coordinate work)** (1): `r5386`
- **IGCSE/0606 (triangle rules, bearings, 3D trig)** (7): `r6408`, `r7368`, `r8917`, `r8987`, `r9259`, `r9694`, `r9792`
- **P3 numerical methods (root-finding)** (1): `r8231`

## 6. Primary picks of record

As lanes 2–4 record: the Mode-2 shortlist section is retired (deep-link pilot dropped by operator directive 2026-10-22; text ships directly under ADR-UGM-0001 as amended 2026-10-23). One **primaryPick** of record per spec point — starred on the hub index once lane 5 is served:

- **1.5.1**: Going round in circles (`going-round-in-circles`, building-blocks, Triangles to Functions) — the unit-circle foundation: similar right triangles produce sinθ, cosθ, tanθ and the point (cosθ, sinθ); the definitional entry to the whole topic.
- **1.5.2**: Trig tables (`trig-tables`, fluency-exercise, Triangles to Functions) — exact-value fluency at 30°/45°/60° and related angles, the canonical 1.5.2 drill.
- **1.5.3**: Inverse or not? (`inverse-or-not`, food-for-thought, Triangles to Functions) — y=arctan(tan x) against y=tan(arctan x): principal values made visible, the exact misconception 1.5.3 exists to fix.
- **1.5.4**: Can we prove this trig identity to solve this equation? (`r5269`, review-question, Triangles to Functions; UCLES provenance) — identity proof via sin²+cos²=1 feeding straight into equation solving: the 1.5.4→1.5.5 pipeline CIE papers test.
- **1.5.5**: How many solutions does $\sin^2x+3\sin x\cos x+2\cos^2 x=0$ have? (`r6138`, review-question, Triangles to Functions) — divide by cos²x, deploy tan x = sin x/cos x, solve the quadratic in tan: both identities in one solution count.

Pattern/doctrine exemplars of this lane (Mode-4 candidates for the owning specs): `general-solutions` (solution-set structure beyond the specified interval), `can-you-find-trigonometry-edition` (graph reconstruction under constraints), `muddled-trig` (describe-the-graph discrimination), `equation-or-identity-i` (identity-vs-equation discipline).

## 7. S1 provenance bridge status for this lane

23 of 41 aligned resources carry provenance tuples parsed in the P3b enrichment sheets: UCLES A/AS and O-level series (Mathematics 1–2, Additional Mathematics 1–2, O level Mathematics C, Pure Mathematics 1), Oxford & Cambridge Schools Examination Board, Oxford (MAT), and other boards recorded per resource in the machine twin. As in lanes 1–4, the old UCLES series and MAT rows do not collide with the CIE 9709 paper series — the S1 join against `syllabai-pastpapers` remains pending fleet-wide.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record + served** — enrichment #55, text #58 (main@91eed732), hub #308 (merged).
- Lane 2 (functions, 1.2.1–1.2.5): **of record + served** — enrichment + text #61 (a32c6c0f, MANIFEST v2), hub #312 (merged).
- Lane 3 (coordinate geometry, 1.3.1–1.3.2 with fragments folded): **of record + served** — cross-map @ cb947595, enrichment + text #66 (MANIFEST v3), hub #321 (merged).
- Lane 4 (circular measure, 1.4.1 with 1.4.1a folded — first strand lane): **of record + served** — cross-map @ b52cf1bf, corpus #74 → `1585c4ff` (MANIFEST v4), hub #327 → `2684a8e4` (cross-lane join law established).
- **Lane 5 (this lane, 1.5.1–1.5.5, two-station lane)**: cross-map of record here; corpus + enrichment filed as `T-UGM-MODE1-5` / `T-UGM-IMPORT-5` (MANIFEST v5, branch `ugm/pure-1-trigonometry`); hub consumption awaits operator order as `T-UGM-HUB-CONSUME-5` on the syllabai-v2 side — the importer's lane-5 block is a 2+2-station lane block (expected census: 41 resources / 55 rows / 41 aligned / 36 non-overlap) plus **two cross-lane fact joins** (r9924, r8411 → 1.5.4 against existing lane-2 bodies), reusing the lane-4 join law unchanged.
- Next hops by spine adjacency: **1.6 Series** (`sequences` + `counting-and-binomials` stations), then 1.7/1.8 (calculus stations, where of-record item attachment is densest: 51 + 14 parts); the compound-angles station's P3 2.3 mapping (24 recorded non-overlaps here) is the natural substrate preview for a future P3 trigonometry lane.

Corpus sweep provenance: candidates from the keyword sweep over `resources/ugm-clean/*` (\sin/\cos/\tan, inverse-trig, sine/cosine rule, identity, degree/radian patterns; 855 resources screened, 2026-10-23); verdicts read against question wells and solutions; machine-readable twin `resources/derived/cross-map-trigonometry.json`.
