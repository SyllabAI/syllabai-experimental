# MANIFEST — images/ (Mathematics International(0607), complete set)

Downloaded: 2026-10-22T06:50:54Z · Source: `https://www.exam-mate.com` TOPICAL PAST PAPERS, subject `categoryID=3` (IGCSE) / `subjectID=136` (Mathematics International(0607)) · Method: fixed-fingerprint headless Chromium, in-page `fetch()` pipeline (WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of 4 concurrent fetches, 1 s between batches.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, original site filenames preserved. Local path after `images/` == URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs the source URL. |
| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ answer, parsed fields, image lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → entries (site topic strings verbatim). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 4224 unique image URLs referenced by 1906 harvested questions (`questions.jsonl`) → **4224 downloaded** (112.56 MB).
- 2189 question images, 2035 answer images.
- Years covered (parsed from paper refs): 2015, 2016, 2017, 2018, 2019.
- Topics (11): Algebra, Coordinate Geometry, Functions, Geometry, Mensuration, Number, Probability, Sets, Statistics, Trigonometry, Vectors And Transformations.
- Harvested at: 2026-10-22T02:09:36+0000.

## INDEX.jsonl fields

`file`, `url` (source), `kind` (question|answer), `sha256`, `bytes`, `content_type`, `status`, `width`/`height`/`format`, `qid` (site list id), `src_qid` (image-store id from the URL path — both id spaces preserved), `qfolder`, `event_key`, `page`, `paper_ref` (site's own reference string), `parsed` {syllabus, paper, season, year, question}, `topics` (verbatim), `mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 recorded at download time in `INDEX.jsonl`.
- Coverage cross-check: 4224/4224 unique URLs on disk.

## Copyright note

These PNGs reproduce exam-board copyrighted questions via the third-party site exam-mate.com. Experimental research copy only — license review required before any of this content ships (same discipline as `syllabai-pastpapers`).
