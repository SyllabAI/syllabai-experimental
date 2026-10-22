# Pedagogy model — how Seneca's learning loop is built (first read)

**Captured**: 2026-10-22 · sources: bundle chunk names, service map,
public help-centre articles, App Store copy. Structural inference, marked
as such — Phase 2 verifies against live payloads.

## The loop (product claim → service evidence)

```
course content (course service + course-cdn-v2)
   →  learning session (session service + session-ws WebSocket)
        · short explanation → immediate question (retrieval practice)
        · wrong answer → chatbot /api/explain-wrong-answer (targeted remediation)
        · free-text → short-answer service (AI marking)
        · exam questions → chatbot /api/exam-question-conversation (AI marking + talk-through)
   →  memory state (memory service, /api/memories)
        · "memory strength" bars per topic/section; forgetting-curve decay
   →  aggregates (stats service: /api/stats/{contents,courses,sections})
   →  motivation layer (xp, tournaments, challenges, class/school leaderboards, live-feed)
   →  planning layer (Revision Planner: AI weekly plan, target-grades service,
        catch-up sessions, break rewards)
   →  accountability layer (assignments, class/school analytics, MIS sync, report cards, parents)
```

Every arrow above lands on a **dedicated microservice** — the pedagogy is
the architecture. Notable: the learner model is not embedded in the
session service; it is its own `memory` service with a CRUD-ish
`/api/memories[/{id}]` contract, meaning memory state is portable across
surfaces (app, web, planner, parent views).

## Signals of AI-native learning mechanics

- `enrichEQWithGenerationSeed` chunk — exam questions (EQ) carry a
  **generation seed**: procedurally varied question instances from a
  template bank. SyllabAI parallel: our question generation plans.
- `anonymousQuizStorage` — pre-signup quiz attempts persisted (conversion
  funnel: let them try a quiz before an account).
- `sessionsCompletedCounter` — streak/completion gamification at chunk
  level (it is a core loop citizen, not a widget).
- Chatbot family covers the three pedagogical moments where a tutor adds
  value: concept explanation, wrong-answer remediation, exam-question
  technique. This is a **tutor-shaped AI**, not a chat-with-PDF — the same
  framing as SyllabAI's KA-RAG tutor positioning.
- Text-to-speech as a first-class service — accessibility + review-mode
  narration.

## Cognitive-science framing (public)

Their stated mechanisms: retrieval practice, spaced repetition,
interleaving, visual memory cues (memes/GIFs via Giphy/Tenor CDN
allow-list), forgetting-curve scheduling, dual coding. Efficacy evidence:
RCT (1,120 Year-9 pupils; means 8.39 vs 5.15/4.08). For Paper A/B: Seneca
operationalises the same science base SyllabAI's learner model (BKT/BDT/
decay) targets, but their public material is mechanism-light — no learner
model is documented in public; the memory service schema is the real
answer (Phase 2).

## Engagement economics

Free tier is genuinely functional (15M users); monetisation gates:
premium features (what-is-premium surfaces on dashboard AND parent
routes), school contracts, tutoring marketplace, B2B white-label.
Gamification (XP, leaderboards, tournaments, maths prize draw with real
T&Cs PDF) is the retention engine that makes free viable at scale.

## Open questions for Phase 2

> **Session-4/5 status update:** 1 and 2 are answered — memory schema captured
> (`2026-10-22-memory-model.md`) and the session protocol is lifecycle-only WS +
> single REST emit (`2026-10-22-session-lifecycle.md`). The learner model itself
> is now *decoded*, not inferred: an exponential forgetting curve
> (`τ = 4·e^(spacing^1.4)` days) with a fractional spacing scheduler — **not BKT**
> — with the posterior computed client-side (exact formulas and the honest
> residual gap in `2026-10-22-memory-math.md`). Remaining open: 3 (planner
> contract), 4 (chatbot grounding), 5 (entitlement split — partially answered by
> the Magic Quiz forced-public gate).

---

## Addendum (session 6, 2026-10-22): the posterior is decoded — final answer on BKT

The "client-side posterior" flagged throughout this note is now fully decoded
(see `2026-10-22-posterior-formula.md`): it is **not BKT under any framing**.
The mastery value is `y = round(50·min(1, timesStudied/(spacing·3)) +
50·min(1, averageScore/0.9))` per unit, group-averaged `Σy/(100·N)`, rounded
to 3 dp, and faded by the exponential curve above for display. No slip/guess
parameters exist; the per-input `hits[]` evidence ledger does not feed the
update (only final module scores do). The SyllabAI comparison in §"BKT-style"
should be read as: Seneca = SR-bookkeeping blend trusted from the client;
SyllabAI = server-side BKT over the response ledger — strictly more
informative, and now demonstrably differentiated from the incumbent.
