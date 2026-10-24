# Cross-map lane 9: the UGM algebra plane → CIE 9709 Pure 3, 3.1 Algebra (first lane on the pure-3 course plane)

## 1. What this is

Lane 9 of the P3c generalisation, and the **first lane beyond the completed Pure 1 spine**: the
Pure 1 export closed of record at 33 rows (1.1–1.8) with lane 8, and the plan's recorded next
substrates — "the P2/P3 spine sections beyond Pure 1" with the lane-6/7/8 P3 preview pools
(real-index binomial + power series from lane 6, the 32 lane-8 P3-integration routings) — make
**Pure 3 subtopic 3.1 Algebra** the natural lane 9. Target of record: `cie-a-level-maths-20-pure-3`,
spec points 3.1.1–3.1.6, verbatim from the repaired hub spine parse (the parse warning documents
`T-SPECS-CIE-PARSE-REPAIR-1`: official 2.1.1 was split into the 3.1.1 meaning/graph limb and the
3.1.2 relations limb, and official bullets 2–5 were recovered as 3.1.3–3.1.6 — codes authoritative,
no fold fragments needed). Operator order (trace `1a16f46476941295`): *"review+merge #357 then
proceed with lane 9"* — #357 verified merged of record before this build began.

## 2. Lane coverage — headline numbers

| measure | value |
|---|---|
| corpus screened | 855 resources / 25 stations |
| raw sweep hits → candidates | 97 → 90 (deduped across codes) |
| substrate (fresh resources) | 51 = 35 aligned + 16 non-overlap |
| aligned rows of record | 47 = 38 fresh rows + 9 cross-lane rows |
| cross-lane rows | 9 = 5 flips (r8427, r5245, r6295, r6340, r7477) + 4 one-to-many (r5362, r9523, r9082, r9701) |
| of-record candidates rejected with reasons | 30 |
| new text bodies (T-UGM-IMPORT-9) | 35 under `UGM-Resources/pure-3-algebra/` |
| corpus fleet | 479 → 514 files |

The lane-6/7/8 P3 preview pools land exactly where predicted: the lane-6 real-index binomial
non-overlaps (r6295, r6340, r7477) **flip** to 3.1.6 aligned; the fresh power-series pair
(r7436, r6601) sweeps in as the 3.1.6 substrate core.

## 3. Spec-point ↔ UGM resource map

### 3.1.1 — 5 rows, pick **absolutely**

> understand the meaning of | x |, sketch the graph of y = | ax + b | and use relations such as

- `absolutely` (Investigation, high) **PICK** — the modulus function scaffolded from its graph: the V-shape read as piecewise y=±x, 'this function is known as the modulus function. It is often written as |x|' — the canonical meaning-of-|x| task
- `piece-it-together` (Problem requiring decisions, medium) — Graph 2 is built from y=2x and y=−2x with 'another way you could describe it' as the modulus function y=|2x|; Taking it further writes the four cards' equations incl. modulus forms
- `inequalities` (Many ways problem, medium) **PICK** — Taking it further: solve |x+1|>2|x−1| by branch equations x+1=2(1−x) and x+1=2(x−1) over modulus graphs, and by squaring to (x+1)²=4(x−1)² — modulus graphs in inequality solving
- `r5362` (Review question, medium) (cross-lane one-to-many, body of record under UGM-Resources/pure-1-functions) — sketching f(x)=|x+[x]| over −3≤x≤3 exercises the modulus graph limb (|x+1| branches per unit interval); one-to-many on the lane-2 1.2.1/1.2.2/1.2.3 rows
- `r8427` (Review question, medium) (cross-lane flip, body of record under UGM-Resources/pure-1-functions) — parts (iii)–(iv): y=|(x−a)/x| sketched by reflecting the negative branches of y=(x−a)/x — the absolute-value graph transform is the tested step; flips the lane-2 non-overlap whose P1 limb was the rational sketch

### 3.1.2 — 2 rows, pick **inequalities**

> | a | = | b | ⇔ a² = b² and | x – a | < b ⇔ a – b < x < a + b when solving equations and inequalities

- `inequalities` (Many ways problem, medium) **PICK** — Taking it further: solve |x+1|>2|x−1| by branch equations x+1=2(1−x) and x+1=2(x−1) over modulus graphs, and by squaring to (x+1)²=4(x−1)² — modulus graphs in inequality solving
- `r9523` (Review question, medium) (cross-lane one-to-many, body of record under UGM-Resources/pure-1-functions) — statement 3 '|x+1|<1 ⟹ x<0' judged false — the |x−a|<b ⟺ a−b<x<a+b relation is exactly what the true/false test exercises; one-to-many on the lane-2 1.2.2 row

### 3.1.3 — 5 rows, pick **whats-left**

> divide a polynomial, of degree not exceeding 4, by a linear or quadratic polynomial, and identify the quotient and remainder (which may be zero)

- `whats-left` (Package of problems, high) **PICK** — quotient/remainder degree reasoning across eight divisions p(x)/d(x) incl. quadratic divisors, with worked algebraic division and the remainder-form generalisation
- `function-builder-ii` (Building blocks, medium) — algebraic long division of x²−5x+8 by x+1 (quotient x−6, remainder 14) identifies the behaviour of b(x)/a(x) for the graph-matching grid
- `r6317` (Review question, medium) — (4x−1)/(x+5) rewritten as 4−21/(x+5) by linear/linear division — the quotient-and-remainder form is load-bearing for the asymptote sketch and the following inequality
- `r5276` (Review question, high) — remainder of p_n(x)/p_{n−1}(x) by long division (Approach 1) and by the remainder theorem at the root of p_{n−1} (Approach 2); linear-by-linear division with quotient n/(n−1)
- `r6577` (Review question, high) **PICK** — remainder-theorem evaluations f(±2), factor theorem on the zero remainder → complete factorisation of the cubic, then exact divisibility by the quadratic x²+x−6 via its linear factors

### 3.1.4 — 22 rows, pick **r6577**

> use the factor theorem and the remainder theorem

- `r5276` (Review question, high) — remainder of p_n(x)/p_{n−1}(x) by long division (Approach 1) and by the remainder theorem at the root of p_{n−1} (Approach 2); linear-by-linear division with quotient n/(n−1)
- `r6577` (Review question, high) **PICK** — remainder-theorem evaluations f(±2), factor theorem on the zero remainder → complete factorisation of the cubic, then exact divisibility by the quadratic x²+x−6 via its linear factors
- `can-you-find-cubic-edition` (Many ways problem, high) — cubics built from root/touch conditions: 'if α is a root, x−α is a factor' used across all five parts incl. repeated-root touch cases and y-intercept constraints
- `how-not-to-solve-a-cubic` (Food for thought, medium) — common-root condition formalised by the factor theorem: f(k)=g(k)=0 ⟹ (x−k) divides both polynomials, forcing k∈{0,1} and the two families of shared-root cubics
- `r5032` (Review question, high) — factor-theorem proof that x−1 is a factor of x^m−1 for all positive integers m, powering the deduction that 26ⁿ ends in the same two digits
- `r5248` (Review question, high) — remainders 10, 3, 4 under x−1, x−2, x−3 recovered as f(1), f(2), f(3) by the remainder theorem, solving for a, b, c in the nested product form
- `r6299` (Review question, high) — factor theorem with a value table finds the root x=2 of x³−3x−2, then complete factorisation (x−2)(x+1)²; the reciprocal-curve sketch reads the double root
- `r6431` (Review question, medium) — rational-root search on 3x³+14x²+2x−4 (factor-theorem candidate testing) completes the cubic left by the squared surd equation
- `r6488` (Review question, high) — common factor x−2 evaluated at x=2 in both expressions (factor theorem → simultaneous equations); same remainder under x+a and x−2a from f(−a)=f(2a)
- `r6546` (Review question, medium) — show a+b+c is a factor of a³+b³+c³−3abc and find the other factor — the factor theorem with the c=−a−b substitution inside the AM-GM deduction
- `r6612` (Review question, medium) — sketch selection via the Factor Theorem: y=x³−x²−x+1=(x+1)(x−1)² cuts at −1 and touches at 1
- `r6790` (Review question, high) — remainder theorem MCQ: the remainder on dividing 1+3x+5x²+…+99x⁴⁹ by x−1 is p(1)=1+3+…+99, summed as an arithmetic progression
- `r7036` (Review question, high) — x²−1 is a factor iff the polynomial vanishes at x=±1 (factor theorem applied twice), with the parity case-split settling n=10/15
- `r7108` (Review question, high) — xⁿ+1 divisible by x+1 ⟺ (−1)ⁿ=−1 ⟺ n odd — a pure factor-theorem iff argument
- `r7243` (Review question, high) — x²+1 | (3+x⁴)ⁿ−(x²+3)ⁿ(x²−1)ⁿ resolved by the factor theorem on the composed polynomial f(x²) at x²=−1 (complex-root route noted)
- `r7991` (Review question, high) — (a−b) shown to be a factor of a³(b−c)+b³(c−a)+c³(a−b) by the factor theorem in a, then complete factorisation; part (i) uses the integer-index binomial only as technique
- `r8468` (Review question, high) — remainder theorem squared relation (a²−3)²=f(−a) reduced to 9a²+2a−7=0 and factorised
- `r8701` (Review question, high) — remainder theorem gives f(k)=k → cubic 2k³−3k+1=0 factorised by the factor theorem; the remainder under (x−1)(x−2) read from p=(x−1)(x−2)q(x)+Ax+B
- `r9006` (Review question, high) — small-integer root search by the factor theorem factorises x³−30x²+108x−104=(x−2)²(x−26) — repeated-root MCQ
- `r9330` (Review question, high) — f(−½)=0 and f(2)=0 (factor theorem) pin a and b; the quartic is factorised into three factors and the f(x)>0 set read from the signs
- `r5196` (Review question, medium) — f=(x−a)²g(x) ⟹ (x−a) divides f′(x) via the product rule; the two-equal-roots condition on x³−4x²−3x+p resolved through the factor theorem on f and f′
- `r9082` (Review question, medium) (cross-lane one-to-many, body of record under UGM-Resources/pure-1-differentiation) — repeated-root proof and the repeated root of 4x⁴+x²+3x+1 found via the factor theorem on f′ (16x³+2x+3); one-to-many on the lane-7 1.7.2 row

### 3.1.5 — 7 rows, pick **r7792**

> recall an appropriate form for expressing rational functions in partial fractions, and carry out the decomposition, in cases where the denominator is no more complicated than ( ax + b )( cx + d )( ex + f ), ( ax + b )( cx + d )², ( ax + b )( cx² + d )

- `frightening-function` (Food for thought, high) — telescoping via partial-fraction splitting of 1/((x−k)(x−k−1)) terms; Taking it further decomposes three denominators of the (ax+b)(cx+d) type
- `r7792` (Review question, high) **PICK** — Express 3x/((x−1)(x+2)) in partial fractions is asked outright (cover-up and coefficient comparison both shown), then used to differentiate and sketch the curve
- `r5126` (Review question, medium) — 1/(4−sin²x) decomposed as (1/4)(1/(2−sinx)+1/(2+sinx)) after u=sinx — an (ax+b)(cx+d)-type decomposition carried out inside the integral proof
- `r8694` (Review question, medium) — ∫√(x+1)/(x−3)dx via u²=x+1 reduces to polynomial division plus 8/((u−2)(u+2)) split by partial fractions
- `r8152` (Review question, medium) — case 3 density a²r/(a+r)³ integrated after the decomposition A+B/(1+t)+C/(1+t)²+D/(1+t)³ — the repeated-linear-factor (ax+b)(cx+d)² form of record
- `r5245` (Review question, high) (cross-lane flip, body of record under UGM-Resources/pure-1-series) — Express 2/(r²+4r+3) in partial fractions is asked as part (i) (A/(r+1)+B/(r+3) by equations and by the cover-up shortcut) before the telescoping sum; flips the lane-6 non-overlap whose P1 limb was the summation
- `r9701` (Review question, medium) (cross-lane one-to-many, body of record under UGM-Resources/pure-1-integration) — part (ii) ∫x/((x+1)(x+2)²)dx — a repeated-factor partial-fraction decomposition carried out in full; one-to-many on the lane-8 1.8.1 row

### 3.1.6 — 6 rows, pick **r7436**

> use the expansion of (1 + x)ⁿ, where n is a rational number and | x | < 1

- `r7436` (Review question, high) **PICK** — (1+x)^{3/2}+(1−2x)^{3/4} expanded to x³ by the real-index binomial series with the |x|<1 validity condition stated
- `r6601` (Review question, high) — (1+ax)^{−2} expanded by the |x|<1 binomial series to x³; the vanishing x-coefficient pins a=3/2 and the expansion is completed
- `from-parabolas-to-catenaries` (Package of problems, medium) — the arc-length integrand √(1+x²) expanded by the binomial series at index ½ inside the iterative catenary derivation (resource flagged draft-form on site)
- `r6295` (Review question, high) (cross-lane flip, body of record under UGM-Resources/pure-1-series) — n=1/2 and x=1/3 recognised from the given expansion of (1+x)ⁿ with the |x|<1 validity condition discussed — real-index binomial recognition; flips the lane-6 non-overlap (P1 1.6.1 covers positive-integer index only)
- `r6340` (Review question, high) (cross-lane flip, body of record under UGM-Resources/pure-1-series) — √((1+x)/(1−x)) ≈ 1+x+x²/2 via (1±x)^{±1/2}, then x=1/9 gives √5≈181/81 — real-index binomial approximation; flips the lane-6 non-overlap
- `r7477` (Review question, high) (cross-lane flip, body of record under UGM-Resources/pure-1-series) — (a±b)^{1/2} expansions valid for |b/a|<1 yield rational approximations to √5−√3 and √5+√3 — real-index binomial; flips the lane-6 non-overlap

## 4. Cross-lane joins — the preview pools realised

Five flips: the lane-6 non-overlaps r6295/r6340/r7477 (recorded there with explicit "P3 Series
bearing" reasons) and r5245 (its part (i) asks the decomposition outright) and the lane-2
non-overlap r8427 (parts (iii)–(iv) test the absolute-value graph transform) — each `flipOfPrior
NonOverlap: true` with the prior role retained. Four one-to-many joins: r5362 (+3.1.1) and r9523
(+3.1.2) on the lane-2 functions rows, r9082 (+3.1.4) on lane-7 1.7.2, r9701 (+3.1.5) on lane-8
1.8.1. All nine ride bodies of record (pure-1-functions / pure-1-series / pure-1-differentiation /
pure-1-integration) — **no new text** for cross-lane rows, the join law unchanged since #327.

## 5. Verdict honesty — the 3.1 boundary

Three verdict boundaries carried this lane, all recorded per-row: **(a) integer vs rational binomial
index** — thirteen positive-integer-index candidates of record under 1.6.1/1.7.1 are rejected for
3.1.6, which is the rational-index `|x| < 1` expansion (the lane-6 finding realised); **(b) squaring
is not modulus** — the surd/distance squaring pool (r5847, r7533, r8419, r9768, r8080, r5701, r7626,
r5365, apollonius…) stays out of 3.1.2; only modulus-notation squaring (the `inequalities` taking-
it-further and r9523's statement) carries the `|a| = |b| ⟺ a² = b²` relation; **(c) vector norms are
not scalar modulus** — r6449/r8456 rejected on notation. The 30 of-record rejections and 16 fresh
non-overlaps each carry their reason in `sweepRouting` / `nonOverlapRows`.

## 6. Corpus law for this lane

Bodies from `ugm-clean` through the byte-proven converter (pre-flight of record: **10/10 byte-identity
against the lane-8 of-record bodies**). Filenames `{ugm_id}-{title-slug}.md` under the majority slug
law (fitted 360/479 against the fleet; the of-record filename space is non-uniform — drift across the
lost lane builds — so filenames are cosmetic, `ugm_id` remains the only join key, consistent with the
importer). fm planes mirror lane 8 with `curriculum_code: CIE-9709-P3-2023`, `lane:`
`cie-a-level-maths-20-pure-3`, `task: T-UGM-IMPORT-9`. Candidate-model lane: the 16 fresh non-overlaps
are recorded **by reference only** (`bodyImported: false` in `nonOverlapRows`) — no text import for
resources whose tested skill sits outside the lane, the lane-8 law. `examProvenance` = acknowledgement
first line verbatim (lane-8 law; 42/59 records carry acknowledgements).

## 7. Primary picks of record

| code | pick | why |
|---|---|---|
| 3.1.1 | `absolutely` | the canonical modulus-meaning scaffolded task (piecewise |x| from the V-graph) |
| 3.1.2 | `inequalities` | the |x+1|>2|x−1| taking-it-further: branch equations and the squaring relation side by side |
| 3.1.3 | `whats-left` | the dedicated quotient/remainder-degree task incl. quadratic divisors |
| 3.1.4 | `r6577` | remainder theorem + complete factorisation + quadratic-divisor divisibility in one canonical arc |
| 3.1.5 | `r7792` | the decomposition asked outright and then used (derivative + sketch) |
| 3.1.6 | `r7436` | the purest real-index expansion task with the |x|<1 condition stated |

## 8. Next hops by spine adjacency

Pure 3 continues in syllabus order: **3.2 Logarithmic and exponential functions** (3.2.1–3.2.4) is
the natural lane 10 — the UGM exp-and-log station substrate is essentially untouched (lane-5 strays
excepted) and this lane's `to-log-or-not-to-log` + `powerful-derivatives` non-overlaps already carry
3.2 bearings. Downstream: 3.3 Trigonometry (the lane-5 P3-2.3 finding), 3.4 Differentiation and
3.5 Integration (the lane-7/8 technique pools + 32 lane-8 P3-integration routings await). The hub
consume (T-UGM-HUB-CONSUME-9) opens the pure-3 bundle plane — a separate operator order after this
PR merges.
