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

### Phase 2 — Anonymous + account surface `[~]` (session 1: 2026-10-22)

**Operator provided a teacher account (2026-10-22) — session 1 executed.**
Captured: verified auth token flow (Firebase ID token as `access-key`
header — Cognito demoted to secondary), service auth matrix, XP model,
feature-flag dump, teacher class record, full 2,761-course catalogue
(+ slim taxonomy committed), Elasticsearch queryCourses, tag tree,
assignment-flow endpoint set. Remaining items below.

- [x] Account session + Cognito token flow capture — superseded by the
      real finding: **Firebase ID token** rides the `access-key` header;
      see research/2026-10-22-auth-token-flow.md
- [~] Course taxonomy catalogue: list + query captured (2,761 courses,
      Elasticsearch-backed `queryCourses`, tag filters); **section/slide
      payloads are CloudFront-signed** — resolution flow still open
- [x] The learning session loop (session 4, 2026-10-22): **session-ws
      protocol + session emit fully captured** — `wss://session-ws…?access-
      key=<JWT>&sessionId=<uuid>` is lifecycle-only (start-session +
      keep-connection-alive OUT, session-xp IN); all answers buffered
      client-side and flushed by one `POST /api/session` carrying the full
      module ledger incl. the client-computed mastery posterior (0 → 0.495;
      ~~BKT~~ — mechanism decoded in session 6, see below)
      and per-input scoring (`moduleScore.hits[]`); see
      research/2026-10-22-session-lifecycle.md + captures/sessions/
- [x] Memory model (session 4, 2026-10-22): **both stores schema'd** —
      memory service = palace-deposit ledger `(courseId, sectionId) →
      location{name,country,lat/long}`; stats service = spaced-repetition
      state (`proficiency`, `spacing` counter, `recentSectionEvents[]`
      prior→posterior log); see research/2026-10-22-memory-model.md
- [x] Learner-model math (session 5, 2026-10-22): **decoded from bundles** —
      NOT BKT: exponential forgetting curve
      `P·exp(−Δt_days / 4·e^(spacing^1.4))` + fractional spacing scheduler
      (`optimal = 1.5s²+1.5s−2` days; at-optimal review doubles spacing,
      >15× overdue earns nothing, spacing never decreases). Both live-
      re-confirmed in session 6; see research/2026-10-22-memory-math.md
- [x] **In-session posterior formula (session 6, 2026-10-22): DECODED** —
      NOT BKT, no slip/guess, per-input evidence ignored: mastery =
      `y = round(50·min(1, timesStudied/(spacing·3)) + 50·min(1,
      averageScore/0.9))` per unit, group-averaged `Σy/(100·N)`, stored at
      3 dp, faded for display by the session-5 curve; course fields are
      exact aggregates (/208 proficiency, bestScore/244). Verified on 4
      emits incl. two controlled-score sessions; server write is blind.
      Tooling lesson: 602 corpus chunks were gzip-saved and greps skipped
      them — decompress before mining. See
      research/2026-10-22-posterior-formula.md + captures/sessions/
      (emit-A, emit-C)
- [x] Magic Quiz AI flow (session 4, 2026-10-22): **full contract** —
      `POST user-quiz…/api/quizzes/generate` {resourceText, type, tags,
      options.maxQuestions} → poll `{status: generating→complete}` →
      21-module quiz (text-block/MC/wordfill+distractors), 12-endpoint
      client surface, entitlement gate `FREE_USER_CAN_ONLY_CREATE_PUBLIC_
      QUIZ`; see research/2026-10-22-magic-quiz-ai-flow.md +
      captures/magic-quiz/
- [~] XP/gamification: `/api/xp/me?date=` verified (level thresholds 100
      XP; daily/weekly/monthly/yearly buckets); **session 4: XP formula
      decoded from session-xp frame** (completion + score + memory
      components; level thresholds 200→350); tournaments service
      rejects the token (auth-split family); leaderboards unprobed
- [x] AI surface: chatbot (session 8, 2026-10-22) — full
      ChatbotServiceClient decoded (14 methods), streaming protocol
      (200 + text/event-stream, raw text chunks, error-as-body enum),
      model stack (gpt-4o / gpt-4o-mini @ temp 0.1, 700-tok responses,
      300-tok embedding context), Amelia payloads, freemium quota as XP
      rewards, session CRUD + admin surface; live probes show AI
      endpoints gated for free teacher / non-UK egress (session CRUD
      reachable); see research/2026-10-22-chatbot-ai.md +
      captures/chatbot/. Open remainder: short-answer marking payloads
      (AutoMarkType/LLM_MARKING_PROMPT_IDS discovered — Smart Mark
      family, needs a real marking event)
- [x] Teacher flows: class (`/api/classes/me`), assignments
      (`/api/teacher/me/assignments*`, `/api/classes/{id}/assignments`),
      tags/subjects funnel verified
      **Session 3 (2026-10-22): assignment CRUD contract fully cracked**
      — create (`POST /api/teacher/assignments` → 201), update
      (`PATCH /api/classes/{classId}/assignments/{id}`), delete
      (`DELETE` → 204), share-link + `autoEnrolNewUsers` mechanism,
      cutoff = due+14d, aggregation blocks; see
      research/2026-10-22-assignments-model.md. Resource Hub also
      mapped (below).
- [x] **Class analytics / school reporting (session 9, 2026-10-22): FULL
      contracts** — stats-service op-contract (`?ids=` collections; windowed
      per-user + multi-user `POST /api/stats/users/windowed/courses/{courseId}`
      with context-scoped 403 access control), knowledge-gap machinery
      (`POST class /api/classes/section-stats`, best-score threshold 0.8,
      500-on-empty server bug), async custom-report pipeline
      (`school-analytics` service → S3-presigned 3-sheet XLSX), class detail
      path (`/api/classes/me/{id}`), user-info Origin-allowlist. MIS "School
      Sync" = sales lead form only; Scheme of learning = premium AI
      concierge beta (email intake). see
      research/2026-10-22-class-analytics.md + captures/class-analytics/
- [x] Resource Hub (sessions 3 + 7, 2026-10-22): `query-resources` ES
      contract, 132-tag taxonomy, 74-subject × type count matrix
      (207,629 resources), Edexcel iGCSE Chemistry section tree
      (`queryCourses types=["section"]`); **session 7: FULL metadata
      harvest complete — 206,982 rows / 70 subjects (99.68%; residual =
      stable aggregation-vs-item-query delta), per-subject JSONL.gz +
      sha256 catalog, ageGroup sharding for >9,800-row cells,
      vocabulary = course-scoped REST (not an index type), `pdf` =
      aggregation-only type**; see research/2026-10-22-resource-hub.md
      + captures/resource-hub/ (by-subject/)
- [x] Resource Hub **full-CONTENT corpus** (session 11, 2026-10-23,
      operator approval recorded in IP notes): 207,006 rows / 70
      subjects with questionTitleMd + markScheme + generationScript +
      topicNotes + quizSummary; quiz PII scrubbed (0 leaks); per-course
      Edexcel iGCSE Chemistry layer (14 courses); 93 MB gz at
      captures/resource-hub-content/; build script
      scripts/seneca_build_content_corpus.py. **Assignments feature
      prototype built on this slice** (Next.js 16 + Prisma, teacher
      create/list/stats + student view/complete/score full loop;
      staged for the production repo)
- [ ] Parent flows (needs a parent-linked view — open)
- [~] Premium/entitlements: catalogue `subscriptionTier` FREE/PREMIUM
      split captured (1,789/971); runtime gate placement open

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
