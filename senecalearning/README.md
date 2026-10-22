# senecalearning — reverse engineering of Seneca Learning (app.senecalearning.com)

**Status**: Phase 1 complete + Phase 2 session 1 (2026-10-22) — live
teacher session: auth token flow verified, service auth matrix, XP model,
feature flags, 2,761-course catalogue captured, assignment-flow endpoints.
**Target**: https://app.senecalearning.com/ (the student/teacher/parent SPA)
and its supporting services. Marketing site: https://senecalearning.com/en-gb.

## Why this experiment

Seneca is the closest large-scale analogue to SyllabAI: a free-tier,
curriculum-linked revision platform with cognitive-science learning loops,
spaced-repetition memory modelling, AI-marked questions, an AI tutor
("Amelia"), teacher assignment flows and parent monitoring — at 15M+ student
scale, on a $0-for-students freemium model. Understanding how they structure
content delivery, the learning session loop, the memory/XP model and the AI
marking/tutoring surface directly informs SyllabAI design decisions (Smart
Mark scale-out, memory/decay model, tutor chat, entitlement gates).

## Layout

| Path | What |
|---|---|
| `docs/REVERSE-ENGINEERING-PLAN.md` | phased plan with status |
| `docs/IP-AND-COPYRIGHT-NOTES.md` | what we capture, what we never commit |
| `research/2026-10-22-site-overview.md` | company, scale, product surface, business model |
| `research/2026-10-22-technical-architecture.md` | stack, bundling, PWA, infra, white-labelling |
| `research/2026-10-22-service-map.md` | the 40+ microservices of record (from `env.js`) |
| `research/2026-10-22-auth-model.md` | Cognito + Firebase + reCAPTCHA + variant auth |
| `research/2026-10-22-api-catalogue.md` | API surface: verified paths, CORS, auth gating |
| `research/2026-10-22-url-schemes.md` | app routes + mobile deep-link scheme |
| `research/2026-10-22-pedagogy-model.md` | the learning loop: memories, XP, sessions, AI marking |
| `research/2026-10-22-syllabai-relevance.md` | what SyllabAI should adopt / avoid |
| `resources/captures/` | evidence: env.js, versions.js, manifest, AASA, chunk manifest, extracted paths |
| `resources/captures/js/` | 290 minified app chunks — **not committed** (4.6 MB, re-fetchable via script) |
| `resources/scripts/fetch-app-bundles.sh` | reproduce the bundle capture |

## Key facts (Phase 1 headline)

- React SPA (`window.Seneca.version = "4.6.264"`), built with **Rolldown**
  (the Rust bundler), Redux + Immer + Reselect + TanStack Query, PWA with
  service worker + push (Firebase Cloud Messaging), offline via localforage.
- **~40 backend microservices** behind `*.app.senecalearning.com`, each a
  separate host behind AWS API Gateway + CloudFront (env.js names them all:
  authentication, course + course-cdn-v2, user-info, stats, **memory**,
  session (+ `wss://session-ws`), assignments, chatbot (AI tutor endpoints),
  subscriptions, xp, tournaments, challenges, schools, class/class
  leaderboards, text-to-speech, pdf, mis-sync, …).
- **Auth = AWS Cognito** (user pool `eu-west-1_5sGUjs8Wq`, client
  `5e9bhjn9pn9tf41hrr7s1rqhr4`, custom endpoint
  `identity.app.senecalearning.com`) + Firebase (`seneca-auth-production`)
  for messaging/analytics, with reCAPTCHA enterprise config endpoints.
- The SPA is a **white-label shell**: origin sniffing selects the Seneca /
  GoStudent (`learning.gostudent.org`) / Studienkreis variants; Plurall
  (Brazil, `adapta.plurall.net`) rides an OIDC Firebase project.
- The **chatbot service** exposes `/api/query`, `/api/explain`,
  `/api/explain-wrong-answer`, `/api/exam-question-conversation` — an
  AI-tutor API family, Cognito-gated (401 anonymous, verified live).
- A dedicated **memory service** (`memory.app.senecalearning.com`,
  `/api/memories`) is the spaced-repetition/forgetting-curve state of
  record — SyllabAI's closest structural analogue is our learner model.

Nothing here is of record; see the root README ground rules.
