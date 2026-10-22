# Cross-map pilot: UGM quadratics → CIE 9709 Pure 1 Quadratics

**Status**: pilot for operator review (P3c in `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-22 · machine-readable twin: `resources/derived/cross-map-quadratics.json`

## 1. What this is

The quadratics station is UGM's richest (59 resources, 41 review questions). This pilot maps every UGM quadratics resource onto the SyllabAI of-record spine **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.1 Quadratics** (spec points 1.1.1–1.1.5), with confidence, mode flags (§1 of the integration plan) and provenance highlights. A contrast export for CIE IGCSE 0580 Extended (2025–2027) quadratics-bearing spec points is in `resources/derived/spine-export/cie-igcse-maths-25-extended.json`.

Method: each UGM resource was aligned by reading its question well / task statement against the spec-point wording of the of-record spine export (`resources/derived/spine-export/cie-a-level-maths-20-pure-1.json`). Alignments are one-to-many (a resource may serve two spec points); never forced — non-overlaps are explicit.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| UGM quadratics resources mapped | 59 |
| Aligned to ≥1 CIE 9709 P1 spec point | 56 (95%) |
| Explicit non-overlap notes | 3 |
| Resources with provenance tuple (S1 bridge) | 46 (41 exam-board + 5 NRICH) |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** |

Attachment-context finding: in the current of-record content map (`syllabai-v2/apps/hub/content-maps/cie-a-level-maths-20-pure-1.json`), only 10 items are attached to 1.1.x (2 notes per spec point) out of 1,728 course items — item attachment is still sparse lane-wide. The UGM enrichment therefore attaches at **spec-point / lane level** (facts + links), which is independent of item-attachment progress.

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **verbatim from the of-record spine export**; the CIE spec parse carries known text artifacts (e.g. interleaved example text) — codes are authoritative.

### 1.1.1 — carry out the process of completing the square for a quadratic polynomial ax + bx + c and use y a completed sq

8 UGM resources:
- [review-question] For what values of $k$ is $x^2 + 6kx +144$ always positive? (`r6526`, confidence high)
- [review-question] Given the minimum point, what's this parabola's equation? (`r6756`, confidence high)
- [review-question] If $7 - px - x^2 = 16 - (q + x)^2$, what are $p$ and $q$? (`r9724`, confidence high)
- [package-of-problems] Name that graph (`name-that-graph`, confidence high)
- [package-of-problems] Paired parabolas (`paired-parabolas`, confidence medium)
- [package-of-problems] Quadratic symmetry (`quad-symmetry`, confidence high)
- [package-of-problems] Which parabola? (`which-parabola`, confidence high)
- [building-blocks] Which quadratic? (`which-quadratic`, confidence high)

### 1.1.2 — find the discriminant of a quadratic polynomial ax + bx + c and use the discriminant ‘repeated root’ is includ

12 UGM resources:
- [review-question] Can we show $(b^2 - 2ac)x^2 + 4(a + c)x = 8$ always has real roots? (`r8812`, confidence high)
- [package-of-problems] Discriminating (`discriminating`, confidence high)
- [resource-in-action] Discriminating - teacher support (`discriminating-teacher-support`, confidence high)
- [review-question] For what values of $k$ is $x^2 + 6kx +144$ always positive? (`r6526`, confidence high)
- [review-question] When are the coefficients of a quadratic equal to its roots? (`r7350`, confidence medium)
- [review-question] When are the roots for $x^2-bx+c=0$ real and positive? (`r5138`, confidence high)
- [review-question] When do these simultaneous equations have no real solutions? (`r9658`, confidence high)
- [review-question] When does $(p+1)x^2+4px+9=0$ have a repeated root? (`r7455`, confidence high)
- [review-question] When does $x^2 + ax + a = 1$ have distinct real roots? (`r9659`, confidence high)
- [review-question] When does $x^2+(3k-7)x+(2k+6)=0$ have real roots? (`r6828`, confidence high)
- [review-question] When does $x^2-4x-1=2k(x-5)$ have equal roots? (`r5316`, confidence high)
- [review-question] Where does $y = px^2 + 8x + p - 6$ cross the $x$-axis? (`r9742`, confidence high)

### 1.1.3 — solve quadratic equations, and quadratic By factorising, completing the square and using the inequalities, in 

20 UGM resources:
- [review-question] Can we find both roots if one is double the other? (`r6638`, confidence high)
- [review-question] Can we fit a quadratic to this given data? (`r8775`, confidence medium)
- [review-question] Can we prove this inequality involving two square roots? (`r7533`, confidence medium)
- [review-question] Can we solve $12/(x-3) < x+1$? (`r7035`, confidence high)
- [review-question] Can we solve $nx^2+2x\sqrt{pn^2+q}+rn+s=0$? (`r6246`, confidence high)
- [package-of-problems] Factorisable quadratics (`factorisable-quads`, confidence high)
- [package-of-problems] GeoGebra constructions... quadratic edition (`geogebra-constructions-quadratic`, confidence medium)
- [review-question] How do we increase the roots of a quadratic equation by $1$? (`r6712`, confidence medium)
- [review-question] If we know two values satisfying a quadratic, can we find the quadratic? (`r7972`, confidence medium)
- [fluency-exercise] Inequalities for some occasions (`inequalities-for-some-occasions`, confidence high)
- [review-question] Into how many regions do these parabolas divide the plane? (`r8781`, confidence medium)
- [package-of-problems] Irrational roots (`irrational-roots`, confidence high)
- [fluency-exercise] Pick a card... (`pick-a-card`, confidence high)
- [scaffolded-task] Proving the quadratic formula (`proving-quad-formula`, confidence medium)
- [rich-example] Quadratic grids (`quadratic-grids`, confidence medium)
- [fluency-exercise] Quadratic solving sorter (`quad-solving-sorter`, confidence high)
- [review-question] When are these quadratic inequalities true together? (`r9989`, confidence high)
- [review-question] When is $12x^2+7x-10$ negative? (`r5059`, confidence high)
- [review-question] Where does $y = px^2 + 8x + p - 6$ cross the $x$-axis? (`r9742`, confidence high)
- [building-blocks] Which quadratic? (`which-quadratic`, confidence high)

### 1.1.4 — solve by substitution a pair of simultaneous e.g. equations of which one is linear and one is 2 quadratic

10 UGM resources:
- [review-question] Can we find the midpoint of a chord of this parabola? (`r8045`, confidence high)
- [review-question] Can we find the tangents to a circle from a point? (`r6804`, confidence medium)
- [review-question] Can we solve these simultaneous equations, both of degree two? (`r7520`, confidence medium)
- [review-question] Can we solve these simultaneous equations, one linear, one quadratic? (`r6429`, confidence high)
- [review-question] Given two simultaneous equations of degree two, can we solve them? (`r7588`, confidence medium)
- [review-question] Into how many regions do these parabolas divide the plane? (`r8781`, confidence medium)
- [review-question] When do these simultaneous equations have no real solutions? (`r9658`, confidence high)
- [review-question] When does $y=kx$ intersect the parabola $y=(x-1)^2$? (`r9614`, confidence high)
- [review-question] When does $y=mx-5$ intersect $y=x^2-1$  twice? (`r5287`, confidence high)
- [review-question] When is this line a tangent to this parabola? (`r7328`, confidence high)

### 1.1.5 — recognise and solve equations in x which are quadratic in some function of x . tan

11 UGM resources:
- [review-question] Can we solve $\sqrt{3-3x} - \sqrt{2-x} = 1$? (`r7485`, confidence high)
- [review-question] Can we solve the simultaneous equations $x + y + \sqrt{xy} = 39$ and $x^2 + y^2 + xy = 741$? (`r5682`, confidence high)
- [review-question] Can we solve these simultaneous equations that involve reciprocals? (`r8128`, confidence medium)
- [review-question] Can we solve this inequality with three square roots? (`r6387`, confidence medium)
- [review-question] How do we  solve $x + 3\sqrt{x} − 1/2 = 0$? (`r6215`, confidence high)
- [review-question] How do we solve an equation containing three square roots? (`r5847`, confidence medium)
- [review-question] If $2y = a^x + a^{-x}$, can we find $a^x$? (`r6816`, confidence high)
- [food-for-thought] Powerful quadratics (`powerful-quads`, confidence medium)
- [review-question] What does the curve $x^4-y^2=y+1$ look like? (`r8855`, confidence medium)
- [review-question] When can this equation involving algebraic fractions hold? (`r8407`, confidence medium)
- [review-question] When does $x^4=(x-c)^2$ have four real roots? (`r9546`, confidence high)

## 4. Full alignment table

| UGM resource | Type | CIE P1 spec point(s) | Conf | Modes | Provenance | Note |
|---|---|---|---|---|---|---|
| Can we find both roots if one is double the other? | review-question | 1.1.3 | high | 1,2 | UCLES 1985 Q1 | Roots related by an integer factor; factorise or use root relationships. |
| Can we find the midpoint of a chord of this parabola | review-question | 1.1.4 | high | 1,2 | UCLES 1982 Q13 | Chord of a parabola: line meets curve, then midpoint (coordinate-geometry flavour). |
| Can we find the tangents to a circle from a point? | review-question | 1.1.4 | medium | 1 | UCLES 1964 Q2 | Tangents from a point to a circle — sits with P1 coordinate geometry (1.3); tangency via discriminant is the shared skill. |
| Can we fit a quadratic to this given data? | review-question | 1.1.3 | medium | 1,2 | UCLES 1967 Q1 | Form a quadratic from given data/conditions. |
| Can we prove this inequality involving two square ro | review-question | 1.1.3 | medium | 1 | UCLES 1981 Q6(i) | Inequality proof with two square roots — beyond routine, but discriminant/sign reasoning. |
| Can we show $(b^2 - 2ac)x^2 + 4(a + c)x = 8$ always  | review-question | 1.1.2 | high | 1,2 | UCLES 1980 Q12(b) | Show a quadratic always has real roots — discriminant condition. |
| Can we solve $12/(x-3) < x+1$? | review-question | 1.1.3 | high | 1,2 | UCLES 1980 Q2 | Rational inequality reduces to a quadratic inequality (critical values). |
| Can we solve $nx^2+2x\sqrt{pn^2+q}+rn+s=0$? | review-question | 1.1.3 | high | 1 | UCLES 1999 Q2 | Quadratic formula with literal coefficients. |
| Can we solve $\sqrt{3-3x} - \sqrt{2-x} = 1$? | review-question | 1.1.5 | high | 1,2 | UCLES 1979 Q1 | Surds equation squared down to a quadratic. |
| Can we solve the simultaneous equations $x + y + \sq | review-question | 1.1.5 | high | 1 | UCLES 1981 Q4(a) | Substitution u = sqrt(xy) makes the simultaneous system a hidden quadratic. |
| Can we solve these simultaneous equations that invol | review-question | 1.1.5 | medium | 1 | UCLES 1975 Q2a | Reciprocal simultaneous equations; hidden quadratic in 1/x and 1/y. |
| Can we solve these simultaneous equations, both of d | review-question | 1.1.4 | medium | 1 | UCLES 1980 Q2(b) | Both equations degree two — extends the P1 linear+quadratic case (1.1.4). |
| Can we solve these simultaneous equations, one linea | review-question | 1.1.4 | high | 1,2 | UCLES 1983 Q5 | Canonical linear+quadratic simultaneous system. |
| Can we solve this inequality with three square roots | review-question | 1.1.5 | medium | 1 | UCLES 1958 Q3(i) | Three-square-root inequality — extension of 1.1.3/1.1.5 techniques. |
| Discriminating | package-of-problems | 1.1.2 | high | 1,2,4 |  | MUST/MAY/CAN'T discriminant family; teacher support available (pattern exemplar). |
| Discriminating - teacher support | resource-in-action | 1.1.2 | high | 1 |  | Teacher-support sibling of "discriminating" (opportunities-for-learning table). |
| Factorisable quadratics | package-of-problems | 1.1.3 | high | 1,2,4 |  | Fluency family on factorisable quadratics. |
| For what values of $k$ is $x^2 + 6kx +144$ always po | review-question | 1.1.2, 1.1.1 | high | 1,2 | UCLES 1981 Q12(b) | Always-positive quadratic: discriminant + completing the square. |
| GeoGebra constructions... quadratic edition | package-of-problems | 1.1.3 | medium | 1 |  | Dynamic constructions of parabola properties; supports sketching (1.1.3/1.2). |
| Given the minimum point, what's this parabola's equa | review-question | 1.1.1 | high | 1,2 | UCLES 1958 Q2(i) | Equation of a parabola from its minimum point — vertex form. |
| Given two simultaneous equations of degree two, can  | review-question | 1.1.4 | medium | 1 | UCLES 2010 Q1 | Two quadratics simultaneously — extension of 1.1.4. |
| How do we  solve $x + 3\sqrt{x} − 1/2 = 0$? | review-question | 1.1.5 | high | 1,2 | UCLES 2013 Q1 | Canonical hidden quadratic: x + 3sqrt(x) - 1/2 = 0. |
| How do we increase the roots of a quadratic equation | review-question | 1.1.3 | medium | 1 | UCLES 1962 Q7(i) | Shift roots by 1: substitution y = x - 1, expansion and comparison. |
| How do we solve an equation containing three square  | review-question | 1.1.5 | medium | 1 | UCLES 1970 Q5(ii) | Three square roots; squaring chain reduces to a quadratic. |
| How fast are these particles sliding when they pass? | review-question | — | — | — | UCLES 1974 Q1 | NON-OVERLAP for P1 pure lane: kinematics context (particles sliding); the underlying quadratic solving is 1.1.3. |
| If $2y = a^x + a^{-x}$, can we find $a^x$? | review-question | 1.1.5 | high | 1,2 | UCLES 1973 Q2 | Hidden quadratic in a^x; then a^{-x} read off reciprocally. |
| If $7 - px - x^2 = 16 - (q + x)^2$, what are $p$ and | review-question | 1.1.1 | high | 1,2 | UCLES 1980 Q13 | Identity comparison after completing the square. |
| If we know two values satisfying a quadratic, can we | review-question | 1.1.3 | medium | 1 | O&C (Oxford & Cambridge SEG) 1972  | Reconstruct a quadratic from two known values. |
| Inequalities for some occasions | fluency-exercise | 1.1.3 | high | 1,2 |  | Quadratic-inequality fluency exercise. |
| Into how many regions do these parabolas divide the  | review-question | 1.1.4, 1.1.3 | medium | 1 | Oxford (MAT) Specimen 2 Q1J | Regions bounded by parabolas; line-parabola positions + inequalities. |
| Irrational roots | package-of-problems | 1.1.3 | high | 1,2 |  | Surd roots via formula; surd manipulation in root conditions. |
| Name that graph | package-of-problems | 1.1.1 | high | 1,2,4 |  | Match parabola equations to graphs (vertex form, translations). |
| Paired parabolas | package-of-problems | 1.1.1 | medium | 1,2 |  | Vertex/axis reasoning across parabola pairs. |
| Parabella | food-for-thought | — | — | — | NRICH | NON-OVERLAP for this lane: parabola families belong with P1 Functions (1.2) / transformations. |
| Parabolic mirrors | bigger-picture | — | — | — |  | NON-OVERLAP: enrichment (bigger-picture) — no 9709 P1 quadratics spec point; context material. |
| Pick a card... | fluency-exercise | 1.1.3 | high | 1,2 |  | Solving fluency (factorising/formula choice). |
| Powerful quadratics | food-for-thought | 1.1.5 | medium | 1 | NRICH | Equations quadratic in x^n. |
| Proving the quadratic formula | scaffolded-task | 1.1.3 | medium | 1,4 | NRICH | Derive the quadratic formula (completing the square) — CIE hands the formula, derivation is enrichment. |
| Quadratic grids | rich-example | 1.1.3 | medium | 1 |  | Structure/multiplication-grid identities for quadratics. |
| Quadratic solving sorter | fluency-exercise | 1.1.3 | high | 1,2 |  | Sort by solution method (factorise / complete square / formula). |
| Quadratic symmetry | package-of-problems | 1.1.1 | high | 1,2 |  | Axis of symmetry and vertex via completed-square form. |
| What does the curve $x^4-y^2=y+1$ look like? | review-question | 1.1.5 | medium | 1 | Oxford (MAT) 2013 Q1D | Hidden quadratic in y; curve sketching itself exceeds P1 scope. |
| When are the coefficients of a quadratic equal to it | review-question | 1.1.2 | medium | 1 | UKMT 2011 Q15 | Coefficients equal to roots — root/condition reasoning (UKMT). |
| When are the roots for $x^2-bx+c=0$ real and positiv | review-question | 1.1.2 | high | 1,2 | UCLES 2001 Q3 | Roots real and positive: discriminant + root sign conditions. |
| When are these quadratic inequalities true together? | review-question | 1.1.3 | high | 1,2 | Oxford (MAT) Specimen 1 Q1G | Two quadratic inequalities true together. |
| When can this equation involving algebraic fractions | review-question | 1.1.5 | medium | 1 | UCLES 2005 Q3 | Algebraic-fraction equation reduced to a quadratic. |
| When do these simultaneous equations have no real so | review-question | 1.1.4, 1.1.2 | high | 1,2 | UCLES 1972 Q5(ii) | No real solutions of a line-quadratic system = discriminant condition. |
| When does $(p+1)x^2+4px+9=0$ have a repeated root? | review-question | 1.1.2 | high | 1,2 | UCLES 1986 Q5(a) | Repeated root with parameter: discriminant = 0. |
| When does $x^2 + ax + a = 1$ have distinct real root | review-question | 1.1.2 | high | 1,2 | Oxford (MAT) 2013 Q1A | Distinct real roots: discriminant > 0 (MAT). |
| When does $x^2+(3k-7)x+(2k+6)=0$ have real roots? | review-question | 1.1.2 | high | 1,2 | UCLES 1958 Q2(ii) | Real roots condition in k: discriminant >= 0. |
| When does $x^2-4x-1=2k(x-5)$ have equal roots? | review-question | 1.1.2 | high | 1,2 | UCLES 1966 Q7(ii) | Equal roots after rearranging a line-equals-quadratic identity. |
| When does $x^4=(x-c)^2$ have four real roots? | review-question | 1.1.5 | high | 1,2 | Oxford (MAT) 2009 Q1C | x^4 = (x-c)^2: quadratic in x^2; count four real roots (MAT). |
| When does $y=kx$ intersect the parabola $y=(x-1)^2$? | review-question | 1.1.4 | high | 1,2 | Oxford (MAT) 2010 Q1A | y = kx meets y = (x-1)^2: intersection conditions (MAT). |
| When does $y=mx-5$ intersect $y=x^2-1$  twice? | review-question | 1.1.4 | high | 1,2 | UCLES 1986 Q5(b) | y = mx - 5 cuts y = x^2 - 1 twice: discriminant in m. |
| When is $12x^2+7x-10$ negative? | review-question | 1.1.3 | high | 1,2 | UCLES 1962 Q7(ii),Q7(iii) | Solve and interpret a quadratic inequality (1962 UCLES). |
| When is this line a tangent to this parabola? | review-question | 1.1.4 | high | 1,2 | UCLES 1977 Q13(b) | Tangency of line to parabola via discriminant = 0. |
| Where does $y = px^2 + 8x + p - 6$ cross the $x$-axi | review-question | 1.1.2, 1.1.3 | high | 1,2 | UCLES 1983 Q13(a) | x-axis crossings of a parameterised quadratic. |
| Which parabola? | package-of-problems | 1.1.1 | high | 1,2,4 | NRICH | Identify the parabola from graph features (NRICH). |
| Which quadratic? | building-blocks | 1.1.1, 1.1.3 | high | 1,2,4 | NRICH | Which quadratic satisfies the clues — build/verify quadratics (NRICH). |

## 5. Non-overlaps and extensions (never forced)

- **r6864** — NON-OVERLAP for P1 pure lane: kinematics context (particles sliding); the underlying quadratic solving is 1.1.3.
- **parabella** — NON-OVERLAP for this lane: parabola families belong with P1 Functions (1.2) / transformations.
- **parabolic-mirrors** — NON-OVERLAP: enrichment (bigger-picture) — no 9709 P1 quadratics spec point; context material.

Extensions (aligned with caveat):
- **r7520** — Both equations degree two — extends the P1 linear+quadratic case (1.1.4).

## 6. Mode-2 deep-link shortlists (pilot candidates per spec point)

If the operator approves the Mode-2 pilot (ADR required; rel-nofollow, link-health job, Wayback fallback), these are the 3–5 curated deep links per spec point, chosen for low-threshold-high-ceiling spread and suggestion-before-solution pedagogy:

- **1.1.1**: [Name that graph](https://undergroundmathematics.org/quadratics/name-that-graph); [Paired parabolas](https://undergroundmathematics.org/quadratics/paired-parabolas); [Quadratic symmetry](https://undergroundmathematics.org/quadratics/quad-symmetry); [Which parabola?](https://undergroundmathematics.org/quadratics/which-parabola); [Which quadratic?](https://undergroundmathematics.org/quadratics/which-quadratic)
- **1.1.2**: [Discriminating](https://undergroundmathematics.org/quadratics/discriminating); [When are the roots for $x^2-bx+c=0$ real and positive?](https://undergroundmathematics.org/quadratics/r5138); [When does $x^2-4x-1=2k(x-5)$ have equal roots?](https://undergroundmathematics.org/quadratics/r5316); [For what values of $k$ is $x^2 + 6kx +144$ always positive?](https://undergroundmathematics.org/quadratics/r6526); [When does $x^2+(3k-7)x+(2k+6)=0$ have real roots?](https://undergroundmathematics.org/quadratics/r6828)
- **1.1.3**: [Factorisable quadratics](https://undergroundmathematics.org/quadratics/factorisable-quads); [Inequalities for some occasions](https://undergroundmathematics.org/quadratics/inequalities-for-some-occasions); [Irrational roots](https://undergroundmathematics.org/quadratics/irrational-roots); [Pick a card...](https://undergroundmathematics.org/quadratics/pick-a-card); [Quadratic solving sorter](https://undergroundmathematics.org/quadratics/quad-solving-sorter)
- **1.1.4**: [When does $y=mx-5$ intersect $y=x^2-1$  twice?](https://undergroundmathematics.org/quadratics/r5287); [Can we solve these simultaneous equations, one linear, one quadratic?](https://undergroundmathematics.org/quadratics/r6429); [When is this line a tangent to this parabola?](https://undergroundmathematics.org/quadratics/r7328); [Can we find the midpoint of a chord of this parabola?](https://undergroundmathematics.org/quadratics/r8045); [When does $y=kx$ intersect the parabola $y=(x-1)^2$?](https://undergroundmathematics.org/quadratics/r9614)
- **1.1.5**: [How do we  solve $x + 3\sqrt{x} − 1/2 = 0$?](https://undergroundmathematics.org/quadratics/r6215); [If $2y = a^x + a^{-x}$, can we find $a^x$?](https://undergroundmathematics.org/quadratics/r6816); [Can we solve $\sqrt{3-3x} - \sqrt{2-x} = 1$?](https://undergroundmathematics.org/quadratics/r7485); [When does $x^4=(x-c)^2$ have four real roots?](https://undergroundmathematics.org/quadratics/r9546)

## 7. S1 provenance bridge status for this lane

46 of 59 resources carry provenance tuples (41 exam-board, 5 NRICH-derived), parsed into structured form in `resources/derived/review-question-provenance.json`. The exam-board corpus is dominated by UCLES papers 1953–2013 (codes 417/1, 471/1, 9200/1 …), plus Oxford MAT and UKMT rows. These do **not** collide with the CIE 9709 paper series, so direct matches into a CIE 9709 Official-ExamQuestion corpus are expected to be rare — the S1 join should be run against the full `syllabai-pastpapers` corpus (old UCLES/O&C papers included) before concluding. The tuples are ready for that join.

## 8. Generalisation proposal (after operator review)

1. Extract `spine-export` for the remaining IAL/Pure lanes (9709 P1/P3 subtopics; Edexcel IAL WMA11/12 maps already exist in the hub repo).
2. Repeat the alignment pass per station (script-assisted shortlist + human/LLM verdict per row, same schema).
3. Land the mode-1 artifacts (facts: spec-point ↔ UGM slug mappings) via PR to `syllabai-resources`; keep mode-2 rendering behind the ADR.
4. Mode-4 follow-ups demonstrated by this lane: suggestion-layer hints (per UGM Suggestion sections), MUST/MAY/CAN'T archetype tags (`discriminating`), teacher-prompt tables (teacher-support pages).
