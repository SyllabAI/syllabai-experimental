# undergroundmathematics

Experiment workspace inside `syllabai-experimental`. Target of study:
[undergroundmathematics.org](https://undergroundmathematics.org/) — free
web-based resources for teaching post-16 (A level) mathematics, built at the
University of Cambridge (2012–, originally the Cambridge Mathematics Education
Project, now hosted by Cambridge Mathematics).

Goal: **reverse engineer the site** — its information architecture, content
model, pedagogy layer, authoring/rendering pipeline and public API — to inform
SyllabAI's content platform design (stations/lines vs CIE/Edexcel spines,
review-question corpus model, teacher-support layer, resource taxonomies).

## Layout

```
undergroundmathematics/
  research/    # dated research notes — site analysis, architecture, API findings
  resources/   # scraped metadata captures (public API JSON) + manifest
  docs/        # working docs — plan, IP/copyright policy
```

## Conventions

Inherited from the repo ground rules plus [`exam-mate/`](../exam-mate/README.md):

- **Provenance first**: every capture in `resources/` is documented in
  [`resources/manifest.md`](./resources/manifest.md) with source URL, capture
  date and method. Captured API payloads are metadata-only (see IP notes).
- **Research notes are dated**: `YYYY-MM-DD-topic.md`, chronological trail.
- **Docs record decisions**: plan, phase status, and the IP/copyright policy
  live in `docs/`.
- **Nothing here is of record** — scratch space; graduations to the platform
  go through proper PRs against the receiving repo.

## Key findings (TL;DR)

- **Scale**: 855 public resources across 29 "stations" (24 live, 4 under
  construction); 569 of them (66%) are **review questions** digitised from
  historical UCLES/Cambridge exam papers going back to the 1960s; 113 station
  key questions; 6 pervasive ideas; 5 lines; 14 resource types.
- **Information architecture**: a London-tube-map metaphor — stations
  (topics) joined by coloured lines (Number, Algebra, Geometry, Functions,
  Calculus), with cross-cutting "pervasive ideas". Not tied to any syllabus.
- **Content model**: every resource = markdown + embedded LaTeX source in
  MySQL, sections like Problem → Suggestion → Solution, with teacher notes,
  key questions, interactivity labels (GeoGebra), related resources, and
  printable PDF generated via Pandoc → LaTeX.
- **Tech stack**: AngularJS 1.4 SPA with server-side pre-rendering, MySQL +
  a public REST API (`/api/*`, 215 endpoints in the client bundle), MathJax
  2.7, Pandoc-based print pipeline, ServiceWorker offline cache.
- **The site self-documents its pipeline** on `/about/website` — including a
  retrospective regret about Markdown-with-significant-whitespace.

## Status

- 2026-10-22: **Phase 1** — site identification, taxonomy + inventory capture
  (metadata), content model and technical architecture analysis.
- 2026-10-22: **Phase 2** — polite full-content crawl (2,486 pages, 0
  failures) + section extraction: 855 resources / 2,181 section bodies
  committed under `resources/content/` per operator decision (see
  `docs/IP-AND-COPYRIGHT-NOTES.md`). Discovery notes in
  `research/2026-10-22-phase2-crawl-and-extraction.md`.
- 2026-10-22: **Integration plan** — rights ladder (modes 0–4), eight
  integration surfaces, phased P3a–P6: `docs/INTEGRATION-PLAN.md`.
- 2026-10-22: **Phase 3a (corpus cleanup)** — qwell dedup into a shared
  `questionWell` field (2,204 duplicates stripped, 584 section-unique
  preserved) → `resources/ugm-clean/`; all 623 acknowledgements parsed into
  structured provenance tuples →
  `resources/derived/review-question-provenance.json`.
- 2026-10-22: **Phase 3c (spine cross-map pilot)** — UGM quadratics ↔
  CIE 9709 Pure 1 Quadratics (1.1.1–1.1.5): 56/59 resources aligned (95%),
  mode-2 deep-link shortlists per spec point, S1 provenance-bridge status;
  `docs/cross-map-quadratics.md` + machine-readable twin. Ready for
  operator review; generalisation to all lanes proposed (doc §8).
- Next: **P3b** (relation-graph export + per-station enrichment sheets),
  then **P4** (ADR: UGM integration mode) — see `docs/INTEGRATION-PLAN.md`.
