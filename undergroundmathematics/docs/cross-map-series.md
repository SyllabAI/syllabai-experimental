# Cross-map lane 6: UGM sequences + counting-and-binomials stations → CIE 9709 Pure 1 Series

**Status**: lane 6 of the P3c generalisation (operator instruction **“lane 6 (CIE 9709 P1 1.6 Series)”**; per §8 of `cross-map-trigonometry.md` and `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-23 · machine-readable twin: `resources/derived/cross-map-series.json`

## 1. What this is

Lanes 1–5 mapped the Quadratics, Combining Functions, Geometry-of-Equations + Circles, the circular-measure strand and the two trigonometry stations onto CIE 9709 Pure 1 subtopics 1.1–1.5; lane 5 §8 pre-identified this lane's substrate: *“1.6 Series (`sequences` + `counting-and-binomials` stations)”*. The operator now directs exactly that lane. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.6 Series**, carried by the hub spine parse as **four rows** — 1.6.1 through 1.6.4 — with **no fold fragments** (no `a`-suffix rows exist, so no fold decision is required).

**Station-lane scope (lanes 1–3/5 shape).** UGM has two dedicated series stations — **Sequences** (42 resources) and **Counting and Binomials** (51 resources) — so this is a full-station lane: the substrate is all 93 station resources, plus a corpus-wide sweep of all 25 stations for series content (arithmetic/geometric progression, common difference/ratio, sum to infinity, convergence, binomial, Pascal, factorial, recurrence, nth-term/sum patterns) so that cross-station strays whose tested skill is 1.6.x are caught and everything else is routed to its recorded home — never forced (AGENT.md rule 3). The two dedicated stations plus the six stray-home stations (chain-rule, thinking-about-algebra, divisibility-and-induction, exp-and-log, introducing-calculus, product-rule) give a multi-station lane in the lane-5 shape.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| Corpus screened | 855 resources (25 stations) |
| Sweep candidates verdicted | 137 |
| Substrate resources considered | 93 (42 + 51 across the two series stations) |
| Aligned to CIE 9709 P1 1.6.x | 49 resources / 56 alignment rows — 43 substrate + 6 cross-station strays |
| Explicit non-overlap notes | 50 (11 Sequences + 39 Counting-and-Binomials) |
| Cross-lane fact joins (already-of-record bodies) | 2 (r7553, r9527 — lane-2 text untouched) |
| Routed to recorded home with reason | 36 |
| Aligned resources with provenance tuple (S1 bridge) | 43 of 49 |
| Hub content-map attachment | zero course items attached to any 1.6.x spec point (zero 1.6 references among the content map's 1,728 items of record) — spec-point/lane-level attachment, as in every lane |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** — every candidate resolved: aligned, non-overlap-noted, cross-lane-joined, or routed with a recorded reason; substrate alignedShare 0.46 (43/93) reflects the counting-and-binomials station's honest combinatorics/logic verdict (§5) |

Station facts of record (P3b enrichment sheets): Sequences — 42 resources; Counting and Binomials — 51 resources. Of-record item attachment: **zero course items are attached to any 1.6.x spec point in the hub content map of record** (the map's 1,728 items carry no 1.6 references; the lane-5-era `uncoveredSpineCodeList` field has since been regenerated into the `spcptUnmapped`/internal-id schema). The UGM enrichment therefore attaches at spec-point/lane level, as in every lane so far. Text import law (station-lane corpus law, lane-3/5 shape): the lane's res dir `pure-1-series/` carries the **whole substrate's text of record — 99 files**: the 49 aligned resources (43 substrate + 6 strays) MAPPED, plus the 50 non-overlaps imported UNMAPPED with the coverage note (their recorded homes live in the enrichment's `nonOverlapRows`; 3 of the 99 are excerpt/title-only captures per the of-record bigger-picture/teacher-support law). No mapping is manufactured for the unmapped files (AGENT.md rule 3).

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **working texts** of the of-record spine rows; the CIE spec parse carries known text artifacts (interleaved example text) — codes are authoritative, and the machine twin plus the imported front-matter carry each row's **verbatim** parse title.

### 1.6.1 — use the expansion of (a + b)^n, where n is a positive integer

13 UGM resources (primary pick **r7078** ⭐; stations: Chain Rule + Counting and Binomials + Thinking About Algebra):

- [review-question] Can we find the coefficient of $x^2$ in $(5 + 4x)(1 - x/2)^{10}$? (`r7078`, counting-and-binomials, confidence high, modes 1,4) ⭐
- [review-question] Can we find the minimum value of $x^2+2/x$ for $x$ positive? (`r5640`, chain-rule, confidence medium, modes 1)
- [review-question] Which power of $x$ has the greatest coefficient? (`r5563`, counting-and-binomials, confidence high, modes 1)
- [review-question] What is the coefficient of $x^3y^5$ in the expansion of  $(1+xy+y^2)^n$? (`r5965`, counting-and-binomials, confidence high, modes 1)
- [review-question] Can we prove these four binomial coefficient identities? (`r6102`, counting-and-binomials, confidence high, modes 1)
- [review-question] Can we estimate a difference of eighth powers? (`r6503`, counting-and-binomials, confidence high, modes 1)
- [review-question] Can we find an inequality from the expansion of $[ 1+1/\sqrt{n}]^n$? (`r6770`, counting-and-binomials, confidence medium, modes 1)
- [review-question] Can we find an approximation to $(1.0099)^6$? (`r7489`, counting-and-binomials, confidence high, modes 1)
- [review-question] Can we use a binomial expansion to evaluate $\left(19\tfrac{3}{4}\right)^6$? (`r7978`, counting-and-binomials, confidence high, modes 1)
- [review-question] Can we show $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-2}{r-1}+\binom{n-3}{r-1}+\dotsb+\binom{r-1}{r-1}$? (`r8014`, counting-and-binomials, confidence medium, modes 1)
- [review-question] Can we find the coefficients of $x^{−12}$ and $x^2$ in this expansion? (`r9207`, counting-and-binomials, confidence high, modes 1)
- [review-question] If $x - 1/x = u$, what's $x^3 - 1/x^3$? (`r9928`, counting-and-binomials, confidence medium, modes 1)
- [review-question] Can we factorise  $(x+y)^6 - (x-y)^6$ completely? (`r9404`, thinking-about-algebra, confidence medium, modes 1)

### 1.6.2 — recognise arithmetic and geometric progressions

3 UGM resources (primary pick **sort-it-out** ⭐; stations: Sequences):

- [building-blocks] Sort it out (`sort-it-out`, sequences, confidence high, modes 1,4) ⭐
- [package-of-problems] Common terms (`common-terms`, sequences, confidence high, modes 1)
- [food-for-thought] Connect three? (`connect-three`, sequences, confidence medium, modes 1)

### 1.6.3 — use the formulae for the nth term and for the sum of the first n terms to solve problems involving arithmetic or geometric progressions

26 UGM resources (primary pick **r8907** ⭐; stations: Counting and Binomials + Divisibility And Induction + Exp And Log + Introducing Calculus + Sequences):

- [review-question] If an AP has $S_{10}=3S_5$, what's the ratio of $u_{10}$ to $u_5$? (`r8907`, sequences, confidence high, modes 1,4) ⭐
- [review-question] If $f(n) > k$ for all $n \geq 1$, what can we say about $k$? (`r7031`, counting-and-binomials, confidence medium, modes 1)
- [review-question] What's the next number to occur in both sequences? (`r9916`, divisibility-and-induction, confidence medium, modes 1)
- [review-question] Can we solve the equation $\log_2 x + \log_3 x = 1 + \log_4 x$? (`r8260`, exp-and-log, confidence medium, modes 1)
- [review-question] Can we use the trapezium rule to estimate this integral? (`r6592`, introducing-calculus, confidence medium, modes 1)
- [rich-example] Change one thing (`change-one-thing`, sequences, confidence high, modes 1)
- [package-of-problems] Common terms (`common-terms`, sequences, confidence high, modes 1)
- [review-question] If AP terms $a_4,a_8, a_{16}$ are in GP, are $a_3, a_6, a_{12}$ in GP too? (`r5345`, sequences, confidence high, modes 1)
- [review-question] Can we find the sum of the integers from $2k$ to $4k$ inclusive? (`r5849`, sequences, confidence high, modes 1)
- [review-question] How are the $p$th, $q$th and $r$th terms of an AP related? (`r6137`, sequences, confidence high, modes 1)
- [review-question] If $u_n = a + bn + c2^n$, what's the sum of the first $n$ terms? (`r6153`, sequences, confidence medium, modes 1)
- [review-question] Can we sum the first $2n$ terms of $1,1,2,\frac{1}{2},4,\frac{1}{4},8,\frac{1}{8},..$? (`r6257`, sequences, confidence high, modes 1)
- [review-question] What can we say if $a, x_1, x_2, x_3, x_4, x_5, b$ are in arithmetic progression? (`r6405`, sequences, confidence high, modes 1)
- [review-question] If a GP has $S_n=(3^n - 2^n)/2^{n-5}$, what's its common ratio? (`r6608`, sequences, confidence high, modes 1)
- [review-question] If $27$, $x$, $y$ are in GP, with sum $21$, what are $x$ and $y$? (`r7258`, sequences, confidence high, modes 1)
- [review-question] Can we sum from $1000$ to $2000$ excluding multiples of 5? (`r7424`, sequences, confidence high, modes 1)
- [review-question] When does the sum of this series first exceed $2999/4000$? (`r7487`, sequences, confidence high, modes 1)
- [review-question] When does the sum of this series equal $60$? (`r8121`, sequences, confidence high, modes 1)
- [review-question] If $S_n =  6 - 2^{n+1}/3^{n-1}$, can we show that we have a GP? (`r8163`, sequences, confidence high, modes 1)
- [review-question] What is the sum of the multiples of 5 or 8 but not both? (`r8249`, sequences, confidence high, modes 1)
- [review-question] How are the sums of $n$, $2n$ and $3n$ terms connected here? (`r8493`, sequences, confidence high, modes 1)
- [review-question] What are the first term and common ratio given two facts about this geometric progression? (`r9177`, sequences, confidence high, modes 1)
- [review-question] Should I hire a TV or borrow to buy it? (`r9375`, sequences, confidence high, modes 1)
- [review-question] What can we tell about the signs of this arithmetic sequence? (`r9468`, sequences, confidence high, modes 1)
- [review-question] Given $S_n = S_{3n}$, can we express $a$ in terms of $n$? (`r9613`, sequences, confidence high, modes 1)
- [review-question] Can we sum $1^2-2^2+3^2-4^2+\dotsb+ (2n-1)^2-(2n)^2$? (`r9819`, sequences, confidence medium, modes 1)

### 1.6.4 — use the condition for the convergence of a geometric progression, and the formula for the sum to infinity of a convergent geometric progression

14 UGM resources (primary pick **square-spirals** ⭐; stations: Product Rule + Sequences):

- [food-for-thought] Square spirals (`square-spirals`, sequences, confidence high, modes 1,4) ⭐
- [review-question] Can we find the area between $y=e^{-x}$ and $y=e^{-x}\sin x$? (`r9312`, product-rule, confidence medium, modes 1)
- [rich-example] Bouncing to nothing (`bouncing-to-nothing`, sequences, confidence medium, modes 1)
- [many-ways-problem] Can you find... series edition (`can-you-find-series-edition`, sequences, confidence medium, modes 1)
- [go-and-think-about-it] A puzzling pentagon (`puzzling-pentagon`, sequences, confidence medium, modes 1)
- [review-question] Can we find the sum of the integers from $2k$ to $4k$ inclusive? (`r5849`, sequences, confidence high, modes 1)
- [review-question] What can we say if $a, x_1, x_2, x_3, x_4, x_5, b$ are in arithmetic progression? (`r6405`, sequences, confidence high, modes 1)
- [review-question] Can we sum from $1000$ to $2000$ excluding multiples of 5? (`r7424`, sequences, confidence high, modes 1)
- [review-question] When does the sum of this series first exceed $2999/4000$? (`r7487`, sequences, confidence high, modes 1)
- [review-question] Given the sequence $(x_n)$, what is  $\sum_{k=0}^\infty 1/x_k$? (`r8248`, sequences, confidence medium, modes 1)
- [review-question] How are the sums of $n$, $2n$ and $3n$ terms connected here? (`r8493`, sequences, confidence high, modes 1)
- [review-question] How do we add the odd-numbered terms of a geometric series? (`r8617`, sequences, confidence high, modes 1)
- [review-question] What are the first term and common ratio given two facts about this geometric progression? (`r9177`, sequences, confidence high, modes 1)
- [review-question] When does $1 + 2/3 + (2/3)^2 + \dotsb$ first exceed $0.9999S_\infty$? (`r9185`, sequences, confidence high, modes 1)

## 4. Full alignment table

| Resource | Station | Type | Codes | Confidence | Evidence |
|---|---|---|---|---|---|
| Can we find the minimum value of $x^2+2/x$ for $x$ positive? (`r5640`) | chain-rule | review-question | 1.6.1 | medium | part 1 is the binomial expansion: coefficient of x^7 in (x^2+2/x)^8 (parts 2-3 are calculus — 1.7/1.8 bearings recorded in the cross-map) |
| Which power of $x$ has the greatest coefficient? (`r5563`) | counting-and-binomials | review-question | 1.6.1 | high | greatest-coefficient comparison for (1+1/2 x)^10 via c_{k+1}/c_k or direct ℒ₂ evaluation |
| What is the coefficient of $x^3y^5$ in the expansion of  $(1+xy+y^2)^n$? (`r5965`) | counting-and-binomials | review-question | 1.6.1 | high | coefficient of x^3 y^5 in (1+xy+y^2)^n by writing (1+y(x+y))^n and applying the binomial expansion twice |
| Can we prove these four binomial coefficient identities? (`r6102`) | counting-and-binomials | review-question | 1.6.1 | high | binomial-coefficient identities (ΣC=2^n, kΣ, ΣC/(k+1), k²Σ) proved by substituting x=1/x=-1-style values into (1+x)^n |
| Can we estimate a difference of eighth powers? (`r6503`) | counting-and-binomials | review-question | 1.6.1 | high | expand (1+x)^8, then evaluate (1.001)^8-(0.999)^8 by combining the (1±x)^8 expansions — canonical numerical binomial question |
| Can we find an inequality from the expansion of $[ 1+1/\sqrt{n}]^n$? (`r6770`) | counting-and-binomials | review-question | 1.6.1 | medium | first three terms of [1+1/√n]^n truncated to prove an inequality — extension-level application of the expansion |
| If $f(n) > k$ for all $n \geq 1$, what can we say about $k$? (`r7031`) | counting-and-binomials | review-question | 1.6.3 | medium | worst case at n=1 then arithmetic-series sum 2+3+⋯+101 = 100(2+101)/2 = 5150 — the AP sum is the load-bearing computation in a STEP-style MC |
| Can we find the coefficient of $x^2$ in $(5 + 4x)(1 - x/2)^{10}$? (`r7078`) ⭐ | counting-and-binomials | review-question | 1.6.1 | high | first four terms of (1-x/2)^10 then coefficient of x^2 in (5+4x)(1-x/2)^10 — the canonical CIE P1 binomial question |
| Can we find an approximation to $(1.0099)^6$? (`r7489`) | counting-and-binomials | review-question | 1.6.1 | high | expand (1+p)^6, substitute p=x-x^2, then choose x to evaluate (1.0099)^6 — expansion with substitution and numerical use |
| Can we use a binomial expansion to evaluate $\left(19\tfrac{3}{4}\right)^6$? (`r7978`) | counting-and-binomials | review-question | 1.6.1 | high | expand (x-y)^6 by the binomial theorem and evaluate (19 3/4)^6 to the nearest thousand — canonical (a-b)^n numerical question |
| Can we show $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-2}{r-1}+\binom{n-3}{r-1}+\dotsb+\binom{r-1}{r-1}$? (`r8014`) | counting-and-binomials | review-question | 1.6.1 | medium | ΣC(n,r)=2^n, Vandermonde-style ℒ(2n,n) identity and the hockey-stick identity — binomial-theorem identities with combinatorial proofs |
| Can we find the coefficients of $x^{−12}$ and $x^2$ in this expansion? (`r9207`) | counting-and-binomials | review-question | 1.6.1 | high | coefficients of x^-12 and x^2 in (x^4-1/x^2)^5 (x-1/x)^6 by expanding both brackets — binomial expansion with negative powers of the variable |
| If $x - 1/x = u$, what's $x^3 - 1/x^3$? (`r9928`) | counting-and-binomials | review-question | 1.6.1 | medium | x^3-1/x^3 and x^5-1/x^5 in terms of u=x-1/x by expanding (x-1/x)^3 and (x-1/x)^5 with the binomial theorem |
| What's the next number to occur in both sequences? (`r9916`) | divisibility-and-induction | review-question | 1.6.3 | medium | common term of two APs via nth-term forms 2005+7j and 2005+9k (LCM structure) |
| Can we solve the equation $\log_2 x + \log_3 x = 1 + \log_4 x$? (`r8260`) | exp-and-log | review-question | 1.6.3 | medium | part 1 proves the GP-term log identity via a = AR^{p-1} (part 2 is a log-change-of-base equation — exp-and-log bearing) |
| Can we use the trapezium rule to estimate this integral? (`r6592`) | introducing-calculus | review-question | 1.6.3 | medium | the trapezium-rule MC resolves by summing the GP 2^{1/N}+...+2^{(N-1)/N} — the GP sum formula is the decisive step |
| Can we find the area between $y=e^{-x}$ and $y=e^{-x}\sin x$? (`r9312`) | product-rule | review-question | 1.6.4 | medium | ΣA_n for the e^{-x}/e^{-x}sin x areas closes as a GP sum to infinity (integration is the vehicle) |
| Bouncing to nothing (`bouncing-to-nothing`) | sequences | rich-example | 1.6.4 | medium | bouncing ball: heights ×3/4 each bounce — total distance before stopping is a GP sum to infinity (mechanics context, suvat as vehicle) |
| Can you find... series edition (`can-you-find-series-edition`) | sequences | many-ways-problem | 1.6.4 | medium | construct infinite series meeting constraints — the GP convergence condition -1<r<1 is the central tool (general-series extensions recorded honestly) |
| Change one thing (`change-one-thing`) | sequences | rich-example | 1.6.3 | high | last term of the AP 3, 3.5, 4, ... with 25 terms, solved several ways — a_n = a_1+(n-1)d consolidation (acknowledged capture) |
| Common terms (`common-terms`) | sequences | package-of-problems | 1.6.2, 1.6.3 | high | construct an AP and a GP sharing u_2=6, u_4=54 — d=(54-6)/2=24 vs r^2=9; nth-term formulae of both progressions load-bearing |
| Connect three? (`connect-three`) | sequences | food-for-thought | 1.6.2 | medium | find an arithmetic progression containing any three given numbers — AP structure recognition and construction |
| A puzzling pentagon (`puzzling-pentagon`) | sequences | go-and-think-about-it | 1.6.4 | medium | puzzling pentagon interactive — provider description: created with geometric series in mind (nested-pentagon GP sum); excerpt capture, no question well |
| If AP terms $a_4,a_8, a_{16}$ are in GP, are $a_3, a_6, a_{12}$ in GP too? (`r5345`) | sequences | review-question | 1.6.3 | high | a_4, a_8, a_16 of an AP are consecutive GP terms; show a_3, a_6, a_12 too — nth-term formulae of AP and GP interplay |
| Can we find the sum of the integers from $2k$ to $4k$ inclusive? (`r5849`) | sequences | review-question | 1.6.3, 1.6.4 | high | sums over 2k..4k; prove the GP sum formula a(1-r^n)/(1-r); recurring decimal 0.075075... as an infinite GP — AP sum + GP sum + sum to infinity |
| How are the $p$th, $q$th and $r$th terms of an AP related? (`r6137`) | sequences | review-question | 1.6.3 | high | P(q-r)+Q(r-p)+R(p-q)=0 for AP terms and the log analogue for GP terms — nth-term formulae of both progressions |
| If $u_n = a + bn + c2^n$, what's the sum of the first $n$ terms? (`r6153`) | sequences | review-question | 1.6.3 | medium | u_n = a+bn+c 2^n summed over n terms — the sum splits into an AP part (a n + b Σk) and a GP part (c Σ2^k); both 1.6.3 formulae load-bearing |
| Can we sum the first $2n$ terms of $1,1,2,\frac{1}{2},4,\frac{1}{4},8,\frac{1}{8},..$? (`r6257`) | sequences | review-question | 1.6.3 | high | sum of first 2n terms of 1,1,2,1/2,4,1/4,... by separating the two interleaved GPs — GP sum formula twice |
| What can we say if $a, x_1, x_2, x_3, x_4, x_5, b$ are in arithmetic progression? (`r6405`) | sequences | review-question | 1.6.3, 1.6.4 | high | seven terms in AP; a,x_2,b in GP; then GP series with \|r\|<1 — express r via S_n, S_∞ and prove S_{2n}=S_n(2S-S_n)/S |
| If a GP has $S_n=(3^n - 2^n)/2^{n-5}$, what's its common ratio? (`r6608`) | sequences | review-question | 1.6.3 | high | S_n=(3^n-2^n)/2^{n-5} — find first term and common ratio — canonical GP-sum-formula problem |
| If $27$, $x$, $y$ are in GP, with sum $21$, what are $x$ and $y$? (`r7258`) | sequences | review-question | 1.6.3 | high | 27, x, y in GP with sum 21 — common-ratio quadratic with two solution pairs |
| Can we sum from $1000$ to $2000$ excluding multiples of 5? (`r7424`) | sequences | review-question | 1.6.3, 1.6.4 | high | prove the AP range-sum formula, sum 1000..2000 excluding multiples of 5; GP r=0.95 least n with S-S_n<1 |
| When does the sum of this series first exceed $2999/4000$? (`r7487`) | sequences | review-question | 1.6.3, 1.6.4 | high | sum of 1/2+1/6+1/18+... (formula must be proved), sum to infinity, least n exceeding 2999/4000 |
| When does the sum of this series equal $60$? (`r8121`) | sequences | review-question | 1.6.3 | high | recognise 3/n^3+4/n^3+...+(n^3-3)/n^3 as an AP and solve for n — AP recognition + sum formula |
| If $S_n =  6 - 2^{n+1}/3^{n-1}$, can we show that we have a GP? (`r8163`) | sequences | review-question | 1.6.3 | high | S_n = 6 - 2^{n+1}/3^{n-1} — show the series is geometric; state a and r — canonical S_n-to-GP question |
| Given the sequence $(x_n)$, what is  $\sum_{k=0}^\infty 1/x_k$? (`r8248`) | sequences | review-question | 1.6.4 | medium | recursion x_n=Σx_k gives x_n=2^{n-1}; Σ1/x_k closes by the GP sum to infinity — one-to-many extension of 1.6.4 inside a recursion question |
| What is the sum of the multiples of 5 or 8 but not both? (`r8249`) | sequences | review-question | 1.6.3 | high | sum of multiples of 5 or 8 but not both up to 1000 — three AP-sum applications with inclusion-exclusion |
| How are the sums of $n$, $2n$ and $3n$ terms connected here? (`r8493`) | sequences | review-question | 1.6.3, 1.6.4 | high | S_3=3(S_2-S_1) for an AP; sum of 1+3x/(1+2x^2)+... and the \|r\|<1 condition for a sum to infinity |
| How do we add the odd-numbered terms of a geometric series? (`r8617`) | sequences | review-question | 1.6.4 | high | GP sum to infinity 8; odd-numbered terms sum to infinity 6 — find r — canonical S_∞ work |
| If an AP has $S_{10}=3S_5$, what's the ratio of $u_{10}$ to $u_5$? (`r8907`) ⭐ | sequences | review-question | 1.6.3 | high | S_10=3S_5 gives a=3d; ratio u_10/u_5=12/7; then S_200 from u_5=0.14 — S_n and u_n formulae together |
| What are the first term and common ratio given two facts about this geometric progression? (`r9177`) | sequences | review-question | 1.6.3, 1.6.4 | high | GP with a exceeds second term by 2, u_2+u_3=4/3 — two (a,r) pairs; positive-terms branch summed to infinity |
| When does $1 + 2/3 + (2/3)^2 + \dotsb$ first exceed $0.9999S_\infty$? (`r9185`) | sequences | review-question | 1.6.4 | high | least number of terms of 1+2/3+(2/3)^2+... exceeding 99.99% of S_∞ — convergence + remainder |
| Should I hire a TV or borrow to buy it? (`r9375`) | sequences | review-question | 1.6.3 | high | TV-hire payments form a GP (r=4/5) — total over 8 years vs compound-interest debt — applied GP modelling |
| What can we tell about the signs of this arithmetic sequence? (`r9468`) | sequences | review-question | 1.6.3 | high | S_8>3S_6 — deduce the signs of a and d from the AP sum formula — formula-driven reasoning MC |
| Given $S_n = S_{3n}$, can we express $a$ in terms of $n$? (`r9613`) | sequences | review-question | 1.6.3 | high | S_n=S_3n with d=-1 — express a in terms of n — clean AP-sum-formula algebra |
| Can we sum $1^2-2^2+3^2-4^2+\dotsb+ (2n-1)^2-(2n)^2$? (`r9819`) | sequences | review-question | 1.6.3 | medium | prove the AP sum formula by Gauss pairing, then apply to alternating squares — formula derivation plus non-AP application |
| Sort it out (`sort-it-out`) ⭐ | sequences | building-blocks | 1.6.2 | high | sort a deck of infinite sequences into self-chosen groups — builds the AP/GP classification from properties (increasing, arithmetic, geometric) |
| Square spirals (`square-spirals`) ⭐ | sequences | food-for-thought | 1.6.4 | high | square spirals: shaded fractions 1/4+1/16+1/64+... — a visual infinite GP sum (Introducing level) |
| Can we factorise  $(x+y)^6 - (x-y)^6$ completely? (`r9404`) | thinking-about-algebra | review-question | 1.6.1 | medium | all three solution routes run through binomial expansions of (x±y)^6 (factorisation is the wrapper) |

## 5. Non-overlaps, boundary cases and sweep routing (never forced)

**50 recorded non-overlaps** (imported UNMAPPED with the coverage note):

- `line-crossings` (counting-and-binomials): Combinatorial line-arrangement reasoning (C(n,2) context only) — no binomial expansion or AP/GP formula work.
- `r5157` (counting-and-binomials): Truth-teller/liar deduction puzzle — no series content.
- `r5212` (counting-and-binomials): Digit-counting on calendar dates — combinatorial case analysis, no binomial expansion or AP/GP formulae.
- `r5245` (counting-and-binomials): Telescoping sum via partial fractions — standard-sum series work outside P1 1.6 (the 2023-2025 Pure 1 spec has no standard summations).
- `r5246` (counting-and-binomials): Standard sums Σr, Σr², Σr³ — outside P1 1.6 (no standard summations in the 2023-2025 Pure 1 spec).
- `r5344` (counting-and-binomials): Truth-teller/liar deduction puzzle — no series content.
- `r5512` (counting-and-binomials): Hat-colour epistemic deduction puzzle — no series content.
- `r5848` (counting-and-binomials): Venn-diagram inclusion-exclusion with averages — set enumeration, no series content.
- `r5875` (counting-and-binomials): Recursive function summed by block-doubling structure — recursion work, not AP/GP formulae.
- `r6093` (counting-and-binomials): Truth-teller/liar deduction puzzle — no series content.
- `r6295` (counting-and-binomials): General-index binomial expansion (n = 1/2, x = -1/3) — P3 Series bearing: the infinite binomial series is not the positive-integer expansion of P1 1.6.1.
- `r6340` (counting-and-binomials): Real-index binomial approximation ((1±x)^{±1/2}) — P3 Series bearing; P1 1.6.1 covers positive integer n only.
- `r6463` (counting-and-binomials): Saint/liar circular-arrangement counting — logic and case analysis, no series content.
- `r6707` (counting-and-binomials): Venn-diagram inclusion-exclusion — set enumeration, no series content.
- `r6970` (counting-and-binomials): Tile-match combinatorics (Post-correspondence-style) — constructive reasoning, no series content.
- `r6993` (counting-and-binomials): Counter-example reasoning about integer products — proof skills, no series content.
- `r7059` (counting-and-binomials): Modular-sum game strategy — combinatorial game reasoning, no series content.
- `r7397` (counting-and-binomials): Grid-tour existence arguments — parity/graph reasoning, no series content.
- `r7399` (counting-and-binomials): Digit-sum counting via table structure — combinatorial enumeration; the Σ1..9 step is incidental arithmetic, not AP-formula testing.
- `r7477` (counting-and-binomials): Real-index binomial approximation ((a±b)^{1/2}) — P3 Series bearing; positive-integer expansion only in P1 1.6.1.
- `r7507` (counting-and-binomials): Recursive function evaluation and recursion depth — recursion, no series content.
- `r7878` (counting-and-binomials): Combinatorial game (HT-2) with pattern avoidance — no series content.
- `r7906` (counting-and-binomials): Recursive-function counting via factorisations — enumeration, no series content.
- `r8021` (counting-and-binomials): Combinatorial selection with C(n,k) counts — no expansion tested; P1 1.6.1 is the binomial expansion, not selection counting.
- `r8033` (counting-and-binomials): Pell-equation solution sequences via recurrence — number-theory iteration, not AP/GP.
- `r8168` (counting-and-binomials): Piecewise-recursive function evaluation — enumeration, no series content.
- `r8203` (counting-and-binomials): Robot-program recursion (powers of two) — recursive structure, not AP/GP formulae.
- `r8279` (counting-and-binomials): Liar/switcher/truth-teller deduction — logic puzzle, no series content.
- `r8605` (counting-and-binomials): Highest-power bookkeeping in nested polynomials — degree arithmetic, no series content.
- `r8691` (counting-and-binomials): Liar/truth-teller/random deduction — logic puzzle, no series content.
- `r9059` (counting-and-binomials): Oxflip row/column-flip game — parity/invariant reasoning, no series content.
- `r9323` (counting-and-binomials): Permutation counting and probability — combinatorics, no series content.
- `r9341` (counting-and-binomials): Arrangements with indistinguishable objects + probability — combinatorics, no expansion.
- `r9473` (counting-and-binomials): Cubic-formula sequence monotonicity via a quadratic inequality — the sequence is polynomial, not an AP/GP; skill is inequality solving.
- `r9664` (counting-and-binomials): Fibonacci-style pebble-row recurrence — recurrence relations are outside P1 1.6.
- `r9749` (counting-and-binomials): Mixed-doubles pairing count — combinatorics, no series content.
- `r9750` (counting-and-binomials): Formal-word production rules — constructive reasoning, no series content.
- `r9800` (counting-and-binomials): Square-number criterion via index parity — number theory, no series content.
- `r9884` (counting-and-binomials): Recurrence-derived quadratic sequence with ΣH_i = n³ proof — recurrence-to-closed-form work; the Σ(1..n-1) AP-sum is a tool, not the tested skill.
- `achilles-and-the-tortoise` (sequences): Zeno's-paradox bigger-picture excerpt on general infinite series — P1 1.6.4 covers convergence of geometric progressions only; excerpt capture.
- `r5416` (sequences): Alternating squares sum by bracketing — standard-sum series work outside P1 1.6.
- `r5602` (sequences): Integral bounds on the harmonic series — calculus estimation, not AP/GP formulae.
- `r5995` (sequences): Iterated reciprocal-function cycle — functional iteration, not progressions.
- `r6143` (sequences): Derivation of Σr² and Σr³ — standard sums outside P1 1.6.
- `r6555` (sequences): Recurrence-defined sequences with quadratic closed forms — recurrence work; the AP-sum appears as a tool only.
- `r7240` (sequences): Bracketed-integer pattern proof with Σn given as an assumption — pattern/proof work; the AP formula is not the tested skill.
- `r8404` (sequences): Iterative rational bounds for √2 — convergence of a non-GP iteration, outside P1 1.6.
- `r8998` (sequences): Alternating ±n partial sums — pairing argument, not AP/GP formulae.
- `same-different` (sequences): Sigma-notation equivalence on quadratic sums — general series manipulation outside P1 1.6.
- `sum-estimating` (sequences): Integral estimates of Σr² — calculus-summation links, outside P1 1.6.

**Boundary cases recorded honestly (not forced):** the general-index binomial questions (r6295, r6340, r7477) are recorded as non-overlaps with P3 Series bearings — the infinite binomial series is not the positive-integer expansion of P1 1.6.1; the power-series station's r7436/r6601 are routed with the same P3 bearing, which remains the natural substrate preview for a future P3 lane (mirroring lane 5's P3 2.3 finding for compound angles). Load-bearing sub-step alignments (r7031 AP sum inside a STEP-style MC; r8248/r9312 GP sums to infinity inside recursion/integration questions; r6592 GP sum inside a trapezium-rule MC) are aligned at **medium** confidence with the wrapper skill named; r9884/r6555 stay non-overlaps because the recurrence construct dominates their tested skill.

**Sweep routing (36):**

- `r7692` → 1.7/1.8 Calculus (gradient of x^n via binomial-chord expansion; the expansion is scaffolding)
- `r5348` → 1.7 Differentiation (derivatives of powers via binomial-chord patterns)
- `r6276` → Polynomials/root-coefficients (roots constrained to an AP/GP are modelling wrappers; skill is symmetric functions)
- `r7111` → Polynomials/root-coefficients (roots in GP are a modelling wrapper; skill is symmetric functions)
- `r5634` → P3 Series bearings (series to n terms by induction/partial fractions + log-series sum to infinity)
- `r8499` → Combinatorial recurrence (stairs/Fibonacci counting) — outside P1 1.6
- `r6099` → Exp-and-log fluency (log n! manipulation; factorial notation without expansion)
- `r7436` → P3 Series (real-index binomial expansion)
- `r6601` → P3 Series (real-index binomial expansion with validity condition)
- `r5162` → Thinking-about-geometry (many-ways geometry problem; keyword false positive)
- `r6509` → 1.7 Differentiation (mapping diagrams; binomial mention false positive)
- `r6920` → 1.7 Differentiation (zooming-in gradients; cross-reference false positive)
- `r9701` → 1.8 Integration (rationalisation; (1+x)-pattern false positive)
- `r5053` → 1.3 Coordinate geometry (normals to a parabola; AP false positive)
- `r9045` → 1.3 Circles (loci; AP false positive)
- `r9768` → 1.3 Circles (loci; AP false positive)
- `r6735` → 1.2 Functions (inverse meeting points; (1+x) false positive)
- `r5973` → 1.2 Functions (invertibles building block; (1+x) false positive)
- `r8880` → Number theory (divisibility; (1+x)-pattern false positive)
- `r7688` → Number fluency (factorial fun) — factorial arithmetic without expansion
- `r6234` → 1.3 Geometry of equations (point on a circle; AP false positive)
- `r5202` → 1.3 Geometry of equations (perpendicular foot; AP false positive)
- `r7696` → P3/Hyperbolic functions (catenaries; binomial mention false positive)
- `r8994` → Hyperbolic functions food-for-thought (weight pulling; AP false positive)
- `r7991` → Polynomials (cyclic factorisation; binomial false positive)
- `r9189` → Polynomials (quartic roots; recurrence false positive)
- `r6790` → Polynomials (remainder theorem; AP false positive)
- `r5276` → Polynomials (remainder of p_n by p_{n-1}; AP false positive)
- `r9484` → 1.7 Curve sketching (e^{-x}/(1+x^2); (1+x) false positive)
- `r7533` → 1.1 Quadratics (inequality with square roots; (1+x) false positive)
- `r7604` → 1.5 Trigonometry (of record, lane 5; the (1+2c)^3 expansion step is incidental)
- `r5795` → 1.5 Trigonometry (of record, lane 5; AP false positive)
- `r6589` → 1.5 Trigonometry (of record, lane 5; AP false positive)
- `r6079` → 1.5 Trigonometry (of record, lane 5; common-difference false positive)
- `r8704` → Vectors (parallelogram; AP false positive)
- `r7285` → Vectors (collinearity; AP false positive)

## 6. Primary picks of record

- **1.6.1 → `r7078`** (Can we find the coefficient of x² in (5 + 4x)(1 − x/2)¹⁰?) — the canonical CIE P1 binomial question: expansion with a linear substitution then coefficient extraction.
- **1.6.2 → `sort-it-out`** (Sort it out) — Introducing-level classification of sequences; students build their own AP/GP recognition criteria.
- **1.6.3 → `r8907`** (If an AP has S₁₀ = 3S₅, what's the ratio of u₁₀ to u₅?) — uses BOTH the Sₙ and uₙ formulae of record in one clean question.
- **1.6.4 → `square-spirals`** (Square spirals) — Introducing-level visual infinite GP sum; the sum-to-infinity construct without formal prerequisites.

## 7. S1 provenance bridge status for this lane

43 of the 49 aligned resources carry a provenance tuple of record (board/qualification/paper/year/questions/permission) from the P3b review-question-provenance sweep (`resources/derived/review-question-provenance.json`); the tuples ride the enrichment rows and the imported front-matter `exam_reference` fields. The remainder are UGM originals or captures without board metadata — recorded as null, never invented.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record + served** — enrichment #55, text #58 (main@91eed732), hub #308 (merged).
- Lane 2 (functions, 1.2.1–1.2.5): **of record + served** — enrichment + text #61 (a32c6c0f, MANIFEST v2), hub #312 (merged).
- Lane 3 (coordinate geometry, 1.3.1–1.3.2 with fragments folded): **of record + served** — cross-map @ cb947595, enrichment + text #66 (MANIFEST v3), hub #321 (merged).
- Lane 4 (circular measure, 1.4.1 with 1.4.1a folded — first strand lane): **of record + served** — cross-map @ b52cf1bf, corpus #74 → `1585c4ff` (MANIFEST v4), hub #327 → `2684a8e4` (cross-lane join law established).
- Lane 5 (trigonometry, 1.5.1–1.5.5 — first two-station lane): **of record + served** — cross-map @ f3ef5745, corpus #79 → `cf79ecd2` (MANIFEST v5), hub #330 → `16bef479` (merged 2026-10-23).
- **Lane 6 (this lane, 1.6.1–1.6.4, two-station lane)**: cross-map of record here; corpus + enrichment filed as `T-UGM-MODE1-6` / `T-UGM-IMPORT-6` (MANIFEST v6, branch `ugm/pure-1-series`); hub consumption awaits operator order as `T-UGM-HUB-CONSUME-6` on the syllabai-v2 side — the importer's lane-6 block is a 2+6-station lane block (expected census: 99 files / 56 rows / 43 aligned / 50 non-overlap) plus **two cross-lane fact joins** (r7553, r9527 → 1.6.3 against existing lane-2 bodies), reusing the lane-4/-5 join law unchanged.
- Next hops by spine adjacency: **1.7 Differentiation** (the calculus stations — where of-record item attachment is densest: 51 + 14 parts — and where lanes 4–6 routed pools already hold a large preview substrate), then 1.8 Integration; the power-series station's real-index binomial pool (r7436/r6601 + recorded non-overlaps here) is the natural substrate preview for a future P3 Series lane, mirroring lane 5's P3 2.3 finding.

Corpus sweep provenance: candidates from the keyword sweep over `resources/ugm-clean/*` (arithmetic/geometric progression, common difference/ratio, sum to infinity, convergence, binomial, Pascal, factorial, recurrence, nth-term and sum-of-first-n patterns; 855 resources screened, 2026-10-23); verdicts read against question wells and solutions; machine-readable twin `resources/derived/cross-map-series.json`.
