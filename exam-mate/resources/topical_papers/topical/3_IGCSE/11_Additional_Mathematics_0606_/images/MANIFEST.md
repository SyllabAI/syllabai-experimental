# MANIFEST — images/ (CIE IGCSE Additional Mathematics 0606, complete set)

Downloaded: 2026-10-22 (UTC) · Source: `https://www.exam-mate.com` TOPICAL PAST
PAPERS, subject `categoryID=3` (CIE IGCSE) / `subjectID=11` (Additional
Mathematics 0606) · Method: fixed-fingerprint headless Chromium, in-page
`fetch()` pipeline (WAF-immune; see `scripts/exam_mate_image_bulk.py` and
`docs/exam-mate-scrape-runbook.md`) · Rate: batches of 4 concurrent fetches,
1 s between batches, no auth, anonymous session.

## Contents

| Path | What |
|---|---|
| `INDEX.jsonl` | **Per-image metadata ledger — the provenance record.** One JSON object per unique image URL, sorted by qid. |
| `questions/{qfolder}/{src_qid}/{original_filename}.png` | 3,087 PNGs (1,579 question + 1,508 answer images), original site filenames preserved. Canonical layout **mirrors the source URL path**: `https://www.exam-mate.com/` + `<file>` reconstructs the exact source URL. |
| `by_paper.json` | Derived view: `paper_ref` (e.g. `0606/23_Winter_2019_Q10`) → qid, topics, MCQ answer, parsed fields, image file lists. Sorted newest-first. |
| `by_topic.json` | Derived view: individual topic → `{qid, paper_ref, file}` entries (site topic strings verbatim, incl. their typos). |
| `_summary.json` | Machine summary of the download + integrity run. |

## Coverage vs. harvest

- 3,088 unique image URLs referenced by the 1,333-question harvest
  (`questions.jsonl`) → **3,087 downloaded** (64.96 MB), **1 failed**:
  - `https://www.exam-mate.com/questions/168/887/168_a_887_11_2.png` —
    HTTP **404 on the origin** (dead link on the site's side; early-era
    qfolder `168`, answer image 2 of qid 887). Recorded in `INDEX.jsonl`
    with `status: 404`; not fabricated or substituted.

## INDEX.jsonl fields

`file` (path relative to `images/`), `url` (source), `kind`
(`question`|`answer`), `sha256`, `bytes`, `content_type`, `status`,
`width`/`height`/`format` (Pillow), `qid` (site list id, e.g. 60043),
`src_qid` (image-store id from the URL path, e.g. 61890 — the two id
spaces are both preserved), `qfolder`, `event_key`, `page`, `paper_ref`
(site's own reference string), `parsed` {syllabus, paper, season, year,
question} (parsed from `paper_ref`), `topics` (verbatim site string),
`mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.

## Integrity

- Every file's SHA-256 is recorded at download time in `INDEX.jsonl`.
- The 7 pilot samples from the earlier proof-of-pipeline run
  (`image_samples/`, since pruned) matched the canonical store **7/7 by
  SHA-256** — byte-identical, proving download determinism.
- Post-run spot-check: 25 random files re-hashed → 25/25 match.
- `INDEX.jsonl` was compacted once after the run (3,089 → 3,088 lines) to
  remove a single duplicate entry caused by a process interruption; files
  on disk were never affected.

## Copyright note

These PNGs reproduce Cambridge (CIE) exam questions via the third-party
site exam-mate.com. This experimental copy is for SyllabAI internal
research/provenance prototyping only — license review required before any
of this content ships in a product (same discipline as
`syllabai-pastpapers`: source attribution + SHA-256 chain, takedown-aware).
