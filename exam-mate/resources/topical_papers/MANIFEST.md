# MANIFEST — topical_papers dataset

Harvested: 2026-10-22 (UTC+8) · Source: `https://www.exam-mate.com/` TOPICAL
PAST PAPERS feature · Method: fixed-fingerprint headless Chromium + Livewire
DOM harvest (see `research/2026-10-22-exam-mate-topical-past-papers-reverse-engineering.md`
and `scripts/`).

## Contents

| Path | What | Rows |
|---|---|---|
| `catalog.json` | Full board/curriculum tree: 21 categories (CIE, Edexcel, OCR, AQA, IB MYP/Diploma, Turkish YKS, SPM) with every subject id+label | 21 categories, 180 subjects |
| `subject_taxonomy.json` | Per-subject filter metadata: topic list (the "topical" taxonomy), zones, papers (with Core/Extended and paper-code mappings), seasons, years, canonical deep-link URL | 180 entries |
| `topical/3_IGCSE/11_Additional_Mathematics_0606_/meta.json` | Subject 11 filter metadata snapshot at harvest time | — |
| `topical/3_IGCSE/11_Additional_Mathematics_0606_/questions.jsonl` | Every question of CIE IGCSE Additional Mathematics 0606 (the site's default subject), one JSON per line: `qid`, `eventKey`, `page`, `payload{question_images[], answer_images[], mcq_answer, topics, question_text, answer_text}` | **1,333 questions** (= the site's own total badge), 1,579 question-image URLs, 1,509 answer-image URLs, 1,333 MCQ answers, 28 distinct topic strings |
| `topical/3_IGCSE/11_Additional_Mathematics_0606_/images/` | **Complete image set + per-image metadata ledger** (`INDEX.jsonl`: sha256, bytes, dimensions, both site id spaces, paper_ref, topics, MCQ answer, download timestamp) + derived views `by_paper.json` / `by_topic.json` + `MANIFEST.md` | 3,087/3,088 PNGs (64.96 MB), 1 origin-404 recorded |

## Provenance & integrity notes

- Question totals cross-checked against the site's own count badge (1333/1333).
- Every record carries the raw payload parsed from the site's own
  `onclick=selectQuestion(...)` attribute — fields are reproduced verbatim
  (including the site's own typos, e.g. topic "Functions, Modolus").
- Image serving was **not** metered (unlike question-list serving): the
  2026-10-22 bulk run (operator-approved) fetched 3,087/3,088 unique PNGs
  through the in-page fetch pipeline at batch-4/1 s politeness, anonymous
  session. Details + integrity chain: `topical/3_IGCSE/
  11_Additional_Mathematics_0606_/images/MANIFEST.md`.
- Earlier pilot folders that contained stale-list contamination (questions of
  subject 11 mislabeled as subjects 13/247) were **deleted**; only the
  verified subject-11 dataset is kept.
- No authentication was used; everything here was served to an anonymous
  visitor session.

## Known gaps

- Questions for non-default subjects (all except CIE IGCSE Add Maths 0606):
  the anonymous list-serving path never re-queries after a subject switch
  (403 quota / server 500s / string-type seeding bug on deep links — full
  analysis in the research note). Extending per-subject coverage requires
  either a subscribed account in the crawler or periodic re-runs.
- One image URL is dead at the origin (HTTP 404:
  `questions/168/887/168_a_887_11_2.png`); everything else is on disk.

## Image pipeline proof (superseded by the full set)

The original 7-sample proof (`image_samples/`) matched the completed bulk
store **7/7 by SHA-256** and was pruned on 2026-10-22 — the canonical set in
`topical/3_IGCSE/11_Additional_Mathematics_0606_/images/` supersedes it.
