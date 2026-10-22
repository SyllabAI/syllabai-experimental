# Magic Quiz AI Flow — Reverse-Engineered Contract

**Date:** 2026-10-22 (Phase 2, session 4) · **Method:** authenticated teacher walkthrough with in-page fetch instrumentation + JS bundle static analysis (`out-BsbuqlBf.js`, `client-BI1pX8mm.js`, `routes-DLV9sAat.js`)

---

## What "Magic Quiz" is

Magic Quiz is Seneca's **LLM quiz generator**: a teacher pastes source material (or a
YouTube link / file upload), picks level + subject + exam-board tags and a question
budget, and the platform generates a complete quiz — title, explainer text block,
multiple-choice questions with distractors, and wordfill (cloze) items with per-blank
distractor sets. Generated quizzes live in a per-teacher quiz library (`My Quizzes`),
can be copied, edited, assigned to classes like any assignment task, exported to PDF,
and — on paid tiers — kept private or school-shared.

Two product facts that frame the whole surface:

1. **`magic-quiz` is a first-class course/resource type** in the content taxonomy
   (`MAGIC_QUIZ = 'magic-quiz'` alongside `CORE_CONTENT`, `EXAM_QUESTIONS`,
   `HARDEST_QUESTIONS`, …). The marketing copy in the routes bundle describes it as
   *"Quizzes written by teachers and shared across Seneca"* — i.e. the public Magic
   Quiz library is the corpus of teacher-generated quizzes.
2. **Entitlement gating** (paywall feature flags observed in `routes-DLV9sAat.js`):
   `UnlimitedMagicQuizzes`, `SchoolSharingMagicQuizzes`, `PrivateMagicQuizzes`,
   `SharingMagicQuizzesWithTeachers`. The free tier is capped and, critically,
   **forced-public**: trying to un-list a generated quiz returns
   `400 {"reason":"Free user can only make public quizzes","pointer":"FREE_USER_CAN_ONLY_CREATE_PUBLIC_QUIZ"}`.
   This is a clean DC3-analogue entitlement gate for SyllabAI.

## Service and client

- **Service host:** `https://user-quiz.app.senecalearning.com` (microservice
  `user-quiz`; also referenced as `UserQuizServiceClient` in the generated API-client
  bundle). Env.js also exposes `parent-quiz.app.senecalearning.com` (parent-facing
  quiz surface).
- **Auth:** standard Phase-2 contract — Firebase ID token in the `access-key` header
  (see `2026-10-22-auth-token-flow.md`).
- **Quiz entity types:** `QuizEntityType = quizOverview | content | module`.
- **Source-material types:** `QuizResourceTypes = TEXT | YOUTUBE | PDF | PRESENTATION |
  DOCUMENT | TRANSCRIPT`.

## Generation flow (live-captured end-to-end)

**Entry points:** teacher navbar `Create → Magic Quiz` → route
`/teacher/quizzes/create` ("Create engaging material instantly"). The editor page for
a generated quiz is `/teacher/quizzes/{quizId}`; the student-facing study endpoint is
separate (`/api/study/quizzes/me/{quizId}`).

### Step 1 — UI form

| Control | Detail |
|---|---|
| Content input | 3 modes: `Input text` (free textarea, placeholder "Paste your notes, a passage, or type a topic…"), `YouTube link`, `Upload file` |
| Question budget | Range slider (observed 1–5+; request carried `options.maxQuestions`) |
| "Tailor to your students" | 3 radio groups mapped to the tag taxonomy: ageGroup (GCSE, A Level, KS3, …14 options), subject (Chemistry + 74 subjects), examBoard (AQA, Edexcel, **Edexcel iGCSE**, …) |

### Step 2 — `POST /api/quizzes/generate` → `201 {"quizId": "…"}`

Captured request body (verbatim shape, content is our own probe text):

```json
{
  "resourceText": "The periodic table arranges elements in order of …",
  "type": "TEXT",
  "tags": {
    "3df4913a-5a19-4777-9fdf-1c1d74f40491": ["f4c68c00-728c-472b-a715-e9c8dab47689"],
    "8c71d055-ff40-4536-8629-5073c618ea53": ["ae73bf6e-802a-4f72-9f8e-437aa6828a07"],
    "29304df7-aad4-4b2f-ac43-2fb169c04ebd": ["b38ff4d5-9228-4e43-b1d6-3d3243b9d9f7"]
  },
  "shareWithSchool": false,
  "isPublic": true,
  "options": { "maxQuestions": 25 }
}
```

- `tags` = `{tagCategoryId: [tagId]}` — same taxonomy as the Resource Hub
  (`resources/captures/resource-hub/tags-taxonomy-slim.json`): the three IDs above are
  GCSE / Chemistry / Edexcel iGCSE.
- `isPublic: true` is **forced by the client for free accounts** (see entitlement
  gate above).
- An anonymous variant exists: `POST /api/quizzes/generate-anonymous` (same body minus
  sharing fields; used for logged-out marketing generators; client restricts it to
  `TEXT`/`YOUTUBE` types).
- Non-text sources presumably upload via `POST /api/files/upload-url`
  `{fileName, contentType}` → signed URL (422 on validation), then reference the
  uploaded object.

### Step 3 — async generation + status polling

The client then polls `GET /api/quizzes/me/{quizId}` roughly every 2 s:

1. `status: "generating"` — `quizOverview` stub: `name` = raw `"Quiz {quizId}"`,
   `contentIds: []`, `access: "private"`.
2. `status: "complete"` — overview now carries the **LLM-generated title**
   ("The Periodic Table: Groups, Trends & Reactivity"), populated `contentIds`, and
   **re-assigned tags** (the model infers/normalises subject tagging from the source
   text — the returned tag map differed from the requested one).
   UI progress stages observed: "Generating questions…" → "Adding distractors to
   questions…" (~20–50 s total for a short passage).

### Step 4 — generated artefact shape

`GET /api/quizzes/me/{quizId}` → `{quizOverview, contents[]}`:

```jsonc
{
  "quizOverview": {
    "type": "TEXT", "entityType": "quizOverview",
    "quizId": "…", "id": "…", "name": "The Periodic Table: Groups, Trends & Reactivity",
    "status": "complete", "published": false, "isPublic": true, "access": "private",
    "region": "GB", "numCopies": 1,
    "creationDate": "2026-10-22", "creationDateTime": "2026-10-22T01:43:51.960Z",
    "userId": "…", "creatorId": "…", "userDetails": {"givenName","nickname","creatorName"},
    "tags": {"29304df7-…": ["b38ff4d5-…"], "3df4913a-…": ["f4c68c00-…"], "8c71d055-…": ["ae73bf6e-…"]},
    "contentIds": ["822aa719-…"]
  },
  "contents": [{ "contentId": "…", "modules": [ /* 21 modules */ ] }]
}
```

Our probe (maxQuestions=25, ~120-word source) produced **21 modules**:
`1 × text-block + 10 × multiple-choice + 10 × wordfill`. Module shapes:

- **text-block** — `{content: {body: "<markdown>"}, moduleType: "text-block"}`; the
  LLM restructures the source into titled markdown sections.
- **multiple-choice** — `{content: {question, correctAnswer, wrongAnswers: [3]} }`.
- **wordfill** — `{content: {words: [ "literal ", {word, distractors: [3],
  otherPermittedWords: []}, " literal …" ]}}` — a token stream where blanks are
  objects carrying the missing word plus distractor pool; `title` renders blanks as
  `_______`.

(`contentId → modules` mirrors the course content model: quiz `content` = one
container, `modules` = linear list, each module has `parentId = contentId`,
`testingActive`, `entityType: "module"`.)

## Full UserQuizServiceClient endpoint surface (from generated client bundle)

| Method | Endpoint | Notes (status codes observed in client) |
|---|---|---|
| `fetchTeacherQuiz` | `GET /api/quizzes/me/{quizId}` | 200/400/403/404 |
| `fetchStudyQuiz` | `GET /api/study/quizzes/me/{quizId}` | student study view |
| `requestGenerateQuiz` | `POST /api/quizzes/generate` | 201/400/403 → `{quizId}` |
| `requestGenerateQuizAnonymous` | `POST /api/quizzes/generate-anonymous` | 201/400 |
| `updateTeacherQuiz` | `POST /api/quizzes/me/{quizId}/update` | **full-document update**, body = `{quizOverview, …}` (422 with `pointer` on missing field) |
| `queryTeacherQuizOverviews` | `POST /api/quizzes/me/query` | body `{lastKey?, limit?, status?, published?, tags?, archived?, schoolId?}` → DynamoDB-style `lastKey` pagination |
| `querySchoolQuizOverviews` | `POST /api/quizzes/schools/{schoolId}/query` | same shape, school scope |
| `saveTeacherFeedback` | `POST /api/quizzes/me/{quizId}/feedback` | emoji rating (😢🙁🙂😀🤩 in UI) |
| `copyQuiz` | `POST /api/quizzes/{quizId}/copy` | 201/404/403/422 ("cannot be duplicated") |
| `backfillQuiz` | `POST /api/quizzes/{quizId}/backfill` | 200/404 |
| `saveQuiz` | `POST /api/quizzes/{quizId}/save` | 200/201/404/403/422 |
| `generateQuizPdf` | `GET /api/quizzes/{quizId}` | printable PDF export |
| `createUploadUrl` | `POST /api/files/upload-url` | `{fileName, contentType}` → signed upload |

Error taxonomy (typed client errors): `QuizDoesNotExistError`,
`QuizBadRequestError(reason, pointer)`, `QuizUnprocessableEntityError`,
`UserNotPermittedError`, `FileUploadUnprocessableEntityError`, `InternalServerError`.

## Assignment integration

The quiz editor exposes **"Assign quiz"** (routes into the standard assignment
creation funnel with the quiz pre-selected) and **"Create game"** (Game Beta).
`QuizResourceTypes`/`query-resources` from the Resource Hub study
(`2026-10-22-resource-hub.md`) already treat `quiz` as a first-class resource type
(3,382 Chemistry quizzes in the public library), so assigning works through the same
`spec.tasks[]` contract documented in `2026-10-22-assignments-model.md` (task
references the quiz id rather than a `courseId` section).

Editor also offers **"See how it looks"** → `/quiz-preview` (student-view preview;
non-interactive for teachers in our test) and per-module **add-image** (via
`/api/files/upload-url`).

## Generation constants (session-5 addendum, `out-BsbuqlBf.js`)

Decoded distractor-pipeline tuning constants alongside the client:

```js
MC_MIN_GENERATION_COUNT = 2            // min MC questions per generation batch
WF_MIN_GENERATION_COUNT = 2            // min wordfill items per batch
WF_MIN_GENERATION_ALTERNATIVE_WORDS = 0
WF_MAX_GENERATION_ALTERNATIVE_WORDS = 2 // otherPermittedWords budget
WF_MIN_GENERATION_DISTRACTOR_WORDS = 3  // distractor pool size per blank
GENERATE_ID_PLACEHOLDER = "generate!"   // client-side id for in-flight items
UPLOADED_CONTENT_MAX_FILE_SIZE = 26_214_400  // 25 MB
```

Confirms the two-stage server pipeline observed live (questions → distractors)
has per-type minimums and a 3-distractor-per-blank floor for wordfill, matching
the captured module shape (`distractors: [3]`).

## SyllabAI relevance

- **Direct analogue of SyllabAI's "AI-generated quiz from syllabus source" story** —
  Seneca's whole generation contract fits in one POST + polling loop, with
  server-side LLM pipeline (questions → distractors) and tag inference.
- **Entitlement gates worth copying:** free-tier cap + forced-public sharing is a
  growth loop (every free teacher's generated quiz seeds the shared library) enforced
  server-side by a single named error code — exactly the DC3 pattern.
- **Structured MC/wordfill output with distractor sets** matches SyllabAI's
  Smart-Mark question schema; the `words[]` token-stream wordfill format with
  `otherPermittedWords` is a good model for accept-multiple-answers marking.

## Cleanup note

Probe quiz `d564a220-db24-43ba-91dc-31a55cde29cb` left in place as an **unpublished
draft** (`published: false` ⇒ not listed in the public library); it cannot be made
private on a free account (documented gate above) and the client exposes no delete
endpoint. No assignments were created; no class changes.
