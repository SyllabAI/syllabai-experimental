# SyllabAI relevance — what to adopt, avoid, and steal for the backlog

**Captured**: 2026-10-22 · author's synthesis of the Phase 1 dossier.
Nothing here is of record; candidates graduate only via proper PRs against
of-record repos (root README ground rules).

## Direct validations of SyllabAI choices

1. **Tutor-shaped AI, three moments.** Seneca's chatbot family
   (query / explain / explain-wrong-answer / exam-question-conversation)
   is a one-to-one match with SyllabAI's tutor moments (KA-RAG chat,
   misconception remediation, Smart Mark feedback). Validation that the
   AI surface should be endpoint-families per pedagogical moment, not a
   general chatbot.
2. **Learner model as an isolated service.** Their `memory` service owns
   the forgetting-curve state, separate from sessions and stats — the same
   separation SyllabAI draws between learner model (BKT/BDT/decay) and
   assessment evidence. It makes the model inspectable, portable and
   explainable (memory-strength bars are a UI over a service contract).
   Candidate adoption: SyllabAI exposes a memory-strength read model to
   the hub even if the engine stays internal to the api.
3. **Content CDN separate from content API.** `course` (API) +
   `course-cdn-v2` (payloads) — immutable content on a CDN, mutable state
   on the API. SyllabAI's R2 + api split already matches; keep it.
4. **Runtime env config + feature-flag service.** One fetched `env.js`
   re-points the whole fleet; a dedicated feature-flags service gates
   rollout. Cheap for SyllabAI: the hub already ships a config object;
   consider server-driven flags when the CIE rollout needs per-band
   enablement (mirrors T-SM-ROLLOUT's data-first enablement).
5. **PWA fleet hygiene.** `versions.js` force-upgrade (cache purge +
   SW unregister) with a school-holiday motivation — directly reusable
   pattern for the hub when we ship offline/PWA.
6. **Free-first economics.** Their $0-for-students model at 15M scale
   (premium upsell + B2B) matches SyllabAI's free-tier LLM chain thesis;
   their monetisation gate (trials/subscriptions services + entitlement
   at API level) is a live reference implementation for our DC3
   entitlement gate — including a **trials service distinct from
   subscriptions**, like our free/paid/trial policy trichotomy.

## Candidate adoptions (Phase 4 decisions pending)

| Idea | Where it lands in SyllabAI |
|---|---|
| Memory-strength bar as a hub surface over the learner model | hub learner view; api read endpoint |
| `explain-wrong-answer` as a named tutor endpoint family | api tutor module (maps to our misconception links from T-011) |
| Exam-question conversation mode (marking + talk-through in one thread) | Smart Mark → Smart Chat hand-off design |
| Generation-seeded question variants (`enrichEQWithGenerationSeed`) | question bank expansion without content-scale cost |
| Anonymous quiz before signup (conversion) | pilot recruitment funnel for Cycle-1 classrooms |
| Revision Planner (AI weekly plan + catch-up sessions + break rewards) | candidate Addendum for the hub; uses target grades + memory |
| Staged release channels (dev/edge/app) in AASA | hub mobile strategy, later |

## What to avoid (informed by their shape)

1. **40-service fleet.** Their split is a scale answer with real
   operational cost; SyllabAI's modular monolith + two deployables is
   right for Cycle 1. Adopt their client-side registry, not their fleet.
2. **Zero anonymous content surface.** Everything 401s — great for
   entitlements, terrible for SEO and for research reproducibility.
   SyllabAI should keep a deliberate public metadata layer (as we already
   do with resources corpus) without exposing paid content.
3. **Runtime DOM localisation** (Localize widget) — pragmatic for 6
   locales but heavy and fragile; if SyllabAI localises, prefer
   build-time i18n with the same per-locale marketing SEO they use.

## Open intel we still need (Phase 2 → credentials required)

- Memory schema + write cadence (the actual learner-model contract).
- Session WS protocol (what a "session" is quantitatively: minutes, per
  section? their planner quotes time targets per subject per day).
- Chatbot payload shapes, grounding behaviour, refusal styles.
- Entitlement gate placement (which endpoints check premium; how trials
  expire; the free→premium upgrade surface).
- Course taxonomy granularity for iGCSE Chemistry vs our 4CH1 spine
  (cross-map deliverable named in the plan, Phase 4).

## Bottom line

Seneca independently converged on SyllabAI's core architecture — content
fabric, session runtime, isolated learner model, per-moment tutor AI,
entitlement services — at 15M-user scale. That convergence is the single
most useful external validation we have collected so far. Phase 2's
memory/session/chatbot payloads are the highest-value captures remaining,
and they need one throwaway student account (operator decision; conduct
rules in IP notes).
