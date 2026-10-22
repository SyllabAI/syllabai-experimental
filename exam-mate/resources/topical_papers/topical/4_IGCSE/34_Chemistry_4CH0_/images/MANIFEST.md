# MANIFEST — images/ (Chemistry(4CH0), complete set)

Downloaded: 2026-10-22T07:24:53Z · Source: `https://www.exam-mate.com` TOPICAL PAST PAPERS, subject `categoryID=4` (IGCSE) / `subjectID=34` (Chemistry(4CH0)) · Method: fixed-fingerprint headless Chromium, in-page `fetch()` pipeline (WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of 4 concurrent fetches, 1 s between batches.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, original site filenames preserved. Local path after `images/` == URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs the source URL. |
| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ answer, parsed fields, image lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → entries (site topic strings verbatim). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 1662 unique image URLs referenced by 419 harvested questions (`questions.jsonl`) → **1662 downloaded** (136.99 MB).
- 893 question images, 769 answer images.
- Years covered (parsed from paper refs): 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019.
- Topics (27): Acids, Alkanes, Atomic Structure, Bonding, Calculations From Equations, Electrolysis, Electrolysis Calculations, Energy Calculations, Formulae And Equations, Introducing Energy Changes In Reactions, Introducing Organic Chemistry, Introducing Reversible Reactions, Kinetic Theory And Diffusion, Making Salts, Manufacturing Chemicals, Metals, Oxygen And Oxides, Polymers, Rams And Moles, Rates Of Reaction, Separating And Analysing, Structure, The Periodic Table, The Reactivity Series, Titration Calculations, Useful Products From Crude Oil, alkenes And Alcohols.
- Harvested at: 2026-10-22T01:49:51+0000.

## INDEX.jsonl fields

`file`, `url` (source), `kind` (question|answer), `sha256`, `bytes`, `content_type`, `status`, `width`/`height`/`format`, `qid` (site list id), `src_qid` (image-store id from the URL path — both id spaces preserved), `qfolder`, `event_key`, `page`, `paper_ref` (site's own reference string), `parsed` {syllabus, paper, season, year, question}, `topics` (verbatim), `mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 recorded at download time in `INDEX.jsonl`.
- Coverage cross-check: 1662/1662 unique URLs on disk.

## Copyright note

These PNGs reproduce exam-board copyrighted questions via the third-party site exam-mate.com. Experimental research copy only — license review required before any of this content ships (same discipline as `syllabai-pastpapers`).
