# Cross-map lane 7: UGM introducing-calculus + calculus-of-powers stations → CIE 9709 Pure 1 Differentiation

**Status**: lane 7 of the P3c generalisation (operator instruction **“Proceed Lane 7”**; per §8 of `cross-map-series.md` and `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-24 · machine-readable twin: `resources/derived/cross-map-differentiation.json`

## 1. What this is

Lanes 1–6 mapped the Quadratics, Combining Functions, Geometry-of-Equations + Circles, the circular-measure strand, the two trigonometry stations and the two series stations onto CIE 9709 Pure 1 subtopics 1.1–1.6; lane 6 §8 pre-identified this lane's substrate: *“1.7 Differentiation (the calculus stations — where of-record item attachment is densest: 51 + 14 parts — and where lanes 4–6 routed pools already hold a large preview substrate)”*. The operator now directs exactly that lane. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.7 Differentiation**, carried by the hub spine parse as **four rows** — 1.7.1 through 1.7.4 — with **no fold fragments** (no `a`-suffix rows exist, so no fold decision is required).

**Station-lane scope (lanes 1–3/5/6 shape).** UGM has two dedicated calculus stations — **Introducing Calculus** (27 resources) and **Calculus of Powers** (48 resources) — so this is a full-station lane: the substrate is all 75 station resources, of which 3 Introducing-Calculus resources are already of record via lanes 5–6 (r6592, r7912, problem-areas), leaving **72 new-text substrate resources**, plus a corpus-wide sweep of all 25 stations for differentiation content (derivatives, gradients of curves, tangents and normals, stationary points, chain rule, rates of change, small increments, optimisation vocabulary) so that cross-station strays whose tested skill is 1.7.x are caught and everything else is routed to its recorded home — never forced (AGENT.md rule 3). The two dedicated stations plus the six stray-home stations (chain-rule, calculus-meets-functions, calculus-trig-log, product-rule, power-series) give a multi-station lane in the lane-5/6 shape.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| Corpus screened | 855 resources (25 stations) |
| Sweep candidates verdicted | 195 |
| Substrate resources considered | 72 new-text (24 + 48 across the two calculus stations; 3 already of record via lanes 5–6) |
| Aligned to CIE 9709 P1 1.7.x | 74 resources / 107 alignment rows — 40 substrate + 34 cross-station strays |
| Explicit non-overlap notes | 32 (15 Introducing-Calculus + 17 Calculus-of-Powers) |
| Cross-lane fact joins (already-of-record bodies) | 3 (r5640 → lane 6; r7115, r8936 → lane 4 — text untouched) |
| Routed to recorded home with reason | 86 |
| Aligned resources with provenance tuple (S1 bridge) | 54 of 74 |
| Hub content-map attachment | the lane-6 §8 pre-embed recorded 1.7 as the densest of-record item attachment (51 + 14 parts); the UGM enrichment attaches at spec-point/lane level, as in every lane |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** — every candidate resolved: aligned, non-overlap-noted, cross-lane-joined, or routed with a recorded reason; substrate alignedShare 0.56 (40/72) reflects the honest trapezium-rule and kinematics verdicts in Introducing Calculus (§5) |

Station facts of record (P3b enrichment sheets): Introducing Calculus — 27 resources; Calculus of Powers — 48 resources. Text import law (station-lane corpus law, lane-3/5/6 shape): the lane's res dir `pure-1-differentiation/` carries the **whole substrate's text of record — 106 files**: the 74 aligned resources (40 substrate + 34 strays) MAPPED, plus the 32 non-overlaps imported UNMAPPED with the coverage note (their recorded homes live in the enrichment's `nonOverlapRows`; 4 of the 106 are excerpt/title-only captures per the of-record bigger-picture/teacher-support law). No mapping is manufactured for the unmapped files (AGENT.md rule 3).

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **working texts** of the of-record spine rows; the CIE spec parse carries known text artifacts (interleaved example text) — codes are authoritative, and the machine twin plus the imported front-matter carry each row's **verbatim** parse title.

### 1.7.1 — understand the gradient of a curve at a point as the limit of the gradients of a suitable sequence of chords, and use the notations dy/dx, f'(x), f''(x) for first and second derivatives

5 UGM resources (primary pick **binomials-are-the-answer** ⭐; stations: Calculus Meets Functions + Calculus of Powers + Calculus Trig Log + Introducing Calculus):

- [investigation] Binomials are the answer! (`binomials-are-the-answer`, calculus-of-powers, confidence high, modes 1,4) ⭐
- [building-blocks] Gradients of gradients (`gradients-of-gradients`, calculus-meets-functions, confidence medium, modes 1)
- [problem-requiring-decisions] Estimating gradients (`estimating-gradients`, calculus-trig-log, confidence medium, modes 1)
- [building-blocks] Mapping a derivative (`mapping-a-derivative`, introducing-calculus, confidence medium, modes 1)
- [scaffolded-task] Zooming in (`zooming-in`, introducing-calculus, confidence high, modes 1)

### 1.7.2 — use the derivative of x^n (for any rational n), together with constant multiples, sums and differences of functions, and of composite functions using the chain rule

38 UGM resources (primary pick **r9942** ⭐; stations: Calculus Meets Functions + Calculus of Powers + Chain Rule + Power Series + Product Rule):

- [review-question] If we increase $x$ by a small amount, what happens to $y$? (`r9942`, calculus-of-powers, confidence high, modes 1,4) ⭐
- [many-ways-problem] Can you find... curvy cubics edition (`can-you-find-curvy-cubics`, calculus-meets-functions, confidence high, modes 1)
- [investigation] Curvy cubics (`curvy-cubics`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] Can we maximise the volume of this metal tin? (`r6180`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does $3x^4-16x^3+18x^2=k$ have exactly two real roots? (`r6537`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When is the cost of producing this chemical a minimum? (`r6867`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When is $f(x) = 2x^3 − 9x^2 + 12x + 3$ smallest over this range? (`r6868`, calculus-meets-functions, confidence high, modes 1)
- [review-question] Can we sketch the graph of this piecewise function? (`r7196`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] What's the area enclosed by $y=x(x-3)^2$ and a tangent? (`r7386`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] How small can this triangle be? (`r7720`, calculus-meets-functions, confidence high, modes 1)
- [review-question] If $y=f(x)$ has a turning point when $x=\frac{1}{4}$, can we find $\lambda$? (`r7998`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] Given $f'(x)$ and $g'(x)$, what is $f''(2x)$? (`r8588`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] When does this function of two variables have a minimum? (`r9671`, calculus-meets-functions, confidence high, modes 1)
- [fluency-exercise] Floppy hair (`floppy-hair`, calculus-of-powers, confidence high, modes 1)
- [building-blocks] Gradient spotting (`gradient-spotting`, calculus-of-powers, confidence high, modes 1)
- [review-question] Where do two tangents cross, and where do two normals cross? (`r5703`, calculus-of-powers, confidence high, modes 1)
- [review-question] Where does $f(x) = x^2 - 2px + 3$ have its minimum? (`r5732`, calculus-of-powers, confidence high, modes 1)
- [review-question] When is the area of a face of this pyramid a minimum? (`r6820`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the area of the triangle created by a common tangent? (`r6877`, calculus-of-powers, confidence high, modes 1)
- [review-question] What's the most economical speed for this ship's journey? (`r7280`, calculus-of-powers, confidence high, modes 1)
- [review-question] What is the gradient of this curve at its $x$-intercepts? (`r7391`, calculus-of-powers, confidence high, modes 1)
- [review-question] Given the line $PRQ$, when is $OP + OQ$ a minimum? (`r7586`, calculus-of-powers, confidence high, modes 1)
- [review-question] When is the volume of this cylinder inside a cone a maximum? (`r7785`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the triangle areas given by a tangent? (`r8286`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the locus of a midpoint created by a parabola? (`r8399`, calculus-of-powers, confidence high, modes 1)
- [review-question] When does $y=kx^3-(k+1)x^2+(2-k)x-k$ have a minimum at $x =1$? (`r8441`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we show these two cubic curves touch? (`r8543`, calculus-of-powers, confidence high, modes 1)
- [review-question] What's the least surface area of this rocket-shaped solid? (`r8548`, calculus-of-powers, confidence high, modes 1)
- [review-question] When is the volume of this cuboid a maximum? (`r9260`, calculus-of-powers, confidence high, modes 1)
- [review-question] What can we say about the combined area of these two shapes? (`r9599`, calculus-of-powers, confidence high, modes 1)
- [building-blocks] Chain mapping (`chain-mapping`, chain-rule, confidence medium, modes 1)
- [fluency-exercise] I can see $u$! (`i-can-see-u`, chain-rule, confidence high, modes 1)
- [review-question] Can we sketch $y = x^2(2-x)$, and from this, $y^2 = x^2(2-x)$? (`r7839`, chain-rule, confidence high, modes 1)
- [review-question] When is the volume of this pyramid a maximum? (`r9905`, chain-rule, confidence medium, modes 1)
- [building-blocks] Slippery slopes... another derivative (`slippery-slopes-another-derivative`, chain-rule, confidence medium, modes 1)
- [investigation] Designing a polynomial (`designing-a-polynomial`, power-series, confidence medium, modes 1)
- [building-blocks] Producing a rule (`producing-a-rule`, product-rule, confidence medium, modes 1)
- [review-question] Can we find the repeated root for  $4x^4+x^2+3x+1=0$? (`r9082`, product-rule, confidence medium, modes 1)

### 1.7.3 — apply differentiation to gradients, tangents and normals, increasing and decreasing functions and rates of change

29 UGM resources (primary pick **r8065** ⭐; stations: Calculus Meets Functions + Calculus of Powers + Chain Rule + Introducing Calculus):

- [review-question] What (approximately) is the square root of $26$? (`r8065`, calculus-of-powers, confidence high, modes 1,4) ⭐
- [review-question] What can we say if $y = m(x-a)$ is tangent to $y = x^3 - x$? (`r8287`, calculus-meets-functions, confidence high, modes 1)
- [food-for-thought] Slippery slopes (`slippery-slopes`, calculus-meets-functions, confidence medium, modes 1)
- [many-ways-problem] Two-way calculus (`two-way-calculus`, calculus-meets-functions, confidence high, modes 1)
- [review-question] Where do two tangents cross, and where do two normals cross? (`r5703`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find a percentage increase using the gradient? (`r6345`, calculus-of-powers, confidence high, modes 1)
- [review-question] When does the normal to a parabola pass through this point? (`r6352`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the area inside a parabola, a tangent, and the $x$-axis? (`r6584`, calculus-of-powers, confidence medium, modes 1)
- [review-question] Can we find the area of the triangle created by a common tangent? (`r6877`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we track this constantly growing patch of fluid? (`r6959`, calculus-of-powers, confidence high, modes 1)
- [review-question] What is the gradient of this curve at its $x$-intercepts? (`r7391`, calculus-of-powers, confidence high, modes 1)
- [review-question] Is the gradient function increasing or decreasing on this curve? (`r7433`, calculus-of-powers, confidence high, modes 1)
- [review-question] Given three clues, can we find the equation of the curve? (`r7734`, calculus-of-powers, confidence medium, modes 1)
- [review-question] How many common tangents can two parabolas have? (`r7750`, calculus-of-powers, confidence high, modes 1)
- [review-question] A cubic has one real root—can we find an approximation to it? (`r8231`, calculus-of-powers, confidence medium, modes 1)
- [review-question] Can we find the triangle areas given by a tangent? (`r8286`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the locus of a midpoint created by a parabola? (`r8399`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we show these two cubic curves touch? (`r8543`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find the area enclosed by this quadratic and the $x$-axis? (`r9138`, calculus-of-powers, confidence medium, modes 1)
- [review-question] If we increase $x$ by a small amount, what happens to $y$? (`r9942`, calculus-of-powers, confidence high, modes 1)
- [package-of-problems] Tangent or normal (`tangent-or-normal`, calculus-of-powers, confidence medium, modes 1)
- [review-question] If we know the object's speed, can we find the speed of the image? (`r8625`, chain-rule, confidence medium, modes 1)
- [review-question] Can we find this area by integrating with respect to $y$? (`r9815`, chain-rule, confidence medium, modes 1)
- [building-blocks] A tangent is ... (`a-tangent-is`, introducing-calculus, confidence medium, modes 1)
- [building-blocks] Gradient match (`gradient-match`, introducing-calculus, confidence high, modes 1)
- [bigger-picture] Why are gradients important in the real world? (`gradients-important-real-world`, introducing-calculus, confidence medium, modes 1)
- [building-blocks] Speed vs velocity (`speed-vs-velocity`, introducing-calculus, confidence medium, modes 1)
- [investigation] Talking about curves (`talking-about-curves`, introducing-calculus, confidence medium, modes 1)
- [building-blocks] Walk-sorting (`walk-sorting`, introducing-calculus, confidence medium, modes 1)

### 1.7.4 — locate stationary points and determine their nature, and use information about stationary points in sketching graphs

35 UGM resources (primary pick **r9260** ⭐; stations: Calculus Meets Functions + Calculus of Powers + Chain Rule + Introducing Calculus):

- [review-question] When is the volume of this cuboid a maximum? (`r9260`, calculus-of-powers, confidence high, modes 1,4) ⭐
- [go-and-think-about-it] Average turning points (`average-turning-points`, calculus-meets-functions, confidence medium, modes 1)
- [many-ways-problem] Can you find... curvy cubics edition (`can-you-find-curvy-cubics`, calculus-meets-functions, confidence high, modes 1)
- [investigation] Curvy cubics (`curvy-cubics`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] Can we maximise the volume of this metal tin? (`r6180`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does $3x^4-16x^3+18x^2=k$ have exactly two real roots? (`r6537`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does this cubic equation have three distinct real roots? (`r6703`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When is the cost of producing this chemical a minimum? (`r6867`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When is $f(x) = 2x^3 − 9x^2 + 12x + 3$ smallest over this range? (`r6868`, calculus-meets-functions, confidence high, modes 1)
- [review-question] Can we sketch the graph of this piecewise function? (`r7196`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] What's the minimum area of this variable triangle? (`r7212`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] What's the area enclosed by $y=x(x-3)^2$ and a tangent? (`r7386`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] How small can this triangle be? (`r7720`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does a cubic curve have two turning points? (`r7861`, calculus-meets-functions, confidence high, modes 1)
- [review-question] If $y=f(x)$ has a turning point when $x=\frac{1}{4}$, can we find $\lambda$? (`r7998`, calculus-meets-functions, confidence medium, modes 1)
- [review-question] When does $3x^4 - 16x^3 +18x^2 + k = 0$ have four real solutions? (`r8959`, calculus-meets-functions, confidence high, modes 1)
- [review-question] How many stationary points does $y = 2x^3 - 6x^2 + 5x - 7$  have? (`r9582`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does this function of two variables have a minimum? (`r9671`, calculus-meets-functions, confidence high, modes 1)
- [review-question] When does this cubic equation have distinct real positive solutions? (`r9781`, calculus-meets-functions, confidence medium, modes 1)
- [many-ways-problem] Two-way calculus (`two-way-calculus`, calculus-meets-functions, confidence high, modes 1)
- [fluency-exercise] Floppy hair (`floppy-hair`, calculus-of-powers, confidence high, modes 1)
- [review-question] Where does $f(x) = x^2 - 2px + 3$ have its minimum? (`r5732`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we find a curve from its gradient function? (`r5768`, calculus-of-powers, confidence medium, modes 1)
- [review-question] When is the area of a face of this pyramid a minimum? (`r6820`, calculus-of-powers, confidence high, modes 1)
- [review-question] What's the most economical speed for this ship's journey? (`r7280`, calculus-of-powers, confidence high, modes 1)
- [review-question] Is the gradient function increasing or decreasing on this curve? (`r7433`, calculus-of-powers, confidence high, modes 1)
- [review-question] Given the line $PRQ$, when is $OP + OQ$ a minimum? (`r7586`, calculus-of-powers, confidence high, modes 1)
- [review-question] When is the volume of this cylinder inside a cone a maximum? (`r7785`, calculus-of-powers, confidence high, modes 1)
- [review-question] When does $y=kx^3-(k+1)x^2+(2-k)x-k$ have a minimum at $x =1$? (`r8441`, calculus-of-powers, confidence high, modes 1)
- [review-question] What's the least surface area of this rocket-shaped solid? (`r8548`, calculus-of-powers, confidence high, modes 1)
- [review-question] What can we say about the combined area of these two shapes? (`r9599`, calculus-of-powers, confidence high, modes 1)
- [review-question] Can we sketch $y = x^2(2-x)$, and from this, $y^2 = x^2(2-x)$? (`r7839`, chain-rule, confidence high, modes 1)
- [review-question] When is the volume of this pyramid a maximum? (`r9905`, chain-rule, confidence medium, modes 1)
- [review-question] When is this parabola's turning point nearest to the origin? (`r9506`, introducing-calculus, confidence medium, modes 1)
- [investigation] Talking about curves (`talking-about-curves`, introducing-calculus, confidence medium, modes 1)

## 4. Full alignment table

| Resource | Station | Type | Codes | Confidence | Evidence |
|---|---|---|---|---|---|
| Average turning points (`average-turning-points`) | calculus-meets-functions | go-and-think-about-it | 1.7.4 | medium | can a cubic have a stationary point midway between two intersections — the condition becomes a derivative condition on f' (extension-level investigation) |
| Can you find... curvy cubics edition (`can-you-find-curvy-cubics`) | calculus-meets-functions | many-ways-problem | 1.7.2, 1.7.4 | high | construct cubics from prescribed stationary points and increasing/decreasing behaviour — derivative reasoning backwards from f' conditions |
| Curvy cubics (`curvy-cubics`) | calculus-meets-functions | investigation | 1.7.2, 1.7.4 | medium | form equations for four sketched cubics — roots plus stationary-point structure; the calculus hint for curve C is explicit |
| Gradients of gradients (`gradients-of-gradients`) | calculus-meets-functions | building-blocks | 1.7.1 | medium | second derivative introduced as the gradient of the gradient — sketching f'' from f' (the f'' notation clause of 1.7.1) |
| Can we maximise the volume of this metal tin? (`r6180`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | cylindrical tin plus 2 cm-overlap lid from 350*pi cm^2 of metal: maximise the volume — canonical CIE P1 optimisation |
| When does $3x^4-16x^3+18x^2=k$ have exactly two real roots? (`r6537`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | turning points of 3x^4-16x^3+18x^2 with nature, sketch, and the k-set for exactly two real roots |
| When does this cubic equation have three distinct real roots? (`r6703`) | calculus-meets-functions | review-question | 1.7.4 | high | x^3-3a^2x+b has three distinct real roots implies 4a^6>b^2 — turning-point condition is the load-bearing argument |
| When is the cost of producing this chemical a minimum? (`r6867`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | cost C=3x+100/x minimised — derivative 3-100/x^2 with a second-derivative confirmation |
| When is $f(x) = 2x^3 − 9x^2 + 12x + 3$ smallest over this range? (`r6868`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | smallest value of 2x^3-9x^2+12x+3 on 0<=x<=2 — stationary points plus endpoint comparison |
| Can we sketch the graph of this piecewise function? (`r7196`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | medium | piecewise sketch with a turning point from the quadratic piece — differentiation drives the labelled sketch |
| What's the minimum area of this variable triangle? (`r7212`) | calculus-meets-functions | review-question | 1.7.4 | medium | minimum area of triangle OXY in the unit square as x varies — calculus optimisation (an algebraic-inequality route is also recorded) |
| What's the area enclosed by $y=x(x-3)^2$ and a tangent? (`r7386`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | medium | gradient zero at P(1,4) on y=x(x-3)^2 and the stationary-driven sketch — 1.7.2/1.7.4 load-bearing; the tangent-revisit area carries a recorded 1.8 bearing |
| How small can this triangle be? (`r7720`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | line of gradient m through (1,2): intercepts give the triangle area, minimised over m — classic P1 optimisation |
| When does a cubic curve have two turning points? (`r7861`) | calculus-meets-functions | review-question | 1.7.4 | high | cubic with two distinct turning points — the discriminant condition on f'=3x^2+2ax+b is the load-bearing argument |
| If $y=f(x)$ has a turning point when $x=\frac{1}{4}$, can we find $\lambda$? (`r7998`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | medium | turning point of f(x)=(x-2)^2-lambda(x+1)(x+2) at x=1/4 fixes lambda — derivative condition load-bearing; the equal-roots part is the 1.1 discriminant skill (recorded) |
| What can we say if $y = m(x-a)$ is tangent to $y = x^3 - x$? (`r8287`) | calculus-meets-functions | review-question | 1.7.3 | high | line y=m(x-a) tangent to y=x^3-x — the derivative supplies the tangency gradient with a double-root condition |
| Given $f'(x)$ and $g'(x)$, what is $f''(2x)$? (`r8588`) | calculus-meets-functions | review-question | 1.7.2 | medium | f'(x)=g(x+1), g'(x)=h(x-1) => f''(2x)=h(2x) — translation-chain differentiation and second-derivative notation bookkeeping |
| When does $3x^4 - 16x^3 +18x^2 + k = 0$ have four real solutions? (`r8959`) | calculus-meets-functions | review-question | 1.7.4 | high | 3x^4-16x^3+18x^2+k=0 has four real solutions exactly when -27<k<-5 — stationary-value structure is decisive |
| How many stationary points does $y = 2x^3 - 6x^2 + 5x - 7$  have? (`r9582`) | calculus-meets-functions | review-question | 1.7.4 | high | y=2x^3-6x^2+5x-7 stationary-point count via the discriminant of y'=6x^2-12x+5 — canonical MC |
| When does this function of two variables have a minimum? (`r9671`) | calculus-meets-functions | review-question | 1.7.2, 1.7.4 | high | x^4y=8 with z=x+y: stationary value and its nature via z=x+8/x^4 — rational-power derivative in a constrained optimisation |
| When does this cubic equation have distinct real positive solutions? (`r9781`) | calculus-meets-functions | review-question | 1.7.4 | medium | turning point of y=x^2-2bx+c then root conditions — the stationary point is the entry step (the root-condition part is the 1.1 discriminant skill, recorded) |
| Slippery slopes (`slippery-slopes`) | calculus-meets-functions | food-for-thought | 1.7.3 | medium | gradients of f(x), f(x)-8, 3f(x), 3f(x)+8 at matched points — constant-multiple/sum derivative structure read graphically |
| Two-way calculus (`two-way-calculus`) | calculus-meets-functions | many-ways-problem | 1.7.3, 1.7.4 | high | two-way table: generate functions with prescribed stationary points, local extrema and increasing/decreasing ranges — differentiation central (the inflection clause is extension, recorded) |
| Binomials are the answer! (`binomials-are-the-answer`) ⭐ | calculus-of-powers | investigation | 1.7.1 | high | gradients of chords (3,9)->(3.5,12.25)->(3.1,9.61)->... then the general gradient of y=x^n via the binomial expansion — the derivation-of-record from chord limits to the power rule (lane-6 sweep routing pre-identified it for 1.7) |
| Floppy hair (`floppy-hair`) | calculus-of-powers | fluency-exercise | 1.7.2, 1.7.4 | high | differentiate five curves with fractional indices, locate each maximum, match equations to curves — rational-n power rule load-bearing |
| Gradient spotting (`gradient-spotting`) | calculus-of-powers | building-blocks | 1.7.2 | high | applet pattern-hunt for the gradient of ax^2+bx+c and of cubics — inducing the power rule with each coefficient's contribution to the gradient |
| Where do two tangents cross, and where do two normals cross? (`r5703`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | tangents and normals to xy=1/2 via y=(1/2)x^-1 (rational n = -1): intersecting tangents T and normals N |
| Where does $f(x) = x^2 - 2px + 3$ have its minimum? (`r5732`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | f(x)=x^2-2px+3 has one stationary value in 0<x<1 iff 0<p<1 — parameterised stationary analysis |
| Can we find a curve from its gradient function? (`r5768`) | calculus-of-powers | review-question | 1.7.4 | medium | curve from gradient 4x-3 with minimum value -1/8 — the decisive step is locating the stationary point (the reverse-of-differentiation wrapper carries a recorded 1.8 bearing) |
| Can we find a percentage increase using the gradient? (`r6345`) | calculus-of-powers | review-question | 1.7.3 | high | percentage increase in y=3x-2x^2 via the derivative — small-increment rates work (17p/7%) |
| When does the normal to a parabola pass through this point? (`r6352`) | calculus-of-powers | review-question | 1.7.3 | high | normal to y=x^2 at (a,a^2) through (0,1) — normal equation plus solve for a (two values) |
| Can we find the area inside a parabola, a tangent, and the $x$-axis? (`r6584`) | calculus-of-powers | review-question | 1.7.3 | medium | tangent to y=x^2 at P, x-intercept Q — the tangent construction is the 1.7.3 load-bearing step; the shaded-area computation carries a recorded 1.8 bearing |
| When is the area of a face of this pyramid a minimum? (`r6820`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | minimise A^2 = 9V^2/(16x^2) + x^4 for the pyramid face — negative-power and quartic derivatives with a prove-the-minimum clause |
| Can we find the area of the triangle created by a common tangent? (`r6877`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | prove y^2=16x and y=x^2+3 touch at (1,4) via equal gradients (y=4x^(1/2) power rule) then the unit-area tangent triangle |
| Can we track this constantly growing patch of fluid? (`r6959`) | calculus-of-powers | review-question | 1.7.3 | high | circular patch growing at 5 cm^2/s: dA/dt = (dA/dr)(dr/dt) chain-rule rate for the radius |
| What's the most economical speed for this ship's journey? (`r7280`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | most economical ship speed: 2400(150/v + 8v/3) minimised — v^-1 + v derivative with a nature check |
| What is the gradient of this curve at its $x$-intercepts? (`r7391`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | gradient 17 at P on y=3x^2+5x-12, then gradients at the x-intercepts — plain power-rule fluency with a quadratic solve |
| Is the gradient function increasing or decreasing on this curve? (`r7433`) | calculus-of-powers | review-question | 1.7.3, 1.7.4 | high | sign table for dy/dx (+/-/0) and its monotonicity (I/D) at six marked points — increasing/decreasing behaviour and stationary structure read from a curve |
| Given the line $PRQ$, when is $OP + OQ$ a minimum? (`r7586`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | OP+OQ minimum for the line y=c-mx through R(a,b) — differentiate a + ma + b/m |
| Given three clues, can we find the equation of the curve? (`r7734`) | calculus-of-powers | review-question | 1.7.3 | medium | curve with gradient ax+b through two points and tangent parallel to y=x — gradient-function reconstruction with a tangent condition (the reverse-of-differentiation step carries a recorded 1.8 bearing) |
| How many common tangents can two parabolas have? (`r7750`) | calculus-of-powers | review-question | 1.7.3 | high | tangent to a parabola at the point of gradient m: y-mx = c-(m-b)^2/(4a), then common-tangent analysis for two parabolas |
| When is the volume of this cylinder inside a cone a maximum? (`r7785`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | cylinder inscribed in a truncated cone: maximum volume by polynomial optimisation |
| What (approximately) is the square root of $26$? (`r8065`) ⭐ | calculus-of-powers | review-question | 1.7.3 | high | delta y ~ (dy/dx) delta x with y=sqrt(x) gives sqrt(26) ~ 5.1 — the canonical small-increment review question |
| A cubic has one real root—can we find an approximation to it? (`r8231`) | calculus-of-powers | review-question | 1.7.3 | medium | uniqueness of the positive root of x^3+3x^2-3 via f'=3x(x+2)>0 for x>0 — increasing-function argument; the 3-dp approximation is sign-change iteration |
| Can we find the triangle areas given by a tangent? (`r8286`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | tangent to xy=c^2 at (ct,c/t) via dy/dx=-c^2/x^2 — rational-index power rule plus tangent construction with area links |
| Can we find the locus of a midpoint created by a parabola? (`r8399`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | tangent to y=(x+k)^2 at x=2k (expand-then-differentiate; the chain-rule alternative is named in the solution) plus the midpoint locus |
| When does $y=kx^3-(k+1)x^2+(2-k)x-k$ have a minimum at $x =1$? (`r8441`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | cubic kx^3-(k+1)x^2+(2-k)x-k has its minimum at x=1 precisely for k>1/2 — dy/dx(1)=0 plus nature conditions on k |
| Can we show these two cubic curves touch? (`r8543`) | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | show the parametrised cubic touches y=x^3 — tangency via equal gradients across a parameter family |
| What's the least surface area of this rocket-shaped solid? (`r8548`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | rocket-shaped solid of fixed volume: least surface area — optimisation with a fractional-power slant |
| Can we find the area enclosed by this quadratic and the $x$-axis? (`r9138`) | calculus-of-powers | review-question | 1.7.3 | medium | quadratic through (1,0) and (2,0) with gradient 2 at (2,0) — gradient conditions are the 1.7.3 step; the area computation carries a recorded 1.8 bearing |
| When is the volume of this cuboid a maximum? (`r9260`) ⭐ | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | cuboid of surface area 150 cm^2: show h=(75-x^2)/2x then maximise the volume — canonical CIE P1 optimisation |
| What can we say about the combined area of these two shapes? (`r9599`) | calculus-of-powers | review-question | 1.7.2, 1.7.4 | high | 100 cm wire into an equilateral triangle and a square: show the total-area formula then find the least area — canonical CIE P1 optimisation |
| If we increase $x$ by a small amount, what happens to $y$? (`r9942`) ⭐ | calculus-of-powers | review-question | 1.7.2, 1.7.3 | high | dy/dx of 4x^3-7x^2 at (2,4), then the small increment dx that raises y from 4 to 4.05 — power rule plus small-increment application |
| Tangent or normal (`tangent-or-normal`) | calculus-of-powers | package-of-problems | 1.7.3 | medium | match tangent/normal line pairs then recover curves from gradient functions — perpendicular-gradient structure (curve recovery carries a recorded 1.8 reverse bearing) |
| Estimating gradients (`estimating-gradients`) | calculus-trig-log | problem-requiring-decisions | 1.7.1 | medium | estimate the gradient of y=sin x at three points from tangent lines, then sketch the derivative — the gradient-of-a-curve skill in a trig setting; no trig derivatives required |
| Chain mapping (`chain-mapping`) | chain-rule | building-blocks | 1.7.2 | medium | mapping-diagram derivation of the chain rule (local scalings multiply); the worked examples extend beyond the P1 linear-inner scope (recorded) |
| I can see $u$! (`i-can-see-u`) | chain-rule | fluency-exercise | 1.7.2 | high | identify the inner function for (2x+3)^-2-style composites and differentiate dy/dx — the P1 linear-inner chain-rule clause in fluency form |
| Can we sketch $y = x^2(2-x)$, and from this, $y^2 = x^2(2-x)$? (`r7839`) | chain-rule | review-question | 1.7.2, 1.7.4 | high | sketch y=x^2(2-x) via dy/dx=-3x^2+4x stationary structure, then the y^2 symmetry extension |
| If we know the object's speed, can we find the speed of the image? (`r8625`) | chain-rule | review-question | 1.7.3 | medium | lens-formula related rates — expressible via v=f+f^2(u-f)^-1 and the chain rule (P1-compatible route; the recorded solutions often go implicit) |
| Can we find this area by integrating with respect to $y$? (`r9815`) | chain-rule | review-question | 1.7.3 | medium | tangent to 27y^2=x^3 at (12,8) via y=x^(3/2)/(3sqrt3) — rational-index power rule; the integration-wrt-y part carries bearings beyond P1 1.8 (recorded) |
| When is the volume of this pyramid a maximum? (`r9905`) | chain-rule | review-question | 1.7.2, 1.7.4 | medium | pyramid frame maximum volume — V^2 differentiable as a polynomial avoiding the product rule; stationary-point nature checked |
| Slippery slopes... another derivative (`slippery-slopes-another-derivative`) | chain-rule | building-blocks | 1.7.2 | medium | derivatives of (2x+1)^-1 via translated 1/x graphs — a pre-chain-rule view of the linear-inner composite |
| A tangent is ... (`a-tangent-is`) | introducing-calculus | building-blocks | 1.7.3 | medium | tangent-to-a-curve definition refinement with circle counter-examples; the zoom chord-to-tangent interactivity carries the 1.7.1 construct — concept building block for tangent/normal work |
| Gradient match (`gradient-match`) | introducing-calculus | building-blocks | 1.7.3 | high | pair twelve sketch graphs into function/gradient-function pairs — qualitative differentiation across polynomial and translated families |
| Why are gradients important in the real world? (`gradients-important-real-world`) | introducing-calculus | bigger-picture | 1.7.3 | medium | rates-of-change motivation: any changing system described by rates visualised as gradients (bigger-picture article; excerpt/title-only capture, no sections) |
| Mapping a derivative (`mapping-a-derivative`) | introducing-calculus | building-blocks | 1.7.1 | medium | the derivative as a local scaling via mapping diagrams for f(x)=x^2 (acknowledged capture); the construct later proves the chain rule — lane-6 sweep routing pre-identified it for 1.7 |
| When is this parabola's turning point nearest to the origin? (`r9506`) | introducing-calculus | review-question | 1.7.4 | medium | turning point of y=x^2-2ax+1 closest to the origin as a varies — stationary-point location with transformations as the alternative approach |
| Speed vs velocity (`speed-vs-velocity`) | introducing-calculus | building-blocks | 1.7.3 | medium | sketch velocity-time graphs from displacement-time and vice versa — graphical gradient-function construction in a kinematics context |
| Talking about curves (`talking-about-curves`) | introducing-calculus | investigation | 1.7.3, 1.7.4 | medium | sign of the function vs sign of its gradient across turning regions — increasing/decreasing behaviour and stationary-point structure |
| Walk-sorting (`walk-sorting`) | introducing-calculus | building-blocks | 1.7.3 | medium | match displacement-time graphs with velocity-time graphs — graphical differentiation in a real walking context |
| Zooming in (`zooming-in`) | introducing-calculus | scaffolded-task | 1.7.1 | high | zoom-in construction on y=x^2: local linearity, chord gradients collected to a formula for the gradient function — the limit-of-gradients-of-chords construct of 1.7.1 (lane-6 sweep routing pre-identified this resource for 1.7) |
| Designing a polynomial (`designing-a-polynomial`) | power-series | investigation | 1.7.2 | medium | design p(x) with p(x)=p'(x) — term-by-term power-rule differentiation with coefficient matching (the exponential-series connection is the bigger picture) |
| Producing a rule (`producing-a-rule`) | product-rule | building-blocks | 1.7.2 | medium | differentiating quadratics in factorised form — the discovered shortcut is the linear-factor product structure; expand-and-differentiate keeps it P1-compatible (the generalisation clause anticipates the P3 product rule, recorded) |
| Can we find the repeated root for  $4x^4+x^2+3x+1=0$? (`r9082`) | product-rule | review-question | 1.7.2 | medium | repeated root => root of f'(x)=0, applied to 4x^4+x^2+3x+1 — polynomial differentiation load-bearing; the general proof anticipates the product rule (P3 bearing recorded) |

## 5. Non-overlaps, boundary cases and sweep routing (never forced)

**32 recorded non-overlaps** (imported UNMAPPED with the coverage note):

- `calculus-of-variations` (calculus-of-powers): Calculus of variations bigger-picture excerpt — beyond P1 (excerpt/title-only capture).
- `integral-chasing` (calculus-of-powers): Definite-integral fluency — 1.8 bearing, no differentiation tested.
- `meaningful-areas` (calculus-of-powers): Areas between curves by several routes — 1.8 bearing.
- `queen-dido` (calculus-of-powers): Queen Dido bigger-picture excerpt — calculus-of-variations history (excerpt/title-only capture).
- `r5007` (calculus-of-powers): Area then volume of revolution for y=ax-x^2 — 1.8 bearings; no differentiation.
- `r5584` (calculus-of-powers): Solid of revolution and centre of mass — 1.8 and mechanics bearings.
- `r6067` (calculus-of-powers): I(c) integral with a non-calculus inequality argument — 1.8 bearing.
- `r6372` (calculus-of-powers): y^2=x^3 sketch by symmetry then area and volume — 1.8 bearings; the sketch needs no differentiation.
- `r7236` (calculus-of-powers): I(a)=integral of (x^2-a)^2 — the definite-integral evaluation is load-bearing (1.8); the quadratic-in-a minimisation is a light wrapper.
- `r7444` (calculus-of-powers): Area between y=x^2 and a line — 1.8 bearing; intersections by quadratics.
- `r7628` (calculus-of-powers): Sphere-slice volume and centre of gravity — 1.8 and mechanics bearings.
- `r7724` (calculus-of-powers): Zero integral by symmetry — 1.8 bearing.
- `r8350` (calculus-of-powers): Area comparison f vs g — integration decisive (1.8 bearing).
- `r8716` (calculus-of-powers): dI/da via the fundamental theorem with 2^(x^2) — beyond P1 1.7 (P3 bearings).
- `r8931` (calculus-of-powers): Polynomial degree bookkeeping for d^2/dx^2 of products — leading-term arithmetic; the differentiation is a wrapper avoided by design.
- `r9357` (calculus-of-powers): Area between parabola and line MC — 1.8 bearing.
- `stretch-the-function` (calculus-of-powers): Definite-integral scaling — 1.8 bearing.
- `approximating-areas` (introducing-calculus): Area approximation and over/under-estimation — the trapezium-rule cluster is not in the 2023-2025 P1 spec (1.8 is analytic integration; no numerical-integration row).
- `average-speed` (introducing-calculus): Average-speed situations resolved by weighted means and graph reasoning — rate intuition without differentiation.
- `discussing-distance` (introducing-calculus): Distance vs displacement graph interpretation — graph-reading skill, no differentiation tested.
- `newton-and-leibniz` (introducing-calculus): Newton and Leibniz history excerpt — no testable calculus skill (excerpt/title-only capture).
- `r5642` (introducing-calculus): Trapezium-rule exactness MC — not in the 2023-2025 P1 spec.
- `r5782` (introducing-calculus): Average-speed arithmetic for two trains — no differentiation.
- `r6841` (introducing-calculus): Stopping distance via uniform retardation — mechanics suvat, no differentiation.
- `r7140` (introducing-calculus): Average-speed arithmetic — no differentiation.
- `r7250` (introducing-calculus): Speed-time graph: straight-section gradients and areas — arithmetic graph work (mechanics context), no curve differentiation.
- `r7903` (introducing-calculus): Derivation of the trapezium rule — not in the 2023-2025 P1 spec.
- `r8140` (introducing-calculus): Trapezium rule on a floor-function integrand — not in the 2023-2025 P1 spec.
- `r9586` (introducing-calculus): Constant-acceleration suvat — mechanics kinematics, no differentiation tested.
- `rectangles-in-triangles` (introducing-calculus): Rectangle-in-triangle maximisation explicitly without calculus — the tested skill is geometric reasoning (similar triangles/algebra).
- `serpentine-lake` (introducing-calculus): Serpentine lake area by trapezia — not in the 2023-2025 P1 spec.
- `underneath-the-arches` (introducing-calculus): Trapezium-rule over/underestimates from concavity — not in the 2023-2025 P1 spec.

**Boundary cases recorded honestly (not forced):** the Introducing-Calculus trapezium-rule/area-approximation cluster (r5642, r7903, r8140, r9188, serpentine-lake, underneath-the-arches, plus the average-speed and suvat review questions) is recorded as non-overlap — the trapezium rule is not in the 2023–2025 P1 spec and the kinematics questions test mechanics skills, not differentiation. The three lane-4/6 deferred substrates are caught as **cross-lane joins**: lane 4's non-overlap row for r7115 *names 1.7 as the tested skill* (the canonical cone optimisation), and lane 6's r5640 carries 1.7.2/1.7.4 calculus parts alongside its of-record 1.6.1 alignment; r8936's arc-length maximum (lane 4, 1.4.1) is a one-to-many 1.7.4 extension. The chain-rule, product-rule and calculus-trig-log stations are dominated by P3-bearing work — general chain rule with non-linear inner functions, product/quotient rule, trigonometric/exponential/logarithmic derivatives, parametric and implicit differentiation — recorded as 86 routings with the P3 bearings named; the lane-6 routing pointers into 1.7 (r7692, r6509, r6920, r5348, r9484) are all resolved here (three aligned, two routed with P3 bearings).

**Sweep routing (86):**

- `r5053` → P3/further conics (parabola normals via implicit/parametric differentiation)
- `r5237` → P3/further conics (ellipse normal; implicit differentiation)
- `r5251` → P3 Differentiation (trig derivatives: d/dx cos 3x via the chain rule)
- `r5376` → P3 Differentiation (implicit differentiation of conics meeting at right angles)
- `r5678` → P3/further conics (hyperbola tangent; parabola focus geometry)
- `r5696` → P3 Differentiation (parametric curve normals)
- `r5739` → 1.1 Quadratics / curve-sketch case analysis (tangency via discriminants; no differentiation load-bearing)
- `r5990` → P3 Differentiation (trig derivatives + chain rule; identity deduction)
- `r6710` → P3/further conics (ellipse tangent and normal at the focus-above point)
- `r6843` → P3/further conics (ellipse chord equation; trig manipulation)
- `r7042` → P3/further conics (parabola-ellipse right-angle intersection; implicit/parametric)
- `r7431` → P3 Differentiation (derivative of ln(1+x^2); inequality deduction)
- `r7792` → P3 Differentiation + algebra (partial fractions then dy/dx; P3 bearings)
- `r7833` → P3 Differentiation (implicit tangents to hyperbolas; square construction)
- `r8620` → P3 Differentiation (parametric dy/dx and normal)
- `r8694` → P3 Integration (tan^3 and substitution integrals)
- `r8778` → P3 Integration (substitution integrals incl. sec^4)
- `r8836` → 1.8/Mechanics bearings (cylinder centre of mass by integration)
- `r8890` → P3 Integration (integration by substitution)
- `r8939` → P3 Differentiation (parametric sec/tan normal)
- `r9085` → P3 Differentiation (tangent to 1/(1+x^2) — non-linear-inner composite)
- `r9297` → P3 Differentiation/Integration (tan^3 derivative, tan^4 integral)
- `r9325` → P3/further conics (ellipse tangent meeting x=a)
- `r9413` → P3/further conics (epicycloid normal; parametric trig)
- `r9809` → P3/further conics (parabola normals; implicit/parametric)
- `can-you-find-chain-rule-edition` → P3 Differentiation (chain-rule construction with general/ln composites)
- `differentiating-exponentials` → P3 Differentiation (derivative of a^x; excerpt/title-only capture)
- `implicit-circles` → P3 bearings (implicit differentiation intro; the P1 route is the 1.3 radius-perpendicularity)
- `integral-sorting` → P3 Integration (integral-substitution matching)
- `odd-one-out` → Mixed function properties (trig/translates in play; no P1 1.7 skill load-bearing)
- `parametric-paths` → P3 (parametric curve sketching)
- `parametric-points` → P3 Differentiation (parametric stationary points via the chain rule)
- `parametric-preliminaries` → P3 (parametric equations introduction)
- `powerful-derivatives` → P3 Differentiation bearings (real-index power rule proved via exponentials/logarithms — the P1 rule covers rational n; lane-6 routing recorded)
- `reflecting-on-change` → P3 Differentiation (inverse-function derivative intuition)
- `slippery-areas` → 1.8 bearings (areas under transformed graphs)
- `the-law-of-reflection-and-saving-time` → P3 bearings (chain rule for the reflection law; excerpt/title-only capture)
- `which-substitution` → P3 Integration (substitution on 1/sqrt(1-x^2))
- `additional-integrals` → 1.8 bearings (linearity of the integral)
- `choose-your-families` → Open graph-classification task — calculus features optional, never load-bearing
- `keep-your-distance` → Modelling investigation (traffic flow) — the flow-rate maximum is investigated graphically/numerically, not by clean P1 calculus
- `r5090` → 1.2 Functions (bilateral symmetry f(x)=f(2alpha-x); proof skill)
- `r5324` → Trapezium rule — not in the 2023-2025 P1 spec
- `r7461` → 1.2 Functions (transformations f(-x), f(x-1), -f(x)); the I(c) clause is a translation argument, not calculus
- `r8130` → 1.8 bearings (area as a sum of integrals)
- `r8396` → 1.8 bearings (integral inequality)
- `r8987` → 1.3/Geometry (hexagon area 2(x^2+xy+y^2); no calculus)
- `what-else-do-you-know` → 1.8 bearings (areas under transformed functions)
- `thinking-constantly` → 1.8/Mechanics bearings (integration constants in kinematics)
- `two-way-calculus-teacher-support` → Teacher-support notes for two-way-calculus (the aligned main task carries the mapping; teacher-support pages ship only alongside substrate mains)
- `r6938` → P3 Differentiation (turning points of sin x + cos x)
- `r7074` → P3 Differentiation (maxima of sin 2x / sin x)
- `r7616` → P3 Integration (product of trig integrals sign analysis)
- `r8071` → P3/Mechanics bearings (SHM: s=12sin(3t/2); trig derivatives)
- `rotating-derivatives` → P3 Differentiation (derivatives of sin/cos via circular motion)
- `similar-derivatives` → P3 Differentiation (derivatives of tan/sec/cot/cosec)
- `sine-stretching` → P3 Differentiation (derivative of sin(ax))
- `to-the-limit` → P3 Differentiation bearings (chord-limit machinery is 1.7.1 but the target a^x carries P3 bearings)
- `trig-gradient-match` → P3 Differentiation (trig gradient-function matching)
- `sine-on-the-dotted-line` → 1.8/P3 bearings (areas under sin x)
- `stretching-an-integral` → P3 Integration (stretching 1/x toward ln)
- `two-for-one` → P3 Integration (ln|x| and the modulus)
- `inverse-integrals-teacher-support` → Teacher-support notes (inverse integrals lesson) — outside P1
- `trigsy-integrals` → P3 Integration (trig and inverse-trig integrals)
- `how-does-your-rectangle-grow` → P3 Differentiation (product-rule visual derivation d(uv)=u'v+uv')
- `integral-chasing-2` → P3 Integration (integral-chasing II)
- `r5126` → P3 Integration (trig/log integrals)
- `r5501` → P3 Differentiation (turning points of x^2/(1+x^4); quotient rule)
- `r6530` → P3 Differentiation (e^(2x)(2cos3x+3sin3x))
- `r6549` → P3 Differentiation (stationary points of cot x - 8cos x)
- `r6620` → P3 Differentiation (gradient x(1-x^2)e^(-x^2))
- `r6855` → 1.2/Algebra bearings (rational sketch by difference of squares)
- `r6863` → 1.2/Algebra bearings (rational sketch plus y^2 version; sign analysis)
- `r7129` → 1.1 Quadratics bearings (discriminant range analysis)
- `r7410` → P3 Differentiation (product rule intended for x(5-x)^4; the P1 binomial-expansion route exists but is not the designed path)
- `r8134` → P3 Differentiation/Integration (reduction for e^(-x)sin^n x)
- `r8152` → 1.8/P3 bearings (average density by integration)
- `r8387` → P3 Differentiation (product rule intended for x(x+1)(x-2)^4)
- `r8671` → P3 Differentiation (x^(1/x) via logarithmic differentiation)
- `r8765` → 1.1 Quadratics bearings (rational range via discriminant)
- `r8774` → 1.8/Mechanics bearings (displacement from velocity by integration)
- `r9329` → 1.1 Quadratics bearings (rational range; inflection clause is P3)
- `r9391` → 1.1 Quadratics bearings (rational range via discriminant)
- `r9484` → P3 Differentiation bearings (dy/dx of e^(-x)/(1+x^2) needs the quotient rule and exp; lane-6 routing's 1.7 curve-sketching pointer recorded honestly as P3-bearing)
- `r9795` → P3 Differentiation (product + chain rule on (x+6)^7(x-9)^8)
- `r9898` → P3 Differentiation (stationary points of (x-a)e^x/(x-b))

## 6. Primary picks of record

- **1.7.1 → `r7692`** (Binomials are the answer!) — the derivation-of-record: chord gradients at (3,9) → (3.5,12.25) → (3.1,9.61) → … generalised to the gradient of y = xⁿ via the binomial expansion; the limit-of-chords construct and the power rule in one resource (modes [1,4]).
- **1.7.2 → `r9942`** (If we increase x by a small amount, what happens to y?) — the canonical CIE P1 question: differentiate 4x³ − 7x², evaluate dy/dx at a point, then the small-increment application.
- **1.7.3 → `r8065`** (What (approximately) is the square root of 26?) — the canonical small-increment question: δy ≈ (dy/dx)δx with y = √x.
- **1.7.4 → `r9260`** (When is the volume of this cuboid a maximum?) — the canonical CIE P1 optimisation: constrain, express, differentiate, determine the nature, conclude.

## 7. S1 provenance bridge status for this lane

54 of the 74 aligned resources carry a provenance tuple of record (board/qualification/paper/year/questions/permission) from the P3b review-question-provenance sweep (`resources/derived/review-question-provenance.json`); the tuples ride the enrichment rows and the imported front-matter `exam_reference` fields. The remainder are UGM originals or captures without board metadata — recorded as null, never invented.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record + served** — enrichment #55, text #58 (main@91eed732), hub #308 (merged).
- Lane 2 (functions, 1.2.1–1.2.5): **of record + served** — enrichment + text #61 (a32c6c0f, MANIFEST v2), hub #312 (merged).
- Lane 3 (coordinate geometry, 1.3.1–1.3.2 with fragments folded): **of record + served** — cross-map @ cb947595, enrichment + text #66 (MANIFEST v3), hub #321 (merged).
- Lane 4 (circular measure, 1.4.1 with 1.4.1a folded — first strand lane): **of record + served** — cross-map @ b52cf1bf, corpus #74 → `1585c4ff` (MANIFEST v4), hub #327 → `2684a8e4` (cross-lane join law established).
- Lane 5 (trigonometry, 1.5.1–1.5.5 — first two-station lane): **of record + served** — cross-map @ f3ef5745, corpus #79 → `cf79ecd2` (MANIFEST v5), hub #330 → `16bef479` (merged 2026-10-23).
- Lane 6 (series, 1.6.1–1.6.4 — second two-station lane): **of record + served** — cross-map @ 6c3649a7+82964ce4, corpus #89 → `bcc36476` (MANIFEST v6), hub #337 → `cdd7fcfc` (merged 2026-10-23; 6 lanes / 20 stations / 22 spec points / 320 rows / 113 non-overlaps / 363 bodies served).
- **Lane 7 (this lane, 1.7.1–1.7.4, two-station lane)**: cross-map of record here; corpus + enrichment filed as `T-UGM-MODE1-7` / `T-UGM-IMPORT-7` (MANIFEST v7, branch `ugm/pure-1-differentiation`); hub consumption awaits operator order as `T-UGM-HUB-CONSUME-7` on the syllabai-v2 side — the importer's lane-7 block is a 2+6-station lane block (expected census: 106 files / 107 rows / 74 aligned / 32 non-overlap) plus **three cross-lane fact joins** (r5640, r7115, r8936), reusing the lane-4/-5/-6 join law unchanged.
- Next hops by spine adjacency: **1.8 Integration** (the final Pure 1 subtopic — the integration stations and the 1.8-bearing pools recorded across lanes 6–7), which completes the P1 spine; the P3 preview pools (real-index binomial + power series from lane 6; product/chain-rule and trig/exp/log derivative pools recorded here) remain the natural substrate for future P3 lanes.

Corpus sweep provenance: candidates from the keyword sweep over `resources/ugm-clean/*` and `resources/content/*` (derivativ-, differentiat-, dy/dx and f′/f″ notations, gradient of a curve, tangent/normal, stationary/turning points, chain rule, second derivative, rate of change, increasing/decreasing, maximis-/minim-, chord/limit patterns; 855 resources screened, 2026-10-24); verdicts read against question wells and solutions; machine-readable twin `resources/derived/cross-map-differentiation.json`.
