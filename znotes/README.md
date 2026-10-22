# znotes — reverse engineering of ZNotes (znotes.org)

**Status**: Phase 1 + Phase 2 complete (2026-10-22). **Recreation built & verified:** all four generators recreated with 100% structural fidelity vs live-captured anchors — see `research/2026-10-22-recreation.md` and `recreation/`. Phase 1 reconstructed
the educator "My Teaching Toolkit" statically from public bundles; Phase 2
verified everything **live** in the teacher account — all 4 generators
driven end-to-end (1 free prompt each, 1 of 5 left), outputs inspected,
exports confirmed, and three corrections/additions recorded (wizard
Subject→Module step, computed rubric scale, 6-tab Learning Coach output).
**Target**: https://znotes.org (marketing + SPA) · `api.znotes.org` (API).

## Why this experiment

ZNotes is the closest *content-and-teacher-tool* analogue in SyllabAI's
ecosystem: a free, syllabus-linked revision platform (CAIE/Edexcel/IB/AQA/
AP/CBSE/WAEC) at 6M-student scale that has added an **educator AI toolkit**
— four generators (Lesson Plan, Scheme of Work, Rubric, Clarify/Challenge)
grounded in **the same chapter taxonomy that serves their student notes**.
That grounding — resource generation keyed to the platform's own content
graph (subject → module → chapter → cards, with chapter `outcomes` feeding
learning objectives) — is exactly the pattern SyllabAI's teacher tools
(T-TEACH track) need. Understanding their form design, option presets,
async-generation UX, freemium quota gating (FREE 5 / PLUS 100 prompts) and
export surface directly informs SyllabAI's teacher-tool contracts.

## Layout

| Path | What |
|---|---|
| `docs/REVERSE-ENGINEERING-PLAN.md` | phased plan with status |
| `docs/IP-AND-COPYRIGHT-NOTES.md` | what we capture, what we never commit |
| `research/2026-10-22-site-overview.md` | company, scale, product surface, boards covered |
| `research/2026-10-22-technical-architecture.md` | stack, bundling, API host, auth model, session protocol |
| `research/2026-10-22-teaching-toolkit.md` | **the core deliverable** — the 4 generators end-to-end |
| `research/2026-10-22-syllabai-relevance.md` | what SyllabAI should adopt / avoid |
| `research/2026-10-22-recreation.md` | **recreation proven** — feasibility, fidelity results, new intel (Claude-class backend hint) |
| `recreation/` | runnable recreation app (original prompts, contract-mirrored, fidelity validator) |
| `resources/captures/educator-ai-output-schemas.json` | content-free type-shape anchors from the 4 real responses |
| `resources/captures/` | evidence: sitemap, robots, home/educators/subjects HTML, chunk manifest, toolkit registry JSON |
| `resources/captures/chunks/` | 99 minified app chunks — **not committed** (5.8 MB, re-fetchable) |
| `resources/scripts/fetch-app-bundles.sh` | reproduce the chunk corpus |
| `resources/scripts/scan_bundle.py` | endpoint/keyword scanner used for the analysis |
| `resources/scripts/extract_i18n.py` | dashboard i18n string extractor |

## Key facts (Phase 1 headline)

- React 18-class SPA built with **Vite**, ~99 lazy chunks on CloudFront
  (`d11xgklg0c0p8q.cloudfront.net/assets/*`), API at `api.znotes.org`
  (`/v1/*` content, `/v2/*` accounts/auth, `/api/*` feature families).
- **My Teaching Toolkit = the `educator-ai` dashboard panel**, reachable at
  `/content/dashboard?panel=educator-ai`; deep-linkable per resource via
  `/?panel=educator-ai&responseId={id}`.
- **Four generators, one endpoint**: all four submit to
  `POST /api/znotes-educator-ai` with `{ type, userId, data }` where
  `type ∈ {lesson-plan-generator, rubric-generator, sow-generator,
  clarify-challenge}`; generation is **async** — the server returns a
  `responseId` with `status: pending|processing`, the client polls
  `GET /api/educator-ai/responses/{responseId}` every 20 s (5 min timeout)
  and toasts "{Resource} is ready!" on completion.
- **Grounding is structural**: every form takes `subject/subjectId/module/
  moduleId` from the platform's own taxonomy, and Topic dropdowns are the
  chapters themselves (`/v1/chapters/withCards/dashboard`); lesson-plan
  requests auto-carry the chapter's `outcomes` as `learningObjectives`.
- **Quota model**: 5 lifetime free prompts (`Qn={FREE:5,PLUS:100}`),
  Boost-Plus educators get 100; counters live on the user record
  (`educatorAiUsageCount`), enforced client-side pre-submit.
- **Exports are client-side**: PDF / DOCX / CSV / JSON built in-browser
  (`docx` + `JSZip` shipped in the bundle) — no server render.
- Past-paper/question-bank surface (`/v1/questionBank`,
  `/api/randomQuestions/5/{id}`) and the student AI assistant
  (`/api/knowledge/query`, `/api/newbot/query`, `/chat-history`) also
  catalogued — separate from the toolkit.

## Blocker (resolved)

~~Teacher-account walkthrough blocked~~: the original credential string
failed with `401 INCORRECT_PASSWORD` because the password begins with a
**leading dash** that was absorbed into the "password:" prefix when
transcribed. With the corrected password the email+password login works,
and Phase 2 completed the same day (see the plan doc).

## Key facts (Phase 2 headline, live-verified)

- Account: teacher ("HNA 011", ABC International School); dashboard
  sidebar carries the full teacher panel set; toolkit opens from
  "My Teaching Toolkit".
- Every tool is a **wizard**: Subject* → Module* → tool form. Subject
  list is the full catalogue; Biology (CAIE IGCSE) modules: Theory /
  Alternative to Practical / Topic Explainer / Past Paper Walkthrough /
  Model Answers; Topic dropdowns = the 21 syllabus chapters.
- Free quota visible as "N out of 5 Free prompts left" in the modal
  header; decremented server-side on every submit.
- **Grounding proven**: a generated lesson plan's Learning Objectives
  are the verbatim CAIE 0610 syllabus outcomes for the chapter.
- Rubric scale is **computed from marksPerCriterion** (8 →
  Emerging 2 / Basic 4 / Proficient 6 / Advanced 8); Learning Coach
  outputs render as **6 tabs** (Main Argument … Connections).
- Exports PDF / DOCS / CSV / JSON confirmed in the result view;
  Regenerate re-opens the form without consuming a prompt.
