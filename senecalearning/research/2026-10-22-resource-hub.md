# Resource Hub — model, API contract & metadata catalogue

**Captured**: 2026-10-22 · live teacher session + curl replays.
The Resource Hub is Seneca's teacher-facing content library: every
assignable/previewable item across all subjects. This note documents the
model and commits a **metadata-only** catalogue (~207k resources
covered); content bodies (question text, mark schemes, generation
scripts, lesson content) were observed but stay local-only per the IP
notes.

## UI surface (`/teacher/resource-hub`)

- Resource-type tabs: **All · Core Content · Exam Questions · Quizzes ·
  Vocabulary** (counts rendered as "10,000+" until filtered)
- Filters: **Subject → Age Group → Exam Board → Course** + free-text
  search
- Cards: title, subject, age group, exam board, course, mark value
  (exam questions), "Select resource" (assign/preview)
- The same picker backs the assignment-creation content step
  (`/create/content`) — Hub ⇄ Assignments are one graph, not two
  features. From the picker the teacher selects specific resources;
  each becomes one `spec.tasks[]` entry (see assignments-model note).

## Search API — `POST tutor-resources…/api/v2/query-resources`

Elasticsearch-backed. Request:

```json
{
  "query": "",
  "filters": { "tags": { "<tagTypeId>": ["<tagId>", …] } },
  "resourceFilters": [ { "type": "examQuestion", "must": {} } ],
  "from": 0, "size": 200,
  "aggregatePublishers": false,
  "aggregateResourceTypes": true,
  "aggregateExamQuestionMarksTotal": false,
  "globalAggregations": false
}
```

- Tag filters are `tagTypeId → tagId[]` maps (taxonomy below); subject
  tag-type id = `8c71d055-ff40-4536-8629-5073c618ea53`.
- `resourceFilters[].type` values observed: `courseSection` (core
  content), `examQuestion`, `quiz` (+ `vocabulary` in the UI; API
  returned 422 for vocabulary under a subject filter in our probe —
  vocabulary items live under different tag combinations).
- `size: 200` max observed from the production UI; pagination via
  `from`/`total`.
- The `must` block accepts ES-style term filters (unused in the plain
  UI flow).

Response: `{ items: [ { _index: "tutor-resources-000002", _id, _source
{…} } ], total, aggregations }`.

`_source` **metadata** fields (committed in our catalogue):
`id, title, type, region, timeCreated, questionType, publisher,
marksTotal, answerCount, difficulty, tags {dim → [{id, value}]},
meta.courseIds[], topicBreadcrumbs` (e.g. `Chemistry: AQA GCSE
Foundation > Atomic Structure > Atoms & Elements > Relative Atomic
Mass` — the per-course placement of the resource).

`_source` **content** fields (NOT committed, local-only):
`questionTitleMd` (templated question text, `$var` placeholders),
`markScheme` (full scheme incl. `<tex>` markup), `generationScript`
(procedural randomisation script — `pick(30,35)` etc.), plus the
course-section content bodies for `courseSection` items.

## Tag taxonomy — `GET tags…/api/tags`

Requires the `user-region` header (400 `missing region header`
otherwise). Flat tag list; every tag carries `semanticCategory`:

| semanticCategory | count | examples |
|---|---|---|
| subject | 74 | Chemistry, Biology, Maths, Psychology… |
| ageGroup | 21 | GCSE, A Level, iGCSE, KS2/KS3, Uni & Uni Entrance… |
| examBoard | 12 | AQA, Edexcel, Edexcel iGCSE, OCR, Cambridge International… |
| type | 19 | Standard, Updated, HyperLearning, Higher/ Foundation variants |
| price | 3 | Free, Premium, (third) |
| pathway | 3 | Combined, Triple, … |
| tier | 3 | (subscription tier tags) |

Committed: `resources/captures/resource-hub/tags-taxonomy-slim.json`
(id/text/semanticCategory/parentId/subjectGroup/aliases per tag).

## Catalogue size — subject × type matrix

One aggregation query per subject tag (`aggregateResourceTypes: true`)
gives the exact per-type counts. **Grand total: 207,629 resources
across 74 subjects.** Top subjects (courseSection/examQuestion/quiz):

| Subject | Sections | Exam Qs | Quizzes | Total |
|---|---|---|---|---|
| Biology | 11,538 | 8,518 | 4,796 | 24,852 |
| Physics | 11,884 | 4,852 | 3,038 | 19,774 |
| History | 6,819 | 4,613 | 7,166 | 18,598 |
| Chemistry | 9,833 | 5,091 | 3,382 | 18,306 |
| English Literature | 11,142 | 1,351 | 4,547 | 17,040 |
| Geography | 4,706 | 4,401 | 5,184 | 14,291 |
| Maths | 5,455 | 1,666 | 2,838 | 9,959 |
| … full 74-subject table | | | |
| **Total** | | | | **207,629** |

Committed: `resources/captures/resource-hub/subject-resource-counts.csv`.

## Course & section entities — `POST course…/api/courses/queryCourses`

Same ES cluster as Phase 2 (`_index: course-entities-v2`); filters
discovered this session:

- `{"query": "<full text>"}` → courses (matches title/tags)
- `{"query": "<text>", "types": ["section"]}` → **section entities**:
  `sectionNumber`, `sectionLevel` (`top`/sub), `parentId`,
  `title`, `visibility`, `tags` — the section tree of any course is
  fully enumerable by prefix-matching the course title.
- Course `_source` carries `sectionIds[]`, `startingSectionId`,
  `examQuestionsCount`, `subscriptionTier`, `textToSpeechEnabled`,
  `vocabularyEnabled`, `authors`, full tag map.

Direct `GET /api/courses/{id}` stays 401 (auth-split family, Phase 2
session 1) and course **bodies** stay behind CloudFront signed URLs —
the ES metadata route is the only structural window, and it is enough
for taxonomy work.

## Edexcel iGCSE Chemistry focus slice (SyllabAI Cycle-1 alignment)

Committed under `resources/captures/resource-hub/`:

- `edexcel-igcse-chemistry-courses.json` — the 14-course "Chemistry:
  Edexcel iGCSE" family (incl. `Chemistry: Edexcel iGCSE`
  `967b4370-21e8-11e8-8c0c-d79041e9c8a6`, Free/Standard/Updated, 15
  top-level sections, 1,430 exam questions; and the Premium
  HyperLearning variant)
- `edexcel-igcse-chemistry-sections.json` — 872 section entities across
  the family
- `edexcel-igcse-chemistry-section-tree.json` — readable top/sub
  section tree of the main Free course
- `chemistry-resources-metadata.jsonl.gz` — **18,306 rows**, examQuestion titles nulled (they are question stems — see title rule in IP notes): every
  Chemistry resource's metadata (id, type, title, tag values,
  breadcrumbs, marks, publisher, answer counts)
- `all-subjects-sample-metadata.jsonl.gz` — first-page (≤200/type) sample
  for the other 69 subjects (18,890 rows) for coverage without a full
  scrape
- `tags-taxonomy-slim.json`, `subject-resource-counts.csv` — taxonomy
  + counts above

Categorisation principle (mirrors IP notes): **identifiers, titles,
structure, counts = metadata (committed); any field that teaches or
assesses (question bodies, mark schemes, section content, generation
scripts) = content (local-only, never committed)**.

## Full payloads (local-only)

`/home/z/my-project/work/seneca-recon/probe-results/rh3/
local-only-full-payloads/` holds the raw query-resources responses
(~250 files, incl. mark schemes / generation scripts) — same posture as
the JS bundle corpus: kept for analysis, excluded from git, re-fetchable
with the scripts in `scripts/` at the repo root of the experiment
(`resources/scripts/`).
