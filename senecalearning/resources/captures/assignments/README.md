# Assignment API exemplars — redacted

**Captured**: 2026-10-22 (Phase 2 session 3) · one throwaway assignment
created on the teacher's own empty class via the production UI, then
deleted (`DELETE` → 204; account ended "0 active · 0 complete").
`creatorId` values redacted to `<REDACTED-userId>`; the classId is the
same already-committed `s11w5yatia` (class-me-redacted.json).

| File | Endpoint | Note |
|---|---|---|
| `assignment-create-request.json` | `POST /api/teacher/assignments` | exact body: name, spec.tasks[], autoEnrolNewUsers, classes[{classId,startDate,dueDate}] |
| `assignment-create-response.json` | → 201 | teacher-view record |
| `assignment-update-request.json` | `PATCH /api/classes/{classId}/assignments/{id}` | full-document update (not a delta) |
| `assignment-class-view-with-stats.json` | `GET /api/classes/{classId}/assignments/{id}?omitLegacyStats=true` | class view: cutoff date (due+14d), aggregation blocks (section/content/question/total) |

Full contract + lifecycle: `research/2026-10-22-assignments-model.md`.
