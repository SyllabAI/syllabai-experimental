# Memory Math — the exact forgetting-curve + spacing scheduler (decoded)

**Date:** 2026-10-22 (Phase 2, session 5) · **Method:** static analysis of the app's
JS bundles. The Phase-1/4 corpus (292 chunks) was extended with ~60 targeted lazy
route chunks (see §6 for the reproducible fetch recipe). Minified code was decoded
by hand; every constant below is verbatim from the bundle, and the formulas were
re-implemented and sanity-checked numerically (§4).

**Headline: Seneca's durable learner model is NOT BKT.** The prior→posterior
value we saw in the session emit (`startingProficiency 0 → endingProficiency
0.495`, `2026-10-22-session-lifecycle.md`) is computed inside the session player
and shipped to the server as an opaque number. The *decodable* model — the one
with real math in the client — is an **Ebbinghaus exponential forgetting curve
with a super-exponential time constant driven by a fractional spacing counter**,
plus a sweet-spot-bumped spacing update. That is the machinery SyllabAI should
mirror (and improve on server-side).

---

## 1. Where the math lives

| Concern | Chunk | Function(s) (minified → decoded names) |
|---|---|---|
| Fade + spacing math | `state-B6uAS2cl.js` | `calculateProficiencyFade`, `calculateProficiencyFadeCoefficient`, `updateSpacingValue`, `calculateOptimalSpacingTimeInMins` |
| Stats projections | `out-58RVUDXs.js` (dup in `state-Dd7llvej.js`) | `updateProficiency`, `updateRecentSectionEvents`, `updateBestScore/WorstScore/…` |
| Session reducer | `store-NUmMdL8-.js` | `COMPLETE_SESSION` merge of `{endingProficiency, endingCourseProficiency, endingCourseScore, sessionScore, …}` |
| Section-stats reducer | `state-B6uAS2cl.js` | `U(stats, action, {logUpdateSpacingWarnings})` — wires the above together |
| Constants | same chunks | see below |

Key decoded constants (verbatim):

```js
var A = 4;        // base time-constant (days)
var O = 1.4;      // spacing exponent for the time constant
var S = 1440;     // minutes per day (unit converter)
// constants module:
CORRECT_SCORE = 1;
SPACING_DECIMALS = 10;
MAX_NUMBER_OF_RECENT_SECTION_EVENTS = 10;
```

## 2. The forgetting curve — `calculateProficiencyFade`

Decoded from `state-B6uAS2cl.js` (names restored from exported symbols and
Sentry log labels like `calcu…lateProficiencyFade recieved/calculated incorrect
values`):

```js
// elapsed time in days
transformedTime   = (currentTime − lastStudied) [minutes] / 1440

// time constant τ from the spacing counter
transformedSpacing = 4 · Math.exp(spacing ** 1.4)          // τ in days

// fade coefficient
coefficient = isInvalid(transformedTime) || isInvalid(transformedSpacing)
            ? 1                                            // fail-open: no fade
            : Math.exp(−transformedTime / transformedSpacing)

// faded proficiency
faded = (proficiency == null || proficiency < 0) ? 0
      : proficiency · coefficient
```

In closed form:

```
P_display(t) = P_stored · exp( − Δt_days / τ(spacing) ),   τ(spacing) = 4 · e^(spacing^1.4)  [days]
```

Numerics (verified):

| spacing | τ = 4·e^(s^1.4) (days) | half-life (days) |
|---:|---:|---:|
| 1 | 10.9 | 7.5 |
| 2 | 56.0 | 38.8 |
| 3 | 420.7 | 291.6 |
| 4 | 4,233 | 2,934 |

Guards: invalid/non-finite inputs → coefficient 1 (no fade); negative
proficiency → 0. Warnings are wired to Sentry (`convertToLogObject` payloads),
so production logs would expose any model misuse.

**Where fade is applied:** at *read* time (UI "memory strength", recommendation
scoring). The *stored* section `proficiency` in the stats service is the raw
last posterior — `updateProficiency(stats, action) = action.session.endingProficiency`
verbatim — i.e. each completed session **replaces** the stored value with the
player's posterior, and decay is re-applied on the fly. The next session's
`startingProficiency` is the faded value at session start.

## 3. The spacing scheduler — `updateSpacingValue` + `calculateOptimalSpacingTimeInMins`

Decoded:

```js
// optimal review interval (minutes) — a hand-tuned quadratic in spacing
optimalMins(spacing) = 1440 · (1.5·spacing² + 1.5·spacing − 2)

// spacing bump after a study event
updateSpacingValue(spacing, prevTimeStudied, currentTimeStudied):
  if spacing == null            → 1            // first-ever session
  if spacing < 1                → warn + 1     // clamp (Sentry)
  gap   = currentTimeStudied − prevTimeStudied   [minutes]
  opt   = optimalMins(spacing)
  f     = gap < 0            ? 0               // clock skew → no bump
        : gap ≤ opt          ? gap / opt       // early: proportional credit
        : /* overdue */        max(0, −gap/(14·opt) + (1 + 1/14))
  return round(spacing + f, 10)                  // SPACING_DECIMALS = 10
```

Properties (all verified numerically):

- `optimal(spacing)` in days: **1, 7, 16, 28, 43, …, 163 (s=10)** — the quadratic
  is clearly hand-tuned to give round intervals (1 day, 1 week, ~2 weeks, 4 weeks).
- Reviewing **exactly at the optimal interval doubles the spacing** (f = 1).
- Reviewing **early** gives proportional partial credit (f = gap/optimal) — no
  punishment, just slower growth.
- Reviewing **overdue** decays the credit **linearly**, hitting f = 0 at
  **gap = 15 × optimal** (the function is continuous at gap = optimal and
  non-negative; the 1/14 terms implement exactly that 15× window).
- **Spacing never decreases** — f ≥ 0 always. It is a monotonically increasing
  confidence counter, capped at +1 per review.
- `spacing` is **fractional** (10 dp) — matches the captured `spacing: 1` after
  the first session.

## 4. Putting it together (the full loop)

```
session start     startingProficiency = fade(P_stored, spacing, now − lastStudied)
during session    modules answered; per-input scoring (hits[]/inputScores[])
session end       player computes endingProficiency (CLIENT-side, opaque formula)
                  POST /api/session {session{starting…, ending…}, modules[]}
stats write       P_stored ← endingProficiency          (replace, no blending)
                  spacing ← updateSpacingValue(spacing, lastStudied, timeFinished)
                  recentSectionEvents ← unshift({starting…, ending…, averageScore})
                  (ring buffer capped at 10 — MAX_NUMBER_OF_RECENT_SECTION_EVENTS)
recommendations   fade(P_stored, spacing, now) drives "memory strength" bars and
                  the Spaced-Repetition recommendation source (classroom UI)
```

Sanity check against the live capture (session 4): first session on a fresh
section → `spacing == null → 1` ✓; `proficiency: 0.495` stored un-faded ✓;
`recentSectionEvents` exactly the `{startingSectionProficiency, endingSectionProficiency,
averageScore, timeFinished}` shape built by `updateRecentSectionEvents` ✓.

If that section is never revised: P=0.495 @ spacing 1 fades to 0.452 after 1 day,
0.260 after a week, 0.125 after a fortnight. Reviewing on day 1 (the optimal
interval) doubles spacing to 2 → half-life jumps 7.5 → 38.8 days.

## 5. What is still open (honest gap)

**The within-session posterior update** — how `(startingProficiency, module
ledger)` → `endingProficiency` is computed — lives in the session player and was
NOT recovered: the player logic chunk imports `CompleteSessionPayload` through a
dep chain that name-directed fetching did not reach, and source maps are not
exposed (`/*.js.map` returns the SPA HTML shell — checked). One observed data
point: prior 0, tested modules scoring {1.0, 1.0, 0.67} (sessionScore 0.89) →
posterior 0.495. The posterior is clearly **discounted below the raw session
score** (0.495 ≈ 0.56 × 0.89), consistent with a prior-weighted Bayesian-style
blend and/or dilution by untested (notes) modules — but n=1; we will not
curve-fit a formula to one point. `RECONCILE_SESSION_PROFICIENCIES`
(`generateModuleStudiedEvent-BjZaYd-1.js`) proves the client reconciles its
optimistic posteriors against server stats after offline play, i.e. the server
*accepts and stores* client values (cheat surface, already flagged in
`2026-10-22-session-lifecycle.md` §6).

Internal `sessionType` enum (`SessionType-z3R5G623.js`) is richer than the wire
enum seen in the emit: `adaptive | wrongAnswers | smartLearning | quiz |
multiSection | vocabulary | examQuestions | revision`.

## 6. Reproducing the chunk dig

The 292-chunk Phase-1 corpus came from the static import graph (`chunk-list.txt`).
The lazy classroom/session-player graph is referenced from `Routes-BWEsPjqk.js`
via a Rolldown/Vite `__vite__mapDeps` asset array (1,445 assets) — extract the
array, diff against local files, and fetch candidates from the public asset CDN
(politely):

```bash
curl -s --compressed "https://app.senecalearning.com/assets/<name>.js" \
  -H "User-Agent: <descriptive-UA>"   # static CDN, bounded set, ≤1 req/s with sleep
```

Useful discovery shortcuts that paid off here:

- `grep -lao '<term>' *.js` over the corpus (the Grep tool skips minified
  multi-KB single-line files — use `grep -ao`).
- Route → asset mapping lives in `Routes-BWEsPjqk.js` `m.f=[…]` array; consumer
  chunks are found by matching the dep **index** inside
  `import('./X.js')…__vite__mapDeps([…])` calls.
- Semantically-named chunks exist for high-value domains:
  `state-B6uAS2cl.js` (memory math), `CompleteSessionPayload-j5kBDqpB.js`,
  `generateModuleStudiedEvent-BjZaYd-1.js`, `session-C9dh1Pqk.js`,
  `makeGetSmartLearningSectionSuggestions-CuX2YKd4.js` (SR recommender).
- Source maps are NOT published (`.js.map` → SPA HTML 404 shell).

## 7. SyllabAI relevance

- **Adopt the shape, fix the trust model.** The stored-projection design
  (`proficiency` + fractional `spacing` + capped `recentSectionEvents[]` prior→
  posterior log) is exactly the audit surface SyllabAI's `bkt_mastery` /
  `next_review_at` schema needs; SyllabAI should compute the posterior
  server-side instead of trusting the client.
- **The spacing bump is a better-behaved SM-2 substitute:** fractional credit
  (early = partial, at-optimal = full, >15× overdue = zero) is smoother than
  SM-2's binary quality scores and never shrinks the interval. Trivial to port.
- **τ = 4·e^(spacing^1.4) days** is a defensible forgetting-curve prior for
  SyllabAI's decay model: super-exponential in the review counter, half-life
  7.5 days at spacing 1. Note it grows *much* faster than Ebbinghaus-linear —
  by spacing 3 mastery is effectively permanent (τ ≈ 14 months).
- **Fail-open decay** (invalid inputs → no fade, negative mastery → 0) plus
  Sentry-instrumented model guards is good production hygiene worth copying.
- The **two-time-constant split** (scheduler interval `1.5s²+1.5s−2` days vs
  decay τ `4·e^(s^1.4)` days) decouples "when to show it again" from "how fast
  it fades" — cleaner than coupling both to one interval.

---

## Addendum (session 6, 2026-10-22): both formulas live-confirmed

Two controlled sessions in one authenticated pass re-verified this note's math
against fresh server data with no revisions needed:

- **Fade**: stored 0.435 displayed as `startingProficiency 0.4348007590641192`
  ≈ 20 min later (τ = 18.12 d at spacing 1.3452 → predicted 0.434796…);
  stored 0.465 → 0.4645320376226589 ≈ 40 min after the prior session. Exact
  within timestamp precision.
- **Spacing**: 1.3451737338 → 1.3492407596 across a 16 m 08 s gap =
  `f = gap/optimal(s) = 0.0040670` added — matches the fractional bump rule
  (`optimal = 1440·(1.5s²+1.5s−2)` min, early reviews earn proportional
  credit) to 10 dp.
- The **displayed** proficiency input to these formulas is itself the decoded
  posterior from `2026-10-22-posterior-formula.md` — the two notes now form a
  closed loop: blend → 3-dp store → fade for display → spacing ladder from
  the same `spacing` state.
