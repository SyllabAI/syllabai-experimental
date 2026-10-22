# STORAGE SPLIT — summary for the sister repo's side

**Full decision record (canonical):**
[`syllabai-experimental-2/exam-mate/docs/STORAGE-SPLIT.md`](https://github.com/SyllabAI/syllabai-experimental-2/blob/main/exam-mate/docs/STORAGE-SPLIT.md)

## TL;DR (2026-10-22)

- A companion repo **[`SyllabAI/syllabai-experimental-2`](https://github.com/SyllabAI/syllabai-experimental-2)**
  was created holding **all exam-mate image downloads from 2026-10-22
  onward**, under `exam-mate/resources/topical_papers/topical/...` — same
  folder name and layout as this repo's workspace folder.
- **This repo is frozen for images**: its 18 image subject dirs (~4.4 GB)
  stay here, immutable, never moved. The image download phase paused here
  at the sandbox disk ceiling (~30% done).
- Questions remain **source-of-record in this repo** (questions.jsonl +
  meta.json for 132 subjects, catalog, taxonomy). The image-phase driver
  in repo 2 reads questions from this repo and writes images into repo 2.
- This repo's local checkout is **sparse-checked out**: the big
  `images/` trees are NOT materialized on disk (they live on GitHub —
  re-materialize with `git sparse-checkout disable` if ever needed).
- Machine-readable pointer: `sister_repo.json` at this repo's root
  (mirrored in repo 2). **Never re-run image downloads against this repo**;
  use repo 2's `exam-mate/scripts/exam_mate_images_all.py`.
