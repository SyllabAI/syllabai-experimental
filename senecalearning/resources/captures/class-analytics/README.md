# Class-analytics captures — session 9 (2026-10-22)

Sanitized, commit-ready evidence for the teacher analytics surface
(research companion: `research/2026-10-22-class-analytics.md`).

**Redaction applied**: userId → `<userId-redacted>`; names/emails dropped;
class name → `<class-name-redacted>`; S3 presigned URLs → structural sketch;
no tokens (JWT lived in `/tmp` only, deleted after the session).

| File | What |
|---|---|
| `endpoints-contract.json` | master contract: verified endpoints (method/path/host/status/note), access-control rule, empty-class behaviour matrix |
| `stats-windowed-envelope.json` | `GET /api/stats/users/{uid}/windowed/courses` response with real study history (2 courses) |
| `stats-multi-user-windowed-envelope.json` | `POST /api/stats/users/windowed/courses/{courseId}` — the class-analytics core, populated for the requester; `stats` keyed by userId |
| `stats-course-aggregate-envelope.json` | `GET /api/stats/courses?ids=…` — per-(user,course) aggregate incl. server-stored `proficiency` + `score` (session-6 formula output) |
| `section-stats-request-contract.json` | `POST /api/classes/section-stats` knowledge-gap request (section list truncated) |
| `school-analytics-report-contract.json` | async custom-report lifecycle record: `{status:succeeded, downloadUrl, isMISEnabled, isPremium, meta.classIds…}` |
| `custom-report-xlsx-structure.json` | the generated report's OOXML structure: 3 sheets + column schema + empty-class error cell |

Provenance: live authenticated teacher session (≤1 req/s), request bodies
captured via an in-page `fetch` hook, responses replayed via curl with the
session's `access-key` header. Raw (unredacted) probe artifacts stayed in the
workspace `probe-results/s9/` (git-ignored path, not committed).
