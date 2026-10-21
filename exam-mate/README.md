# exam-mate

Experiment workspace inside `syllabai-experimental`. All work — research,
scraped resources, and docs — lives in this folder.

## Layout

```
exam-mate/
  research/    # research notes, dossiers, findings, references
  resources/   # scraped resources — raw captures, extracted content, manifests
  docs/        # experiment docs — design notes, specs, decisions, runbooks
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
- This folder is **not of record** — scratch space is fine here, but the
  conventions above keep it re-joinable to the main SyllabAI line later.
