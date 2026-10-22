# Reverse-engineering plan — undergroundmathematics.org

**Status legend**: [x] done · [~] in progress · [ ] open

## Objective

Produce a complete structural understanding of undergroundmathematics.org —
IA, content model, pipeline, API — sufficient to (a) inform SyllabAI content
platform design decisions and (b) enable a metadata-complete, rights-respectful
dataset of the corpus if the experiment graduates.

## Phases

### Phase 1 — Identification & inventory `[x]` (2026-10-22)

- [x] Site identity, history, philosophy (research/2026-10-22-site-overview.md)
- [x] Full station taxonomy + 855-resource inventory via public API
      (resources/api/)
- [x] Lines, pervasive ideas, key questions, resource types captured
- [x] Content-model schema documented (research/2026-10-22-content-model.md)
- [x] Tech stack + authoring pipeline (research/2026-10-22-technical-architecture.md)
- [x] API surface catalogue (research/2026-10-22-api-catalogue.md)
- [x] URL scheme verification (research/2026-10-22-url-schemes.md)

### Phase 2 — Content-structure crawl `[x]` (2026-10-22)

- [x] Polite crawl of all 855 resource pages + section pages + teacher-support
      pages: **2,486 HTML pages, 0 failures**, ~0.4 s spacing, resumable
      (research/2026-10-22-phase2-crawl-and-extraction.md)
- [x] Parsed each page into the section model: question/problem, suggestion,
      solution, interactive graph, teacher support, acknowledgements,
      "last updated" — one section per URL, `qwell` duplication pattern
      documented
- [x] Resolved URL shapes: sections are first-class URLs
      (`/{station}/{slug}/{section}`); teacher support is a sibling resource
      with its own section URLs; PDF assets live under `/components/` and
      `/download/`
- [x] Extraction committed per operator decision:
      `resources/content/{station}.json` (2,181 section bodies incl.
      question/solution HTML+text) + `resources/content-assets.json`
- [ ] Tubemap SVG rendering spec (line paths, label layout) — moved to a
      later pass
- [ ] Search endpoint parameters (UI-equivalent query) — low priority

### Phase 3 — Canonical extraction `[~]`

- [x] Canonical JSON schema implemented in the extractor (identity,
      taxonomy, sections with html+text, teacher support, assets,
      provenance) — see research/2026-10-22-phase2-crawl-and-extraction.md
- [x] Full corpus extracted and committed (855 resources, 2,181 sections)
- [ ] `qwell` dedup pass (strip re-displayed question wells from
      suggestion/solution bodies into a shared `questionWell` field)
- [ ] Station→line→key-question→pervasive-idea relation graph export
      (JSON/GraphML)
- [ ] Cross-map UGM stations/lines to CIE (and Edexcel) spines from
      `syllabai-v2` (cie-phase1/2 registry work) — the deliverable that
      makes this experiment platform-relevant

### Phase 4 — Design synthesis `[ ]`

- [ ] Decision doc: what SyllabAI adopts (candidates: review-question
      schema + acknowledgement model; suggestion-before-solution section
      layer; type/level tagging; teacher-support as separate content
      objects; modal-navigation UX; markdown+LaTeX→HTML+PDF pipeline with
      their retrospective taken into account).
- [ ] Decision doc: licensing path for any content reuse (see IP notes) —
      Cambridge Mathematics contact before any content lands of record.
- [ ] If graduating: proper PR(s) against the receiving of-record repo per
      repo ground rules.

## Working rules

- Crawl politely; identify ourselves; stay far below any rate that could
  annoy the operators; prefer the public API over HTML scraping where both
  exist.
- Captured raw content stays out of git; only metadata + analysis is
  committed (policy in docs/IP-AND-COPYRIGHT-NOTES.md).
- Every capture logged in resources/manifest.md.
- Nothing here is of record; conclusions graduate via PRs.
