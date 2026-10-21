# IP & copyright notes — what we may capture, commit and reuse

**Set**: 2026-10-22 · applies to everything under `undergroundmathematics/`
in the **public** repo `SyllabAI/syllabai-experimental`.

## The rights situation

- Site content: **© and Database Right 2013–2026 University of Cambridge,
  all rights reserved** (site footer + `/terms`).
- Review questions: each carries an acknowledgement string stating the
  question **remains © UCLES** (University of Cambridge Local Examinations
  Syndicate), reproduced on their site "by kind permission of Cambridge
  Assessment Group Archives".
- The tubemap, station pages, teacher notes, solutions and pedagogy prose
  are Cambridge's copyrighted work.
- The site is free to *use*; that is not the same as free to *re-publish*.

## Policy for this experiment

**Committed to this public repo — allowed:**

1. **API metadata captures** (`resources/api/*.json`): ids, slugs, titles,
   type/level/publish flags, taxonomy relations, station questions, key
   questions, map coordinates, timestamps. Factual catalogue data about
   published resources, captured from the site's own public API for
   research/interoperability.
2. **URL lists** and structural observations (section names, endpoint
   names, status codes).
3. Our own analysis, schemas, summaries and short attributed quotes for
   commentary.

**NOT committed to this repo:**

1. Full text of questions, suggestions, solutions, teacher notes or any
   other substantive site content (HTML captures, PDFs, extracted bodies).
2. Site assets (images, CSS/JS bundles, fonts, GeoGebra materials).
3. Bulk mirrors of pages "to preserve them" — not our call to make.

Raw content captured locally during research stays on the researcher's
machine (or private storage), is used for analysis, and is discarded once
the structural understanding is extracted into our own words.

**If SyllabAI ever wants to reuse UGM content of record** (e.g. review
questions into the Smart Mark corpus, or the pedagogy wrappers): that
requires a licensing conversation with Cambridge Mathematics / Cambridge
Assessment Group Archives *first* — mirroring how UGM itself needed
permission from UCLES to reproduce the exam questions. Until such an
agreement exists, the platform integrates *ideas and schema*, not text.

## Hygiene rules for contributors

- When adding research notes, summarise; quote sparingly and attribute.
- Never paste scraped question bodies into docs, issues, PRs or commit
  messages in any SyllabAI repo (most are public).
- Keep captures metadata-only by default; if a local raw capture is truly
  needed for a bug/analysis, keep it out of git and say so in the manifest
  (file name + "local only").
- The manifest (`resources/manifest.md`) is the audit trail: every capture
  gets source URL, date, method, and what was/wasn't kept.
