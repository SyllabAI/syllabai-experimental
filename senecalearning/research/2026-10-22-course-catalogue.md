# Course catalogue — 2,761 courses, tiers, regions, product lines

**Captured**: 2026-10-22 · source: `GET course-cdn-v2…/api/courses?limit=3000&maxVisibility=HIDDEN`
(anonymous + correlationId). Full 3.9 MB dump kept local
(`~/work/seneca-recon/probe-results/courses_full.json`); slim taxonomy
committed at `resources/captures/courses-taxonomy.jsonl` (2,761 rows:
courseId, name, tier, visibility, regions, sectionsCount,
examQuestionsCount, TTS flag).

## Headline numbers

| Metric | Value |
|---|---|
| Total courses (incl. hidden) | **2,761** |
| Visibility PUBLIC / HIDDEN | 2,185 / 576 |
| subscriptionTier FREE / PREMIUM | 1,789 / 971 |
| Regions | GB 1,696 · BR 218 · DE 204 · IT 125 · US 116 · AT 115 · ES 115 · FR 100 (+ more) |
| Sections per course | e.g. free Edexcel iGCSE Science(Double) Chem: **152 sections, 15 exam questions** |
| TTS flag | per-course `textToSpeechEnabled` |
| Authors field | publisher partners (e.g. "SOMOS Educação" for BR) |

## Product lines (from course names — the SKU taxonomy)

HyperLearning (main course) · HyperFlashcards · The Night Before (pre-exam
cram) · Predicted Papers · Half-Term HyperCram · Hardest Questions ·
Diagnostic Misconceptions · 7-9 Exclusive / 4-5 Booster (grade-band
variants) · Standardised Assessments · Paper 1 / Paper 2 splits ·
Super/SloModel regional variants. **One curriculum → many paid SKU
courses** — the freemium monetisation is content-packaging, not feature
walling alone.

## Qualification spine

All UK lanes present: GCSE (AQA/Edexcel/OCR A/B/Gateway, Foundation &
Higher), iGCSE (Edexcel), International A Level, A Level, KS2–KS3, IB,
plus US (SAT Subject Test, TEKS, High School), BR (ENEM-era partners),
DE/AT (Studienkreis), IT, ES, FR. **For SyllabAI**: the iGCSE Chemistry
lane maps directly onto our 4CH1 spine —
`Chemistry: Edexcel iGCSE` (free, 152 sections) is the reference course
for cross-mapping (courseId committed in the taxonomy JSONL).

## Course content model (list-level)

```json
{ "courseId": uuid, "name", "description", "headerImageURL":
  "seneca-image-cdn:///…", "sectionIds": [uuid…], "sectionsCount",
  "startingSectionId", "examQuestionsCount",
  "hardestQuestionsSectionsCount", "averageScorePercentiles",
  "subscriptionTier": "FREE|PREMIUM", "visibility": "PUBLIC|HIDDEN",
  "regions": ["GB"], "tags": {tagDefId: [{id}…}], "authors": [],
  "references": [], "textToSpeechEnabled": bool, "darkText": bool }
```

`seneca-image-cdn:///` is a custom URL scheme resolved against their image
CDNs. `averageScorePercentiles` implies cross-cohort score analytics
baked into the catalogue (they can rank course difficulty nationally).

## Query + delivery architecture

- **Catalogue list**: public CDN endpoint (S3/CloudFront, correlationId
  only) — cheap anonymous reads.
- **Catalogue query**: `POST course.app…/api/courses/queryCourses` —
  **Elasticsearch** (`_index: course-entities-v2`, `_score`, `total`).
- **Course payloads (sections/slides/questions)**: CloudFront **signed
  URLs** (`Key-Pair-Id` required; direct CDN path 403 `MissingKey`) —
  content delivery is signature-gated, so course bodies are not reachable
  even with an account token via plain API calls; the SPA resolves signed
  links through a flow we have not yet captured (open item).

## Tag system

Course `tags` reference tag-definition ids (resolved via
`tags.app…/api/tags?includeNonCourseFilters=true`) — the assignment
course-picker filters by subject → age group → exam board → course using
this tag tree (verified live: "Pick your subject" funnel with per-subject
resource counts, e.g. Chemistry 14,753 resources).
