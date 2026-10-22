# MANIFEST — images/ (Physics(4PH0), complete set)

Downloaded: 2026-10-22T07:29:07Z · Source: `https://www.exam-mate.com` TOPICAL PAST PAPERS, subject `categoryID=4` (IGCSE) / `subjectID=44` (Physics(4PH0)) · Method: fixed-fingerprint headless Chromium, in-page `fetch()` pipeline (WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of 4 concurrent fetches, 1 s between batches.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, original site filenames preserved. Local path after `images/` == URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs the source URL. |
| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ answer, parsed fields, image lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → entries (site topic strings verbatim). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 1569 unique image URLs referenced by 451 harvested questions (`questions.jsonl`) → **1569 downloaded** (271.64 MB).
- 943 question images, 626 answer images.
- Years covered (parsed from paper refs): 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019.
- Topics (27): Application Of Radioactivity, Astronomy, Atoms And Radioactivity, Current And Voltage In Circuits, Density And Pressure, Electric Charge, Electric Motors And Electromagnetic Induction, Electrical Resistance, Energy Resources And Electricity Generation, Energy Transfers, Forces And Movement, Forces And Shape, Light Waves, Liquids And Gases, Magnetism And Electromagnetism, Mains Electricity, Momentum, Movement And Position, Particles, Properties Of Waves, Radiation And Half-life, Solids, Sound, The Turning Effect Of Forces, Thermal Energy, Using Waves, Work And Power.
- Harvested at: 2026-10-22T01:54:54+0000.

## INDEX.jsonl fields

`file`, `url` (source), `kind` (question|answer), `sha256`, `bytes`, `content_type`, `status`, `width`/`height`/`format`, `qid` (site list id), `src_qid` (image-store id from the URL path — both id spaces preserved), `qfolder`, `event_key`, `page`, `paper_ref` (site's own reference string), `parsed` {syllabus, paper, season, year, question}, `topics` (verbatim), `mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 recorded at download time in `INDEX.jsonl`.
- Coverage cross-check: 1569/1569 unique URLs on disk.

## Copyright note

These PNGs reproduce exam-board copyrighted questions via the third-party site exam-mate.com. Experimental research copy only — license review required before any of this content ships (same discipline as `syllabai-pastpapers`).
