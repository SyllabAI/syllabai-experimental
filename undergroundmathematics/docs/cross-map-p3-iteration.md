# Cross-map lane 14: the UGM numerical-methods plane → CIE 9709 Pure 3, 3.6 Numerical solution of equations

## 1. What this is

Of-record verdicts for lane 14 of the P3c generalisation programme: every UGM candidate bearing on CIE 9709 Pure 3 subtopic **3.6 Numerical solution of equations** (spec points 3.6.1–3.6.3, the verbatim spine rows of record — parse artifacts disclosed, no fold fragments) is closed here: **11 aligned rows** (3 fresh bodies — the lane's new text of record — plus 1 cross-course flip and 7 one-to-many joins by reference), **1 non-overlap** recorded with a companion disclosure, and **36 of-record candidates rejected because their prior alignments/rows stand**. Operator order: *"review+merge #377 then 'lane 14'"* (trace `1a174f2cc1265e79`); lane-14 identity named of record by the lane-13 findings (*"Lane-14 = 3.6 Numerical iteration (3.6.1–3.6.3 verbatim spine rows await)"*).

## 2. Lane coverage — headline numbers

| | |
|---|---|
| corpus screened | 855 resources / 25 stations |
| sweep | 48 candidates of record (tight pass-2 iteration/sign-change/convergence regex + pass-1 title/description + four targeted angle patterns — decimal-places+root, rearrangement-form, trial-and-improvement, fixed-point, x=g(x), successive-approximations; dossier read against well AND solution). NO pre-baked bearing pool this lane — no prior lane routed rows to 'P3 3.6' |
| aligned rows | **11** = 3 fresh bodies + 1 cross-course flip (r8404 — the circular-slice precedent: rides its lane-6 whole-station body under `pure-1-series/`, whose `spec_points` were `[]` unmapped-by-design) + 7 one-to-many joins |
| cross-lane joins | **7 one-to-many** beside standing alignments: r8231 (1.7.3), r8679 (3.5.1 — the lane-13 pick body), r7549 (1.3.2), r5948 (1.3.1/1.3.2), to-log-or-not-to-log (3.2.3), see-the-power (3.2.1), r9082 (1.7.2/3.1.4) |
| fresh non-overlaps | **1 by reference** (`bodyImported: false`) — staircase-sequences-revisited, the companion disclosure |
| of-record candidates rejected | **36 with reasons** — every one aligned or non-overlapping of record elsewhere |

Primary picks of record: **r8711 (3.6.1, fresh)** / **r8404 (3.6.2 — rides its lane-6 body, the r6018 fresh-pick-impossible convention, disclosed)** / **r8231 (3.6.3 — rides its lane-3 body, disclosed)**. No honest gap this lane: every spec point carries rows.

## 3. Per-spec-point detail

### 3.6.1 — locate approximately a root of an equation, by means of graphical considerations and/or searching for a sign change

Spine title verbatim (parse artifacts carried — no fold fragments). 8 aligned row(s), pick `r8711`:

- `r8013` (exp-and-log, Review question, high) — The well demands the graph then 'Use your graph to find the roots of the equation 3^x=3x+2'; the solution reads both intersections off the plot to two decimal places (x=-0.48 and x=1.83, checked against the exact -0.4673.../1.8344...) - locating roots by graphical considerations, 3.6.1 verbatim. Supersedes its stale lane-3-logarithmic-and-exponential-functions non-overlap row of record.
- `r8711` (polynomials, Review question, high) **[pick]** — The purest sign-change search in the corpus: the solution tabulates f(x) across x=-2..6, reads three sign changes bracketing three real roots ('one between x=-2 and x=-1; one between 1 and 2; a third between 5 and 6'), then hones the negative root between -1.3 and -1.2 (f(-1.25)=0.671875>0) to conclude x=-1.3 to one decimal place - locating a root by searching for a sign change and refining the bracket, the verbatim 3.6.1 skill.
- `r5948` (geometry-of-equations, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — The well derives the chord-intercept approximation (af(b) - bf(a))/(f(b) - f(a)) from the sign-bracketed interval f(a) < 0 < f(b) and applies it to x^2 + x^(1/2) - 37 = 0 ('find two consecutive integers between which a root lies... calculate an approximation to the root, giving three significant figures') - locating a root by a graphical/linear-interpolation consideration between two sign-change bounds (the method r8679's survey names 'linear interpolation'), riding the standing 1.3.1/1.3.2 alignments of record.
- `r7549` (circles, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — 'Find the positive root of the equation correct to one decimal place': the solution reads ~1.4 off the sketch (graphical consideration), tabulates f(1.3)/f(1.4)/f(1.5), and applies the continuity + sign-change law ('As there is a sign change and the function is continuous, the root we seek must fall between 1.3 and 1.4'), refined by trial and improvement to 1.4 - riding the standing 1.3.2 alignment of record.
- `r8231` (calculus-of-powers, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — Method 1 is trial-and-improvement interval refinement to three decimal places; Method 3 is the Newton-Raphson iteration in x_{n+1} notation ('x_{n+1} = x_n - f(x_n)/f'(x_n)', here x_{n+1} = x_n - (x^3+3x^2-3)/(3x^2+6x)); and the uniqueness argument ('since the curve is continuous... it must cut the x-axis somewhere between x=0 and x=1') is sign-change reasoning - 3.6.1 and 3.6.3 ride beside the standing 1.7.3 alignment of record.
- `r9082` (product-rule, Review question, medium) (ONE-TO-MANY — rides the body of record under ``;  stands) — Locating the repeated root via f': 'f'(x) must have a root between -1 and 0, since f'(x) is continuous and we have a change of sign. The value -1/2 is a sensible choice to test' - sign-change root location used as the instrument bounding the double root, beside the standing 1.7.2/3.1.4 alignments of record (medium: instrumental step, not the target skill).
- `see-the-power` (exp-and-log, Building blocks, medium) (ONE-TO-MANY — rides the body of record under ``;  stands) — The solution bounds x between 1.25 and 1.5 and narrows the bracket ('We could narrow this range by trial and improvement or by plotting a graph') before the exact digit-counting logarithms take over - interval-search root location beside the standing 3.2.1 alignment (medium: instrumental, subordinate to the log-law purpose).
- `to-log-or-not-to-log` (exp-and-log, Problem requiring decisions, medium) (ONE-TO-MANY — rides the body of record under ``;  stands) — The solution confronts 5^x = x^5 ('This is another example of an equation we don't know how to solve exactly. We could use a numerical method such as trial and improvement to find an approximate solution. Most numerical methods work best if you know roughly where the solution is. A sketch... might help') - the locate-approximately stance of 3.6.1 inside the standing 3.2.3 alignment (medium: the numerical method is advised, not executed to an answer).

### 3.6.2 — understand the idea of, and use the notation for, a sequence of approximations which converges to a root of an equation

Spine title verbatim (parse artifacts carried — no fold fragments). 3 aligned row(s), pick `r8404`:

- `r8404` (sequences, Review question, high) **[pick]** (FLIP — rides the body of record under ``; supersedes the stale non-overlap row) — The solution names the machinery verbatim ('Thus we have in action here the x = g(x) iteration, or the rearrangement method, where we start with f(x) = 0, and move to x = g(x)'), proves the alternating bracketing of sqrt(2) by consecutive terms, establishes the error decay |x_{n+1}^2 - 2| = |x_n^2 - 2|/(x_n+1)^2 < |x_n^2 - 2|, and drives the iteration to prescribed accuracy (41/29 and 99/70 differing from sqrt(2) by less than 5x10^-4) - the 3.6.2 sequence-of-approximations notation and the 3.6.3 iteration-based-on-a-rearrangement to a prescribed degree of accuracy. FLIP: rides its lane-6 whole-station body under UGM-Resources/pure-1-series (spec_points [] — unmapped-by-design under rule 3); supersedes its stale lane-1-series non-overlap row of record (the circular-slice precedent).
- `staircase-sequences` (thinking-about-numbers, Investigation, high) — The solution sets up the self-similar fixed point ('If I call that x... x seems to reappear inside itself: x = 1 + 1/x'), rearranges to x^2 - x - 1 = 0 and identifies the limit as its positive root (1+sqrt(5))/2, with the term table (1, 2, 1.5, 1.666..., 1.6, 1.625, ...) a convergent sequence of approximations observed to alternate either side of the root - the 3.6.2 idea and the 3.6.3 relation between x = F(x) and the equation being solved, in an exploratory register.
- `r8679` (calculus-trig-log, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — The solution surveys the numerical canon verbatim ('decimal search, binary search, linear interpolation, the rearrangement method or simply zooming in with graphing software') and executes Newton-Raphson from the given first approximation 1.5 to the second approximation 1.43 (3 sf) with a substitution check - the first/second-approximation language of 3.6.2 and a given-iteration application to prescribed accuracy under 3.6.3, riding the fresh lane-13 3.5.1 pick body.

### 3.6.3 — understand how a given simple iterative formula of the form x = F( x ) relates to the equation being solved, and use a given iteration, or an iteration based on a given rearrangement of an equation, to determine a root to a prescribed degree of accuracy.

Spine title verbatim (parse artifacts carried — no fold fragments). 4 aligned row(s), pick `r8231`:

- `r8404` (sequences, Review question, high) **[pick]** (FLIP — rides the body of record under ``; supersedes the stale non-overlap row) — The solution names the machinery verbatim ('Thus we have in action here the x = g(x) iteration, or the rearrangement method, where we start with f(x) = 0, and move to x = g(x)'), proves the alternating bracketing of sqrt(2) by consecutive terms, establishes the error decay |x_{n+1}^2 - 2| = |x_n^2 - 2|/(x_n+1)^2 < |x_n^2 - 2|, and drives the iteration to prescribed accuracy (41/29 and 99/70 differing from sqrt(2) by less than 5x10^-4) - the 3.6.2 sequence-of-approximations notation and the 3.6.3 iteration-based-on-a-rearrangement to a prescribed degree of accuracy. FLIP: rides its lane-6 whole-station body under UGM-Resources/pure-1-series (spec_points [] — unmapped-by-design under rule 3); supersedes its stale lane-1-series non-overlap row of record (the circular-slice precedent).
- `staircase-sequences` (thinking-about-numbers, Investigation, high) — The solution sets up the self-similar fixed point ('If I call that x... x seems to reappear inside itself: x = 1 + 1/x'), rearranges to x^2 - x - 1 = 0 and identifies the limit as its positive root (1+sqrt(5))/2, with the term table (1, 2, 1.5, 1.666..., 1.6, 1.625, ...) a convergent sequence of approximations observed to alternate either side of the root - the 3.6.2 idea and the 3.6.3 relation between x = F(x) and the equation being solved, in an exploratory register.
- `r8231` (calculus-of-powers, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — Method 1 is trial-and-improvement interval refinement to three decimal places; Method 3 is the Newton-Raphson iteration in x_{n+1} notation ('x_{n+1} = x_n - f(x_n)/f'(x_n)', here x_{n+1} = x_n - (x^3+3x^2-3)/(3x^2+6x)); and the uniqueness argument ('since the curve is continuous... it must cut the x-axis somewhere between x=0 and x=1') is sign-change reasoning - 3.6.1 and 3.6.3 ride beside the standing 1.7.3 alignment of record.
- `r8679` (calculus-trig-log, Review question, high) (ONE-TO-MANY — rides the body of record under ``;  stands) — The solution surveys the numerical canon verbatim ('decimal search, binary search, linear interpolation, the rearrangement method or simply zooming in with graphing software') and executes Newton-Raphson from the given first approximation 1.5 to the second approximation 1.43 (3 sf) with a substitution check - the first/second-approximation language of 3.6.2 and a given-iteration application to prescribed accuracy under 3.6.3, riding the fresh lane-13 3.5.1 pick body.

## 4. Cross-lane joins of record

| slug | kind | codes | prior of record | text of record under |
|---|---|---|---|---|
| `r8404` | flip | 3.6.2,3.6.3 | lane-1-series non-overlap row of record (the whole-station body of record lives under pure-1-series with spec_points [] — unmapped-by-design under rule 3) | `UGM-Resources/pure-1-series` |
| `r5948` | one_to_many | 3.6.1 | lane-coordinate-geometry alignments 1.3.1/1.3.2 of record (the line-geometry derivation) | `UGM-Resources/pure-1-coordinate-geometry` |
| `r7549` | one_to_many | 3.6.1 | lane-coordinate-geometry alignment 1.3.2 of record | `UGM-Resources/pure-1-coordinate-geometry` |
| `r8231` | one_to_many | 3.6.1,3.6.3 | lane-pure-1-differentiation alignment 1.7.3 of record (the cubic root-approximation body) | `UGM-Resources/pure-1-differentiation` |
| `r8679` | one_to_many | 3.6.2,3.6.3 | lane-13 alignment 3.5.1 of record (the fresh pick body under pure-3-integration) | `UGM-Resources/pure-3-integration` |
| `r9082` | one_to_many | 3.6.1 | lane-algebra alignment 3.1.4 of record (the repeated-root row; the 1.7.2 alignment of the same body stands beside it) | `UGM-Resources/pure-1-differentiation` |
| `see-the-power` | one_to_many | 3.6.1 | lane-log-exp alignment 3.2.1 of record | `UGM-Resources/pure-3-logarithmic-and-exponential-functions` |
| `to-log-or-not-to-log` | one_to_many | 3.6.1 | lane-log-exp alignment 3.2.3 of record | `UGM-Resources/pure-3-logarithmic-and-exponential-functions` |

## 5. Non-overlap closure of record

| slug | routedTo | reason |
|---|---|---|
| `staircase-sequences-revisited` | P3 3.6.2 companion disclosure (the convergents of the golden-ratio and sqrt(3) continued fractions are sequences of increasingly accurate rational approximations to roots of x^2 - x - 1 = 0 and x^2 = 3, and the sqrt(3) expansion is a self-similarity rearrangement) | The resource's centre of gravity is continued-fraction REPRESENTATION (which numbers admit which expansions), not iteration toward a root to prescribed accuracy; the approximation-sequence idea appears as prose inherited from its companion Staircase sequences (aligned here at 3.6.2/3.6.3) and the solutions never iterate numerically nor use x_n notation - the 3.6.2 content of record is carried by the companion; no fresh alignment manufactured |

## 6. Supersede disclosures of record

Per the to-log-or-not-to-log law: every promotion below SUPERSEDES the stale non-overlap row(s) of record named against it.

| slug | verdict | stale row(s) of record |
|---|---|---|
| `r8013` | aligned 3.6.1 | — |
| `r8404` | aligned 3.6.2,3.6.3 (flip) | — |

## 7. Sweep closures — standing rows

The 36 rejected candidates carry their prior of-record treatment: 19 aligned elsewhere (the alignment stands), 17 non-overlapping of record or fresh (the row/absence stands). Every closure verified against the well AND solution of record; the full table lives in `sweepRouting` of the JSON.

## 8. The verdict-reading catches of record

- **r8404's flip**: the dossier read showed the lane-6 body carrying `spec_points: []` ('no CIE P1 spec point asserted — coverage is never manufactured') while the resource is the corpus's REARRANGEMENT-METHOD showcase ('the x = g(x) iteration, or the rearrangement method' — verbatim) → the circular-slice flip law applies, not a fresh body.
- **the Newton-noise class**: seven resources hit the sweep on 'Newton' via Newton's LAWS (mechanics) or the history piece — all rejected with reasons; 'staircase' surfaces only in the staircase-sequences pun.
- **r9082's instrumentality**: the sign-change step locates the root of f′ to bound the repeated root — a genuine 3.6.1 embodiment at medium confidence, joined beside the standing 1.7.2/3.1.4 alignments.
- **the counting-vs-locating line**: r6653 and r9754 determine solution COUNTS graphically and then solve exactly — 3.6.1 requires LOCATING approximately; both rejected.

## 9. Next hops

The pure-3 spine's remaining SUBTOPIC rows after 3.6: 3.7/3.8/3.9 (the spine's SUB3.7–SUB3.9 rows of record name them — vectors and beyond). Lane 15 inherits the usual next-pointer discipline.
