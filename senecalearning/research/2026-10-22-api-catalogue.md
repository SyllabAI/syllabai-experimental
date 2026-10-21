# API catalogue — Seneca Learning (Phase 1 sample)

**Captured**: 2026-10-22 · method: (a) endpoint strings extracted from the
290-chunk bundle corpus (local, not committed), (b) live anonymous probes
with `Origin: https://app.senecalearning.com`. Full machine-readable lists:
`resources/captures/extracted-paths.json` (+ `extracted-paths-2.json`).

## Transport & conventions

- Hosts: `{service}.app.senecalearning.com` (map:
  `2026-10-22-service-map.md`), AWS API Gateway style.
- Headers the contract expects: `Authorization` (Cognito JWT),
  `correlationId`, `user-region`, `user-language` (+ `X-Api-Key`,
  `X-Amz-Security-Token` accepted).
- Errors: uniform `{"message":"..."}` (404/401) or
  `{"code":"BadRequest","message":…,"type":"client"}` (identity host).
- CORS: pinned to the app origin; methods per endpoint (chatbot:
  `OPTIONS,POST` only).
- Live probes (anonymous, no token): chatbot `POST /api/query` → **401
  Unauthorized**; course service paths → 404 (path-locked, auth-locked);
  identity auth paths → structured 400 (needs POST body). **No anonymous
  content access anywhere** — unlike undergroundmathematics, nothing is
  publicly readable.

## Verified endpoint strings from the bundle corpus

### Authentication (`identity.app.…`)
| Path | Notes |
|---|---|
| `POST /v1/token` | token issue/refresh (assumed POST; GET → structured 400) |
| `GET/POST /v1/recaptchaParams`, `/v2/recaptchaConfig` | reCAPTCHA bootstrap |
| `GET/POST /v2/passwordPolicy` | server-driven password rules |

### Learning data (hosts per service map)
| Path | Host | Notes |
|---|---|---|
| `/api/enrollments/me/courses` | enrollments | the student's course list |
| `/api/memories`, `/api/memories/{id}` | memory | spaced-repetition state (R/W) |
| `/api/stats/contents` | stats | per-content stats |
| `/api/stats/courses` | stats | per-course aggregates |
| `/api/stats/sections` | stats | per-section aggregates |
| `/api/grades` | (grades) | grade records |
| `/api/locations`, `/api/locations/{id}` | locations | school/region locations |
| `?schoolId={id}` | schools | school-scoped queries |
| `?includeArchived={bool}` | (assignments/classes) | list modifier |

### AI tutor (`chatbot.app.…`, all Cognito-gated)
| Path | Purpose (name-implied) |
|---|---|
| `POST /api/query` | free-form tutor query |
| `POST /api/explain` | explain-this-concept |
| `POST /api/explain-wrong-answer` | targeted remediation after a wrong answer |
| `POST /api/exam-question-conversation` | conversational marking/feedback on exam questions |

### Resource-shape strings (paths per client, host unresolved yet)
`courses/:legacyCourseId`, `answers/:questionId`, `users/{id}`,
`me/update`, `students/invalid`, `teachers/invalid`, plus bare resource
names: courses, sections, sessions, questions, answers, memories, notes,
assignments, classes, students, teachers, users, parents, schools,
subscriptions, enrollments, notifications, leaderboards, xp, stats.
(Chunk-named services `classLeaderboardsService` / `schoolLeaderboardsService`
corroborate leaderboard scoping.)

## Route-level app surface (for orientation)

`/login`, `/sign-up`, `/dashboard`, `/dashboard/assignments/todo`,
`/dashboard/courses/add`, `/dashboard/what-is-premium`, `/classroom`,
`/session`, `/multi-section/end-session`, `/teacher`, `/parent`,
`/parent/monitoring/overview`, `/parent/tutoring`,
`/parent/what-is-premium`. (`resources/captures/extracted-paths-2.json`.)

## What Phase 2 must resolve

1. The client class → host → path map (each service client builds paths
   from `env.js` config; bundles name clients —
   `ServiceClientRegistry.registerClient(service, ClientClass)` — but
   minification hides literal paths; a browser session with devtools or an
   authenticated token dump resolves this in minutes).
2. Request/response schemas for the learning loop (session events,
   memory writes, XP grants).
3. Chatbot payload shapes + streaming vs batch behaviour.
4. Entitlement gate behaviour (subscriptions/trials) — the DC3 analogue.
