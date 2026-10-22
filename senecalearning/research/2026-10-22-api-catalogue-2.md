# API catalogue — Phase 2 (live, authenticated session)

**Captured**: 2026-10-22 · live teacher session + curl replays with the
`access-key` Firebase token (see `2026-10-22-auth-token-flow.md`). All
responses metadata-level; empty because the account is fresh.

## Verified live (200, saved where noted)

| Endpoint | Result shape |
|---|---|
| `GET class…/api/enrollments/me/classes?limit=100` | `{items:[],count:0}` |
| `GET class…/api/classes/me` | `{classId:"s11w5yatia", name, numStudents:0, numTeachers:1, timeCreated, userId}` — teacher class of record |
| `GET assignments…/api/teacher/me/assignments?from&to` | `{items:[],count:0}` (week-window query) |
| `GET assignments…/api/teacher/me/assignments/top-level?limit=100` | list (observed in UI flow) |
| `GET assignments…/api/classes/{classId}/assignments?limit=100` | class-scoped assignments |
| `GET memory…/api/memories` | `{items:[]}` — works with Firebase token |
| `GET xp…/api/xp/me?date=YYYY-MM-DD` | `{totalUserXp:0, yearly/monthly/weekly/dailyUserXp:0, userLevel:{level:0, currentLevelXpThreshold:0, nextLevelXpThreshold:100}}` |
| `GET feature-flags…/api/flags` | `{static:{…}, release:{…}}` — saved `feature-flags.json` |
| `GET course-cdn-v2…/api/courses?limit=3000&maxVisibility=HIDDEN` | full catalogue (anonymous) — see course-catalogue note |
| `POST course…/api/courses/queryCourses` `{}` | Elasticsearch results (`_index:course-entities-v2`, total 2053 PUBLIC) |
| `GET tags…/api/tags?includeNonCourseFilters=true` | tag tree for course-picker filters |
| `GET course…/api/subjects/me` | subject list for the user funnel |
| `POST tutor-resources…/api/v2/query-resources` | resource search (Core content / Hardest questions groupings, previews) |

## Observed in UI flow, unverified shapes

`GET assignments…/api/teacher/me/assignments/top-level?from=…&limit=100` ·
UI funnel: subject → age group → exam board → course → topics (per-subject
resource counts: Chemistry 14,753; Biology 21,051).

## Refused / unresolved (the auth-split family)

| Endpoint | Result | Note |
|---|---|---|
| `GET course…/api/courses/{id}` | 401 Unauthorized | rejects the Firebase token the other services accept |
| `GET session…/api/sessions` | 403 Missing Authentication Token | session-scoped auth |
| `GET tournaments…/api/tournaments` | 401 Invalid or missing access-key | scope/region mismatch |
| course-cdn-v2 `/api/courses/{id}` | CloudFront 403 `MissingKey` (Key-Pair-Id) | signed-URL delivery for course bodies |
| class `/api/classes`, `/api/classes/{id}`, `/api/teachers/me/classes` | 404 | teacher list lives at `/api/classes/me`; detail paths unresolved |
| stats `/api/stats/courses` | 400 "Unknown operation requested" | op-based contract (e.g. `?op=`) unresolved |
| user-info `/api/users/me`, `/api/me` | 404 | profile paths unresolved (likely `/api/users/{id}` or v2 paths) |

## Feature flags of record (release set, selected)

`invite-parent-reward`, `advertisePremiumiOS`, `sectionNotesPdf`,
`new-section-homepage`, `monthly-package-promo-05-2026-v2`,
`showPromptsToUseApp`, `simple-calculation-post-incorrect-scaffolding`,
`simple-calculation-try-again`, `update-start-session`,
`upload-learning-scheme`, `parent-onboarding`, `student-onboarding`,
`command-menu`, `in-app-admin`, `maths-dashboard-banner`,
`parent-claim-tutoring-modal` … full dump:
`resources/captures/feature-flags.json`. Static set confirms variant
detection (`isPrimaryApp`, `isPlurallApp`, `isGoStudentLearningApp`).

## XP model (verified)

Level = 100 XP per level (`nextLevelXpThreshold:100` at level 0); XP
buckets: total/yearly/monthly/weekly/daily — the engagement loop reads
this per day (`date` param required).

## Phase 2 leftovers (next session)

1. Signed-URL resolution flow for course bodies (watch browser opening a
   course).
2. `course.app`/`session`/`tournaments` auth family (Cognito? sigv4?
   different token?).
3. user-info + stats + class detail path map (need real traffic — create
   nothing; browse a course as a student-equivalent teacher preview).
4. Session loop protocol over `wss://session-ws` (needs a started session).
5. Chatbot payload shapes (costs LLM calls — keep to 1–2 tiny probes).

## Session 4 additions (2026-10-22 — Magic Quiz, session loop, memory)

Verified live (fetch-instrumented walkthrough + curl replays):

| Endpoint | Result shape |
|---|---|
| `POST user-quiz…/api/quizzes/generate` `{resourceText,type,tags,shareWithSchool,isPublic,options}` | `201 {quizId}` — AI quiz generation (full contract: magic-quiz note) |
| `GET user-quiz…/api/quizzes/me/{quizId}` | `{quizOverview, contents[].modules[]}`; poll loop `generating→complete` |
| `POST user-quiz…/api/quizzes/me/{quizId}/update` `{quizOverview,…}` | full-document update; 422 `{reason,pointer}`; free-tier gate `FREE_USER_CAN_ONLY_CREATE_PUBLIC_QUIZ` on `isPublic:false` |
| `POST session…/api/session` (session emit) | `200`; full module ledger + client-computed BKT posterior (session-lifecycle note) |
| `POST memory…/api/memories` `{courseId,courseName,sectionId,sectionTitle,locationId,timeEarned}` | `201` palace deposit |
| `GET memory…/api/memories` | `{items:[{id,courseId,sectionId,locationId,timeEarned,courseName,sectionTitle,location{name,countryName,imageURL,latitude,longitude}}]}` |
| `GET stats…/api/stats/sections?includeHardestQuestionsOnlyStats=true&courseId=` | `{stats:[{sessionsCompleted,totalStudyTime,lastStudied,averageScore,bestScore,worstScore,spacing,proficiency,recentSectionEvents[],moduleIdsStudied[],hardestQuestions*}]}` |
| `GET xp…/api/xp/me?date=` | `214 XP, level 2 (200→350)` after 1 session + quiz probe |
| `POST session…/api/session/quiz` | quiz-mode emit variant (client surface; same envelope) |
| `POST chatbot…/api/prompt` `{prompts,skipModeration}` | Magic/Amelia prompt engine (client surface; InappropriateContentError on 400) |
| `POST chatbot…/api/generate-prompts` / `POST …/api/search` | prompt-generation + search (client surface) |
| `POST /api/files/upload-url` `{fileName,contentType}` (user-quiz host) | signed upload for quiz images/files |
| `GET user-quiz…/api/quizzes/{quizId}` | PDF export (generateQuizPdf) |
| `POST session…/api/get-speech/module` | TTS narration for modules (422 on unsupported modules, observed ×12) |

WebSocket (see session-lifecycle note): `wss://session-ws…?access-key=<JWT>&sessionId=`
— OUT `start-session` / `keep-connection-alive`; IN `session-xp`
(`breakdown{completionXp,scoreXp,memoryXp}`, `reward`, level thresholds).

Observed in UI, unverified: `/quiz-preview` route, Wrong-Answers mode (needs
history), Exam-Questions mode, memory-palace map micro-question
(geolocation guess scored 0–100), weekly-plan (`GET /api/weekly-plan/me?weekStartDate=`).

## Session 8 additions (2026-10-22 — chatbot / Amelia)

Full contract in research/2026-10-22-chatbot-ai.md + captures/chatbot/endpoints-contract.json.
Auth: `access-key` Firebase token; streaming endpoints use raw fetch (correlationId +
access-key + user-region only), JSON endpoints use requestMaker (+X-Amz-Date).

| Endpoint | Style | Notes |
|---|---|---|
| `POST chatbot…/api/query` `{sessionId,text,image?}` | **stream** | Amelia chat; client-gen UUID session ids |
| `POST chatbot…/api/explain` | **stream** | |
| `POST chatbot…/api/explain-wrong-answer` `{courseId,courseName,sessionId,userProperties:{yearGroup},question,correctAnswer,userAnswer}` | **stream** | in-session coach |
| `POST chatbot…/api/exam-question-conversation` | **stream** | |
| `POST chatbot…/api/prompt` `{prompts,skipModeration}` | JSON | 400 InappropriateContent |
| `POST chatbot…/api/generate-prompts` | JSON | |
| `POST chatbot…/api/search` | JSON | live probe 502 (shape unverified) |
| `POST chatbot…/api/generate-image` `{prompt,orientation}` | JSON | 400 moderated / 401 unauthorised |
| `POST chatbot…/api/files/upload-url` `{contentType}` | JSON | `201 {uploadUrl:{fields,url}, key}` S3 presigned POST |
| `GET chatbot…/api/sessions?limit&lastKey` | JSON | `{items[]}` cursor list |
| `GET chatbot…/api/sessions/{id}` | JSON | `{sessionId, chatbotMessages[]}`; unknown id → synthesized empty 200 |
| `PATCH chatbot…/api/sessions/{id}` `{title}` | JSON | rename |
| `DELETE chatbot…/api/sessions/{id}` | JSON | 204; unknown id → 404 |
| `GET chatbot…/api/admin/sessions/{id}/message?userId&timestamp` | JSON | admin/observability surface |
| `GET text-to-speech…/api/get-speech/chatbot?sessionId&timestamp` | JSON | `{items:[{audioUrl,speechMarks}]}`; 400 `{reason,pointer}` |

Streaming protocol: `content-type: text/event-stream` but **raw UTF-8 text chunks**
(no SSE framing); errors signalled as literal StreamErrors strings in the stream
(`400 Bad request: inappropriate content`, `413 …conversation length limit hit`
→ graceful `lengthLimitHit:true`, `422 …`, `Unsupported region`, …).

Model stack (client-bundled constants): `gpt-4o` / `gpt-4o-mini`, temperature 0.1,
max completion 4096, response cap 700 tokens, query cap 500 words, **embeddings
context 300 tokens** — grounded RAG over Seneca course content.

Live gating (free teacher, non-UK egress): session CRUD 200; AI endpoints gated
pre-validation (`/api/query` → 200 + stream body `403 Forbidden`; `/api/prompt`,
`/api/generate-image` → 401 `Invalid or missing access-key`). Entitlement
(Amelia = Premium) and/or IP-region fence; distinguishing test needs UK egress.

Freemium quota: `FreemiumRewardFeature` = {explainMyAnswer, examQuestion,
wrongAnswers, hardestQuestions} granted as XP level-up rewards;
`remainingInvocation = premium ? Infinity : data?.explainMyAnswer ?? 0`.

## Session 9 additions (2026-10-22 — class analytics / school reporting / MIS)

Full contract in research/2026-10-22-class-analytics.md +
captures/class-analytics/. Per-student envelopes captured using the
teacher's own study history (no enrolled students needed).

| Endpoint | Style | Notes |
|---|---|---|
| `GET stats…/api/stats/users` | JSON | caller's own aggregate (sessionsCompleted, totalStudyTime, sessionModules*, recentlyStudiedCourses[]) |
| `GET stats…/api/stats/users/{uid}/windowed/courses?startTime&endTime[&withStatsGroupedByDateRanges=true][&lastKey]` | JSON | per-course windowed stats; 403 for non-context users; cursor-paged |
| `POST stats…/api/stats/users/windowed/courses/{courseId}?startTime&endTime` `{userIds[],contextId?}` | JSON | **class-analytics core**; `stats` map keyed by userId; foreign uid → 403 |
| `POST stats…/api/stats/sections/{sectionId}/enriched` `{userIds[],courseId,schoolId}` | JSON | per-user enriched section stats; 400 `{reason,pointer}` |
| `GET stats…/api/stats/{courses\|sections\|contents}?ids=a,b,c` | JSON | **collection op-contract** — no-ids → 400 "Unknown operation requested" (Phase-2 mystery solved); returns server-stored `proficiency`/`score` per (user,course) |
| `POST stats…/api/admin/stats/sections/aggregated` | JSON | 404 for free teacher (admin knowledge-gap path) |
| `POST class…/api/classes/section-stats` `{courseId,schoolId,classIds[],sectionIds[],bestScoreThreshold:0.8}` | JSON | knowledge-gap aggregation; **500 on empty class** (UI hits it too) |
| `GET class…/api/classes/me/{classId}` | JSON | detail path resolved (Phase-2 `/api/classes/{id}` 404 was a path miss): courseIds[], teachers[]+lastViewed, enrollments[] |
| `GET class…/api/classes/skeletons/me?limit=100` | JSON | lightweight class pickers |
| `POST class…/api/enrollments/me/classes/{classId}/last-viewed` | JSON | view tracking |
| `POST school-analytics…/api/schoolAnalytics/me` `{classIds[],includeTargetGroupsData,dateRange:"last7",wholeSchoolReport,startDate,endDate}` | JSON | **201** async report; requestId; XLSX over S3 presigned (24 h) |
| `GET school-analytics…/api/schoolAnalytics/me/{requestId}` | JSON | `{status:succeeded, downloadUrl, isMISEnabled, isPremium, meta}`; retry path `/retry/me` |
| `GET user-info…/api/user-info/me` · `/api/user-prefs/me` | JSON | profile/prefs — **requires Origin/Referer allowlist** (bare curl → 403) |
| `GET schools…/api/school-info/me` | JSON | 404 for standalone teacher (school-linked only) |

Access control: stats authorize requester→target via class/school context
(teacher-of); self allowed; foreign uid → `403 Not allowed to access this
user's data`. Knowledge gap = section best-score < 0.8. MIS "School Sync" =
sales lead form (`get-a-quote?formType=mis`), free-first-year bundle. Scheme
of learning = premium AI concierge beta (upload-learning-scheme flag; email
intake, no public endpoint). School Reports KPI cards render hard-coded
demo constants (267 / 5h 33m / 73%) on empty schools.
