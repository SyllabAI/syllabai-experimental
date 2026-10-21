# Reverse-engineering plan — Seneca Learning (app.senecalearning.com)

**Status legend**: [x] done · [~] in progress · [ ] open
**Captured**: 2026-10-22 (Phase 1)

## Objective

Produce a complete structural understanding of Seneca Learning — product
surface, learning-loop mechanics, content model, service architecture, API
contract — sufficient to (a) inform SyllabAI product/platform design
decisions (session loop, memory model, AI marking, entitlements, teacher
flows) and (b) enable a rights-respectful metadata study of their course
taxonomy if the experiment graduates. Seneca is a closed, auth-gated SaaS
(unlike undergroundmathematics.org) — the plan is accordingly
**recon-first, account-second**: maximise what the anonymous surface yields
before any authenticated capture.

## Phases

### Phase 1 — Identification & infrastructure recon `[x]` (2026-10-22)

- [x] Company identity, scale, product surface, business model
      (research/2026-10-22-site-overview.md)
- [x] Frontend stack fingerprint + build chain + PWA machinery
      (research/2026-10-22-technical-architecture.md)
- [x] **Full microservice map** — 40+ named services extracted from the
      app's own `/env.js` config (research/2026-10-22-service-map.md)
- [x] Auth model: Cognito pool IDs, Firebase projects, reCAPTCHA, variant
      OIDC (research/2026-10-22-auth-model.md)
- [x] API surface sample: verified paths from the 290-chunk bundle corpus +
      live CORS/401 probes (research/2026-10-22-api-catalogue.md)
- [x] App route map + iOS universal-link scheme
      (research/2026-10-22-url-schemes.md)
- [x] Pedagogy-model first read: memories/XP/session/AI-marking services
      (research/2026-10-22-pedagogy-model.md)
- [x] SyllabAI relevance memo (research/2026-10-22-syllabai-relevance.md)
- [x] Evidence captured to resources/captures/ (env.js, versions.js,
      manifest.json, AASA, chunk manifest, extracted paths)

### Phase 2 — Anonymous + account surface `[ ]`

**Needs an operator decision: create a free student account (and a free
teacher account) for authenticated recon.** Nothing beyond the anonymous
surface can be catalogue-verified until then. Candidate credentials: a
throwaway student signup (email + password; reCAPTCHA will apply) and, if
possible, a teacher demo class. See `docs/IP-AND-COPYRIGHT-NOTES.md` for
the conduct rules we hold ourselves to (own account only, no scraping of
paid content bodies, no redist of copyrighted course material).

- [ ] Account creation + Cognito token flow capture (SRP vs custom
      `identity.app...` endpoints; JWT claims shape; refresh semantics)
- [ ] Course taxonomy catalogue: `course.app.senecalearning.com` +
      `course-cdn-v2` — subjects → courses → sections → lessons structure,
      legacy vs new course IDs (`courses/:legacyCourseId`)
- [ ] The learning session loop: `session.app...` + `wss://session-ws` —
      slide/section sequence, question events, timing/telemetry cadence
- [ ] Memory model: `memory.app...` `/api/memories` read + write cadence —
      what the "memory strength" bar actually persists (interval, decay,
      per-section granularity?)
- [ ] XP/gamification: `xp.app...`, tournaments, challenges, class/school
      leaderboards — event schema and rate limits
- [ ] AI surface: chatbot `/api/query`, `/api/explain`,
      `/api/explain-wrong-answer`, `/api/exam-question-conversation` —
      request/response shape, streaming behaviour, guardrails; short-answer
      service (`short-answer.app...`) for free-text AI marking; exam
      question stats service
- [ ] Teacher flows: class service, assignments, school analytics, MIS
      sync, target grades, report cards
- [ ] Parent flows: parents service, parent quiz, monitoring overview
- [ ] Premium/entitlements: subscriptions + trials services — what gates
      free vs premium (maps onto SyllabAI's DC3 entitlement work)

### Phase 3 — Content-model synthesis `[ ]`

- [ ] Canonical Seneca content schema (course → section → lesson → slide →
      question kinds; GIF/meme usage; TTS coverage; PDF exports)
- [ ] Question-type inventory: multiple choice, wrong-answer targeting,
      short-answer AI marking, exam-question conversation mode
- [ ] Localisation machinery (Localize CDN, per-variant help centres)
- [ ] Content provenance & rights observations (publisher partnerships,
      German Studienkreis PDF pipeline bucket)

### Phase 4 — Design synthesis `[ ]`

- [ ] Decision doc: what SyllabAI adopts (candidates: memory-service
      contract for the learner model; chatbot endpoint family as the
      tutor/Smart-Chat API shape; assignment/entitlement flows; session WS
      telemetry cadence; PWA update machinery like `versions.js`)
- [ ] Cross-map Seneca course taxonomy against the 4CH1 (and CIE) spines
      from `syllabai-v2`
- [ ] What Seneca's scale choices imply for our $0 free-tier chain (where
      they clearly pay for managed services we cannot)

## Method & conduct

Anonymous-only probes for Phase 1: public HTML/JSON assets, the app's own
JS bundle corpus, header/CSP analysis, live endpoint verification limited
to existence/auth behaviour (no content harvesting, no auth bypass, no
rate-stress). Politeness: descriptive UA on bulk fetches, bounded
parallelism (8), CDN-served static files only. All live-probe results are
recorded with the request that produced them.
