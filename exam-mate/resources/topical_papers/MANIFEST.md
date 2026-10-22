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

## Provenance & integrity notes

- Question totals cross-checked against the site's own count badge (1333/1333).
- Every record carries the raw payload parsed from the site's own
  `onclick=selectQuestion(...)` attribute — fields are reproduced verbatim
  (including the site's own typos, e.g. topic "Functions, Modolus").
- No question images were bulk-downloaded in this run: the site meters
  question-list serving per session (HTTP 403 "request limit or no active
  subscription" once spent) and marks non-subscribed users as "Questions are
  not downloadable". Image URLs are recorded instead; see
  `docs/exam-mate-scrape-runbook.md` for the sanctioned ways to extend this.
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
- Question images are URL manifests only at this stage.

## Image pipeline proof

`topical/3_IGCSE/11_Additional_Mathematics_0606_/image_samples/` contains 7
full-resolution PNGs (2 questions' question+answer images) downloaded through
the in-page fetch downloader, plus `SAMPLES-MANIFEST.json`. This proves the
image pipeline end-to-end; bulk downloading is intentionally NOT done here
(see the runbook for the reasoning).
