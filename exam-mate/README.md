# exam-mate

Experiment workspace inside `syllabai-experimental`. All work — research,
scraped resources, and docs — lives in this folder.

> **Storage split (2026-10-22):** image downloads from that date onward go
> to the companion repo [`syllabai-experimental-2`](https://github.com/SyllabAI/syllabai-experimental-2)
> (same `exam-mate/` folder name/layout). Image sets completed here are
> frozen and immutable; questions remain source-of-record in this repo.
> See `docs/STORAGE-SPLIT.md` + `../sister_repo.json`. The local checkout
> of this repo is sparse — its `images/` trees exist on GitHub only.

## Current work: reverse-engineering exam-mate.com's TOPICAL PAST PAPERS

Completed 2026-10-22. Highlights:

- **WAF fully decoded** — the "One moment, please..." splash runs 7 fingerprint
  checks; a fixed-fingerprint Chromium passes all of them and the challenge
  self-solves. Clearing cookie: `wssplashchk`.
- **Feature architecture mapped** — Laravel + Livewire v2 (`"v":"acj"`),
  5 components on the topical page, full state model for
  `filter-box.topical-filter-box` / `list.questions-list` /
  `viewer.question-viewer`, the `filter()` apply button, the
  `gotoPage/nextPage` pagination and the `selectQuestion(...)` payload
  embedded in every question card (images + MCQ answers + topics).
- **Deep-link URL scheme** — `/topicalpastpapers/{Category}-{catID}/{Subject}-{subjID}`
  (labels cosmetic, ids authoritative; has a server-side string-seeding bug
  that empties the list).
- **Full structural harvest** — 21 boards (CIE, Edexcel, OCR, AQA, IB, Turkish
  YKS, SPM), 180 subjects, every subject's topic taxonomy / zones / papers /
  seasons / years → `resources/topical_papers/subject_taxonomy.json`.
- **Full question harvest of the default subject** — CIE IGCSE Additional
  Mathematics 0606: **1,333/1,333 questions** with 1,579 question-image URLs,
  1,509 answer-image URLs, 1,333 MCQ answers → `resources/topical_papers/`.
- **Complete image set downloaded (2026-10-22)** — 3,087/3,088 unique PNGs
  (64.96 MB; the one miss is a dead link on the site's side) via the
  resumable bulk downloader `scripts/exam_mate_image_bulk.py`, with a
  per-image SHA-256 + metadata ledger (`INDEX.jsonl`) and derived
  by-paper / by-topic views →
  `resources/topical_papers/topical/3_IGCSE/11_Additional_Mathematics_0606_/images/`.
- **Logged-in session unlocks non-default subjects (2026-10-22)** — with any
  authenticated account (even "not subscribed"), the apply-button and
  deep-link paths serve other subjects' lists (the anonymous blocker is
  session-specific; subscription only gates exports/MCQ products). First
  logged-in harvest: **Edexcel IGCSE Chemistry 9-1 (4CH1)** — the SyllabAI
  Cycle 1 subject — 40/40 questions + 150/150 images with full ledger →
  `resources/topical_papers/topical/21_IGCSE_9-1_/614_Chemistry_9-1_4CH1_/`.
  Probed counts: 4CH0 = 419, CIE 0620 = 6,398 (not yet harvested).
- **Gating model documented** — question-list serving is metered per session
  (403 "request limit or no active subscription"); the crawler detects it and
  stops cleanly.

Start here: `research/2026-10-22-exam-mate-topical-past-papers-reverse-engineering.md`,
then `docs/exam-mate-scrape-runbook.md` to operate the tooling in `scripts/`.

## Layout

```
exam-mate/
  research/    # research notes, dossiers, findings, references
  resources/   # scraped resources — raw captures, extracted content, manifests
    topical_papers/   # the exam-mate.com dataset (see its MANIFEST.md)
  docs/        # experiment docs — design notes, specs, decisions, runbooks
  scripts/     # harvest tooling (client, crawler, taxonomy, challenge solver)
```

## Conventions

- **Provenance first**: every scraped resource records its source URL,
  capture date, and (where relevant) the tool/method used to capture it.
  Prefer a small `manifest.md` (or `.yaml`) next to the captures over
  metadata living only in someone's head.
- **Research notes are dated**: name files `YYYY-MM-DD-topic.md` so the
  folder sorts into a chronological trail.
- **Docs record decisions**: if the experiment concludes something
  ("we will do X because Y"), write it down in `docs/` — one file per
  decision or topic, no merge-quarterly mega-docs.
- **Raw captures are immutable**: once scraped into `resources/`, treat a
  file as read-only; corrections go in a new file that supersedes the old
  one, with a note pointing from old to new.
- **Stale data is deleted, not kept**: pilot folders that contained
  contaminated records (mislabeled questions) are removed outright —
  a smaller correct dataset beats a bigger wrong one.
- This folder is **not of record** — scratch space is fine here, but the
  conventions above keep it re-joinable to the main SyllabAI line later.
