# RESUME — exam-mate full-archive harvest & image download

> ⚠️ **SUPERSEDED (2026-10-22): the image phase no longer downloads into
> this repo.** All image downloads from 2026-10-22 onward go to the
> companion repo **[`syllabai-experimental-2`](https://github.com/SyllabAI/syllabai-experimental-2)**
> (split storage at the disk ceiling — see `STORAGE-SPLIT.md` in either
> repo + `sister_repo.json`). The commands below are kept for history;
> **running them again would re-download into the wrong repo.** The
> current image-phase runbook lives in
> `syllabai-experimental-2/exam-mate/docs/STORAGE-SPLIT.md`, and its
> driver is `syllabai-experimental-2/exam-mate/scripts/exam_mate_images_all.py`
> (reads questions from this repo, writes images there).
>
> Question harvest remains 100% complete and source-of-record in this repo.

Status snapshot 2026-10-22 (see `progress.json` + driver state files for live
numbers): **question harvest 100% complete** (132 subjects with data = 88,323
questions; 48 subjects site-empty with facet evidence). **Image download
~30% complete** (~60k images, ~4.4 GB committed) — paused at the 9.9 GB
sandbox disk ceiling, NOT at any site limit.

## Environment facts

- Sandbox disk is 9.9 GB. Images cost ~2× (working tree + git objects), so
  the ceiling here is ~4.5 GB of images. A bigger disk (or downloading
  straight to R2) removes the constraint entirely.
- Credentials + session state live OUTSIDE the repo in
  `/home/z/my-project/exam-mate-probe/` (`creds.json`, `client_state.json`,
  `auth_state.json`, `shards/`). Never commit them.
- Background processes do not survive tool-call boundaries — always run
  workers in the foreground under `timeout -k 5 <s>` and resume.

## Resuming the image download (one command per chunk)

```bash
timeout -k 5 520 bash -c 'python3 /home/z/my-project/scripts/exam_mate_images_all.py --cats 4,21,3 --state-file /home/z/my-project/exam-mate-probe/imgstate_A.json --batch 6 --delay 0.7 > /home/z/my-project/exam-mate-probe/img_A.log 2>&1 & python3 /home/z/my-project/scripts/exam_mate_images_all.py --cats 5,6,14,15,16,17,18,19,7,13,53,54,55 --state-file /home/z/my-project/exam-mate-probe/imgstate_B.json --batch 6 --delay 0.7 > /home/z/my-project/exam-mate-probe/img_B.log 2>&1 & wait'
```

- Per-subject resume is automatic (`INDEX.jsonl` + file-size checks).
- Transient failures self-heal: PARTIAL subjects are retried on the next
  pass; per-shard/per-subject validation gates everything.
- Commit + push after each chunk (`git add exam-mate/ && git commit && git push`).
- **Mind the disk**: ~1 GB free at last pause. Before continuing on a small
  disk, commit+push finished subjects and `git gc`; on a fresh machine just
  clone and run the driver.

## Remaining work (driver state)

- Workers A (cats 4/21/3) and B (5/6/14-19/7/13/53-55) process subjects
  biggest-first; `--status` prints per-worker progress.
- In-flight at pause: 3:30 Sociology 0495 (~570 MB, was ~80% done), 7:92 IB
  Physics (~430 MB, ~60% done) — their partial image dirs were pruned to fit
  the disk and will re-download cleanly.
- Everything else: ~100k image URLs outstanding, no other blockers.

## If extending question coverage instead

`python3 /home/z/my-project/scripts/exam_mate_harvest_all.py` — no-op unless
the site adds subjects (all 180 catalog subjects are already resolved);
re-run `exam_mate_taxonomy.py` first if the site's catalogue grows.
