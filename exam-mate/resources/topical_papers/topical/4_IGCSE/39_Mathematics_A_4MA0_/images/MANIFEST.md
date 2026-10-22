# MANIFEST — images/ (Mathematics A(4MA0), complete set)

Downloaded: 2026-10-22T06:38:02Z · Source: `https://www.exam-mate.com` TOPICAL PAST PAPERS, subject `categoryID=4` (IGCSE) / `subjectID=39` (Mathematics A(4MA0)) · Method: fixed-fingerprint headless Chromium, in-page `fetch()` pipeline (WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of 4 concurrent fetches, 1 s between batches.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, original site filenames preserved. Local path after `images/` == URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs the source URL. |
| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ answer, parsed fields, image lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → entries (site topic strings verbatim). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 5092 unique image URLs referenced by 2450 harvested questions (`questions.jsonl`) → **5092 downloaded** (256.34 MB).
- 2585 question images, 2507 answer images.
- Years covered (parsed from paper refs): 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019.
- Topics (12): Algebra, Differentiation &amp; Kinematics, Functions &amp; Graphs, Geometry, Mensuration, Number, Probability, Sets, Statistics, Transformation, Trigonometry, Vectors.
- Harvested at: 2026-10-22T01:51:27+0000.

## INDEX.jsonl fields

`file`, `url` (source), `kind` (question|answer), `sha256`, `bytes`, `content_type`, `status`, `width`/`height`/`format`, `qid` (site list id), `src_qid` (image-store id from the URL path — both id spaces preserved), `qfolder`, `event_key`, `page`, `paper_ref` (site's own reference string), `parsed` {syllabus, paper, season, year, question}, `topics` (verbatim), `mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 recorded at download time in `INDEX.jsonl`.
- Coverage cross-check: 5092/5092 unique URLs on disk.

## Copyright note

These PNGs reproduce exam-board copyrighted questions via the third-party site exam-mate.com. Experimental research copy only — license review required before any of this content ships (same discipline as `syllabai-pastpapers`).
