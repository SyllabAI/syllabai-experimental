# Assignment creation & lifecycle — complete contract

**Captured**: 2026-10-22 · live teacher session (`hussainna071@gmail.com`,
teacher role, own empty class). Every request below was observed in the
production UI and replayed/verified. Payload exemplars (values redacted
where personal) live in `resources/captures/assignments/`.

## Funnel routes (teacher SPA)

| Route | Step |
|---|---|
| `/teacher/assignments/create/class` | 1 — choose class(es) |
| `/teacher/assignments/create/content` | 2 — pick subject → course → topics/resources (the Resource Hub picker) |
| `/teacher/assignments/create/details` | 3 — name, start/due dates, students |
| `/teacher/class/{classId}/edit-assignment/{assignmentId}/content` | edit flow step 1 (content) |
| `/teacher/class/{classId}/edit-assignment/{assignmentId}/details` | edit flow step 2 ("Update") |
| `/share-assignment?assignmentId&classId` | share page (link / Google Classroom / Microsoft Teams / Email) |
| `/delete-class-assignment?classId&assignmentId` | delete confirmation page |
| `/teacher/assignments/scheme-of-learning/classes` | batch planner ("Scheme of learning") — schedule a batch of assignments across weeks; needs a populated class to walk deeper |

Create menu also exposes: **Assignment**, **Scheme of learning** (batch),
**Magic Quiz** (AI-generated material), **Report**, **Class**, **Game**
(Beta).

## CRUD contract (verified live)

| Op | Request | Result |
|---|---|---|
| Create | `POST assignments…/api/teacher/assignments` | 201 → assignment record |
| Read (global) | `GET assignments…/api/assignments/{assignmentId}` | 200 → teacher-view record |
| Read (class-scoped, with stats) | `GET assignments…/api/classes/{classId}/assignments/{assignmentId}?omitLegacyStats=true` | 200 → class view incl. aggregations |
| List (teacher, week window) | `GET assignments…/api/teacher/me/assignments?from=…&to=…&limit=100&withAssignees=true` | 200 `{items,count}` |
| List (teacher, top-level) | `GET assignments…/api/teacher/me/assignments/top-level?from=…&limit=100` | 200 |
| List (class) | `GET assignments…/api/classes/{classId}/assignments?limit=100` (`&date=YYYY-MM-DD` variant observed) | 200 `{items,count}` |
| Update | `PATCH assignments…/api/classes/{classId}/assignments/{assignmentId}` | 200 → updated class view |
| Delete | `DELETE assignments…/api/classes/{classId}/assignments/{assignmentId}` | 204 |

Note the asymmetry: **create** is teacher-global
(`/api/teacher/assignments`), while **update/delete** are class-scoped
(`/api/classes/{classId}/assignments/{id}`). A `PATCH` on
`/api/teacher/assignments/{id}` is 404 — the class path is the only
update route.

## Create payload (exact, verified)

```json
{
  "name": "…",
  "spec": {
    "tasks": [
      {
        "id": "<resource UUID>",
        "taskType": "resource",
        "resourceType": "exam-question",
        "courseId": "<course UUID the resource is attached to>"
      }
    ]
  },
  "autoEnrolNewUsers": true,
  "classes": [
    { "classId": "s11w5yatia",
      "startDate": "2026-10-22T00:30:00.767Z",
      "dueDate":   "2026-10-29T00:45:00.767Z" }
  ]
}
```

- `resourceType` values observed: `exam-question`; the Resource Hub's
  other pickable types imply `core-content`-style section tasks and
  `quiz` (courseSection/quiz resources — see resource-hub note).
- The **UI defaults**: start = now (minute-truncated), due = now + 7 days
  (+15 min). Both user-editable.
- `autoEnrolNewUsers: true` is what makes the share link work for
  students not yet in the class — anyone opening the link joins the
  class and receives the assignment.

## Update payload (exact, verified)

`PATCH` takes the **full document** (not a delta):

```json
{ "startDate": "…", "dueDate": "…", "name": "…",
  "assignees": [],
  "spec": { "tasks": [ … same shape as create … ] },
  "autoEnrolNewUsers": true }
```

`assignees` is the per-student targeting list (empty = whole class).

## Assignment record (server response shapes)

Teacher-view (`/api/assignments/{id}`, `POST` response, list items):
`assignmentId`, `assignmentName`, `autoEnrolNewUsers`, `creatorId`,
`timeCreated`, `timeUpdated`, `spec.tasks[]`, `classIds[]`,
`numAssignees`.

Class view (adds scheduling + stats):
`startDate`, `dueDate`, **`assignmentCutoffDate`** (= dueDate + 14 days
— hard stop after which results can't change), `archived`, `name`,
`assignees[]`, `teacherName`, and three aggregation blocks:

```json
"sectionAggregations": [],            // per course-section rollup
"contentAggregations": [],            // per content-item rollup
"questionAggregations": { "questions": [], "marksTotal": 0, "averageMark": 0 },
"totalAggregations": { "completionRate": 0, "averageScore": 0,
                       "bestScore": 0, "averageStudyTime": 0,
                       "totalCompleted": 0 }
```

With students, the aggregation blocks fill with per-section /
per-question performance data — the analytics layer that SyllabAI's
Insights module mirrors.

## Share surface

- Copy-link: `https://app.senecalearning.com/dashboard/class/{classId}/assignments/assignment/{assignmentId}`
- Native targets: Google Classroom, Microsoft Teams, Email
- Class code path also exists (`Class code: s11w5yatia` on the class
  page — students join with the code instead of the link)

## Status model (observed)

- UI badges: `In Progress` / `Active` vs `Complete` (teacher list tabs:
  "Active" / "Complete"); states derive from startDate/dueDate and
  assignee completion, not a stored enum visible in the record.
- `archived: false` flag on the class-view record (archive ≠ delete).

## Cleanup

The probe assignment used to capture these shapes was deleted via the
production UI (`DELETE` → 204) in the same session; the account ended
clean ("0 active · 0 complete").

---

## Session 7 housekeeping (2026-10-22)

- `GET /api/teacher/me/assignments` → `{items: [], count: 0}` — account
  re-verified clean after sessions 3–6 (no probe assignments remain).
- Resource Hub full metadata harvest completed same session — see
  research/2026-10-22-resource-hub.md session-7 addendum. The
  Hub ⇄ assignment `spec.tasks[]` linkage (session 3) is unchanged.
- Still open on the assignment side: **Scheme-of-learning** and
  **per-student assignment analytics** — both require a class with
  enrolled students; not reachable from tooling alone (operator-side).
