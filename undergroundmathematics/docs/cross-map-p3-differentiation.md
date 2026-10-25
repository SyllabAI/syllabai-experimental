# Cross-map lane 12: the UGM differentiation plane → CIE 9709 Pure 3, 3.4 Differentiation

## 1. What this is

Of-record verdicts for lane 12 of the P3c generalisation programme: every UGM candidate bearing on CIE 9709 Pure 3 subtopic **3.4 Differentiation** (spec points 3.4.1–3.4.3, the verbatim spine rows of record — parse artifacts disclosed, no fold fragments) is closed here: **41 aligned rows** (40 fresh bodies — the lane's new text of record — plus 1 cross-course flip by reference), **29 non-overlaps** recorded with routedTo bearings, and **119 of-record candidates rejected because their prior alignments/rows stand**. Operator order: *"eyeball+merge of #371 then lane 12"* (trace `1a173977b2f547f5`); lane-12 identity named of record by the lane-11 bookkeeping next pointer (*"next: 3.4 via the lane-11 P3-3.4 routings"* @ `b2c31f9d`).

## 2. Lane coverage — headline numbers

| | |
|---|---|
| corpus screened | 855 resources / 25 stations |
| sweep candidates | 189 (pass-1 title/description + pass-2 section-text, plus the 21 pre-baked lane-10/11 'P3 3.4 Differentiation' bearing rows) |
| aligned rows | **41** = 40 fresh rows over 40 substrate resources (single-code) + 1 cross-course flip by reference |
| cross-course joins | **1 flip** — r8931 (the lane-7 non-overlap row whose whole-station body of record lives under `pure-1-differentiation/`, the two-station lane law) maps to 3.4.2 by reference under the lane-9 flip law; **no one-to-many joins** this lane |
| fresh non-overlaps | **29 recorded by reference only** (`bodyImported: false`) — 3 of them honest re-routings of lane-10 dual/3.4 bearings (r6620, r8134 → 3.5; differentiating-exponentials → no extractable text) |
| of-record candidates rejected | **119 with reasons** — every one aligned or non-overlapping of record elsewhere |

Primary picks of record: **r6938** (3.4.1 — the canonical stationary-points-of-sin-cos exercise) / **r6530** (3.4.2 — the product rule over e^(2x)(2cos 3x + 3 sin 3x), the exact CIE showcase) / **r8620** (3.4.3 — parametric dy/dx, stationary point and normal at t = 2). All three ride fresh bodies (the fresh-pick convention holds this lane).

## 3. Per-spec-point detail

### 3.4.1 — use the derivatives of e , ln x , sin x , cos x , tan x , tan x , together with constant multiples, sums, differences and composites

Spine title verbatim (parse artifacts carried — no fold fragments). 13 aligned rows, pick `r6938`:

- `r6938` (calculus-trig-log, Review question, high) **[pick]** (flips its lane-10/11 non-overlap row of record) — turning points of y = sin x + cos x on (0, 2pi) via dy/dx = cos x - sin x = 0 - the canonical 3.4.1 use of the standard derivatives, with the R-form of 3.3.2 as the recorded alternative (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `can-you-find-chain-rule-edition` (chain-rule, Many ways problem, high) (flips its lane-10/11 non-overlap row of record) — working backwards from conditions on f(g(x)) (stationary points at prescribed x, a local minimum of ln g(x), no stationary points) - chain-rule composition reasoning with the 3.4.1 list as the toolset (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `powerful-derivatives` (chain-rule, Building blocks, high) (flips its lane-10/11 non-overlap row of record) — prove d/dx x^a = a x^(a-1) for real a by writing x^a = e^(a ln x) and chaining the standard derivatives - the ln/exponential derivative law of 3.4.1 is the engine (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r5251` (chain-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — d/dx (3 cos x - cos 3x) = 6 sin x cos 2x proved by the chain rule on cos 3x plus the product-to-sum identity, then the increasing ranges and the sketch (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r5990` (chain-rule, Review question, high) — chain rule on sin^4 x, cos^2 x, cos^4 x gives d/dx = 0 identically - the expression is the constant 1; the deduction task on the 3.4.1 composite derivatives
- `r7431` (chain-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — d/dx (x - ln(1+x^2)) = 1 - 2x/(1+x^2) >= 0 by the 3.4.1 composite derivative of ln(1+x^2), deducing x > ln(1+x^2) for x > 0 - the increasing-function argument (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r8071` (calculus-trig-log, Review question, medium) — v = ds/dt and a = dv/dt for s = 12 sin(3t/2) - the 3.4.1 composite derivative of sin(3t/2) by the chain rule is the load-bearing computation (mechanics clothing); the remaining parts are 1.5 trig equations
- `r8671` (product-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — stationary point of x^(1/x) via d/dx(ln y) = (1 - ln x)/x^2 - ln/composite 3.4.1 work deciding e^pi > pi^e without a calculator (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r9085` (chain-rule, Review question, medium) — gradient of y = 1/(1+x^2) via the chain rule on (1+x^2)^-1 giving -2x/(1+x^2)^2, then the tangent-line condition from (0,1) - the derivative work is load-bearing; the pi>3 coda is an area argument (3.5 bearing)
- `rotating-derivatives` (calculus-trig-log, Scaffolded task, high) (flips its lane-10/11 non-overlap row of record) — the unit-circle velocity vector (-sin t, cos t) assembled from the rotating diagrams - the geometric derivation of d/dt(sin t) = cos t and d/dt(cos t) = -sin t, the 3.4.1 standard facts (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `similar-derivatives` (calculus-trig-log, Building blocks, medium) (flips its lane-10/11 non-overlap row of record) — d(tan theta)/dtheta via similar triangles with vertices (1, tan theta) and (cot theta, 1) - in-spec for the tan limb of 3.4.1; the sec/cot extensions are beyond the 3.4.1 list and are disclosed (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `sine-stretching` (calculus-trig-log, Building blocks, high) (flips its lane-10/11 non-overlap row of record) — gradient function of sin 3x selected from cos 3x / 3 cos x / 3 cos 3x by graphical reasoning - the chain-rule composite d/dx(sin 3x) = 3 cos 3x (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `trig-gradient-match` (calculus-trig-log, Building blocks, medium) — pairing trig functions with their gradient functions incl. the scaled composites - builds d/dx(sin x) = cos x and the chain-rule cases graphically; excerpt-capture disclosure: no solution well of record, matched on the provider task statement

### 3.4.2 — differentiate products and quotients e.g.

Spine title verbatim (parse artifacts carried — no fold fragments). 12 aligned rows, pick `r6530`:

- `r6530` (product-rule, Review question, high) **[pick]** (flips its lane-10/11 non-overlap row of record) — d/dx of e^(2x)(2 cos 3x + 3 sin 3x) by the product rule with the 3.4.1 composite derivatives inside - the exact CIE product-rule-plus-standard-derivatives showcase (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `how-does-your-rectangle-grow` (product-rule, Scaffolded task, high) — the fixed-height rectangle argument dA/dt = v du/dt extended to both sides varying - the visual derivation of the product rule d(uv)/dt = v du/dt + u dv/dt, the 3.4.2 law itself
- `r5501` (product-rule, Review question, high) — turning points of y = x^2/(1+x^4) via the product rule on x^2 (1+x^4)^-1 giving dy/dx = 2x(1-x^4)/(1+x^4)^2 - stationary points at 0, +/-1 and the sketch
- `r6549` (product-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — stationary points of y = cot x - 8 cos x: d(cot x)/dx derived by the quotient rule on cos x/sin x (the in-spec 3.4.2 route - resolves the lane-11 'beyond the 3.4.1 list' caveat of record), then -cosec^2 x + 8 sin x = 0 (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r6855` (product-rule, Review question, medium) — stationary points of g(x) = 1/(((x-a)^2-1)((x-b)^2-1)) found by differentiating the product of reciprocal quadratics - the product/quotient-rule work is load-bearing for the three stationary abscissae
- `r8387` (product-rule, Review question, high) — gradient of y = x(x+1)(x-2)^4 shown as (x-2)^3(6x^2+x-2) by the product rule, all stationary points with nature, then the y^2 and even-power variant sketches
- `r8774` (product-rule, Review question, medium) — acceleration as d/dt of v = (2t-1)/(4(2t+1)) by the quotient rule (a = 1/(2t+2)^2) - the quotient-rule computation is the tested skill in kinematics clothing; the displacement part is an integral (3.5 bearing)
- `r9329` (product-rule, Review question, medium) — f'(x) = -2(x^2+x+1)/(x^2-1)^2 by the quotient rule, always negative, with the inflection argued from the behaviour of f' between the asymptotes - the range part is the recorded discriminant method
- `r9391` (product-rule, Review question, medium) — the range of y = x(x-3)/(x-4) shown both by the discriminant and by the quotient rule (both approaches of record) - stationary points at the range endpoints; the 5/x comparison is algebraic
- `r9484` (product-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — y = e^-x/(1+x^2): y always positive and dy/dx never positive by the quotient rule, the stationary point where dy/dx = 0, and the sketch (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r9795` (product-rule, Review question, high) — dy/dx of y = (x+6)^7 (x-9)^8 by the product rule and the zeros of dy/dx - the canonical 3.4.2 product-rule exercise
- `r9898` (product-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — stationary points of y = ((x-a)/(x-b)) e^x by the product and quotient rules giving the (a-b) < 0 or (a-b) > 4 condition, then the two case sketches (flips the lane-10 non-overlap row of record routed 'P3 3.4 Differentiation')

### 3.4.3 — find and use the first derivative of a function e.g. which is defined parametrically or implicitly.

Spine title verbatim (parse artifacts carried — no fold fragments). 15 aligned rows, pick `r8620`:

- `r8620` (chain-rule, Review question, high) **[pick]** — x = (3-2t)^2, y = t^2 - 2t: dy/dx in terms of t, the stationary point, and the normal at t = 2 - the exact CIE 3.4.3 parametric exercise
- `implicit-circles` (chain-rule, Many ways problem, high) — gradient of x^2 + y^2 = 4 at three points and at a general point - implicit differentiation dy/dx = -x/y with the radius-gradient alternative, the canonical 3.4.3 implicit introduction
- `parametric-points` (chain-rule, Fluency exercise, high) (flips its lane-10/11 non-overlap row of record) — dy/dx = -(3 cos t)/(2 sin t) for the parametric ellipse, matched to stationary-point locations and graphs - the 3.4.3 parametric chain-rule law as the matching tool (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r5053` (chain-rule, Review question, high) — normal to the parabola y^2 = 4ax at (at^2, 2at) and the two-normals-through-P proof - implicit/parametric differentiation of the standard parabola with the fixed-point geometry
- `r5237` (chain-rule, Review question, high) — normal to the ellipse x^2/a^2 + y^2/b^2 = 1 at (a cos theta, b sin theta) proved as ax/cos theta - by/sin theta = a^2 - b^2 - parametric differentiation with the eccentricity consequence
- `r5376` (chain-rule, Review question, high) — y^2 = 4ax and xy = c^2 intersecting at right angles via their derivatives, giving c^4 = 32a^4 and TG = 6a - implicit/parametric derivative work on both curves
- `r5678` (chain-rule, Review question, high) — tangent to the hyperbola xy = c^2 through the parabola focus, the a^4 = 2c^4 condition and the acute angle between the tangents - parametric/implicit derivative work on both conics
- `r5696` (chain-rule, Review question, high) — normals to the parametric curve x = 4 - t^2, y = 4t at the y-axis intersections meeting on the x-axis - dy/dx = (dy/dt)/(dx/dt) with the normal equations
- `r6710` (chain-rule, Review question, high) — tangent and normal at the point P above the focus of an ellipse meeting the y-axis, with QR = HP - parametric differentiation on the standard parametrisation
- `r7042` (chain-rule, Review question, high) — the parabola y^2 = 4ax and the ellipse 2x^2 + y^2 = c^2 cutting at right angles via the normal-midpoint proof - implicit/parametric derivatives of both curves
- `r7833` (chain-rule, Review question, high) — tangents to xy = 1 and x^2 - y^2 = 2 at P and Q forming the square PMQN - gradients from implicit differentiation (dy/dx = x/y on the hyperbola), the perpendicularity and the equal sides
- `r8939` (chain-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — normal to x = 5a sec theta, y = 3a tan theta parallel to y = x - parametric differentiation of the sec/tan parametrisation with the gradient condition (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r9325` (chain-rule, Review question, high) — tangent to the ellipse at P meeting the y-axis at Q and the line x = a at T, with the chord A'P construction - parametric differentiation and the tangent equation
- `r9413` (chain-rule, Review question, high) (flips its lane-10/11 non-overlap row of record) — normal to x = n cos t - cos nt, y = n sin t - sin nt proved as x cos((n+1)t/2) + y sin((n+1)t/2) = (n-1) cos((n-1)t/2) - the chain-rule composites cos nt, sin nt inside the parametric derivative (flips the lane-11 non-overlap row of record routed 'P3 3.4 Differentiation')
- `r9809` (chain-rule, Review question, high) — normals to the parabola y^2 = 4ax at parameters t1, t2 with t1 t2 = 2 meeting on the parabola - implicit/parametric normal work with the cyclic-quadrilateral coda

## 4. Cross-course rows (1 by reference, body of record under pure-1-differentiation)

- `r8931` — *What happens if we expand, then differentiate?* (calculus-of-powers, Review question, medium) — the degree-of-derivative MC read off the product-rule structure; **flips the lane-7 non-overlap row of record** (the body of record lives under `pure-1-differentiation/` via the two-station whole-import law) — no new text, the kind/prior-alignment/textOfRecordUnder fields are on the JSON row of record.

## 5. Non-overlaps of record (29 by reference)

Recorded with `routedTo` bearings for future lanes. The three honest re-routings are marked:

- `choose-your-families` (calculus-meets-functions) → false positive — graph-family card sort on function features - no 3.4 skill; the sweep hit the graph/feature language
- `differentiating-exponentials` (chain-rule) → no extractable text **[declines the lane-10 'P3 3.4' bearing — no extractable sections of record]** — the scaffolded task for d/dx a^x has no extractable sections of record (applet-rendered); the lane-10 'P3 3.4 Differentiation' bearing cannot become text this lane - the lane-10 of-record treatments (to-the-limit, see-the-power) already carry the a^x derivative story beside 3.2.2
- `happy-families` (polynomials) → beyond spec — implicit-equation curve exploration (domain and range of an algebraic family) - no differentiation load-bearing
- `how-long-is-a-piece-of-string` (hyperbolic-functions) → beyond spec (arc length) — arc length from first principles for Cartesian and parametric curves - outside the CIE 9709 pure 1-3 scope
- `integral-sorting` (chain-rule) → P3 3.5 Integration — pairing integrals with answers and substitutions - the integration-by-substitution fluency is 3.5 substrate
- `keep-your-distance` (calculus-meets-functions) → false positive — Highway Code stopping-distance modelling - the rate language is contextual, no 3.4 skill
- `mapping-a-function` (thinking-about-functions) → false positive — mapping diagrams for linear functions - pre-calculus; the derivative work lives in the lane-7 of-record companion mapping-a-derivative
- `one-windy-day` (vector-geometry) → false positive — projectile-with-wind parametric modelling - no dy/dx load-bearing (the of-record solution finds the landing point without differentiation)
- `parametric-paths` (chain-rule) → false positive — matching curves with parametric coordinates and sketching - parametric fluency without differentiation (no solution section of record)
- `parametric-preliminaries` (chain-rule) → false positive — parametric equations introduced via locus geometry - pre-3.4.3
- `r5854` (polynomials) → false positive — oblique asymptote shown tangent via the double-root intersection test - algebraic, no differentiation
- `r6620` (product-rule) → P3 3.5 Integration **[re-routes the lane-10 dual 'P3 3.4/3.5' bearing]** — curve analysis from a GIVEN gradient x(1-x^2)e^(-x^2): stationary points and sketch, coordinates recovered by substitution-integration - no differentiation performed; re-routes the lane-10 dual 'P3 3.4/3.5' bearing honestly to 3.5
- `r6863` (product-rule) → false positive — sketching y = f(x) then y^2 = f(x) by sign and limit analysis - no differentiation load-bearing
- `r7017` (polynomials) → false positive — real-root existence for (x-1)(x-2)...(x-n) = k by sign/IVT reasoning - no calculus
- `r7129` (product-rule) → false positive — the range of ax/(x^2+x+1) shown by the quadratic-in-x discriminant of record - no differentiation; the sketch reads off the range
- `r7461` (calculus-meets-functions) → P3 3.5 Integration — I(c) area maximisation decided by symmetry and the sketched 2^(2x-x^2) labelled without calculus - the area work is 3.5 substrate
- `r7678` (vector-geometry) → P1 1.7 (unmapped) — velocity and acceleration by differentiating polynomial components of a position vector - the power-rule skill of the P1 differentiation lane
- `r8134` (product-rule) → P3 3.5 Integration **[re-routes the lane-10 dual 'P3 3.4/3.5' bearing]** — reduction formula for the integral of e^-x sin^n x - the product-rule identity d/dx (cos x sin^(n-1) x) is the scaffold step; the tested skill is 3.5 integration by parts; re-routes the lane-10 dual 'P3 3.4/3.5' bearing honestly to 3.5
- `r8160` (polynomials) → false positive — quintic graph matching by roots and multiplicity - no calculus
- `r8679` (calculus-trig-log) → P3 3.5 Integration — area under cos x - sin x + 2 and the Newton-Raphson refinement - integration and root-finding substrate
- `r8765` (product-rule) → false positive — the values taken twice shown by the parity argument and the rearranged x^2 = (a^2 y + 1)/(y - 1) >= 0 of record - algebraic, no differentiation
- `r8890` (chain-rule) → P3 3.5 Integration — integration by substitution exercises - 3.5 fluency
- `r8987` (calculus-meets-functions) → false positive — hexagon minimum area via the quadratic in x after substituting y = 10 - x - algebraic minimisation, no calculus of record
- `r9108` (polynomials) → P1 1.7 (unmapped) — unique root argued by dy/dx = 3x^2 + 2x + 1 > 0 on the expanded cubic - the power-rule monotonicity skill of the P1 differentiation lane (the of-record solution differentiates)
- `r9259` (thinking-about-geometry) → false positive — incircle/circumcircle ratio by tangent lengths and Pythagoras - circle tangency, not curve tangents
- `r9792` (thinking-about-geometry) → false positive — two tangents to a circle, lengths and angles - circle geometry, no curve differentiation
- `reflecting-on-change` (chain-rule) → beyond spec (inverse-function derivatives) — inverse-function gradient intuition - outside the 3.4 list (inverse-function differentiation is not a CIE 9709 pure topic)
- `the-law-of-reflection-and-saving-time` (chain-rule) → beyond spec (bigger-picture excerpt) — bigger-picture essay: the chain rule and the Fermat-style minimisation behind the reflection law - no exercise well
- `two-way-calculus-teacher-support` (calculus-meets-functions) → teacher-support notes (no 3.4 exercise) — research-project teacher notes for the two-way calculus task - meta content, not a spec embodiment

## 6. Of-record candidates rejected (119)

Every rejected candidate carries its reason in the cross-map JSON `sweepRouting` (outcome `rejected_of_record`). Distribution: 104 aligned of record under lanes 1–11 (prior alignment stands — dominated by the lane-7 P1-differentiation alignments, the densest of-record lane); 15 standing prior non-overlap rows (incl. the two declined lane-10/11 'P3 3.4' bearings odd-one-out and r6843 — the first declined with a no-solution-well disclosure, the second with the solution-verified all-identities derivation); 5 of the 20 standing rows also carry prior alignments (the specific reason is recorded).

## 7. Findings of record

1. **Lane 12 is the mirror image of lane 11's shape problem — and it inverts.** Lane 11 was mostly-mapping because its dedicated stations were whole-imported by lane 5; lane 12's skill area is held by chain-rule and product-rule, which lane 7 did NOT whole-import (only 7 + 2 stray alignments), so the lane-12 substrate is overwhelmingly FRESH: 40 new bodies — the largest fresh-text lane since lane 9 (35), in the lane the lane-7 bookkeeping called the densest item attachment.
2. **The 3.4.1 list boundary is load-bearing and was applied strictly.** CIE 3.4.1 names e^x, ln x, sin x, cos x, tan x plus composites — NOT the power rule, NOT inverse functions, NOT arc length. The P1-flavoured differentiation corpus (stationary points of polynomials, tangents to cubics, optimisation) is of record under lane 7's 1.7.x alignments and is rejected here with those alignments cited; the lane-12 aligned set exercises exactly the named standard derivatives and their composites (13 rows), the product/quotient law (13 rows incl. the r8931 flip), and parametric/implicit work (15 rows).
3. **The lane-10/11 pre-baked pool mostly converts.** Of the 21 bearing rows, 16 promoted to aligned fresh bodies (8 from lane-10, 9 from lane-11 — each superseding its stale row of record per the to-log-or-not-to-log law), 2 re-routed honestly to 3.5 (r6620, r8134 — the given-gradient/reduction-formula tasks whose differentiation is scaffold), 1 declined for no extractable text (differentiating-exponentials), and 2 declined on the merits (odd-one-out — derivative facts are inventory, no solution well; r6843 — the of-record solution differentiates nowhere).
4. **The discriminant-method family is real and was declined honestly.** Five range/sketch review questions (r7129, r8765, r9329-part-1, r9391-part-1, r7461) admit the quadratic-in-y discriminant solution with no calculus; only those whose of-record solutions actually differentiate (r9329's inflection, r9391's Approach 2, r5501, r9085) were aligned, at medium confidence with the dual-method disclosure.
5. **Mechanics clothing is admitted at medium, consistently with the lane-6 bouncing-ball precedent** (r8071 s = 12 sin(3t/2) kinematics; r8774 quotient-rule acceleration; r7678 rejected as pure power-rule kinematics — the 1.7 bearing recorded).

## 8. Next hops by spine adjacency

- **Lane 13 = CIE 9709 Pure 3 subtopic 3.5 Integration** (spec points 3.5.1–3.5.3 per the hub spine of record) — the lane-12 non-overlap rows routed 'P3 3.5 Integration' (integral-sorting, r7461, r8679, r8890, r6620, r8134, r9297-precedent) are its pre-baked bearings, alongside the lane-11 rows routed 3.5 (10 rows) and the lane-10 rows routed 3.5/3.4-dual. The pure-1 integration lane (lane 8) whole-imported only 10 fresh bodies, so the 3.5 substrate is expected to be substantially fresh like this lane.
- The remaining pure-3 spine after 3.5: 3.6 Numerical solution of equations (3 rows), 3.7 Vectors (7 rows), 3.8 Differential equations (4 rows), 3.9 Complex numbers (8 rows) — the hub spine parse carries 43 spec points across the 9 subtopics of record.

