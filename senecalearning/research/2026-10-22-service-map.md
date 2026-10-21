# Service map — the Seneca microservice fleet (of env.js)

**Captured**: 2026-10-22 · source: `https://app.senecalearning.com/env.js`
(committed verbatim at `resources/captures/env/env.js`).
All hosts are `https://{name}.app.senecalearning.com` unless noted. The
grouping below is ours; role annotations are inferred from name + chunk
corroboration and marked where verified.

## Core learning loop

| Service (host prefix) | Role (confidence) |
|---|---|
| `course` | course/curriculum catalogue API. Companion **`course-cdn-v2.app…`** = `baseCdnUrl` for content payloads |
| `session` | learning-session state machine (slide/question progression); **WebSocket** `wss://session-ws.app.…` for live session events |
| `memory` | **spaced-repetition / forgetting-curve state** — `/api/memories`, `/api/memories/{id}`; "memory strength" bars |
| `stats` | per-user learning stats; endpoints seen: `/api/stats/contents`, `/api/stats/courses`, `/api/stats/sections` |
| `xp` | experience points economy |
| `user-quiz` | user-authored/self-quiz attempts |
| `short-answer` | free-text answer marking (AI-marked short answers) |
| `exam-question-stats` | per exam-question aggregates (difficulty/usage) |
| `target-grades` | student target-grade records (feeds Revision Planner personalisation) |
| `student-activity` | activity telemetry |
| `student-report-cards` | generated student reports |
| `text-to-speech` | lesson TTS |
| `pdf` | PDF generation (worksheets/exports) |

## AI layer

| Service | Role |
|---|---|
| `chatbot` | the AI tutor backend. Named function URLs in env.js: `/api/query`, `/api/explain`, `/api/explain-wrong-answer`, `/api/exam-question-conversation`. Cognito-gated (live-verified 401 anonymous; CORS: POST only) |
| `short-answer` (AI marking) | see above — pairs with Smart-Mark-style flows |

GoStudent variant additionally gets a **LiveKit** voice sales-agent
(`goStudentChatbot.liveKitUrl` = `sales-agent-production-fbra5z0j.livekit.cloud`)
— a conversational voice funnel, not learning AI.

## Identity, users, school fabric

| Service | Role |
|---|---|
| `authentication` | auth API facade (`authentication.app…`) |
| (Cognito) | user pool `eu-west-1_5sGUjs8Wq`, client id `5e9bhjn9pn9tf41hrr7s1rqhr4`, custom endpoint **`identity.app.…`** (hosting the token/recaptcha/passwordPolicy surface — live-verified distinct behaviour vs other hosts) |
| `user-info` | user profiles |
| `class` | classes (teacher↔student membership) |
| `schools` | schools + `?schoolId=` queries |
| `school-analytics` | school-level dashboards |
| `mis-sync` | MIS/Wonde-style integrations sync |
| `parents` | parent linkage |
| `parent-quiz` | parent-facing quiz digest |
| `avatars` | student avatars |
| `geolocation` | region resolution (feeds `user-region` header) |
| `admin-gateway` | back-office gateway (staff) |

## Assignments, monetisation, engagement

| Service | Role |
|---|---|
| `assignments` | teacher-set homework/assignments (dashboard route `/dashboard/assignments/todo`) |
| `subscriptions` | premium entitlements (Stripe-backed) |
| `trials` | premium trials — the entitlement-gate analogue to SyllabAI DC3 |
| `enrollments` | user↔course enrolment (`/api/enrollments/me/courses`) |
| `tournaments` | competitive events |
| `challenge` | challenges (incl. `mathsCompetition` config in env.js: course-scoped prize draw with per-tier ids, end date 2026-06-05, hosted T&Cs PDF) |
| `class-leaderboards` / `school-leaderboards` | leaderboards at class/school scope |
| `live-feed` | activity feed |
| `notifications` | notification centre |
| `news` | product news |
| `surveys` / `forms` / `user-feedback` | feedback plumbing |
| `image` / `image-tags` / `imageCdn` | image pipeline (upload → tags → CDNs `image.cdn…`, `image-v2.cdn…`) |
| `feature-flags` | server-side flag service |
| `tutoring` / `tutor-resources` | tutor marketplace + tutor-authored resources |
| `discord` | community linkage |
| `tag` | content tagging |
| `grades` | `/api/grades` (grade records) |
| `locations` | `/api/locations[/{id}]` (school locations?) |

## Cross-cutting observations

1. **Service-per-bounded-context**, ~40 of them, each independently
   addressable at `{name}.app.senecalearning.com` — a much finer split than
   SyllabAI v2's api/hub duo. Their `env.js` runtime registry (the SPA's
   `ServiceClientRegistry` consumes it) keeps this tractable: adding a
   service = config, not deploy. For SyllabAI: our api-of-record monolith
   + selective extraction is fine at pilot scale; the lesson is the
   **client-side service-registry pattern**, not the fleet size.
2. **Learning-loop services are cleanly separated**: course (content),
   session (runtime), memory (learner model), stats (aggregates), xp
   (motivation). That is exactly SyllabAI's curriculum-KG / session /
   learner-model / telemetry split — validation of our module boundaries.
3. The **memory service is the learner model of record** — SyllabAI's
   BKT/decay equivalents map here; Phase 2 must capture its read/write
   cadence to see what granularity they persist (per section? per
   question? interval state?).
4. Monetisation is service-isolated (subscriptions, trials) with the
   entitlement gate observable at API level — Phase 2 target, mirrors our
   DC3 entitlement work.
