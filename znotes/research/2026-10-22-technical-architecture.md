# ZNotes — technical architecture (Phase 1)

**Captured**: 2026-10-22 (anonymous; bundle + live probes)

## Frontend

- **Single React SPA** (React 18-era, `react` 144 hits in the main bundle),
  built with **Vite** (60 hits; hashed chunk names, `__vite` module map).
- ~**99 lazy chunks** (5.8 MB total) served from CloudFront
  (`https://d11xgklg0c0p8q.cloudfront.net/assets/*`); the main bundle
  `app-D0RKGZIv.js` is 1.9 MB. Per-route/per-feature splitting (login,
  educators, boost, dashboard, styles+components).
- i18n baked into the main bundle as flat key-value dictionaries
  (`dashboard_myTeachingToolkit`, `landing_aiLessonTitle`, …) with a
  language selector (site rendered zh-TW on first visit from our client —
  locale auto-detection).
- Component libs bundled: react-router (route table extractable), a
  table component, modal/select primitives; **`docx`** and **`JSZip`**
  ship client-side for in-browser DOCX/PDF/CSV/JSON export generation;
  Google Analytics (G-FY14L6R42F); toast notification system with
  click-through actions.

## Backend

- **API host**: `https://api.znotes.org`
  - `/v1/*` — content domain: boards, subjects, modules, chapters,
    cards, questionBank, partners, resbank (resource bank w/ pdf+image
    upload), quiz results, study-sessions, confidences, badges, PDF
    generation (`/v1/modules/generatePDF/{id}`)
  - `/v2/*` — accounts/auth: `/v2/auth/login`, `/v2/auth/refresh`,
    `/v2/auth/migrate-to-new-tokens`, `/v2/auth/discord/callback`,
    `/v2/account/*`, `/v2/school/*`, `/v2/schools/*`, `/v2/notifications/*`,
    `/v2/schools-team/{id}`, `/v2/schools/subject-time/{school}/`
  - `/api/*` — feature services: `/api/znotes-educator-ai` (toolkit),
    `/api/educator-ai/responses[/...]` (toolkit results),
    `/api/knowledge/query` + `/api/newbot/query` + `/chat-history`
    (AI assistants), `/api/randomQuestions/5/{id}`, `/api/v1/booster/*`
    (subscriptions), `/target-grades`, study-plans, live events
- Error shape observed: `{"error":"Not Found"}` (404) /
  `{"message":"INCORRECT_PASSWORD"}` (401).

## Auth model (what is observable anonymously)

- Email+password, stepped form: email → `POST /v2/auth/login`
  → password step; **Google sign-in button** (GIS iframe) offered at the
  first step; Discord OAuth callback exists (`/v2/auth/discord/callback`).
- Failure mode observed live: `401 {"message":"INCORRECT_PASSWORD"}`
  (email recognised, password rejected) — no rate-limit hit at low volume.
- Token machinery: `/v2/auth/refresh` + `/v2/auth/migrate-to-new-tokens`
  implies rotating refresh tokens with a legacy-token migration shim;
  `ct.getUser()`/`Yh.getUser()` session helpers expose `_id`,
  `accountType` (student/teacher), `school` fields client-side.
- Registration flows: `/register/student/`, `/register/educator/`.

## Dashboard architecture

- Route `/content/dashboard`; **panel switching via query param** —
  `?panel=educator-ai` ("My Teaching Toolkit"), `gradebook`,
  `schooldashboard` ("My School Learning Analytics"), `my-uni`
  ("My Students' Uni Goals"), `my-development` ("My Professional
  Development").
- Deep links into results: `/?panel=educator-ai&responseId={id}`.
- Client-side event bus for async work: window CustomEvents
  `educator-ai-resource-created` / `educator-ai-response-completed`.

## Content grounding pipeline (what feeds the toolkit)

- `GET /v1/boards` — board list (CAIE, Edexcel, IB, …)
- `GET /v1/modules?subject={id}` — module list per subject
- `GET /v1/chapters/withCards/dashboard` — chapters **with their notes
  cards** for the dashboard context (cards = `{_id, title, content}`,
  sorted by `sortKey`); chapter objects also carry `outcomes` — the
  learning objectives the lesson-plan generator auto-attaches.
- URL-context sniffing: if the educator browses from a subject page
  (`/{board}/{level}/{subject}`), the toolkit pre-selects
  board/level/subject from the path (excluding dashboard-ish prefixes).

## Observations relevant to SyllabAI

1. Same-family architecture as SyllabAI v2: SPA + content API + async AI
   service + entitlement gates; ZNotes runs the AI service as a thin
   `POST` → `responseId` queue with client polling — simple, robust,
   and worth comparing against SyllabAI's synchronous Smart Mark lanes.
2. Export happens **client-side** — zero server render cost, but the
   `docx`/JSZip payload rides every dashboard visit.
3. The whole toolkit is grounded in the *content graph* (subject →
   module → chapter → cards/outcomes), not free-form chat — the same
   "generation must cite the corpus" instinct as SyllabAI's grounded
   tutor contract.
