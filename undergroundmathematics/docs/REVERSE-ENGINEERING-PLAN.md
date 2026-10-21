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

### Phase 2 — Content-structure crawl `[ ]`

- [ ] Polite crawl of all 855 resource pages (server-rendered HTML) at
      ~0.5–1 req/s with a descriptive UA; harvest raw HTML into local
      storage only (not committed to this public repo — see IP notes).
- [ ] Parse each page into the section model: question/problem, suggestion,
      solution, teacher support, interactive-graph markers, acknowledgements,
      "last updated".
- [ ] Resolve the open URL shapes (resource-in-action tab; teacher notes
      placement; supporting-materials PDF URL pattern
      `supportingMaterialsViewModel.getPdfDownloadUrl`).
- [ ] Capture the tubemap rendering (SVG structure, line paths, station
      positions from API data) as a spec.
- [ ] Sample the printable PDF pipeline output for a few resources; record
      the HTML→PDF parity behaviours.
- [ ] Investigate the real search endpoint parameters (UI uses
      autocomplete + `/api/search`; our naive probe returned empty).

### Phase 3 — Canonical extraction `[ ]`

- [ ] Define a canonical JSON schema for UGM resources
      (identity, taxonomy links, sections, provenance, rights flags) —
      mirroring the structure their own DB exposes.
- [ ] Extract the full corpus into `resources/` as **metadata + structural
      digests only** (no copyrighted question/solution bodies committed).
- [ ] Build the station→line→key-question→pervasive-idea relation graph
      export (JSON/GraphML) for cross-mapping experiments.
- [ ] Cross-map UGM stations/lines to CIE (and Edexcel) spines from
      `syllabai-v2` (cie-phase1/2 registry work) — the deliverable that
      makes this experiment platform-relevant.

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
