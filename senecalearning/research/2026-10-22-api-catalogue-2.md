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
