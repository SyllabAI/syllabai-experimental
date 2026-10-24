# Cross-map lane 10: the UGM exp-and-log plane → CIE 9709 Pure 3, 3.2 Logarithmic and exponential functions

## 1. What this is

Lane 10 of the P3c generalisation, and the **second lane on the pure-3 course plane**: the Pure 1 spine closed of
record at 33 rows (1.1–1.8) with lane 8, lane 9 opened the pure-3 plane at 3.1 Algebra, and both the plan's recorded
next substrates ("3.2 Logarithmic and exponential functions first — the UGM exp-and-log station is essentially
untouched") and lane 9's cross-map §8 pre-embeds ("this lane's `to-log-or-not-to-log` + `powerful-derivatives`
non-overlaps already carry 3.2 bearings") make **Pure 3 subtopic 3.2** the natural lane 10. Target of record:
`cie-a-level-maths-20-pure-3`, spec points 3.2.1–3.2.4, verbatim from the hub spine parse (`apps/hub/spines/cie-a-level-maths-20-pure-3.json`;
the dropped-math artifacts in the 3.2.2/3.2.3 titles are carried verbatim — no `T-SPECS` repair needed, no fold
fragments). Operator order (trace `1a16fc8102cb1711`): *"merging #358 then proceed with lane 10"* — #358
(T-UGM-HUB-CONSUME-9) was already merged of record at arrival (`7cf01690`, R0-auto) → verified ALL GREEN → lane 10
built per the P3c rhythm.

## 2. Lane coverage — headline numbers

| measure | value |
|---|---|
| corpus screened | 855 resources / 25 stations |
| raw hits → candidates | 71 → **71** (60 pass-1 title/description sweep + 11 pass-2 body-text sweep; all unique) |
| aligned rows | **39** = 34 fresh rows (over 34 substrate resources; all single-code) + **5 cross-course rows** |
| cross-course joins | **5 one-to-many** (r9824, r7607 lane-2 functions; r6137, r8260 lane-6 series; r7184 lane-5 trigonometry) — all riding bodies of record, join law unchanged; **no flips** |
| fresh non-overlaps | **26 recorded by reference only** (`bodyImported: false` — the lane-8 candidate-model law), incl. 1 sweep false positive (a timber log) |
| of-record candidates rejected | **6 with reasons** (r9312 1.6/3.5; floppy-hair 1.7; powerful-quads 1.1.5; r5126, r8694 3.1.5-of-record; i-can-see-u 1.7) |
| substrate stations | exp-and-log **31 of 34** (the dedicated station, 38 fresh of 40) + strays to-the-limit (calculus-trig-log), r7077 + powerful-fractions (thinking-about-algebra) |

**Primary picks of record:** `proving-laws-of-logs` (3.2.1) / `an-irrational-inequality` (3.2.2) / `to-log-or-not-to-log` (3.2.3) / `how-far-did-the-earth-move` (3.2.4).

## 3. Per-spec-point detail

### 3.2.1 — relationship between logarithms and indices; the laws of logarithms (excluding change of base)

16 fresh rows (15 exp-and-log + r6806... all exp-and-log): the proof-sort `proving-laws-of-logs` (pick),
no-calculator law evaluation (r9976, r7471, r9680, r7231, r5080), definition-level rewrites (r7298, r9381,
summing-to-one, factorial-fragments), pre-formal index reading (see-the-power, calculators1950), base relations
derived from the definition (changing-bases, log-lattice, log-lineup), and the reciprocal-relation limb of r6806.
The **change-of-base exclusion is handled honestly**: changing-bases, r7298, r7845 and log-lattice derive base
relations from the definition of the logarithm as the index — the formula itself is never required.

### 3.2.2 — definition and properties of e; e^x/ln x graphs; inverse functions

**The thin limb (lane-9 modulus-limb finding, pure-3 edition)**: 2 fresh rows + 1 join.
`an-irrational-inequality` (pick — e^π vs π^e through e's properties), `to-the-limit` (the special case
lim_(h→0)(a^h−1)/h = 1 that defines e, inside the first-principles derivation), and the r9824 join
(f⁻¹ = e^x, fg = −ln x, graph reflections — the inverse-pair law verbatim, body of record under lane 2).
The reason is structural: **UGM's e/ln corpus rides calculus work** — 11 sweep hits carry the lane-7/8 recorded
P3 3.4/3.5 bearings (powerful-derivatives, differentiating-exponentials, r6530, r6620, r7431, r8134, r8671, r9484,
r9898, two-for-one, inverse-integrals, r7903) and stand on those routings. The station's exponential-graph
intuition family (how-fast-does-it-grow, r5156, reach-for-the-stars, r8013) contains **zero e/ln mentions** and
routes out honestly as 3.2.2 prerequisites.

### 3.2.3 — logarithms on indicial equations and inequalities

14 fresh rows: the method-decision card sort `to-log-or-not-to-log` (pick — **flipping the lane-9
nonOverlapByReference row of record**: the lane-9 reason was the surd card, but the card sort's tested skill is
exactly the 3.2.3 method decision), log-rearranged systems (r9366, r5462, r7845), exponent reduction (r5940,
r7606, r7384, r5103), log-bounds and digit problems (r9747, r6045, r9381-adjacent r7015, r6414), plus the two
lane-5 pre-baked strays (r7077, powerful-fractions). Join: r8260's log-equation limb.

### 3.2.4 — logarithmic transformation to linear form

2 fresh rows, both rich investigations, both lane-5 pre-baked: `how-far-did-the-earth-move` (pick — Richter
magnitude M_L = log₁₀(A/A₀) then log-log linearisation of the energy data) and `plotting-planets` (Kepler-type
power laws recovered by taking logarithms of the planetary data). The pick goes to the resource whose
linearisation-and-constants work is the explicit task.

## 4. Cross-course joins (5, one-to-many, bodies of record)

| resource | prior of record | 3.2 limb | text under |
|---|---|---|---|
| r9824 (combining-functions) | lane-functions 1.2.2/1.2.3/1.2.4 | 3.2.2 — f⁻¹ = e^x, fg = −ln x, reflections | UGM-Resources/pure-1-functions |
| r7607 (combining-functions) | lane-functions 1.2.1/1.2.2/1.2.3 | 3.2.1 — log_a(1/x) + log_a x = 0 | UGM-Resources/pure-1-functions |
| r6137 (sequences) | lane-series 1.6 | 3.2.1 — the GP limb proved via logs | UGM-Resources/pure-1-series |
| r8260 (exp-and-log) | lane-series 1.6.3 | 3.2.3 — log₂x + log₃x = 1 + log₄x | UGM-Resources/pure-1-series |
| r7184 (exp-and-log) | lane-trigonometry 1.5 (stray) | 3.2.1 — log₂ vs log₁₀ comparison limbs | UGM-Resources/pure-1-trigonometry |

## 5. Non-overlaps of record (26 by reference)

Station-local (7): the **no-e/ln family** (how-fast-does-it-grow, r5156, reach-for-the-stars, r8013 — the
exponential-graph intuition resources, 0 e/ln mentions, honest 3.2.2 prerequisites) + the **no-extractable-text
trio** (changing-bases-teacher-support, to-log-or-not-to-log-teacher-support, rediscovering-log-mercator —
video/interactive-only pages, zero sections in the crawl of record). Elsewhere (19): the lane-7/8 P3 3.4/3.5
bearing pool standing on its recorded routings (powerful-derivatives, differentiating-expectations-exponentials,
odd-one-out, can-you-find-chain-rule-edition, r7431, r7106, two-for-one, inverse-integrals, r7903, r6530, r9898,
r9484, r8134, r6620, r8671), the index-law pair (r8779, index-issues), weight-pulling (beyond spec), and the
sweep false positive r7385 (a floating timber log).

## 6. Of-record candidates rejected (6)

r9312 (1.6 GP closure + P3-Integration), floppy-hair (1.7), powerful-quads (1.1.5), r5126 + r8694 (3.1.5 of
record from lane 9 — same course plane), i-can-see-u (1.7). Reasons of record in `sweepRouting`.

## 7. Findings of record

1. **The lane-5 pre-baked bearings all landed.** Ten resources carried lane-5 sweepRouting reasons pointing at
   "2.2 Logarithmic and exponential functions" (the pre-repair P3 numbering = today's 3.2): `changing-bases`, `log-lineup`, `plotting-planets`, `powerful-fractions`, `r5080`, `r7077`, `r9747`, `r9976`, `reach-for-the-stars`, `see-the-power`.
   Nine land aligned this lane; reach-for-the-stars routes out honestly (no e/ln). The lane-6 recorded
   `to-log-or-not-to-log`/`powerful-derivatives` bearings also resolved — one flip-to-aligned, one standing 3.4
   routing.
2. **The exp-and-log station is the 3.2 workhorse and was essentially untouched**: before this lane the fleet
   held only 2 of its 40 resources (r7184 lane-5 stray, r8260 lane-6 review question) — both now joined; 31 of
   34 fresh bodies are station-local.
3. **3.2.2 is structurally thin in UGM** — the e/ln content rides differentiation/integration work whose P3
   3.4/3.5 bearings were recorded at lanes 7/8. Two fresh rows + one join carry the limb; the bearings stand.
4. **Review-question provenance is Oxford-MAT/STEP/UCLES-heavy** in this lane (22 of 34 carry exam provenance,
   first lines verbatim from `pageMeta.acknowledgement`) — the MEI-sourced an-irrational-inequality's first line
   is carried verbatim per the lane-9 law even though the line break lands mid-sentence ("Based on an").
5. No fold fragments: the four spine rows 3.2.1–3.2.4 are verbatim of record (the 3.2.2/3.2.3 title artifacts are
   the hub parse rows verbatim).

## 8. Next hops by spine adjacency

Pure 3 continues in syllabus order: **3.3 Trigonometry** is the natural lane 11 — the pool is pre-baked (the
lane-5 compound-angles station recorded 24 non-overlaps pointing at "P3 2.3" = today's 3.3, plus TTF residuals).
Then **3.4 Differentiation** (the lane-7 recorded bearings pool: powerful-derivatives, r6530, r6620, r7431,
r8134, r8671, r9484, r9898 + differentiating-exponentials) and **3.5 Integration** (two-for-one, inverse-integrals,
stretching-an-integral, integral-sorting, integral-chasing-2, r9085, r8774, r7903), with 3.6–3.9 (numerical,
vectors, differential equations, complex numbers) beyond. Ordering is the operator's call. The hub consume
(T-UGM-HUB-CONSUME-10) extends the pure-3 bundle plane — a separate operator order after this PR merges.
