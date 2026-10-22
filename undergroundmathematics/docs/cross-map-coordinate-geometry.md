# Cross-map lane 3: UGM Geometry of Equations + Circles → CIE 9709 Pure 1 Coordinate geometry

**Status**: lane 3 of the P3c generalisation (per §8 of `cross-map-functions.md`; `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-23 · machine-readable twin: `resources/derived/cross-map-coordinate-geometry.json`

## 1. What this is

Lanes 1–2 mapped the UGM quadratics station (56/59) and the UGM Combining Functions station (27/38) onto CIE 9709 Pure 1 subtopics 1.1–1.2, and lane 2's §8 pre-named the next hop: **1.3 Coordinate geometry, drawing on the `geometry-of-equations` + `circles` stations**. This lane executes exactly that. The of-record spine is **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.3 Coordinate geometry**, which the hub spine parse (`syllabai-v2/apps/hub/spines/cie-a-level-maths-20-pure-1.json`) carries as **four rows**: 1.3.1, 1.3.1a, 1.3.2, 1.3.2a.

**Fold decision (of record).** Rows 1.3.1a and 1.3.2a are interleaved-parse fragments of the parent statements, not independent learning outcomes — the content-map attaches items to 1.3.1 only (40 question parts as of this lane). The cross-map aligns against the two parent codes and folds the fragments in: 1.3.1a's recoverable content ("sufficient information") completes the 1.3.1 statement; 1.3.2a's recoverable content is the **circle statement** — *"(x − a)² + (y − b)² = r represents the circle with centre (a, b) and radius r"* — plus *"understand the relationship between a graph and its associated algebraic equation, and use the relationship between points of intersection of graphs and solutions of equations"*. The spine export (`resources/derived/spine-export/cie-a-level-maths-20-pure-1.json`) still carries **all four rows verbatim**; nothing of record is rewritten.

**Station scope.** Two stations, both fully in scope with honest per-resource verdicts:

- **Geometry of Equations** (38 resources) — the lane's centre of mass: straight-line equations, parallel/perpendicular reasoning, intersections, loci, inequality regions.
- **Circles** (47 resources) — the station's coordinate-equation strand (KQ *"How can we use the Cartesian equation of a circle?"*) serves the folded circle statement; its metric strands (arc/sector mensuration in radians → CIE 1.4, circle theorems, sphere/cone mensuration, ellipse/parametric work → P3) are recorded as non-overlaps for this lane, never forced.

Method unchanged: each resource's question well / task statement read against the spec-point wording; one-to-many allowed; non-overlaps explicit with recorded reasons.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| UGM resources mapped (two stations) | 85 (Geometry of Equations 38 + Circles 47) |
| Aligned to ≥1 CIE 9709 P1 spec point | 61 (71.8%) |
| Explicit non-overlap notes | 24 (Geometry of Equations 4 · Circles 20) |
| Alignment rows (one-to-many) | 77 (1.3.1: 17 · 1.3.2: 60) |
| Aligned resources with provenance tuple (S1 bridge) | 44 |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** |

Station facts of record (P3b enrichment sheets): Geometry of Equations — 38 resources, 27 review questions, 4/4 key questions covered, 31 with parsed provenance; Circles — 47 resources, 35 review questions, 5/5 key questions covered, 36 with parsed provenance, 1 teacher-support page. The station split of the lane: Geometry of Equations 34/38 aligned (89.5%); Circles 27/47 aligned (57.4%) — the Circles non-overlap mass is exactly its non-coordinate strands (radian mensuration, circle theorems, conic/parametric extensions), which is the honest verdict the lane-2 §8 preview anticipated.

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **verbatim from the of-record spine** (hub curriculum parse); the CIE spec parse carries known text artifacts (interleaved example text, fragments folded as §1 documents) — codes are authoritative. The 1.3.2 working text covers three clauses: line forms; the circle statement (from fragment 1.3.2a); the graph↔equation / intersections relationship.

### 1.3.1 — find the equation of a straight line given e.g. given two points, or one point and the gradient. sufficient information

17 UGM resources (primary pick **straight-line-pairs**):

- [investigation] Straight line pairs (`straight-line-pairs`, confidence high) ⭐
- [review-question] A line cuts the axes to make a triangle; can we find its area? (`r6803`, confidence high)
- [review-question] A line through a variable point creates a triangle; can we find its area? (`r6835`, confidence high)
- [review-question] A point $Y$ moves to define a point $P$ — can we find the locus of $P\,$? (`r6583`, confidence high)
- [review-question] Can we calculate an approximation to the root of this function? (`r5948`, confidence medium)
- [review-question] Can we find a rectangle from two vertices and a diagonal? (`r5967`, confidence high)
- [review-question] Can we find the area of this quadrilateral? (`r8748`, confidence high)
- [review-question] Can we find the coordinates of this tilted rectangle? (`r6366`, confidence high)
- [review-question] Can we find the point midway between an intersection and a line? (`r9273`, confidence high)
- [review-question] Can we reflect this point in this line? (`r6230`, confidence medium)
- [review-question] Can we show this parallelogram is a rectangle? (`r8449`, confidence high)
- [bigger-picture] Cartesian coordinates (`cartesian-coordinates`, confidence medium)
- [review-question] Given a right angle and the equations of two sides, can we find the third? (`r5661`, confidence high)
- [building-blocks] Lots of lines! (`lots-of-lines`, confidence high)
- [investigation] Simultaneous squares (`simultaneous-squares`, confidence high)
- [building-blocks] Straight lines (`describing-straight-lines`, confidence high)
- [review-question] Where is the foot of the perpendicular from a point to a line? (`r5202`, confidence high)

### 1.3.2 — interpret and use any of the forms y = mx + c , y – y = m ( x – x ) , ax + by + c = 0 in solving

60 UGM resources (primary pick **teddy-bear**):

- [package-of-problems] Teddy bear (`teddy-bear`, confidence high) ⭐
- [review-question] A line cuts the axes to make a triangle; can we find its area? (`r6803`, confidence high)
- [review-question] A line through a variable point creates a triangle; can we find its area? (`r6835`, confidence high)
- [review-question] A point $Y$ moves to define a point $P$ — can we find the locus of $P\,$? (`r6583`, confidence high)
- [food-for-thought] Between the lines (`between-the-lines`, confidence medium)
- [review-question] Can we calculate an approximation to the root of this function? (`r5948`, confidence medium)
- [review-question] Can we find a rectangle from two vertices and a diagonal? (`r5967`, confidence high)
- [review-question] Can we find an integer solution to three simultaneous inequalities? (`r5281`, confidence medium)
- [review-question] Can we find the area bounded by these two graphs? (`r9386`, confidence medium)
- [review-question] Can we find the area of this quadrilateral? (`r8748`, confidence high)
- [review-question] Can we find the areas enclosed between a circle and its tangent? (`r8946`, confidence medium)
- [review-question] Can we find the coordinates of this tilted rectangle? (`r6366`, confidence high)
- [review-question] Can we find the equation of the inscribed circle of the triangle $ABC$? (`r5777`, confidence medium)
- [review-question] Can we find the equations of two circles that touch another? (`r5624`, confidence high)
- [review-question] Can we find the point midway between an intersection and a line? (`r9273`, confidence high)
- [review-question] Can we find the tangents to this circle from the origin? (`r5903`, confidence high)
- [review-question] Can we find the three inequalities that define this region? (`r8408`, confidence medium)
- [review-question] Can we find the two circles that satisfy these three conditions? (`r8419`, confidence high)
- [review-question] Can we illustrate this pair of inequalities on a graph? (`r7320`, confidence medium)
- [review-question] Can we plot this graph and use it to solve two equations? (`r7296`, confidence high)
- [review-question] Can we reflect this point in this line? (`r6230`, confidence medium)
- [review-question] Can we show that (circle area)/(triangle area) $\geq \pi$? (`r7656`, confidence medium)
- [review-question] Can we show that these four points lie on a circle? (`r5717`, confidence high)
- [review-question] Can we show that these two circles touch? (`r6100`, confidence high)
- [review-question] Can we show that this point moves on a circle? (`r6234`, confidence high)
- [review-question] Can we show these two circles lie entirely outside each other? (`r6390`, confidence high)
- [review-question] Can we show this parallelogram is a rectangle? (`r8449`, confidence high)
- [review-question] Can we show this quartic equation has exactly two real roots? (`r7549`, confidence medium)
- [bigger-picture] Conic sections in real life (`conic-sections-in-real-life`, confidence medium)
- [many-ways-problem] Finding circles (`finding-circles`, confidence high)
- [review-question] Given a right angle and the equations of two sides, can we find the third? (`r5661`, confidence high)
- [review-question] Given three clues, can we find the equation of this circle? (`r9368`, confidence high)
- [review-question] Given two lines crossing a circle, can we show these lengths are equal? (`r9551`, confidence medium)
- [review-question] If $AQ:QP=\lambda:1$, can we show $Q$ lies on a  circle? (`r9045`, confidence high)
- [review-question] If we know the sum and product of two numbers, what are they? (`r5887`, confidence high)
- [building-blocks] Lots of lines! (`lots-of-lines`, confidence high)
- [food-for-thought] Near miss (`near-miss`, confidence medium)
- [many-ways-problem] Negatively triangular (`negatively-triangular`, confidence high)
- [review-question] No solutions, or infinitely many? (`r6514`, confidence high)
- [problem-decisions] Olympic rings (`olympic-rings`, confidence high)
- [review-question] One distance is double another; can we find a locus? (`r8080`, confidence high)
- [package-of-problems] Pairs of circles (`pairs-of-circles`, confidence high)
- [investigation] Simultaneous squares (`simultaneous-squares`, confidence high)
- [building-blocks] Spot the difference (`spot-the-difference`, confidence medium)
- [investigation] Straight line pairs (`straight-line-pairs`, confidence high)
- [building-blocks] Straight lines (`describing-straight-lines`, confidence high)
- [resource-in-action] Teddy bear - teacher support (`teddy-bear-teacher-support`, confidence high)
- [many-ways-problem] The circle of Apollonius... coordinate edition (`the-circle-of-apollonius-coordinate-edition`, confidence high)
- [bigger-picture] The equation of a straight line (`the-equation-of-a-straight-line`, confidence high)
- [review-question] What can we deduce if the loci traced out by two points touch? (`r8509`, confidence high)
- [review-question] What can we say if two circles cut at right angles? (`r7925`, confidence medium)
- [review-question] What is the largest $x$ to satisfy these three inequalities? (`r9709`, confidence medium)
- [review-question] What's the locus of $(p, q)$ if the length of this tangent equals $p$? (`r9768`, confidence high)
- [review-question] What's the locus of the intersection of these variable lines? (`r5255`, confidence high)
- [review-question] When does the origin lie inside this circle? (`r7599`, confidence high)
- [review-question] Where do this pair of tangents to a circle meet? (`r7171`, confidence high)
- [review-question] Where is the foot of the perpendicular from a point to a line? (`r5202`, confidence high)
- [review-question] Which four inequalities define this region? (`r5737`, confidence medium)
- [review-question] Which point on the first circle is closest to the second? (`r9452`, confidence high)
- [review-question] Which point on this circle is closest to the origin? (`r8275`, confidence high)

## 4. Full alignment table

| UGM resource | Station | Type | CIE P1 spec point(s) | Conf | Modes | Provenance | Note |
|---|---|---|---|---|---|---|---|
| Between the lines | Geometry of Equations | food-for-thought | 1.3.2 | medium | 1 |  | Area between two lines given the area of one; linear-function graph reading (gradients/intercepts) is the 1.3.2 vocabulary. |
| Cartesian coordinates | Geometry of Equations | bigger-picture | 1.3.1 | medium | 1 |  | Bigger-picture context: coordinates as the lane's foundation — history of the coordinate plane from Descartes to modern use. |
| Straight lines | Geometry of Equations | building-blocks | 1.3.2, 1.3.1 | high | 1,4 |  | Canonical which-descriptions-determine-a-line sort: y=mx+c, y-y1=m(x-x1), ax+by+c=0, x=k, point+gradient, two points; degenerate cases (y^2=x^2, xy=1, repeated line) sharpen the graph-equation reading. Card-sort pattern exemplar. |
| Lots of lines! | Geometry of Equations | building-blocks | 1.3.2, 1.3.1 | high | 1,4 |  | Matching line-equation pairs by parallel/perpendicular/intercept criteria — forms fluency with geometric conditions. |
| Near miss | Geometry of Equations | food-for-thought | 1.3.2 | medium | 1 |  | Near-identical simultaneous pairs with distant solutions: ill-conditioning read as nearly-parallel line geometry (KQ64). |
| Negatively triangular | Geometry of Equations | many-ways-problem | 1.3.2 | high | 1,4 |  | Which three of four given lines enclose a triangle with negative coordinates — intersections from line forms; create-your-own extension. |
| Where is the foot of the perpendicular from a point to a line? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 2003 Q7 (STEP Mathematics III) | Foot of the perpendicular from P to the line AB through (a,0), (0,b): perpendicularity via gradients and line equations; STEP III depth is extension beyond P1 routine. |
| What's the locus of the intersection of these variable lines? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 1978 Q14 (Additional Mathematics 2) | Locus of the intersection of x+y=t and y=tx as t varies; intersection coordinates in terms of t; the locus equation rides quadratics. |
| Can we find an integer solution to three simultaneous inequalities? | Geometry of Equations | review-question | 1.3.2 | medium | 1 | UCLES 1958 Q1 (Mathematics Scholarship paper) | Three simultaneous linear inequalities deduce bounds on x and y — region reading of boundary lines; linear inequality regions are IGCSE-flavoured extension (recorded medium). |
| Given a right angle and the equations of two sides, can we find the third? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1979 Q5 (Additional Mathematics 1) | Right-angle triangle: two side equations given, third side from the perpendicular gradient through the given vertex. |
| Which four inequalities define this region? | Geometry of Equations | review-question | 1.3.2 | medium | 1 | UCLES 1978 Q23 (Mathematics Syllabus C Paper 1) | Four inequalities defining a triangular region from vertex coordinates — boundary-line reading in 1.3.2 forms; inequality-region language is extension (recorded medium). |
| If we know the sum and product of two numbers, what are they? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 1970 Q1 (Additional Mathematics 1) | Sum/product of two numbers -> plot the corresponding graphs and read the intersection as the solution — the graph-equation relationship verbatim (hyperbola is context vocabulary). |
| Can we calculate an approximation to the root of this function? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | medium | 1 | UCLES 1978 Q16 (Mathematics A 2) | False-position root approximation: chord through (a,f(a)) and (b,f(b)), its x-intercept — line-from-two-points construction riding numerical-methods context (recorded medium). |
| Can we find a rectangle from two vertices and a diagonal? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | O&C (Oxford & Cambridge SEG) 1973 Q5 (Additional Mathematics 2) | Rectangle from two vertices and a point on the diagonal produced: line through two points, perpendicular sides, intersection solving. |
| Can we reflect this point in this line? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | medium | 1 | Oxford (MAT) None Q1C (University Mathematics Aptitude Test) | Reflection of (3,4) in the line 3x+4y=50: perpendicular foot as midpoint — perpendicular gradients plus ax+by+c=0 fluency; MAT MCQ extension (recorded medium). |
| Can we show that this point moves on a circle? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 2005 Q6 (STEP Mathematics I) | AP=2BP locus derived to (x+7)^2+y^2=100 — distance-ratio locus in circle standard form; the folded 1.3.2 circle statement verbatim; STEP I depth is extension. |
| Can we find the coordinates of this tilted rectangle? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1986 Q10 (Additional Mathematics 1) | Tilted rectangle: perpendicular line through B, vertex coordinates by intersection solving — line equations end to end. |
| No solutions, or infinitely many? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 1983 Q30b (Additional Mathematics 2) | Value of k giving infinitely-many/no solutions of a linear pair — degenerate systems read as coincident/parallel lines (KQ64). |
| A point $Y$ moves to define a point $P$ — can we find the locus of $P\,$? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | O&C (Oxford & Cambridge SEG) 1957 Q6 (Additional Mathematics 2) | Construction locus: perpendicular through Y meets the x-axis at Q, P the midpoint — line equations from geometric conditions, locus equation from coordinates. |
| A line cuts the axes to make a triangle; can we find its area? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1981 Q1 (Additional Mathematics 1) | Line through the midpoint of AB parallel to AC: gradient+point construction, axis intercepts, triangle area. |
| A line through a variable point creates a triangle; can we find its area? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1980 Q1 (Additional Mathematics 2) | Line with gradient -2 through (2t,t) enclosing area 4 with the axes — the 1.3.1 statement verbatim plus intercept reading. |
| Can we plot this graph and use it to solve two equations? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 1978 Q7 (Mathematics Syllabus B Paper 1) | Add a suitable straight line to the parabola graph to solve 6x-x^2=8-x/2 — intersection-of-graphs as equation-solving verbatim; the parabola rides 1.1. |
| Can we illustrate this pair of inequalities on a graph? | Geometry of Equations | review-question | 1.3.2 | medium | 1 | O&C (Oxford & Cambridge SEG) 1964 Q5 (Elementary Mathematics 2 (St Dunstan's College)) | Shade (x-2)(y+3)>=0 and x^2+y^2<=25, find p with (3,p) in both — circle-equation graph reading plus inequality-region extension (recorded medium). |
| One distance is double another; can we find a locus? | Geometry of Equations | review-question | 1.3.2 | high | 1 | UCLES 1985 Q16(b) (Additional Mathematics 1) | PA=2PB with A(0,3), B(0,-3) -> x^2+y^2+10y+9=0 — distance-ratio locus to circle equation; the completing-the-square step rides 1.1.1. |
| Can we find the three inequalities that define this region? | Geometry of Equations | review-question | 1.3.2 | medium | 1 | O&C (Oxford & Cambridge SEG) 1969 Q7 (MEI Additional Mathematics 1) | Line with gradient -2 through the ellipse's positive y-intersection; three inequalities bound the region — the line work is 1.3.1/1.3.2 vocabulary; the ellipse is beyond-P1 curve vocabulary (recorded medium). |
| Can we show this parallelogram is a rectangle? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1989 Q15 (Certificate in Additional Mathematics 1) | Parallelogram shown to be a rectangle: perpendicular gradients, vertex coordinates by intersection, area. |
| Can we find the area of this quadrilateral? | Geometry of Equations | review-question | 1.3.1, 1.3.2 | high | 1 | UCLES 1988 Q15 (Additional Mathematics 1) | Perpendicular bisector construction: equations of BD and AC, midpoint M, fourth vertex C, area — 1.3.1/1.3.2 core. |
| Can we find the point midway between an intersection and a line? | Geometry of Equations | review-question | 1.3.2, 1.3.1 | high | 1 | UCLES 1973 Q8 (Additional Mathematics 1) | Intersection point of two lines; midpoint of the segment from P perpendicular to y=2x+8 — intersection solving plus perpendicular construction. |
| What is the largest $x$ to satisfy these three inequalities? | Geometry of Equations | review-question | 1.3.2 | medium | 1 | Oxford (MAT) None Q1D (University Mathematics Aptitude Test) | Largest x satisfying three linear inequalities — vertex exploration of a feasible region; the optimisation framing is LP-flavoured (recorded medium). |
| Simultaneous squares | Geometry of Equations | investigation | 1.3.1, 1.3.2 | high | 1,4 |  | Four lines enclose a square: construct the fourth from three, or from area + vertex — equation-of-line construction from geometric constraints. Investigation pattern exemplar. |
| Spot the difference | Geometry of Equations | building-blocks | 1.3.2 | medium | 1 |  | Factorised equations ((x+y-1)(x^2+y^2)=0) vs their graphs — the graph-equation relationship at degenerate cases (line + point, missing points); implicit cubic vocabulary extension (recorded medium). |
| Straight line pairs | Geometry of Equations | investigation | 1.3.1, 1.3.2 | high | 1,4 |  | Construct line pairs from gradient/intercept difference constraints — 1.3.1 sufficient-information construction as an investigation. Pattern exemplar. |
| The circle of Apollonius... coordinate edition | Geometry of Equations | many-ways-problem | 1.3.2 | high | 1,4 |  | Apollonius circle PA/PB=lambda derived by coordinates — the distance-ratio locus family generalised. Pattern exemplar. |
| The equation of a straight line | Geometry of Equations | bigger-picture | 1.3.2 | high | 1 |  | Bigger-picture exposition on the forms of line equations — the 1.3.2 statement itself as context. |
| Conic sections in real life | Circles | bigger-picture | 1.3.2 | medium | 1 |  | Bigger-picture: conic sections in the world; the circle is the P1 member of the family — context for the 1.3.2 circle statement. |
| Finding circles | Circles | many-ways-problem | 1.3.2 | high | 1,4 |  | How many points define a circle; equations from diameter ends and point sets — the folded circle statement as an investigation. Pattern exemplar. |
| Olympic rings | Circles | problem-decisions | 1.3.2 | high | 1 |  | Recreate the Olympic rings with graph software: circle equations plus domain-restricted plots — centre/radius form fluency. |
| Pairs of circles | Circles | package-of-problems | 1.3.2 | high | 1,4 |  | Inscribed triangle/circle images: find inner/outer circle equations in standard and expanded forms (x^2+y^2-3x-y=45/2 etc.). Pattern exemplar. |
| Can we find the equations of two circles that touch another? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1958 Q2 (Mathematics 2) | Point inside x^2+y^2+4x-8y-80=0; two radius-5 circles through P touching it — centre/radius from the expanded form plus tangency conditions. |
| Can we show that these four points lie on a circle? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1987 Q6 (Mathematics A 1 and Pure Mathematics 1) | Four points shown to lie on a circle; centre and radius found — perpendicular-bisector/completing-the-square work. |
| Can we find the equation of the inscribed circle of the triangle $ABC$? | Circles | review-question | 1.3.2 | medium | 1 | UCLES 1985 Q13 (Mathematics A 1 and Pure Mathematics 1) | Incircle of triangle ABC: centre and radius of the inscribed circle — the equation-of-circle form is 1.3.2; the incentre construction rides triangle-centre geometry (recorded medium). |
| Can we find the tangents to this circle from the origin? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1963 Q2 (Mathematics 2 and Pure Mathematics 2) | Circle through three points shown to touch the y-axis; the other tangent from the origin — circle-from-conditions plus tangent lines. |
| Can we show that these two circles touch? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1986 Q7 (Mathematics A 1 and Pure Mathematics 1) | Circles x^2+y^2=25 and x^2+y^2-24x-18y+125=0 shown to touch; touch point calculated — centre/radius plus tangency. |
| Can we show these two circles lie entirely outside each other? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1953 Q2 (Mathematics 2) | General form x^2+y^2+2gx+2fy+c=0 -> centre/radius proof; two circles shown to lie entirely outside each other — general-form mastery. |
| Where do this pair of tangents to a circle meet? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1970 Q8 (Additional Mathematics 2) | Line x=3 meets the circle at P and Q; tangents at P and Q and their intersection — line-circle intersection plus tangent equations via the radius-perpendicular fact. |
| Can we show this quartic equation has exactly two real roots? | Circles | review-question | 1.3.2 | medium | 1 | UCLES 1980 Q3 (Pure Mathematics 2) | y=x^2 and the circle x^2+y^2-4x+2y-4=0 sketched together show the quartic has exactly two real roots — intersection-of-graphs as equation-roots verbatim; quartic algebra extension (recorded medium). |
| When does the origin lie inside this circle? | Circles | review-question | 1.3.2 | high | 1 | Oxford (MAT) 2016 Q1C (University Mathematics Aptitude Test) | The origin lies inside x^2+ax+y^2+by=c precisely when a^2+b^2>4c — completing the square to centre/radius and the inside test; MAT form, exactly the circle skill. |
| Can we show that (circle area)/(triangle area) $\geq \pi$? | Circles | review-question | 1.3.2 | medium | 1 | Oxford (MAT) 2008 Q4 (University Mathematics Aptitude Test) | Circle through O, (p,0), (0,q): x^2-px+y^2-qy=0, centre and area; the area-ratio >= pi part rides inequality reasoning (recorded medium). |
| What can we say if two circles cut at right angles? | Circles | review-question | 1.3.2 | medium | 1 | UCLES 1965 Q2 (Mathematics Special paper) | Orthogonal-circle condition for general-form circles; the circle orthogonal to three given circles — general-form circle algebra; the orthogonality condition is beyond P1 routine (recorded medium). |
| Which point on this circle is closest to the origin? | Circles | review-question | 1.3.2 | high | 1 | Oxford (MAT) 2009 Q1B (University Mathematics Aptitude Test) | Point on x^2+y^2+6x+8y=75 closest to the origin — completing the square to centre/radius plus distance reasoning. |
| Can we find the two circles that satisfy these three conditions? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1966 Q2 (Mathematics 2 and Pure Mathematics 2) | Two circles from three conditions (x-axis tangent, centre on 2y=x, (14,2) on the circle); 3y=4x shown to be a common tangent — circle-from-conditions plus tangent verification. |
| What can we deduce if the loci traced out by two points touch? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1955 Q1 (Mathematics 2) | OP^2=lambda y locus is a circle with centre (0, lambda/2); touching-loci condition — the locus-to-circle derivation family. |
| Can we find the areas enclosed between a circle and its tangent? | Circles | review-question | 1.3.2 | medium | 1 | Oxford (MAT) 2007 Q4 (University Mathematics Aptitude Test) | Tangent to the circle centre (1,1) radius 1 at angle theta: tangent-line equation and areas A(theta), B(theta) — the line/tangent parts are 1.3.2; the area parts ride trig/radians (recorded medium). |
| If $AQ:QP=\lambda:1$, can we show $Q$ lies on a  circle? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1954 Q2 (Mathematics 2) | Section point Q of AP with AQ:QP=lambda:1 traces a circle; orthogonal-intersection condition — section formula plus the locus-to-circle family; orthogonality extension. |
| Given three clues, can we find the equation of this circle? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1968 Q7 (Additional Mathematics 1) | Circle through (2,0) and (8,0) touching the y-axis; furthest point from (2,0) — circle-from-conditions. |
| Can we find the area bounded by these two graphs? | Circles | review-question | 1.3.2 | medium | 1 | Oxford (MAT) 2013 Q1H (University Mathematics Aptitude Test) | Area between y=sqrt(2-x^2) (upper semicircle) and a line — circle-graph reading plus line form; the area evaluation rides 1.4 radians (recorded medium). |
| Which point on the first circle is closest to the second? | Circles | review-question | 1.3.2 | high | 1 | Oxford (MAT) 2007 Q1D (University Mathematics Aptitude Test) | Closest points between (x-5)^2+(y-4)^2=4 and (x-1)^2+(y-1)^2=1 — centre/radius plus the distance-between-centres reading. |
| Given two lines crossing a circle, can we show these lengths are equal? | Circles | review-question | 1.3.2 | medium | 1 | UCLES 2009 Q1 (STEP Mathematics III) | Lines through circle points S, T, U, V on x^2+(y-c)^2=r^2; substitution gives quadratics in s and t; p+q=0 — substituting lines into the circle equation is 1.3.2; the STEP III proof depth is extension (recorded medium). |
| What's the locus of $(p, q)$ if the length of this tangent equals $p$? | Circles | review-question | 1.3.2 | high | 1 | UCLES 1980 Q6 (Mathematics A 1) | AP=3PB locus is the circle S tangent to the y-axis; tangent-length locus equidistant from a line and a point — the locus-to-circle family; the parabola locus is extension vocabulary. |
| Teddy bear | Circles | package-of-problems | 1.3.2 | high | 1,4 |  | Match 13 circles to equations in both forms ((x+10)^2+(y+15)^2=4pi^2, x^2+y^2+66x-78y+2110=0) — centre/radius fluency, standard and expanded. Pattern exemplar. |
| Teddy bear - teacher support | Circles | resource-in-action | 1.3.2 | high | 1 |  | Teacher-support notes for Teddy bear (research-project notes) — rides the parent resource's 1.3.2 alignment. |
| Can we maximise the profit for this tractor-making business? | Geometry of Equations | review-question | — | — | — | UCLES 1989 Q10 (Applicable Mathematics 1) | NON-OVERLAP for this lane: linear programming — five inequalities, feasible region, profit maximisation (Applicable Mathematics); the tested skill is LP optimisation beyond P1 1.3; the region-shading rides 1.3.2. |
| Can we match this equation to its graph? | Geometry of Equations | review-question | — | — | — | Oxford (MAT) None Q1J (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: implicit curve x^2y^2(x+y)=1 identification (MAT) — cubic/implicit sketching beyond the P1 1.3 forms. |
| Can we find the area of this inscribed quadrilateral? | Geometry of Equations | review-question | — | — | — | UKMT 2012 Q16 (Senior Mathematical Challenge) | NON-OVERLAP for this lane: UKMT axis-intersections of the implicit rotated conic x^2+y^2-xy+x-4y=12 — the conic is the object of study, beyond P1 1.3. |
| Which of these graphs shows the area $A(c)$ as $c$ varies? | Geometry of Equations | review-question | — | — | — | Oxford (MAT) 2012 Q1D (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: A(c) area-function graph for the moving line y=x+c (MAT) — the tested skill is reasoning about the area function, beyond the 1.3 line/circle statements. |
| Belt | Circles | food-for-thought | — | — | — |  | NON-OVERLAP for this lane: wire around two cylinders — common tangent length plus arc pieces in radians; metric circle geometry riding 1.4 mensuration, not coordinate circle equations. |
| Cones | Circles | building-blocks | — | — | — |  | NON-OVERLAP for this lane: frustum volume — mensuration beyond P1 1.3. |
| Cutting spheres | Circles | food-for-thought | — | — | — |  | NON-OVERLAP for this lane: sphere-zone surface area — 3D mensuration beyond P1 1.3. |
| Elliptical crossings | Circles | package-of-problems | — | — | — |  | NON-OVERLAP for this lane: chord-midpoint locus on an ellipse — the ellipse is the object of study, beyond the lines-and-circles lane; previews P3 conic work. |
| What is the locus of these points fixed to a rod? | Circles | review-question | — | — | — | UCLES 1979 Q6 (Mathematics A Special paper) | NON-OVERLAP for this lane: rod-end parametric loci for C and D — parametric curve work is P3; the line-locus conclusion rides 1.3 loosely. |
| What's the area of this square if it sits in this sector? | Circles | review-question | — | — | — | O&C (Oxford & Cambridge SEG) 1967 Q6 (General Mathematics 1) | NON-OVERLAP for this lane: square in a sector — arc length, segment area in radians; 1.4 Circular measure territory. |
| If $x^2+y^2\leq1$, when does $x+y$ have a maximum? | Circles | review-question | — | — | — | Oxford (MAT) 2011 Q4 (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: quarter-disc optimisation (maximise x+y, xy; describe the family x^2+y^2-4x-2y=k) — the tested skill is optimisation over a region; the circle-family description rides 1.3.2. |
| What's the shared area for these two circles? | Circles | review-question | — | — | — | UCLES 1982 Q6 (Mathematics A 1 and Pure Mathematics 1) | NON-OVERLAP for this lane: shared area of two circles — segment/sector mensuration in radians; 1.4 territory. |
| How much of this log is below the surface? | Circles | review-question | — | — | — | UCLES 1986 Q15 (Additional Mathematics 1) | NON-OVERLAP for this lane: floating log — arc length, submerged area, percentage volume in radians; 1.4 territory. |
| What's the area inside both the circle $C$ and the triangle $T$? | Circles | review-question | — | — | — | Oxford (MAT) 2010 Q4 (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: area inside both circle C and triangle T (MAT Q4) — sector/trig mensuration beyond the lines-and-circles statements. |
| Can we find the ratio of the areas of these two sectors? | Circles | review-question | — | — | — | UCLES 1976 Q8 (Additional Mathematics 1) | NON-OVERLAP for this lane: touching circles and sector areas via radians — 1.4 territory. |
| What area do these intersecting circles share? | Circles | review-question | — | — | — | UCLES 1970 Q2 (Additional Mathematics 1) | NON-OVERLAP for this lane: intersecting circles — angles in radians, sector areas, common area; 1.4 territory. |
| When does a circle touch a parabola twice? | Circles | review-question | — | — | — | Oxford (MAT) 2012 Q4 (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: circle resting on the parabola y=x^2 (MAT Q4) — tangency plus sector area with inverse trig, beyond the 1.3 statements. |
| Can we show the locus of the midpoint of $PQ$ is an ellipse? | Circles | review-question | — | — | — | UCLES 1972 Q8 (Mathematics A 1) | NON-OVERLAP for this lane: ellipse parametrisation, OP^2+OQ^2 and the midpoint locus — the ellipse as object plus parametric curves (P3), beyond P1 1.3. |
| Can we find the circles through the points where two ellipses meet? | Circles | review-question | — | — | — | UCLES 2002 Q1 (STEP Mathematics I) | NON-OVERLAP for this lane: STEP I circles through the intersection points of two ellipses — ellipses as objects; pencil-of-circles depth beyond P1. |
| Can we find the area between three touching circles? | Circles | review-question | — | — | — | UCLES 1954 Q7 (Mathematics C) | NON-OVERLAP for this lane: area between three touching circles — equilateral triangle plus sector mensuration; 1.4 territory. |
| When does this area within a circle have a maximum value? | Circles | review-question | — | — | — | Oxford (MAT) 2012 Q1J (University Mathematics Aptitude Test) | NON-OVERLAP for this lane: chords meeting at angle theta, maximal shaded area (MAT MCQ) — sector/segment mensuration beyond the statements. |
| If we know the difference in their areas, how big are these sectors? | Circles | review-question | — | — | — | UCLES 1979 Q4 (Additional Mathematics 1) | NON-OVERLAP for this lane: concentric sectors, area difference and arc lengths — 1.4 territory. |
| Sector spirals | Circles | fluency-exercise | — | — | — |  | NON-OVERLAP for this lane: arc lengths and sector areas fluency — 1.4 territory. |
| Where are you? | Circles | bigger-picture | — | — | — |  | NON-OVERLAP for this lane: latitude/longitude position-finding context — spherical vocabulary, not coordinate-plane line/circle equation work. |

## 5. Non-overlaps and extensions (never forced)

Non-overlaps (24):

- **r7642** (Geometry of Equations) — NON-OVERLAP for this lane: linear programming — five inequalities, feasible region, profit maximisation (Applicable Mathematics); the tested skill is LP optimisation beyond P1 1.3; the region-shading rides 1.3.2.
- **r7757** (Geometry of Equations) — NON-OVERLAP for this lane: implicit curve x^2y^2(x+y)=1 identification (MAT) — cubic/implicit sketching beyond the P1 1.3 forms.
- **r8471** (Geometry of Equations) — NON-OVERLAP for this lane: UKMT axis-intersections of the implicit rotated conic x^2+y^2-xy+x-4y=12 — the conic is the object of study, beyond P1 1.3.
- **r9617** (Geometry of Equations) — NON-OVERLAP for this lane: A(c) area-function graph for the moving line y=x+c (MAT) — the tested skill is reasoning about the area function, beyond the 1.3 line/circle statements.
- **belt** (Circles) — NON-OVERLAP for this lane: wire around two cylinders — common tangent length plus arc pieces in radians; metric circle geometry riding 1.4 mensuration, not coordinate circle equations.
- **cones** (Circles) — NON-OVERLAP for this lane: frustum volume — mensuration beyond P1 1.3.
- **cutting-spheres** (Circles) — NON-OVERLAP for this lane: sphere-zone surface area — 3D mensuration beyond P1 1.3.
- **elliptical-crossings** (Circles) — NON-OVERLAP for this lane: chord-midpoint locus on an ellipse — the ellipse is the object of study, beyond the lines-and-circles lane; previews P3 conic work.
- **r5754** (Circles) — NON-OVERLAP for this lane: rod-end parametric loci for C and D — parametric curve work is P3; the line-locus conclusion rides 1.3 loosely.
- **r6164** (Circles) — NON-OVERLAP for this lane: square in a sector — arc length, segment area in radians; 1.4 Circular measure territory.
- **r6645** (Circles) — NON-OVERLAP for this lane: quarter-disc optimisation (maximise x+y, xy; describe the family x^2+y^2-4x-2y=k) — the tested skill is optimisation over a region; the circle-family description rides 1.3.2.
- **r6838** (Circles) — NON-OVERLAP for this lane: shared area of two circles — segment/sector mensuration in radians; 1.4 territory.
- **r7385** (Circles) — NON-OVERLAP for this lane: floating log — arc length, submerged area, percentage volume in radians; 1.4 territory.
- **r7495** (Circles) — NON-OVERLAP for this lane: area inside both circle C and triangle T (MAT Q4) — sector/trig mensuration beyond the lines-and-circles statements.
- **r7816** (Circles) — NON-OVERLAP for this lane: touching circles and sector areas via radians — 1.4 territory.
- **r7937** (Circles) — NON-OVERLAP for this lane: intersecting circles — angles in radians, sector areas, common area; 1.4 territory.
- **r7979** (Circles) — NON-OVERLAP for this lane: circle resting on the parabola y=x^2 (MAT Q4) — tangency plus sector area with inverse trig, beyond the 1.3 statements.
- **r8051** (Circles) — NON-OVERLAP for this lane: ellipse parametrisation, OP^2+OQ^2 and the midpoint locus — the ellipse as object plus parametric curves (P3), beyond P1 1.3.
- **r8216** (Circles) — NON-OVERLAP for this lane: STEP I circles through the intersection points of two ellipses — ellipses as objects; pencil-of-circles depth beyond P1.
- **r8225** (Circles) — NON-OVERLAP for this lane: area between three touching circles — equilateral triangle plus sector mensuration; 1.4 territory.
- **r9028** (Circles) — NON-OVERLAP for this lane: chords meeting at angle theta, maximal shaded area (MAT MCQ) — sector/segment mensuration beyond the statements.
- **r9423** (Circles) — NON-OVERLAP for this lane: concentric sectors, area difference and arc lengths — 1.4 territory.
- **sector-spirals** (Circles) — NON-OVERLAP for this lane: arc lengths and sector areas fluency — 1.4 territory.
- **where-are-you** (Circles) — NON-OVERLAP for this lane: latitude/longitude position-finding context — spherical vocabulary, not coordinate-plane line/circle equation work.

Extensions (aligned with a recorded caveat): the inequality-region family (r5281, r5737, r7320, r9709) uses linear-inequality region language that sits between IGCSE shading and the 1.3.2 graph-reading statement — recorded medium with caveats, never silently; the ellipse appears as *vocabulary* in r8408 (the line work is the tested skill) but as the *object of study* in elliptical-crossings / r8051 / r8216 / r8471 — those are non-overlaps, and the vocabulary/object line is drawn per resource; STEP/Special-paper depth (r5202, r6234, r7925, r9551, r9768) keeps the alignment because the objects are exactly lines and circles, with depth recorded; area-flavoured circle tasks (r8946, r9386, r7656) align on their circle-equation/line parts with the area work flagged to 1.4.

## 6. Primary picks of record

As lane 2 records: the Mode-2 shortlist section is retired (deep-link pilot dropped by operator directive 2026-10-22; text ships directly under ADR-UGM-0001 as amended 2026-10-23). One **primaryPick** per spec point — the corpus's own curation, starred on the hub index:

- **1.3.1**: Straight line pairs (`straight-line-pairs`, investigation) — equation-of-line construction from "sufficient information" constraints, the 1.3.1 statement as an open investigation.
- **1.3.2**: Teddy bear (`teddy-bear`, package-of-problems) — 13 circles matched to equations in both standard and expanded forms; the folded circle statement made kinesthetic.

Pattern/doctrine exemplars of this lane (Mode-4 candidates for the owning specs): `describing-straight-lines` (sufficient-information card sort), `lots-of-lines` (forms matching), `finding-circles` (how-many-points investigation), `pairs-of-circles` (expanded-form fluency), `simultaneous-squares` (construction investigation), `the-circle-of-apollonius-coordinate-edition` (locus derivation), `negatively-triangular` (create-your-own), `the-equation-of-a-straight-line` (forms exposition).

## 7. S1 provenance bridge status for this lane

44 of 61 aligned resources carry provenance tuples parsed in the P3b enrichment sheets (`geometry-of-equations` 31/38, `circles` 36/47 parsed station-wide): UCLES (Additional Mathematics, Mathematics A/B/C, Pure Mathematics, STEP), O&C/MEI, Oxford MAT, UKMT. As in lanes 1–2, the old UCLES series and MAT/UKMT rows do not collide with the CIE 9709 paper series — the S1 join against `syllabai-pastpapers` remains pending fleet-wide.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record** — enrichment #55, text #58 (main@91eed732), hub #308 (merged).
- Lane 2 (functions, 1.2.1–1.2.5): **of record** — enrichment + text #61 (a32c6c0f, MANIFEST v2), hub #312 (merged).
- Lane 3 (this lane, 1.3.1–1.3.2 with 1.3.1a/1.3.2a folded): cross-map of record here; corpus + enrichment land under task ids `T-UGM-MODE1-3` / `T-UGM-IMPORT-3`; hub consumption follows as `T-UGM-HUB-CONSUME-3`.
- Next hops by spine adjacency: 1.5 Trigonometry (`trigonometry-triangles-to-functions` + `trigonometry-compound-angles` stations), then 1.7/1.8 (calculus stations) where of-record item attachment is densest (51 + 14 parts). The `circles` station's radian-mensuration strand (20 non-overlaps recorded here) is the natural substrate for a future 1.4 Circular measure lane if the of-record spine ever grows one.

