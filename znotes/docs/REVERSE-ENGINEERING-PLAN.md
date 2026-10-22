# Reverse-engineering plan — ZNotes (znotes.org)

**Status legend**: [x] done · [~] in progress · [ ] open
**Captured**: 2026-10-22 (Phase 1)

## Objective

Produce a structural understanding of ZNotes — product surface, content
model, API contract, and above all the **educator "My Teaching Toolkit"**
(4 AI resource generators) — sufficient to (a) inform SyllabAI teacher-tool
design (form ergonomics, option presets, grounded generation, async UX,
quota gating, export formats) and (b) position a possible metadata-level
study of their chapter taxonomy. ZNotes is a freemium login-walled platform
whose notes content is its product: **recon-first, account-second**, and
authenticated work is metadata-only by the IP rules in
`docs/IP-AND-COPYRIGHT-NOTES.md`.

## Phases

### Phase 1 — Identification, public recon & static reconstruction `[x]` (2026-10-22)

- [x] Company identity, scale, product surface, boards/levels covered
      (research/2026-10-22-site-overview.md)
- [x] Frontend stack fingerprint (Vite SPA, chunk architecture, CloudFront
      asset host) + API host + auth protocol
      (research/2026-10-22-technical-architecture.md)
- [x] Sitemap taxonomy census (239 URLs; CAIE IGCSE 42, IB DP 31, AS 18 …)
- [x] **My Teaching Toolkit static reconstruction** — the 4 generators with
      full form schemas, option presets, validation rules, request payloads,
      async polling protocol, quota model, export machinery
      (research/2026-10-22-teaching-toolkit.md)
- [x] Evidence captures: sitemap.xml, robots.txt, home/educators/subjects
      HTML, chunk manifest, toolkit registry JSON (resources/captures/)
- [x] Chunk corpus fetched locally for analysis (99 chunks, 5.8 MB) — not
      committed; reproducible via resources/scripts/fetch-app-bundles.sh

### Phase 2 — Authenticated educator walkthrough `[ ]` **BLOCKED on credentials**

**Blocker**: `POST /v2/auth/login` returns `401 {"message":"INCORRECT_PASSWORD"}`
for the supplied teacher credentials (verified through the app's own form
path and via a direct API probe — not a form/encoding artifact; the email is
recognised). Needs operator action: verify/reset password or provide the
Google sign-in route.

- [ ] Login session capture: token shape (JWT claims), `/v2/auth/refresh`
      cadence, session storage (cookie vs localStorage)
- [ ] Educator onboarding: `/register/educator/` flow, verification,
      school association fields
- [ ] **Live toolkit walkthrough** (metadata-only): open each of the 4
      generators from the dashboard, confirm form presets match the static
      reconstruction, capture chapter-dropdown source
      (`/v1/chapters/withCards/dashboard` response shape, values redacted)
- [ ] One free-prompt generation per tool on a throwaway-safe subject
      (5-prompt free budget): record `POST /api/znotes-educator-ai` request
      shape (already known) + response status flow (`pending → processing →
      success`) + latency + `responseId` semantics
- [ ] Output schemas verified against live payloads: lesson plan
      (`overview`, `lessonPlan|lessonOptions[]`, starter/main activities,
      differentiation map, plenary, homework), SOW (`overarchingObjectives`,
      `lessons[]` with activities/resources/cross-curricular links), rubric
      (`metadata`, `rubric.criteria[].levels{...}`, moderation guidance),
      clarify/challenge body format
- [ ] Quota enforcement observed: `educatorAiUsageCount` decrement, free
      exhaustion toast, Boost-Plus paywall (`/boost/educator`)
- [ ] Export machinery verified: PDF/DOCX/CSV/JSON in-browser generation
- [ ] "Your resources" history panel: list endpoint pagination, response
      retention, regenerate behaviour

### Phase 3 — Content-model & pedagogy synthesis `[ ]`

- [ ] Chapter → notes-cards model vs question bank (`/v1/questionBank`,
      `/api/randomQuestions/5/{id}`) — how quizzes and cards relate
- [ ] ZSlides pipeline (notes → slide decks) as far as publicly observable
- [ ] Student AI assistant surface (`/api/knowledge/query`,
      `/api/newbot/query`, `/chat-history`) — request shape, token budget,
      message-count gating (`/v1/updateMessageCount`)
- [ ] Content QA process (7-step pipeline publicised by ZNotes) mapped to
      SyllabAI's teacher-validation workbench concepts

### Phase 4 — SyllabAI synthesis & graduation `[ ]`

- [ ] SyllabAI relevance memo finalised (research/…-syllabai-relevance.md)
- [ ] Decision memo: which toolkit contracts to adopt for the T-TEACH track
      (option-preset ergonomics, grounded objectives, async UX, export set)
- [ ] Graduation PR(s) drafted for of-record repos if adopted
