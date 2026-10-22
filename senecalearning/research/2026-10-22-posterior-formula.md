# The Seneca posterior formula — decoded (session 6, 2026-10-22)

**Result: Seneca's mastery update is NOT BKT and never was.** The in-session
"posterior" that session 4 observed (`startingProficiency 0 → endingProficiency
0.495`, score 0.89) and session 5 could not recover is a **two-component
saturating blend, computed client-side, rounded to 3 decimal places, and
blinded to the server**. This note closes the last gap from session 5 and
corrects the "client-computed BKT posterior" framing used in earlier notes.

Verified against **four independent session emits** (three captured live in
this session under controlled scoring, one from session 4), plus two live
decay observations and one live spacing increment. Every emitted proficiency
reproduces to the exact 3-dp value from the formula below.

---

## 1. TL;DR — the formula

For a studied section, with the section's lifetime stats record
`(timesStudied, averageScore, spacing)`:

```
y = round( 50 · min(1, timesStudied / (spacing · 3))      # exposure component
         + 50 · min(1, averageScore / 0.9) )              # accuracy component
      # integer 0..100; constants h=3, g=0.9, w1=w2=50 verbatim in the bundle

endingProficiency = Σ_sections y(sectionStats) / (100 · N)
      # N = number of units in the aggregation group; N=2 observed here
      # (States of Matter + its unstudied sibling "Changing State" — y=0)
```

- `averageScore` is the **cumulative mean of tested-module scores across all
  sessions of that section** (not the current session's score).
- `timesStudied` saturates the exposure term quickly (any ≥3 module-touches
  against `spacing ≥ 1` pins it at 50), so in practice **the accuracy term
  alone moves the number** once a section has been studied a few times.
- The emitted `endingProficiency` is stored as-is; what the UI and the next
  session's `startingProficiency` show is the **Ebbinghaus fade** of it
  (session 5's decode, re-confirmed live, §5).
- The server accepts all of this without validation (`POST /api/session` is a
  blind write; stats projections copy `session.endingProficiency` verbatim).

## 2. The four-point proof

All sessions on the same section (Edexcel iGCSE Chemistry → States of Matter,
section `0fde17b0-…`, course `967b4370-…`), adaptive/wrong-answers modes,
teacher account, one browser pass on 2026-10-22.

| # | session | cumulative tested-module scores | mean (`averageScore`) | y = round(50+50·m/0.9) | predicted | emitted |
|---|---------|--------------------------------|----------------------|------------------------|-----------|---------|
| 1 | session 4 (Task 4 walk) | {1, 1, 0.67} | 0.8889 | round(99.39) = **99** | 99/200 = **0.495** | **0.495** ✓ |
| 2 | A — mixed ({T,T},{F},{T,T,T}) | +{1,0,1} → 7/9? no: 4.67/6 | 0.7783 | round(93.24) = **93** | 93/200 = **0.465** | **0.465** ✓ |
| 3 | C — mostly wrong (2 of 5 modules correct; toggles [F,F,F]) | +{1,.75,0,0,1} → 7.42/11 | 0.6745 | round(87.47) = **87** | 87/200 = **0.435** | **0.435** ✓ |
| 4 | D — 100% correct wrong-answers retry | +{1,1,1} → 10.42/14 | 0.7440 | round(91.35) = **91** | 91/200 = **0.455** | **0.455** ✓ |

Notes on the table:

- Session A's emitted `sessionScore` was 0.667 = mean of module scores
  {1, 0, 1} (concept/notes modules score null and are excluded). The
  `averageScore` input to `y` is the **cross-session** mean of those tested
  modules — this is what makes A land on 93, not on a current-session value.
- Session C was engineered to fail (wrong first attempts on the MCs, toggles
  left all-false, wrong-then-corrected wordfills — the correction attempts are
  recorded in `hits[]` but only the final per-input truth feeds the scores).
  Posterior dropped 0.465 → 0.435 purely via the accuracy term.
- Session D (wrong-answers mode, all correct) shows the update is
  **mode-independent** and that a perfect session yields only +0.020: the
  exposure term is already saturated, and the accuracy term is capped by
  `min(·, 1)` against the 0.9 constant — a ceiling Seneca builds in so that
  even flawless performance cannot push a section past
  `round(50 + 50·1)/200 = 0.500` per pass through the group denominator.
- The "0 → 0.495" from session 4 that looked like a BKT posterior was simply
  y=99 (first session, exposure saturated, mean 0.889) divided by 200. The
  0.495/0.465/0.435 −0.03 "steps" that looked like decay-quantization are
  just integer-y arithmetic over the same denominator.

## 3. Where the value is computed — the full client chain

Recovered by one authenticated browser pass (stack-trapping redux subscriber
during a live session) plus static extraction. **Critical tooling note: 602 of
the 948 captured bundles were stored gzip-compressed and therefore invisible
to earlier greps — the "unreachable by name" gap from session 5 was a tooling
artifact, not a missing chunk.** All chunks are decompressed in the local
corpus now.

```
player UI (Finish / last-module complete)
  └─ SessionImageVideo-Bd_2iceM.js  — wires onSessionComplete, dispatches item actions
       └─ types-8ARz3kZb.js  `sn(sessionId)` — the emit thunk:
            1. memory-roll side action zt(sessionId)
            2. dispatch COMPLETE_SESSION with payload built by `nn()`:
                 endingProficiency      = ut(state, sectionId)     ← THE FORMULA
                 endingCourseProficiency= ct(state, courseId)
                 endingCourseScore      = lt(state, courseId, sectionId, sessionScore)
                 sessionScore           = F(state, sessionId)      (mean of tested module scores)
                 averageScore           = Ze(state, sessionId)     (same mean, payload field)
            3. re-read store → build wire payload `qt()`/`Z()` (fields mirror the
               CompleteSessionPayload defaults; platform/clientVersion/userId envelope)
            4. `await xt(payload)` → clientActions barrel →
               sessionService.emitSession → POST /api/session (blind 200)
```

The math itself (exact constants):

```js
// course-DlonVoBz.js (export surface: a/i/n/o/r/t)
var h = 3, g = 0.9, _ = 50, v = 50;

function y(e){                                   // per-unit 0..100 score
  if (!e || !e.spacing) return 0;
  let {timesStudied: t, averageScore: n, spacing: r} = e,
      i = Math.min(1, t / (r * h)),              // exposure saturation
      a = n === null ? 0 : Math.min(1, n / g);   // accuracy saturation
  return Math.round(i * _ + a * v);
}

function b(e, t){                                // per-unit display value (faded)
  return e ? calculateProficiencyFade(y(e), e.spacing, e.lastStudied, t) : 0;
}
function x(e, t, n = y){                         // group aggregate → 0..1
  return e.reduce((e, t) => e + n(t), 0) / (100 * t);
}
```

`ut` (the `endingProficiency` selector) resolves through
`section-DirnkDZH.js: _ → merge(persisted section stats, live section stats)
→ map each unit to y → x(list, N)`. The `calculateProficiencyFade` inside `b`
is the session-5 decay (`P·exp(−Δt_days / τ)`, `τ = 4·e^(spacing^1.4)`); at
emit time `t = now` so the stored posterior is unfaded, while the *next*
session's `startingProficiency` is its faded value.

## 4. Course-level aggregates (same emit, exact fractions)

Observed in the same payloads, all exact rational identities:

- `endingCourseProficiency = endingProficiency / 208` (single studied section;
  208 = the course's proficiency-bearing section count). D emitted
  0.0021875 = 0.455/208 exactly; A 0.0022355769… = 0.465/208 exactly.
- `endingCourseScore = sectionBestScore / 244`. D: 1/244 = 0.00409836065573…
  exactly; A and C: 0.89/244 (best score unchanged by those sessions). The
  244 denominator is visible in the product UI ("1 /244" sections counter on
  the course header). The course-level selector (`C`/`p` in course-DlonVoBz)
  replaces the studied section's contribution with
  `max(sessionScore, existing)` before averaging — best-score semantics.
- Other course counters seen in the UI header: 164 and 1430 (modules and
  contents respectively) — not yet tied to emitted fields.

## 5. Live re-confirmation of the session-5 decay + spacing scheduler

- Starting proficiencies arrived pre-faded and matched `τ = 4·e^(spacing^1.4)`
  exactly: D started at 0.4348007590641192 from a stored 0.435 ≈ 20 minutes
  after C finished (τ = 18.12 d at spacing 1.3452 → predicted 0.434796…).
  C started at 0.4645320376226589 from stored 0.465 (~40 min after A).
- Spacing incremented 1.3451737338 → 1.3492407596 across a 16 m 08 s gap,
  matching session 5's `updateSpacingValue` fractional bump
  (`f = gap/optimal(s)`, `optimal = 1440·(1.5s²+1.5s−2)` min → f = 0.0040670)
  to 10 decimal places. Two independent live confirmations of the session-5
  decode; nothing about it needed revision.

## 6. What this means (and what it is not)

- **Not BKT.** There is no per-skill knowledge parameter, no slip/guess
  pair, no Bayesian conditioning on responses. The `hits[]` per-input ledger
  is recorded and emitted but does **not** feed the posterior — only final
  per-module scores (mean = `averageScore`) do. Wrong-then-corrected answers
  score identically to first-try corrects at the proficiency level (they do
  cost "hearts" and XP-adjacent UX in-session).
- **The mastery number is a spaced-repetition bookkeeping value**, not a
  knowledge estimate: `y` blends how *often* you've studied relative to the
  schedule with how *accurately*, caps at 100, gets averaged over the sibling
  group, and is then decayed for display. Its job is to drive the UI ring,
  the memory-strength pips, and the spacing ladder — which it does fine.
- **The server is fully trusted.** Every proficiency field in the emit is
  client-computed; the stats service copies them. (Session 4's architectural
  conclusion stands, now with the exact function.)
- **Rounding discipline:** stored posterior = 3-dp value (integer y over the
  group denominator); displays = faded full-precision floats; course fields =
  exact rational divisions by section counts. No hidden state.

## 7. Direct consequences for SyllabAI

1. **Keep server-side BKT (or any per-response update).** Seneca's design
   confirms the competitive space: a client-trusted aggregate that cannot see
   per-response evidence. SyllabAI's server-side BKT over the `hits[]`-style
   ledger (already adopted from session 4) strictly dominates informationally.
2. **Steal the two-component blend as a *display* metric.** Seneca's
   `y = 50·sat(exposure) + 50·sat(accuracy/0.9)` is a cheap, explainable
   "strength" gauge that pairs naturally with an SR scheduler (it uses the
   same `spacing` state as the ladder). Candidate for the SyllabAI UI ring,
   computed server-side from BKT posteriors instead of raw means.
3. **The 0.9 accuracy cap is a defensible product choice** — mastery displays
   that saturate below 100% leave headroom for the decay animation to feel
   meaningful. Consider `min(1, BKT_posterior/0.9)` for the same effect.
4. **Group-denominator averaging dilutes single-section updates** (a perfect
   session moved the course needle by 0.0004). If SyllabAI shows course-level
   mastery, weight by recency or study count, not by section count.
5. **Emit-then-reconcile is viable at scale.** Seneca buffers evidence
   client-side and flushes one REST emit at session end (with a reconcile
   path for offline). SyllabAI's planned server-authoritative model is
   stronger, but the single-emit session envelope (payload shape already
   documented in captures/sessions/) remains a good offline-tolerance
   blueprint.

## 8. Reproduction recipe

Local corpus: `resources/captures/js/` (948 chunks, local-only per IP notes;
now fully decompressed — re-run the gzip sweep if re-fetching).

1. `types-8ARz3kZb.js` — emit thunk `sn`, payload assembly `nn` (contains the
   `COMPLETE_SESSION` dispatch with `endingProficiency: ut(a,p)`), wire
   builders `Z`/`Ut`, and the invalid-field validator `ln` (which confirms
   `endingProficiency` is mandatory for non-multiSection/non-vocabulary
   sessions).
2. `section-DirnkDZH.js` — `ut` (`_`): merge persisted+live stats, map `y`,
   aggregate `x(list, N)`.
3. `course-DlonVoBz.js` — constants `h=3, g=0.9, _=50, v=50`; `y`, `b` (fade
   wrapper), `x` (group average), course-level `C`/`p`.
4. `state-B6uAS2cl.js` — section-stats model (fields `timesStudied`,
   `averageScore`, `spacing`, …), `calculateProficiencyFade` module (session
   5), spacing scheduler, and the blind `COMPLETE_SESSION` reducers.
5. `signOut-B19aTuAB.js` — `SessionServiceClient.emitSession` (blind POST) +
   RequestMaker (the runtime stack-trap from the browser pass landed here,
   which is what broke the search open).
6. `session-C9dh1Pqk.js` — session selectors (`Zn` = reader for
   `session.endingProficiency` used by the wire builder).

Runtime trap that worked: install a `store.subscribe` listener on the live
Redux store (reached via the React fiber walk from `#root`), diff the
`sessions` slice on every notification, and capture `new Error().stack` —
redux subscribers run synchronously inside `dispatch`, so a synchronous
completion path (Finish click / last item) yields the dispatching chunk.
Dispatch *patching* fails (react-redux binds dispatch early); subscribe does
not. Then diff `performance`/network-loaded chunk names against the local
corpus and **decompress before grepping** (the 602-file gzip miss cost most
of a session).

## 9. Open items (smaller now)

- Exact semantics of the group denominator `N` (2 observed). Hypothesis: the
  sibling-section group under the topic (States of Matter + Changing State).
  Verifiable by studying a section whose topic has 3+ children and checking
  the denominator shift. The four fits are invariant to this choice only
  because exactly one unit had stats.
- Course counters 164 (modules?) and 1430 (contents?) — not yet tied to
  emitted fields.
- The memory-roll side action `zt(sessionId)` in the emit thunk (won-memory
  lottery seen in session 4) — partially read, not fully traced.
- Source maps remain unpublished; the decode above is from minified bundles
  (all quoted constants are verbatim).

## 10. File cross-references

- Supersedes the "client-computed BKT posterior" wording in
  `research/2026-10-22-session-lifecycle.md` (§emit) and
  `research/2026-10-22-pedagogy-model.md`; both carry addenda pointing here.
- Decay/scheduler math: `research/2026-10-22-memory-math.md` (unchanged,
  now with two live confirmations, §5).
- Raw evidence (sanitized): `resources/captures/sessions/` —
  `session-emit-A-mixed.json`, `session-emit-C-mostly-wrong.json` (userId
  redacted; live capture under controlled scoring), joining the existing
  session-4 exemplar.
