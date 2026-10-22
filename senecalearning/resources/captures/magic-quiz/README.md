# Magic Quiz (AI quiz generator) captures — redacted

**Captured**: 2026-10-22 (Phase 2 session 4) · one quiz generated live through
`/teacher/quizzes/create` on the teacher account with in-page fetch instrumentation.
Source text for generation is our own probe paragraph (not Seneca content). The
LLM-generated output bodies are truncated/answer-redacted per the IP notes — field
shapes kept in full.

| File | What |
|---|---|
| `quiz-generate-request.json` | verbatim `POST https://user-quiz.app.senecalearning.com/api/quizzes/generate` body: `{resourceText, type:"TEXT", tags{categoryId:[tagId]}, shareWithSchool, isPublic, options.maxQuestions}` |
| `quiz-generation-lifecycle.json` | polling contract: `GET /api/quizzes/me/{id}` every ~2s; `status: generating → complete`; UI stages ("Adding distractors to questions…", ~20–50 s) |
| `quiz-generate-result-redacted.json` | final `{quizOverview, contents[].modules[]}` — **21 modules**: text-block + 10 multiple-choice + 10 wordfill (with per-blank distractor sets). userId/creator redacted, answer content redacted/truncated |

Key facts: service `user-quiz.app.senecalearning.com`; free-tier gate
`FREE_USER_CAN_ONLY_CREATE_PUBLIC_QUIZ` (cannot un-list, no delete endpoint — probe
quiz left as unpublished draft); `QuizResourceTypes = TEXT|YOUTUBE|PDF|PRESENTATION|DOCUMENT|TRANSCRIPT`;
full client surface (12 endpoints) in `research/2026-10-22-magic-quiz-ai-flow.md`.

Related research: `research/2026-10-22-magic-quiz-ai-flow.md`.
