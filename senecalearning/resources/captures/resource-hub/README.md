# Resource Hub catalogue — categorisation & metadata

**Captured**: 2026-10-22 (Phase 2 session 3) · authenticated teacher
session via `tutor-resources`/`tags`/`course` services. **Metadata
only** — every file here is structural/factual (ids, titles, counts,
tag values, section trees). Question bodies, mark schemes, lesson
content and generation scripts were observed live but are excluded from
the repo per `docs/IP-AND-COPYRIGHT-NOTES.md` (kept locally, see
research note).

## Contents

| File | What | Rows/size |
|---|---|---|
| `tags-taxonomy-slim.json` | Full tag taxonomy: 74 subjects, 21 age groups, 12 exam boards, price/pathway/tier dimensions — the filter system of the Hub | 132 tags |
| `subject-resource-counts.csv` | Exact resource counts per subject × type (courseSection / examQuestion / quiz) — 207,629 resources total across 74 subjects | 74 rows |
| `chemistry-resources-metadata.jsonl.gz` | **Every Chemistry resource**, metadata only | 18,306 rows, 0.9 MB gz |
| `all-subjects-sample-metadata.jsonl.gz` | First-page (≤200/type) metadata sample for the other 69 subjects — breadth without a full scrape | 18,890 rows, 1.0 MB gz |
| `edexcel-igcse-chemistry-courses.json` | The 14-course "Chemistry: Edexcel iGCSE" family records (tags, sectionIds, tier, TTS/vocab flags) | 14 courses |
| `edexcel-igcse-chemistry-sections.json` | Section entities for the whole family (sectionNumber, level, parentId, title) | 872 sections |
| `edexcel-igcse-chemistry-section-tree.json` | Readable top/sub section tree of the main **Free** course (`Chemistry: Edexcel iGCSE`, 15 top sections) | tree |

The two JSONLs are gzip-9'd (they are >10 MB plain and GitHub does not
render files that size anyway): `zcat chemistry-resources-metadata.jsonl.gz | head`.

## The title rule (examQuestion)

For `courseSection` and `quiz` rows, `title` is a structural name
(section/quiz name) and is kept. For `examQuestion` rows, `title`
equals the plain-text **question stem** — i.e. content — so it is
nulled (`"title": null`) in the committed files; ids, tag values,
breadcrumbs, marks and answer counts remain. The full stems exist only
in the local-only payloads. See `docs/IP-AND-COPYRIGHT-NOTES.md`
("title rule" addendum).

## Schema notes

- **JSONL rows** (metadata files): `id, type (courseSection|examQuestion|quiz),
  title, region, timeCreated, questionType, publisher, marksTotal,
  answerCount, difficulty, courseIds[], topicBreadcrumbs,
  tagValues {tagTypeIdId → [values]}`. `topicBreadcrumbs` carries the
  per-course placement (`Chemistry: AQA GCSE Foundation > Atomic
  Structure > Atoms & Elements > Relative Atomic Mass`), so course
  section trees can be reconstructed without the walled course API.
- **tagValues keys** are tag-type UUIDs; join with
  `tags-taxonomy-slim.json` (id → text/semanticCategory).
- **Sections**: `sectionLevel: "top"` = chapter; children hang off
  `parentId` of the top section id.

## Categorisation principle

identifiers · titles · structure · counts · tag values = **metadata
(committed)** · anything that teaches or assesses (question text, mark
schemes, section content, generation scripts) = **content (local-only,
never committed)**.

## Reproduce

`resources/scripts/` at the experiment root: `fetch-app-bundles.sh`
(bundle corpus), plus this session's downloaders
(`resourcehub-download.py`, `resourcehub-download2.py`,
`sections-download.py`) and the artefact builder
(`build-repo-artifacts.py`) — copied from the working scripts dir.
