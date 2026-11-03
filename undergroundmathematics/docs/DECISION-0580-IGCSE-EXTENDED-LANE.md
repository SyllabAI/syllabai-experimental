# Lane decision — the CIE IGCSE 0580 Extended course plane (2025–2027)

| | |
|---|---|
| **Status** | **Filed of record** — answers the lane-17 further-lanes pointer ("further UGM lanes would need a new course plane, operator's call — the igcse-extended spine export exists of record"); decision taken under operator order trace `1a1a2a96c22e39cd` ("…then the 0580 lane decision with its now-guaranteed P&S honest gaps"); lane 19 opens on operator ack |
| **Date** | 2026-11-03 |
| **Trace chain** | order `1a1a2a96c22e39cd` · UGM-SCOPE-1 survey `1a19d7e16d3217f1` / apply `1a1a0033a9ac36f5` / mirror `1a1a2a96c22e39cd` · quadratics contrast export @ the lane-1 era (`docs/cross-map-quadratics.md` §6) |
| **Spine of record** | `syllabai-v2` `apps/hub/spines/cie-igcse-maths-25-extended.json` @ main, blob sha `1458bcba45…` (generator `build_official_spines.py` cie adapter, family `tier_columns`, scope `code_prefix E`) |
| **Rulings applied** | UGM-SCOPE-1 (INTEGRATION-PLAN P7 tail, commit `d4e2c906`; ADR-UGM-0001 Status Tracking `95258536`) · §3 syllabus fit ("IGCSE overlap is partial… calculus stations out of scope") · Mode-1 cross-map law (never force alignment) |

## 1. The plane of record

CIE IGCSE Maths 0580 **Extended** tier, syllabus 2025–2027: **9 topics, 72
subtopics, 178 spec points** (E-prefixed scope rule). Unlike the P2
full-course plane (lane 18) there is **no twin-substrate law** here — the
0580 spine shares no verbatim codes with the served P1/P2/P3 planes, so
every row would be a fresh adjudication. 0580 Extended carries **no
calculus**: UGM's five calculus stations — the corpus's richest families —
are **out of scope for this plane by subject** (§3: "calculus stations out
of scope"). The effective substrate is the non-calculus station set.

## 2. Feasibility census of record (trace `1a1a2a96c22e39cd`)

Corpus sweep at decision granularity: all 855 resources × 9 topic families
(title/`friendlyName`/description register, the lanes' sweep method). The
full spine census (topics → subtopics → spec points) was walked from the
hub spine node graph. Candidate counts are **pre-adjudication upper
bounds** — the lanes' experience is that 30–60% of title-level hits are
false-family or beyond-spec; they size the effort, not the yield.

| Topic | SPs | Sweep candidates (top stations) | Feasibility of record |
|---|---|---|---|
| TE1 Number | 41 | 77 (thinking-about-numbers 16, scattered) | **partial/thin** — UGM's number work is A-level number-theory flavour; 0580 arithmetic/percentages/money has no dedicated UGM analogue; expect a heavy honest-empty tail |
| TE2 Algebra and graphs | 47 | **278** (combining-functions 35, quadratics 30, polynomials 19, thinking-about-algebra 16) | **STRONG anchor** — the 9-point quadratics contrast export (E2.2.3–E2.11.4) is already of record and the lane-1 pilot ran 56/59 = 95% on the parent content |
| TE3 Coordinate geometry | 10 | 52 (geometry-of-equations 13) | **STRONG anchor** — lane 3 served P1 1.3 from exactly this station family |
| TE4 Geometry | 19 | 82 (thinking-about-geometry 15, circles 8) | **partial** — 0580 angle-facts/constructions/loci thin in UGM; circle + geometry-station core workable |
| TE5 Mensuration | 9 | 79 (calculus-of-powers 17, circles 13) | **thin, sweep-inflated** — top hits are volumes-of-revolution / area-under-curve calculus contexts, not 0580 mensuration; expect near-empty |
| TE6 Trigonometry | 14 | 107 (TTxF 34, TCA 21) | **partial** — strong station presence but A-level depth; 0580 needs right-angle/bearings/sine-cosine-rule — §3's "easier review questions" register |
| TE7 Transformations and vectors | 14 | 40 (vector-geometry 11) | **thin** — UGM vectors are A-level vector algebra (lane-15 register); 0580 transformations (reflect/rotate/enlarge) essentially absent |
| TE8 Probability | 9 | **1** (a `random` false-positive) | **ZERO substrate — guaranteed honest gaps** (UGM-SCOPE-1 ruling 2) |
| TE9 Statistics | 15 | 9 (all mean/median asides in calculus contexts) | **ZERO substrate — guaranteed honest gaps** (UGM-SCOPE-1 ruling 2) |

**The now-guaranteed honest gaps:** TE8 + TE9 = **24 spec points
(13.5% of the plane) are pre-closed zero-substrate rows by UGM-SCOPE-1** —
they require no sweep at lane time and can never carry an alignment row
from UGM substrate. Realistically TE5 (9) and much of TE1 (41) / TE7 (14)
add to the honest-empty tail; the defensible UGM value concentrates in
**TE2 (47 SPs) + TE3 (10 SPs)** anchors with TE4 (19) / TE6 (14) partials.

## 3. Options

### Option A — full-course lane 19 in one pass (the P2 shape)

All 178 spec points adjudicated in one lane, honest-gaps filed fail-closed.

- **For**: one plane, complete closure, the lane-17/18 rhythm at plane scale.
- **Against**: no twin-substrate law (P2's 161 joins came from verbatim P2/P3
  twins — none exist here); a 178-point fresh adjudication with a projected
  majority-honest-empty tail; the largest single-lane effort of the
  programme for much of it pre-closed empty.

### Option B — contrast lanes, substrate-anchored *(recommended)*

Open the igcse-extended course plane, but run it as **per-topic contrast
lanes** ordered by the census: **lane 19 = TE2 Algebra and graphs** (the
record 9-point contrast export generalises to the full 47-point topic),
**lane 20 = TE3 Coordinate geometry**; TE4/TE6 open only on the lane-19/20
yield evidence, operator-gated. TE8/TE9 rows land as pre-ruled
honest-empty rows whenever a full-course closure is wanted — zero sweep
cost by UGM-SCOPE-1.

- **For**: effort lands where substrate is proven first (the lane-1
  contrast precedent); each lane sized like the existing rhythm; the
  guaranteed gaps cost nothing; stop-points are natural.
- **Against**: the plane stays open longer in wall-clock terms.

### Option C — do not open; keep the 9-point contrast export as final

- **For**: zero further effort.
- **Against**: discards the census-proven TE2/TE3 substrate (57 SPs) while
  the lane machinery, importer law and converter pre-flights are warm and
  idle; the lane-17 pointer stays unresolved.

## 4. Decision

**Adopt Option B** (filed under the operator's "proceed … then the 0580
lane decision" order). Specifically:

1. The **igcse-extended course plane is declared open of record**; lane 19
   = TE2 Algebra and graphs (47 spec points, E2-scope), prepared against
   the hub spine `1458bcba45…` and opened as `T-UGM-0580-19` on operator
   ack (the per-lane rhythm: "ordering is the operator's call" stands —
   this doc fixes the order and shape, the ack fires the lane).
2. **TE8 Probability + TE9 Statistics are pre-ruled honest-empty for all
   lanes of this plane** under UGM-SCOPE-1 rulings 1–2: no sweep, no
   candidates, honest-gap rows citing the ruling. The same pre-closure
   applies to any future 0580 P&S-adjacent spec point.
3. TE4/TE6 lanes are expected-but-gated; TE1/TE5/TE7 are expected-thin and
   default to honest-gap-heavy closures if opened at all.
4. Rights posture unchanged: mode-1 facts by default; any text landing
   rides the 2026-10-23 attestation per the P7 law.

## 5. Success measures (lane 19 preview)

- TE2: every one of the 47 spec points closed exactly (aligned /
  non-overlap / honest-empty), zero forced mappings — the lane-17 closure
  standard at topic scale.
- The 9 already-exported contrast points (E2.2.3–E2.11.4) must reconcile
  byte-true with the new lane's rows (the contrast export becomes the
  lane-19 preview pool, the lane-10/11 pre-baked-bearing pattern).
- Converter pre-flight byte-identity against the of-record bodies (the
  lane-N chain) before any corpus PR; MANIFEST bump per the v18 law.
