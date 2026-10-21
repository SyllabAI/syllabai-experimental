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

1. Memory schema: what exactly is a memory row? (per user×section?
   interval? ease? last-seen?) Write cadence per answer or per session?
2. Session event protocol over `session-ws` — what is streamed (timing,
   hints, heartbeats, teacher live views)?
3. How the planner consumes memory+stats to allocate weekly minutes
   (the visible adaptive layer).
4. Whether the chatbot is grounded in course content (RAG over their own
   sections) or open-generation — guardrail surface will hint.
5. Entitlement: which of the above actually gate on
   subscriptions/trials (premium vs free split).
