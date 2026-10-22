# MANIFEST — images/ (Mathematics(0580), complete set)

Downloaded: 2026-10-22T06:25:25Z · Source: `https://www.exam-mate.com` TOPICAL PAST PAPERS, subject `categoryID=3` (IGCSE) / `subjectID=22` (Mathematics(0580)) · Method: fixed-fingerprint headless Chromium, in-page `fetch()` pipeline (WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of 4 concurrent fetches, 1 s between batches.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, original site filenames preserved. Local path after `images/` == URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs the source URL. |
| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ answer, parsed fields, image lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → entries (site topic strings verbatim). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 8859 unique image URLs referenced by 3958 harvested questions (`questions.jsonl`) → **8859 downloaded** (179.50 MB).
- 4703 question images, 4156 answer images.
- Years covered (parsed from paper refs): 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019.
- Topics (50): Angles, Approximation And Estimation, Areas &amp; Volumes Of Similar Shapes, Brackets And Symplifying, Changing The Subject, Circle Theorem, Congruence, Constructions And Loci, Decimals, Distance-time Graphs, Factorising, Foreign Exchange, Formulaee, Functions, Graphical Solution Of Equations, Indices, Linear Equaetion, Linear Programming, Lines, Map Scales, Matrices, Mensuration, Net, Number Facts, Parallel Lines, Percentages, Plotting Curves, Polygons, Probability, Pythagoras Theorem, Quadratic Equations, Ratio And Proportion, Rational And Irrational Numbers, Sequences, Sets, Similarity, Simple And Compound Interest, Simultaneous Equations, Solving Inequalities, Speed, Speed-time Graphs, Standard Form, Statistics, Symmetry, Transformatoin, Trigonometry, Upper And Lower Bound, Variation, Vectors, distance And Time.
- Harvested at: 2026-10-22T03:03:13+0000.

## INDEX.jsonl fields

`file`, `url` (source), `kind` (question|answer), `sha256`, `bytes`, `content_type`, `status`, `width`/`height`/`format`, `qid` (site list id), `src_qid` (image-store id from the URL path — both id spaces preserved), `qfolder`, `event_key`, `page`, `paper_ref` (site's own reference string), `parsed` {syllabus, paper, season, year, question}, `topics` (verbatim), `mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 recorded at download time in `INDEX.jsonl`.
- Coverage cross-check: 8859/8859 unique URLs on disk.

## Copyright note

These PNGs reproduce exam-board copyrighted questions via the third-party site exam-mate.com. Experimental research copy only — license review required before any of this content ships (same discipline as `syllabai-pastpapers`).
