# Resource Hub — FULL CONTENT corpus (v2, operator-approved)

**Captured**: 2026-10-23 (session 11) · authenticated teacher session via
`tutor-resources` `/api/v2/query-resources` · **full teaching content
included** per the operator's 2026-10-23 approval (see
`docs/IP-AND-COPYRIGHT-NOTES.md`, "Content storage approval" addendum,
which supersedes the earlier local-only rule and the examQuestion title
rule **for this directory only**).

## What is here

| Path | What |
|---|---|
| `by-subject/<Subject>.jsonl.gz` | one gzip JSONL per subject (70 files, 93 MB total) — **full content** rows |
| `by-subject/catalog.csv` | subject → rows / per-type counts / bytes / sha256 |
| `courses/edexcel-igcse-chemistry/<Course>.json` | per-course layer: section entities + resources for the 14-course Edexcel iGCSE Chemistry family |
| `courses/edexcel-igcse-chemistry/family-index.json` | family overview (sections / examQuestions per course) |
| `../../scripts/seneca_build_content_corpus.py` | rebuild script (reads the local page cache) |
| `../../scripts/seneca_resourcehub_full_harvest.py` | resumable harvest engine (≤1 req/s, ageGroup sharding) |

**Totals**: 207,006 resources across 70 subjects
(courseSection + examQuestion + quiz). This is a FRESH snapshot taken
2026-10-23; it differs from the 2026-10-22 metadata-only catalog
(206,982) by +24 rows of live-index drift, all additive.

## Row schema (per type)

Common: `id, type, title, region, timeCreated, publisher,
tags {tagTypeId → [{id, value}]}`.

- **courseSection** — `content.topicNotes` (lesson body),
  `content.description` (breadcrumb "course > top > sub"),
  `content.imageUrl / previewUrl / contentUrl`
- **examQuestion** — `content.questionTitleMd` (stem, markdown; `$var`
  templates instantiated at runtime via `content.generationScript`),
  `content.markScheme`, `content.generationScript`,
  `content.topicBreadcrumbs[]`, `questionType`, `marksTotal`,
  `answerCount`, `courseIds[]`
- **quiz** — `content.quizSummary` (markdown), `access`, `isPublic`,
  `saveCount`

## PII policy

Teacher-made quizzes carry third-party identifiers. The builder
**strips `creatorName`, `creatorId`, `schoolId`, `schoolGroupId` from
every quiz row** before writing (verified: 0 leaks in the committed
corpus). Seneca-authored content is otherwise verbatim.

## Reproduce

```bash
# 1) harvest (resumable, ≤1 req/s; token at /tmp/seneca_token.txt)
python3 senecalearning/resources/scripts/seneca_resourcehub_full_harvest.py --budget 3600
# 2) build the corpus
python3 scripts/seneca_build_content_corpus.py   # (project scripts dir copy)
```

The metadata-only predecessor (`../resource-hub/`) is retained as the
2026-10-22 snapshot for provenance.
