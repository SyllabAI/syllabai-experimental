# Class analytics, school reporting & MIS — Reverse Engineering

**Session 9 · 2026-10-22 · authenticated teacher pass + 1,920-chunk static sweep**

Companion artifacts: `resources/captures/class-analytics/` (sanitized contracts
and envelopes). Method: (1) network-instrumented walkthrough of every teacher
reporting surface — Classes ▸ Students / Knowledge gaps / Class settings,
School Reports ▸ Students / Teachers / Parents tabs, the custom-report wizard,
the School Sync funnel; (2) static extraction of the `StatsServiceClient` /
`ClassServiceClient` / `SchoolAnalyticsClient` surfaces from the full
recursive chunk closure (1,920 chunks, re-derived this session); (3) live
probes replayed with the teacher token, ≤1 req/s, using the teacher's own
study history (6 sessions) as the populated-data fixture so per-student
envelopes could be captured without any enrolled students.

---

## 1. Service topology (reporting-relevant)

| Host | Role |
|---|---|
| `stats.app.senecalearning.com` | learner-stats engine: per-user, per-course/section/content aggregates + windowed queries |
| `class.app.senecalearning.com` | class records, roster/enrollments, knowledge-gap section-stats aggregation |
| `school-analytics.app.senecalearning.com` | **new service** — async custom-report generation (XLSX over S3) |
| `user-info.app.senecalearning.com` | profile (`/api/user-info/me`, `/api/user-prefs/me`) |
| `schools.app.senecalearning.com` | school records (`/api/school-info/me`; 404 for standalone teachers) |
| `memory.app.senecalearning.com` | palace deposits (Knowledge-gaps view pulls `?limit=2000`) |

## 2. Teacher reporting surface map (routes)

```
/teacher/classes                          class list (skeletons)
/teacher/class/{id}/overview              setup state, counts
/teacher/class/{id}/assignments           class-scoped assignment list (S3)
/teacher/class/{id}/students              roster (enrollments[] embedded in class detail)
/teacher/class/{id}/knowledge-gaps/sections  per-section gap view (premium pitch when empty)
/teacher/class/{id}/settings              rename / add course / archive / delete
/teacher/reports/students                 "School reports" hub: Students|Teachers|Parents tabs,
                                          KPI cards, custom-report wizard, School Sync CTA
/generate-custom-report/type → /details   report wizard (type → scope/date → generate)
/teacher-custom-report?requestId=…        "Your report has landed!" + download
/teacher/what-is-premium/get-a-quote?formType=mis   MIS sync = sales lead form
```

The INSIGHTS nav group is: School Reports, Student Reports, Knowledge Gaps,
Resource Hub, CPD — the first three all resolve onto the reporting hub above.

**Demo-data quirk**: with 0 students and no school record
(`school-info/me → 404`), the School Reports hub still renders KPI cards —
"267 Active students / 5h 33m / 73%" — with no backing API response observed.
These are client-side placeholder constants (marketing-state defaults), worth
remembering as a UX anti-pattern: SyllabAI should render a true empty state.

## 3. StatsServiceClient — full surface (17 methods, `out-58RVUDXs.js`)

Learner-stats client; mixed GET/POST styles via `requestMaker`.

| Method | Wire call | Notes |
|---|---|---|
| `fetchUserStats()` | `GET /api/stats/users` | caller's own aggregate |
| `fetchUserContentsStats(ids)` | `GET /api/stats/contents?ids=…` | collection op |
| `fetchUserSectionsStats(ids,{includeHardestQuestionsOnlyStats})` | `GET /api/stats/sections?ids=…&includeHardestQuestionsOnlyStats=true` | collection op |
| `fetchUserCoursesStats(ids)` | `GET /api/stats/courses?ids=…` | collection op |
| `fetchCourseSectionStatsForUser(courseId,{})` | `GET /api/stats/sections?courseId=…` | per-course section stats |
| `fetchCourseContentStatsForUser(courseId,{})` | `GET /api/stats/contents?courseId=…` | per-course content stats |
| `fetchAllCourseStatsForUser({})` | paged `GET /api/stats/courses/...` | `_generatePagingQueryParams` |
| `fetchWindowedUserCourseStats(userId,start,end,grouped)` | `GET /api/stats/users/{uid}/windowed/courses?startTime&endTime[&withStatsGroupedByDateRanges=true][&lastKey]` | cursor-paged |
| `fetchWindowedMultiUserCourseStats({contextId,userIds[],courseId,start,end})` | `POST /api/stats/users/windowed/courses/{courseId}?startTime&endTime` body `{userIds,contextId}` | **class-analytics core** |
| `fetchAggregatedEnrichedUserSectionStats({userIds[],sectionId,courseId,schoolId})` | `POST /api/stats/sections/{sectionId}/enriched` | per-user enriched section stats |
| `adminFetchAllCourseStatsForUser` / `adminFetchPageOfAllCourseStatsForUser` | admin variants | 404 for free teacher |
| `adminFetchWindowedCourseStatForUser({courseId,userId,startEpochSeconds,endEpochSeconds})` | admin variant | |
| `adminFetchAggregatedUserSectionStats({courseId,sectionIds[],userIds[],bestScoreThreshold})` | `POST /api/admin/stats/sections/aggregated` | knowledge-gap admin path |

### 3.1 The `?ids=` op-contract (Phase-2 mystery resolved)

Collection endpoints are **op-dispatched**: `GET /api/stats/courses` with no
query → `400 {"reason":"Unknown operation requested"}` (exactly the Phase-2
probe failure). With `?ids=<uuid>,<uuid>,…` →
`200 {"stats":[…],"count":N}`. `buildUrlFromIds` packs ids comma-joined into a
~2,000-character URL budget before paging. Verified:

```
GET /api/stats/courses?ids={studiedCourse}
→ 200 {"stats":[{"userId","courseId","sessionsCompleted":4,"totalStudyTime":1305,
   "lastStudied":1792667022,"sessionModulesStudied":19,"sessionModulesCorrect":9,
   "proficiency":0.0021875,"score":0.004098…,
   "hardestQuestionsTotalStudyTime":0,"hardestQuestionsSessionsCompleted":0,
   "hardestQuestionsSessionModulesStudied":0}],"count":1}
```

**`proficiency` and `score` are server-stored** here (the session-6 formula's
output, written blind by the client at session emit) — this is the row the
teacher dashboards and report exporter read.

### 3.2 Windowed per-user stats (real envelope)

```
GET /api/stats/users/{uid}/windowed/courses?startTime=<epoch>&endTime=<epoch>
→ 200 {"userId","startTime":"…Z","endTime":"…Z","stats":{
    "{courseId}":{"userId","courseId","modulesStudied":19,"modulesTested":14,
      "modulesCorrect":9,"modulesIncorrect":5,"modulesGaveUp":1,
      "averageScore":0.7766…,"studyDuration":1543,"sessionsCompleted":4,
      "earliestStudySession":"…Z","latestStudySession":"…Z"}, …}}
```

- `?withStatsGroupedByDateRanges=true` is a client-flagged variant; observed
  response shape was identical for our window (grouping is applied downstream
  client-side or only activates for longer windows).
- `?lastKey=` cursor paging for long result sets.

### 3.3 Multi-user windowed query — the class-dashboard engine

```
POST /api/stats/users/windowed/courses/{courseId}?startTime=E&endTime=E
     {"userIds":["<uid>", …], "contextId":"<classId>"}
→ 200 {"userIds":[resolved…],"courseId","startTime","endTime",
       "stats":{"{userId}":{…same per-course shape…}}}
```

- With `contextId` = our empty class, the teacher's own uid was **dropped**
  from `userIds` (not an enrolled student) → `stats:{}`.
- Without `contextId`, the requested userIds pass through and the map comes
  back **populated** (`stats` keyed by userId) — captured with the teacher's
  own history as the fixture.
- **Access control**: foreign userId → `403 {"reason":"Not allowed to access
  this user's data"}` (verified with a random uuid). The server authorizes
  the requester against each target user via class/school context
  (teacher-of relationship); self-access is allowed. Auth model is the
  standard `access-key` Firebase token.

### 3.4 Enriched section stats

```
POST /api/stats/sections/{sectionId}/enriched
     {"userIds":["…"],"courseId":"…","schoolId":""}
→ 200 []  (empty for unstudied section; array of per-user enriched records
   when populated)
```
400 family uses the standard `{reason,pointer}` shape; 403 =
`ForbiddenStatsAccessError`.

## 4. Knowledge gaps (per-class, per-section)

Class ▸ Knowledge-gaps tab fires, per course, the **class-service aggregation**:

```
POST class…/api/classes/section-stats
     {"courseId":"…","schoolId":"","classIds":["{classId}"],
      "sectionIds":["…×106"],"bestScoreThreshold":0.8}
```

- `bestScoreThreshold: 0.8` — **a knowledge gap is a section where the
  student's best score never reached 80%**. The client computes the candidate
  section set (from the course section tree) and lets the server aggregate.
- **500-on-empty**: with zero enrolled students the endpoint returns
  `{"message":"Internal Server Error"}` — observed *identically from the real
  UI* (7 consecutive 500s) and from replay. A server-side empty-set bug worth
  noting: Seneca's own dashboard degrades to an error until the class is
  populated.
- The UI wraps the feature in a **premium pitch** ("Knowledge gap assignments
  — assign adaptive, individualised assignments to fill gaps in student
  knowledge") — the free tier sees the gap data machinery but the actionable
  adaptive-assignment flow is gated.
- The same tab pulls `memory…/api/memories?limit=2000` (palace deposits) and
  the course section tree to render the gap grid.

## 5. Custom reports — async pipeline (`school-analytics` service)

The "Create custom report" wizard (Class report) issues:

```
POST school-analytics…/api/schoolAnalytics/me
     {"classIds":["{classId}"],"includeTargetGroupsData":false,
      "dateRange":"last7","wholeSchoolReport":false,
      "startDate":"2026-10-15T00:00:00+00:00",
      "endDate":"2026-10-22T23:59:59+00:00"}
→ 201  (requestId minted; UI redirects to /teacher-custom-report?requestId=…)

GET /api/schoolAnalytics/me/{requestId}
→ 200 {"status":"succeeded","downloadUrl":"<S3 presigned GET, expires=86400>",
       "isMISEnabled":false,"isPremium":false,
       "meta":{"classIds":["…"]},"wholeSchoolReport":false,
       "requestDate","startDate","endDate","userId","requestId"}
```

- Generation completed in **~7 s** for 1 class / 0 students. Client also
  carries a retry path (`/api/schoolAnalytics/retry/me`).
- **Storage**: `s3://seneca-school-analytics-v1/userId=<uid>/reportId=<uuid>`
  — hive-partitioned per-user keys, presigned GET with 24-hour expiry.
- **Artifact**: Microsoft Excel (OOXML), 3 sheets:

| Sheet | Columns |
|---|---|
| Students | First name · Last name · Year group · Total study time (hours) · Questions studied · Correct answers · Average score · Sessions completed |
| Classes | Class name · Class code |
| Subjects | Subject · … (further columns; header-only in our empty-class sample) |

  Empty-class behaviour is explicit: the Students sheet carries a single
  message cell — *"Error - It appears you have no students to report on - try
  generating a report on classes that have students in to see results!"*
- **Demographics gate**: "Include target group breakdown (PP, SEN, EAL, FSM,
  etc)" checkbox is **disabled** on free tier (`includeTargetGroupsData`
  rides the POST payload) — UK school-demographics analytics is premium.

## 6. Class service — roster & lifecycle affordances

- `GET /api/classes/me/{classId}` — the **detail path resolved** (Phase 2's
  bare `/api/classes/{id}` 404'd; the teacher-scoped form works): full record
  with `courseIds[]`, `teachers[]` (incl. `lastViewed`), `enrollments[]`
  (the roster), `myTeacherAccessors[]`.
- `GET /api/classes/skeletons/me?limit=100` — lightweight picker list.
- `POST /api/enrollments/me/classes/{classId}/last-viewed` — view tracking
  (drives `lastViewed` on the teacher accessor).
- Settings tab affordances: rename, add/remove course, **archive class**,
  **delete class** (PATCH/DELETE family left un-exercised this session — the
  class record is load-bearing for future analytics work).
- Students tab lists `enrollments[]` (join code / invite flows live here on
  the UI; roster mutation was out of scope without real students).

## 7. user-info + schools

- `GET user-info…/api/user-info/me` → `{"userId","type":"schoolteacher",
  "teacherRole":"classroom_teacher","displayName","givenName","familyName",
  "nickname","providerData":[…]}` — **requires `Origin`/`Referer`
  (app-origin allowlist)**: bare curl gets 403, browser-origin curl gets 200.
  Same for `/api/user-prefs/me`. Phase 2's user-info 404s were path misses
  (`/api/users/me` vs the real `/api/user-info/me`).
- `GET schools…/api/school-info/me` → 404 for a standalone teacher — school
  records only exist for school-linked accounts (the MIS path below).

## 8. MIS / "Seneca School Sync" — sales-only surface

- Reports hub CTA → `/teacher/what-is-premium/get-a-quote?formType=mis&source=reports-students`:
  a **lead form** (name, work email, role) — no self-serve technical API.
- Bundle copy: *"The School Sync Package is free for the first year with no
  commitment"* — MIS rosters (Wonde/Arbor-style) are sold, not configured.
- Client carries `useIsManagedByMIS` + `MIS_INFO` / `MIS_EXPIRY` routes:
  MIS-synced schools have rosters/assignments managed externally, with
  expiry states surfaced in the teacher shell.

## 9. Scheme of learning — premium AI beta (human-in-the-loop)

Feature flag `upload-learning-scheme`; routes alias `scheme-of-learning`;
gated behind `BatchAssignmentGatingModal` + premium. Product copy from
`UploadLearningSchemeModal`:

> *"We read your scheme of learning document, match it to our content, and
> schedule the whole year — in seconds"* … *"Send us your Scheme of Learning"*
> (mailto link) … *"We'll test the feature against…"*

So the "AI reads your scheme document and schedules the year" flow is, as of
this build, a **concierge beta**: documents go in by email, are matched to
Seneca content offline, and come back as a batch assignment schedule. The
batch-assignment journey saves local drafts ("We found a saved draft of your
scheme of learning from …"). No public endpoint yet — the machine-readable
part is the batch-assignment scheduler it feeds (assignments service, S3).

## 10. SyllabAI takeaways

1. **Windowed stats are the reporting backbone** — one endpoint
   (`POST /api/stats/users/windowed/courses/{courseId}` with `{userIds,
   contextId}`) powers class dashboards, knowledge-gap views and the report
   exporter. SyllabAI should design the same *single* aggregate-query surface
   (Postgres + pgvector-friendly) instead of N per-page endpoints.
2. **Server-side authorization is context-scoped** (teacher-of relationship),
   and the deny case is a clean 403 — mirror this exactly; our pilot's
   50-student rosters make per-user authorization cheap at this scale.
3. **Knowledge gap = best-score threshold (0.8), not recency-weighted
   mastery** — deliberately simple and explainable to teachers. SyllabAI can
   differentiate: threshold *or* mastery-from-the-memory-model, with the
   same "adaptive individualised assignment" upsell attached.
4. **Reports as async artifacts over object storage** (POST → requestId →
   poll → presigned URL) is the right pattern for R2 + our $0 stack; the
   3-sheet XLSX layout (Students / Classes / Subjects) is a sensible export
   schema to match for teacher familiarity.
5. **Seneca's empty-state bugs are instructive**: section-stats 500s on an
   empty class and the report generator's in-file error cell — SyllabAI
   should ship true empty states and idempotent zero-row aggregates.
6. **Demo constants on a paid-analytics surface** (267/5h33m/73% cards) show
   the risk of hard-coded marketing numbers — never ship placeholder KPIs.
7. **MIS sync is sold, not built self-serve** — for SyllabAI's pilot the
   CSV-class-import route (no integration) is the honest v1.

## Probe hygiene

≤1 req/s across all probes; no class/roster mutations (settings affordances
observed, archive/delete unexercised); the one report generated is the
operator's own data over their own classes; userIds in committed captures are
redacted; JWT stayed in `/tmp/seneca_token.txt` (removed post-session); raw
probe bodies remain in workspace `probe-results/s9/` (git-ignored); only
sanitized exemplars committed here. No student PII was ever touched (the
account has no enrolled students).
