# syllabai-experimental

Experimental SyllabAI workspace. Sandboxed experiments live here, one folder
per experiment — separate from the of-record repositories
(`syllabai`, `syllabai-v2`, `syllabai-resources`, …).

> **Companion repo:** [`SyllabAI/syllabai-experimental-2`](https://github.com/SyllabAI/syllabai-experimental-2)
> holds **all exam-mate image downloads from 2026-10-22 onward** (this repo
> paused at its disk ceiling; see `sister_repo.json` at this repo's root and
> `exam-mate/docs/STORAGE-SPLIT.md`). Questions stay source-of-record here.

## Experiments

| Folder | What it is | Status |
|---|---|---|
| [`exam-mate/`](./exam-mate/) | Exam-mate experiment — research, scraped resources, docs | active — questions 100% (88,323), images ~30% (rest → **syllabai-experimental-2**) |
| [`undergroundmathematics/`](./undergroundmathematics/) | Reverse engineering of undergroundmathematics.org (Cambridge A level maths resource site) — IA, content model, API, pipeline research + metadata captures | active |
| [`senecalearning/`](./senecalearning/) | Reverse engineering of Seneca Learning (app.senecalearning.com) — GoStudent-owned freemium revision platform: service map, auth model, API surface, pedagogy model, assignment CRUD contract, Resource Hub metadata catalogue (207k resources, 74 subjects), Magic Quiz AI generator, session-ws protocol, memory/XP models | phase 2 sessions 1–4 done (session 4: Magic Quiz AI generator contract, session-ws protocol, memory/spaced-repetition schema) |
| [`znotes/`](./znotes/) | Reverse engineering of ZNotes (znotes.org) — freemium revision platform: tech stack, API surface, and the educator "My Teaching Toolkit" (4 AI resource generators) reconstructed statically and **verified live** end-to-end in the teacher account | phases 1+2 complete |

## Ground rules

- Nothing in this repo is of record. No contracts, receipts, or census laws
  apply here unless an experiment explicitly imports them.
- Work happens inside the experiment folders; do not scatter files at the root.
- Anything an experiment produces that the platform wants to adopt graduates
  through a proper PR against the receiving of-record repository.
