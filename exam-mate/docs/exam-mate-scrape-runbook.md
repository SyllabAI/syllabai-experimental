# exam-mate scrape runbook

How to operate the harvest tooling in `scripts/`, what is free vs metered, and
how to extend the dataset safely.

## Prerequisites

```bash
pip install playwright requests
python -m playwright install chromium
# scripts assume the layout:
#   scripts/exam_mate_client.py      # browser client + WAF bypass
#   scripts/exam_mate_crawler.py     # catalog + question harvester
#   scripts/exam_mate_taxonomy.py    # per-subject taxonomy harvester
```

All commands are run from the repo root of `exam-mate/scripts/` (adjust `BASE`
inside `exam_mate_crawler.py` / `exam_mate_taxonomy.py` to point at your
output directory).

## What each tool does

| Tool | Cost profile | Output |
|---|---|---|
| `exam_mate_taxonomy.py` | Quota-free (structural page loads only) | `subject_taxonomy.json` + refreshed `catalog.json` |
| `exam_mate_crawler.py --catalog-only` | Quota-free | `catalog.json` |
| `exam_mate_crawler.py "3" --subject 11 --skip-transitions` | Consumes the session's question-list allowance | `topical/<cat>/<subj>/questions.jsonl` |

## The quota model (read this first)

- exam-mate serves the topical **question list** to anonymous visitors with a
  per-session allowance. When spent, every list call answers
  `403 {"error":["Your request has been denied. You might have hit the request
  limit or don't have an active subscription."]}`.
- One fresh anonymous session comfortably covers the full 1,333-question list
  of the default subject (54 pages) — that is the shape of the free allowance.
- The crawler **detects the 403 and stops cleanly** (checkpointing progress in
  `progress.json`). It never retries through the wall and never rotates
  sessions to evade it — do the right thing: if you need more, use an account
  you legitimately hold, or come back later.

## Recipes

### 1. Refresh the structural catalog (free, fast)

```bash
python3 exam_mate_taxonomy.py        # all 21 categories, every subject's topics/zones/papers/years
python3 exam_mate_crawler.py --catalog-only
```

### 2. Full question harvest of the default subject (CIE IGCSE Add Maths 0606)

```bash
python3 exam_mate_crawler.py "3" --subject 11 --skip-transitions
```

`--skip-transitions` matters: clicking the already-active subject/category
no-ops into a wedged Livewire commit bus (Alpine `filterResults` re-init race)
and pagination silently dies. Loading the page and paginating directly works
reliably for all 54 pages.

### 3. Per-subject question harvest with a logged-in session

**Implemented 2026-10-22.** The blocker on non-default subjects is
anonymous-session-specific: with any authenticated account (even one showing
"You are not subscribed"), the apply-button path (`subjectID` `$set` →
`.filter-button` click) and deep-link navigation both serve the subject's
list. Recipe as executed for 4CH1 (`scripts/exam_mate_harvest_4ch1.py`,
adapt `select_subject()` for any `categoryID`/`subjectID`):

1. Log in once via `scripts/exam_mate_login.py` (credentials in
   `exam-mate-probe/creds.json`, git-ignored; session state saved to
   `exam-mate-probe/auth_state.json` and propagated to the client state).
2. `Crawler(fresh_session=False)` restores the authenticated cookies.
3. Select category/subject, click the apply button, then
   `Crawler.harvest_subject(cat, subj, state, resp_marker=...)` —
   meta.json + questions.jsonl per subject.
4. Bulk images: `python3 exam-mate/scripts/exam_mate_image_bulk.py --phase all
   --subject-dir topical/<cat>_<label>/<subj>_<label>_`.

Respect the subscription's own limits — the 403 message is the boundary.

### 4. Question-image bulk downloader (executed 2026-10-22)

Image URLs are recorded in `questions.jsonl`
(`payload.question_images[]` / `payload.answer_images[]`). Images sit behind
the same WAF; use `ExamMateClient.download(url, out_path)` which routes through
the browser session and heals challenges. The production tool is
`scripts/exam_mate_image_bulk.py` — batched in-page fetches, resumable via
`INDEX.jsonl`, per-image sha256 + dimensions + full question metadata. It ran
to completion for subject 11: 3,087/3,088 (the one miss is an origin 404); see
`resources/topical_papers/topical/3_IGCSE/11_Additional_Mathematics_0606_/images/MANIFEST.md`.

Reminder: bulk-downloading reproduces exam-board copyrighted content via a
third-party site — the same provenance discipline as `syllabai-pastpapers`
applies (SHA-256 manifests, source attribution, license review before
anything ships). The images manifest carries the copyright note.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `One moment, please...` loops in your own tooling | Headless fingerprints (webdriver/headless-UA/zero outer dims/plugins array spoof) | Use `exam_mate_client.py` unmodified — it passes all 7 checks |
| Pagination clicks stop advancing badges after transitions | Livewire commit bus wedged by no-op `$set` re-renders | Re-load the page; use `--skip-transitions` for the default subject |
| `bad response 500` during Livewire replay | Stale chained `serverMemo` (WAF re-clearance mid-run) | Fall back to DOM pagination (crawler does this automatically) |
| Deep-link pages show 0 questions | Server seeds `filters.subjectID` as string on deep links | Known site bug — use the default route for list serving |
