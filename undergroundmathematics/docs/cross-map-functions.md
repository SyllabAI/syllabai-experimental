# Cross-map lane 2: UGM Combining Functions → CIE 9709 Pure 1 Functions

**Status**: lane 2 of the P3c generalisation (per §8 of `cross-map-quadratics.md`; `docs/INTEGRATION-PLAN.md` §4) · generated 2026-10-23 · machine-readable twin: `resources/derived/cross-map-functions.json`

## 1. What this is

The quadratics pilot (lane 1, 2026-10-22) mapped the UGM quadratics station onto CIE 9709 Pure 1 subtopic 1.1 (56/59 aligned) and its own §8 proposed the station-by-station generalisation. This lane executes the next hop, which lane 1 itself pre-flagged: the "Parabella" non-overlap note read *"parabola families belong with P1 Functions (1.2) / transformations"*. The lane maps the UGM **Combining Functions** station (38 resources: 23 review questions + 15 classroom-format resources) onto the of-record spine **CIE A Level Maths 9709 Pure 1 (2023–2025), subtopic 1.2 Functions** (spec points 1.2.1–1.2.5), with the same method: read each resource's question well / task statement against the spec-point wording of the of-record spine (`syllabai-v2/apps/hub/content/cie-a-level-maths-20-pure-1/curriculum.json` — the same parse the quadratics spine export came from), align one-to-many, never force.

**Station scope**: UGM spreads functions content over two stations. This lane draws on `combining-functions` only. The sibling `thinking-about-functions` (23 resources) is intentionally out of scope — its centre of mass is modulus functions, asymptotes and odd/even symmetry, which sit with CIE P3 / IAL P2 lanes, not P1 1.2. Boundary cases are named honestly in §5.

## 2. Lane coverage — headline numbers

| Metric | Value |
|---|---|
| UGM combining-functions resources mapped | 38 |
| Aligned to ≥1 CIE 9709 P1 spec point | 27 (71.1%) |
| Explicit non-overlap notes | 11 (incl. 2 interactive-only pages with no extractable text) |
| Alignment rows (one-to-many) | 50 (1.2.1: 11 · 1.2.2: 17 · 1.2.3: 10 · 1.2.4: 3 · 1.2.5: 9) |
| Resources with provenance tuple (S1 bridge) | 24 (13 UCLES + 10 Oxford MAT + 1 NRICH) |
| Success threshold (plan §7) | ≥70% aligned or non-overlap-noted |
| Threshold met | **yes** |

Station facts of record (P3b enrichment sheet): 38 resources, 23 review questions, 5 key questions covered, 18 resources with pervasive ideas, 0 teacher-support pages, 24 with parsed provenance. Unlike lane 1 (46/59 with UCLES/NRICH tuples), this station's review questions come overwhelmingly from Oxford MAT and old UCLES Mathematics B/C papers via the P3b parse.

## 3. Spec-point ↔ UGM resource map

Spec-point titles below are **verbatim from the of-record spine** (hub curriculum parse); the CIE spec parse carries known text artifacts (interleaved example text) — codes are authoritative.

### 1.2.1 — understand the terms function, domain, range, one-one function, inverse function and composition of functions

11 UGM resources (primary pick **forming-functions-defining-domains**):

- [review-question] Can we compose two simple functions? (`r9527`, confidence high)
- [review-question] Can we draw the graph of  $\left| x + [x] \right|$? (`r5362`, confidence high)
- [review-question] Can we find the ranges of $f$ and $g$, and the function $f \circ g$? (`r7607`, confidence high)
- [review-question] Can we sketch the graph of $g \colon x \to x - [x]$? (`r5764`, confidence high)
- [review-question] Can we work with the domain, codomain and range of a bijection? (`r5966`, confidence high)
- [package-of-problems] Compose! (`compose`, confidence high)
- [building-blocks] Composing gets me nowhere (`composing-gets-me-nowhere`, confidence high)
- [fluency-exercise] Domain and range dominoes (`domain-and-range-dominoes`, confidence high)
- [building-blocks] Forming functions — defining domains (`forming-functions-defining-domains`, confidence high) ⭐
- [building-blocks] Invertibles (`invertibles`, confidence high)
- [scaffolded-task] Making inverse functions (`making-inverse-functions`, confidence high)

### 1.2.2 — identify the range of a given function in simple cases, and find the composition of two given functions condition that a composite function

17 UGM resources (primary pick **compose**):

- [review-question] Can we compose these polynomial functions? (`r7553`, confidence high)
- [review-question] Can we compose two simple functions? (`r9527`, confidence high)
- [review-question] Can we draw the graph of  $\left| x + [x] \right|$? (`r5362`, confidence high)
- [review-question] Can we find an inverse and sketch a modulus function? (`r5646`, confidence high)
- [review-question] Can we find the inverse of a function in three parts? (`r8028`, confidence high)
- [review-question] Can we find the ranges of $f$ and $g$, and the function $f \circ g$? (`r7607`, confidence high)
- [review-question] Can we sketch and describe these composite functions? (`r5595`, confidence high)
- [review-question] Can we sketch the graph of $g \colon x \to x - [x]$? (`r5764`, confidence high)
- [review-question] Can we sketch the inverse of this composite function? (`r9824`, confidence high)
- [review-question] Can we work with the domain, codomain and range of a bijection? (`r5966`, confidence high)
- [package-of-problems] Compose! (`compose`, confidence high) ⭐
- [building-blocks] Composing gets me nowhere (`composing-gets-me-nowhere`, confidence high)
- [fluency-exercise] Domain and range dominoes (`domain-and-range-dominoes`, confidence high)
- [review-question] For which $x$-values does a function equal its inverse? (`r6735`, confidence high)
- [building-blocks] Forming functions — defining domains (`forming-functions-defining-domains`, confidence high)
- [review-question] When does this trig function have its maximum value? (`r8411`, confidence medium)
- [review-question] Which of these function statements are true? (`r9523`, confidence medium)

### 1.2.3 — determine whether or not a given function is one-one, and find the inverse of a one-one function in simple cases

10 UGM resources (primary pick **invertibles**):

- [review-question] Can we draw the graph of  $\left| x + [x] \right|$? (`r5362`, confidence high)
- [review-question] Can we find an inverse and sketch a modulus function? (`r5646`, confidence high)
- [review-question] Can we find the inverse of a function in three parts? (`r8028`, confidence high)
- [review-question] Can we find the ranges of $f$ and $g$, and the function $f \circ g$? (`r7607`, confidence high)
- [review-question] Can we sketch the inverse of this composite function? (`r9824`, confidence high)
- [review-question] Can we work with the domain, codomain and range of a bijection? (`r5966`, confidence high)
- [building-blocks] Composing gets me nowhere (`composing-gets-me-nowhere`, confidence high)
- [review-question] For which $x$-values does a function equal its inverse? (`r6735`, confidence high)
- [building-blocks] Invertibles (`invertibles`, confidence high) ⭐
- [scaffolded-task] Making inverse functions (`making-inverse-functions`, confidence high)

### 1.2.4 — illustrate in graphical terms the relation between Sketches should include an indication of the mirror a one-one function and its inverse line

3 UGM resources (primary pick **r9824**):

- [review-question] Can we sketch the inverse of this composite function? (`r9824`, confidence high) ⭐
- [review-question] For which $x$-values does a function equal its inverse? (`r6735`, confidence high)
- [building-blocks] Invertibles (`invertibles`, confidence high)

### 1.2.5 — understand and use the transformations of the Including use of the terms 'translation', 'reflection' graph of y = f( x ) given by and 'stretch' in describing transformations. Questions y = f( x ) + a , y = f( x + a ) , may involve algebraic or trigonometric functions, or other graphs with given features. y = a f( x ) , y = f( ax ) and simple combinations of these.

9 UGM resources (primary pick **order-order**):

- [review-question] Can we identify the right sketch of a transformed function? (`r7119`, confidence high)
- [review-question] Can we sketch and describe these composite functions? (`r5595`, confidence high)
- [review-question] How do these transformations change the graph of $f(x)$? (`r9673`, confidence high)
- [bigger-picture] It's a matter of perspective (`its-a-matter-of-perspective`, confidence medium)
- [food-for-thought] Name that graph again (`name-that-graph-again`, confidence medium)
- [investigation] Order! Order! (`order-order`, confidence high) ⭐
- [many-ways-problem] Transformers (`transformers`, confidence high)
- [package-of-problems] Translating or not? (`translating-or-not`, confidence high)
- [review-question] Which transformations give us the graph of $y=2^{x^2-4x+3}$? (`r6607`, confidence high)

## 4. Full alignment table

| UGM resource | Type | CIE P1 spec point(s) | Conf | Modes | Provenance | Note |
|---|---|---|---|---|---|---|
| Can we compose these polynomial functions? | review-question | 1.2.2 | high | 1 | Oxford (MAT) 2007 Q['Q2'] | Composition/iteration of polynomial functions f_n(f_n(...)); the maximum-value part rides P1 1.1 quadratics. |
| Can we compose two simple functions? | review-question | 1.2.2, 1.2.1 | high | 1 | Oxford (MAT) 2012 Q['Q2'] | Canonical composition builder: fg vs gf order, powers f^i, all forms yielding 4x+4, f^i g f^j g^k. |
| Can we draw the graph of  $\left\| x + [x] \right\|$ | review-question | 1.2.2, 1.2.1, 1.2.3 | high | 1 | UCLES 1979 Q['Q1'] [848/0] | Range of \|x+[x]\|; one-one question; inverse of a restricted mapping. Floor function is an extension beyond P1 "simple cases". |
| Can we find an inverse and sketch a modulus function | review-question | 1.2.3, 1.2.2 | high | 1 | UCLES 1989 Q['Q17'] [8175/1] | Find f⁻¹ for f:x->1/(3-2x); ff(2); self-mapping values. The \|x^2-4x+3\| sketch part is modulus-graph work beyond P1 1.2 (P2/P3 territory). |
| Can we find the inverse of a function in three parts | review-question | 1.2.3, 1.2.2 | high | 1 | UCLES 1972 Q['Q2'] [848/1] | Range of a three-part function, sketch, inverse relation and whether it is a function (one-one reasoning). Piecewise form extends "simple cases". |
| Can we find the ranges of $f$ and $g$, and the funct | review-question | 1.2.2, 1.2.3, 1.2.1 | high | 1 | UCLES 1981 Q['Q4'] [9202/1] | Ranges of log_a x and 1/x; f∘g with h(x)+f(x)=0; why g∘f needs a restricted domain (the composite-formation condition); define both inverses fully. log/exp vocabulary sits in 9709 P2/P3 — the range/composition/inverse skills are exactly 1.2.x. |
| Can we identify the right sketch of a transformed fu | review-question | 1.2.5 | high | 1 | Oxford (MAT) Q['Q1B'] [Specimen 2] | Identify the sketch of y=-f(x+1): translation then reflection — exactly the 1.2.5 vocabulary. |
| Can we sketch and describe these composite functions | review-question | 1.2.2, 1.2.5 | high | 1 | UCLES 1986 Q['Q13'] [9205/1 and 9206/1] | Sketch and describe f, gf, fg (e^x and x-1); the shifted-graph relationships read as translations. e^x vocabulary is P2/P3 in CIE. |
| Can we sketch the graph of $g \colon x \to x - [x]$? | review-question | 1.2.2, 1.2.1 | high | 1 | UCLES 1976 Q['Q2'] [848/1] | Ranges of [x] and x-[x]; sketch; solve f(x)=g(x) and fg(x)=gf(x). Floor function beyond P1 routine. |
| Can we sketch the inverse of this composite function | review-question | 1.2.4, 1.2.3, 1.2.2 | high | 1 | UCLES 1988 Q['Q16'] [9205/1 and 9206/1] | Define fg and f⁻¹; state the relationship between the graphs of f and fg and of f and f⁻¹ (mirror line); prove hf is not one-one. ln vocabulary is P2/P3 in CIE. |
| Can we work with the domain, codomain and range of a | review-question | 1.2.1, 1.2.2, 1.2.3 | high | 1 | UCLES 1980 Q['Q3'] [9202/2] | Domain/codomain/range/bijective vocabulary; range of f and of g∘f; bijectivity <-> inverse existence. phi/psi cycle extends beyond P1 routine. |
| Compose! | package-of-problems | 1.2.2, 1.2.1 | high | 1, 4 |  | Largest domain/range for A-D, then decompose composite functions — composition fluency package (pattern exemplar). |
| Composing gets me nowhere | building-blocks | 1.2.2, 1.2.3, 1.2.1 | high | 1 |  | ff(x)=x self-composition; self-inverse naming and examples — inverse fluency extension. |
| Domain and range dominoes | fluency-exercise | 1.2.1, 1.2.2 | high | 1, 4 |  | Describe domain/range in words then notation (domino fluency; pattern exemplar). |
| For which $x$-values does a function equal its inver | review-question | 1.2.3, 1.2.2, 1.2.4 | high | 1 | UCLES 1979 Q['Q10'] [986/1] | f⁻¹ and ff for f:x->1/(x+1); solve f=f⁻¹ and f=ff (both reduce to x^2+x-1=0). f=f⁻¹ invites the y=x mirror-line reading. |
| Forming functions — defining domains | building-blocks | 1.2.1, 1.2.2 | high | 1, 4 |  | Function = domain + rule + range; choose domains, state ranges, sketch; largest possible domain. Canonical 1.2.1 builder. |
| How do these transformations change the graph of $f( | review-question | 1.2.5 | high | 1 | UCLES 1988 Q['Q6'] [9205/1 and 9206/1] | Sketch y=f(x)+2, y=f(x+2), y=f(2x) tracking the maximum point — the spec list verbatim. |
| Invertibles | building-blocks | 1.2.3, 1.2.4, 1.2.1 | high | 1, 4 |  | Match functions with their inverses (incl. domain-restricted quadratics <-> surds, fractional forms) and with graphs; draw inverse graphs. Card-sort pattern exemplar. |
| It's a matter of perspective | bigger-picture | 1.2.5 | medium | 1 |  | Animated translation thinking on a parabola (GeoGebra applet; interactive recorded, not fetched). |
| Making inverse functions | scaffolded-task | 1.2.3, 1.2.1 | high | 1, 4 |  | Function-machine inversion of f(x)=2x+1, then algebraic rearranging — scaffolded 1.2.3 intro (pattern exemplar). |
| Name that graph again | food-for-thought | 1.2.5 | medium | 1 |  | Parabola equation via the parent/transformed (red/blue) reading; the equation-finding approaches ride 1.1/1.3. |
| Order! Order! | investigation | 1.2.5 | high | 1, 4 |  | Sketch transformed graphs for translations (-2,0)/(0,-4) and stretches x3 // x, 1/2 // y; write equations in terms of f. Investigation covering the full 1.2.5 list (pattern exemplar). |
| Transformers | many-ways-problem | 1.2.5 | high | 1, 4 |  | Sort 12 curve cards into transformation categories (translations/reflections/stretches) — many-ways-problem classification (pattern exemplar). |
| Translating or not? | package-of-problems | 1.2.5 | high | 1, 4 |  | y=1/(x+a) and y=1/(x^2+a) parameter study: genuine translations vs lookalikes (non-example design; pattern exemplar). |
| When does this trig function have its maximum value? | review-question | 1.2.2 | medium | 1 | Oxford (MAT) 2007 Q['Q1B'] | Greatest value of (3sin^2(10x+11)-7)^2 by inner->outer bounding — composite-range technique; the inner bounds come from P1 1.5.4. |
| Which of these function statements are true? | review-question | 1.2.2 | medium | 1 | UCLES 1979 Q['Q9'] [986/2] | True/false including the fg-order misconception (f:x^2, g:x^3 gives fg=x^6, not x^5); the implication-logic items sit beyond 1.2. |
| Which transformations give us the graph of $y=2^{x^2 | review-question | 1.2.5 | high | 1 | Oxford (MAT) 2014 Q['Q1I'] | Reach y=2^(x^2-4x+3) from y=2^(x^2) by stretch + translation — "simple combinations of these" verbatim. 2^x vocabulary is P2/P3 in CIE. |
| Can we identify the right sketch graph of this recip | review-question | — | — | — | Oxford (MAT) 2008 Q['Q1G'] | NON-OVERLAP for this lane: reciprocal-graph sketch via completing the square — rides 1.1.1/quadratics and curve sketching; the range work exceeds P1 1.2 "simple cases". |
| Can we identify the right sketch of a product of fun | review-question | — | — | — | Oxford (MAT) 2007 Q['Q1G'] | NON-OVERLAP for this lane: product of functions (2^-x sin^2 x^2) with trig beyond P1 — arithmetic combination, not composition/transformations. |
| Can we pick the graph of $y=\sin^2{\sqrt{x}}$? | review-question | — | — | — | Oxford (MAT) 2010 Q['Q1D'] | NON-OVERLAP for this lane: graph identification via trig behaviour of sin^2(sqrt x); composite structure noted, but the tested skill is trig beyond P1. |
| Can we sketch these four related curves? | review-question | — | — | — | UCLES 1988 Q['Q11'] [9205/2] | NON-OVERLAP for this lane: rational + modulus curve sketching with asymptotes — \|f(x)\| is not in the P1 1.2.5 transformation list. |
| Can we solve this equation with a sum of square root | review-question | — | — | — | UCLES 2011 Q['Q1'] | NON-OVERLAP for this lane: surds-equation solving via curve sketching; rides P1 surds/quadratics work, not 1.2.x. |
| Function builder I | fluency-exercise | — | — | — |  | NON-OVERLAP for this lane: sums/products of functions (function algebra) — not a P1 1.2 mode of combination; the sketching rides 1.1. |
| Going backwards | bigger-picture | — | — | — |  | NON-OVERLAP for this lane: bigger-picture page with no extractable text sections (interactive applet page) — no alignment claim possible. |
| How many solutions does this composite function equa | review-question | — | — | — | Oxford (MAT) 2009 Q['Q1E'] | NON-OVERLAP for this lane: composite shell (2^(sin^2 x)) but the tested skill is sin^2+cos^2=1 range bounding (P1 1.5.4) with P2/P3 exponential vocabulary. |
| Maths for dinner | bigger-picture | — | — | — |  | NON-OVERLAP for this lane: bigger-picture page with no extractable text sections (interactive applet page). |
| Picture the process II | food-for-thought | — | — | — | NRICH | NON-OVERLAP for this lane: real-world graph modelling (bacteria/drug/oscillation); not a 1.2.x skill. |
| When does $f$ satisfy the identity $f(t)-f(1-t)=g(t) | review-question | — | — | — | Oxford (MAT) 2013 Q['Q2'] | NON-OVERLAP for this lane: functional equations via substitution t->1-t — beyond P1 1.2 scope. |

## 5. Non-overlaps and extensions (never forced)

Non-overlaps (11):

- **r5868** — NON-OVERLAP for this lane: reciprocal-graph sketch via completing the square — rides 1.1.1/quadratics and curve sketching; the range work exceeds P1 1.2 "simple cases".
- **r8749** — NON-OVERLAP for this lane: product of functions (2^-x sin^2 x^2) with trig beyond P1 — arithmetic combination, not composition/transformations.
- **r6656** — NON-OVERLAP for this lane: graph identification via trig behaviour of sin^2(sqrt x); composite structure noted, but the tested skill is trig beyond P1.
- **r8427** — NON-OVERLAP for this lane: rational + modulus curve sketching with asymptotes — |f(x)| is not in the P1 1.2.5 transformation list.
- **r6653** — NON-OVERLAP for this lane: surds-equation solving via curve sketching; rides P1 surds/quadratics work, not 1.2.x.
- **function-builder-i** — NON-OVERLAP for this lane: sums/products of functions (function algebra) — not a P1 1.2 mode of combination; the sketching rides 1.1.
- **going-backwards** — NON-OVERLAP for this lane: bigger-picture page with no extractable text sections (interactive applet page) — no alignment claim possible.
- **r9924** — NON-OVERLAP for this lane: composite shell (2^(sin^2 x)) but the tested skill is sin^2+cos^2=1 range bounding (P1 1.5.4) with P2/P3 exponential vocabulary.
- **maths-for-dinner** — NON-OVERLAP for this lane: bigger-picture page with no extractable text sections (interactive applet page).
- **picture-the-process-ii** — NON-OVERLAP for this lane: real-world graph modelling (bacteria/drug/oscillation); not a 1.2.x skill.
- **r9798** — NON-OVERLAP for this lane: functional equations via substitution t->1-t — beyond P1 1.2 scope.

Extensions (aligned with a recorded caveat): the log/exp/eˣ/2ˣ vocabulary in r7607, r5595, r9824, r6607 sits in 9709 P2/P3, but the tested skills (range, composition, inverse, transformations) are exactly the 1.2.x statements; the floor-function items (r5362, r5764) and the three-part inverse (r8028) extend "simple cases" — recorded medium-confidence with caveats, never silently.

## 6. Primary picks of record

Lane 1's Mode-2 shortlist section is retired (the deep-link pilot was dropped by operator directive 2026-10-22 before implementation; the text now ships directly into SyllabAI under ADR-UGM-0001 as amended 2026-10-23). What the hub consumes instead is one **primaryPick** per spec point — the corpus's own curation, starred on the hub index:

- **1.2.1**: Forming functions — defining domains (`forming-functions-defining-domains`, building-blocks)
- **1.2.2**: Compose! (`compose`, package-of-problems)
- **1.2.3**: Invertibles (`invertibles`, building-blocks)
- **1.2.4**: Can we sketch the inverse of this composite function? (`r9824`, review-question)
- **1.2.5**: Order! Order! (`order-order`, investigation)

Pattern/doctrine exemplars of this lane (Mode-4 candidates for the owning specs): `compose` (decomposition fluency), `invertibles` (inverse card sort with graphs), `transformers` (transformation classification), `order-order` (full transformation list), `forming-functions-defining-domains` (domain-definition builder), `domain-and-range-dominoes` (notation fluency), `making-inverse-functions` (function-machine scaffold), `translating-or-not` (non-example design).

## 7. S1 provenance bridge status for this lane

24 of 38 resources carry provenance tuples (13 UCLES, 10 Oxford MAT, 1 NRICH), parsed in `resources/derived/enrichment-sheets/combining-functions.json` and re-recorded per row here. Of the 27 aligned resources, 16 carry provenance. As with lane 1, the old UCLES Mathematics B/C and Oxford MAT rows do not collide with the CIE 9709 paper series — the S1 join against `syllabai-pastpapers` remains pending fleet-wide.

## 8. Lane status and next hops

- Lane 1 (quadratics, 1.1.1–1.1.5): **of record** — enrichment `syllabai-resources` #55, text `syllabai-resources` #58 (merged main@91eed732), hub consumption `syllabai-v2` #308 (merged).
- Lane 2 (this lane, 1.2.1–1.2.5): cross-map of record here; corpus + enrichment + hub consumption land under task ids `T-UGM-MODE1-2` / `T-UGM-IMPORT-2` / `T-UGM-HUB-CONSUME-2`.
- Next hops by spine adjacency: 1.3 Coordinate geometry (`geometry-of-equations` + `circles` stations), then 1.5 Trigonometry (`trigonometry-triangles-to-functions` + `trigonometry-compound-angles`). The 2 interactive-only bigger-picture pages of this station stay unaligned until their applet content is addressable.

