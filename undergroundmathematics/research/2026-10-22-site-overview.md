# Site overview — undergroundmathematics.org

**Captured**: 2026-10-22 · sources: `https://undergroundmathematics.org/`, `/about`, `/about/website`, `/bundles`, `/hub` (see `../resources/manifest.md`)

## What the site is

Underground Mathematics provides free web-based resources that support the
teaching and learning of **post-16 mathematics** (UK A level). It aims to make
post-16 mathematics "a richer, more coherent and more stimulating experience
for students and teachers alike". All resources are free for all users.

Identity facts:

| Field | Value |
|---|---|
| Domain | undergroundmathematics.org |
| Operator | University of Cambridge, hosted by Cambridge Mathematics |
| Funding | UK Department for Education grant |
| Origin | Started 2012 as the **Cambridge Mathematics Education Project (CMEP)** |
| Pilot | 2013–2016 partner-school trials on a pilot site |
| Public launch | February 2016 (current website) |
| Copyright | © and Database Right 2013–2026 University of Cambridge, all rights reserved |
| Contact | info@undergroundmathematics.org · Twitter @UndergroundMath |
| Analytics | Google Analytics, property `G-EB3PK96QD8` |

## History timeline

1. **2012** — project founded as CMEP at Cambridge (directors: Martin Hyland,
   Professor of Mathematical Logic, DPMMS; Lynne McClure, Director of
   Cambridge Mathematics).
2. **2013–2016** — resource design + classroom trials with partner schools;
   the predecessor pilot site used review-question ids still visible in the
   API as `oldSiteId` (e.g. `Q255` for review questions, `C3_RT6_3` for
   teaching resources).
3. **Feb 2016** — current site released openly. The 2016-vintage content
   (`updatedDate` mostly 2015–2017) has remained live and essentially frozen
   since; the `/hub` shows site activity/news/event surfaces that are now
   largely dormant (e.g. `/bundles` renders the feature shell but reports
   "No bundles found").
4. **Now** — hosted by Cambridge Mathematics; team roster on `/about`
   includes directors, resource designers, evaluation, web developers,
   champions and partner schools.

## Stated philosophy (from /about)

The work is informed by explicit beliefs about mathematics education, which
the resource design operationalises:

- Mathematics is a worthwhile, interesting, **human activity**; everyone
  should have the opportunity to be mathematical and to succeed
  mathematically; **ability is not fixed**.
- A key activity is **grappling with problems one does not yet know how to
  solve**; exchanging questions and ideas is valuable; mistakes and
  misconceptions are worth studying; there are **many ways to be
  mathematical**.
- Resources are designed to be **low-threshold high-ceiling**, combining
  problem solving, mathematical reasoning and fluency — and *all* students
  should work on such resources, not only high achievers.
- Design goals for classroom use: give students the opportunity to **think
  mathematically**; support them in **developing their own understanding**;
  invite students to **make connections** for themselves; nurture
  **mathematical independence**; develop **resilience, flexibility and
  creativity**.

The site explicitly says the tubemap "is not tied to any syllabus" and does
"not place a strong emphasis of doing one topic before another" — the
organisation is mathematical, not curricular. (Relevant to SyllabAI: this is
the inverse of an exam-board spine, and the two views can be cross-mapped.)

## Site map (top-level surfaces)

| Path | What it is | State 2026-10-22 |
|---|---|---|
| `/` | Angular SPA home — "Rich resources for teaching A level maths" | live |
| `/{station}` | 29 station (topic) pages, e.g. `/quadratics` | 24 live, 4 under construction |
| `/{station}/{resource}` | resource pages (named + review questions) | live |
| `/pervasive-ideas/{slug}` | 6 cross-cutting theme pages | live |
| `/resource-types` | taxonomy explainer for the 14 types | live |
| `/map` (modal) | tubemap navigation (modal dialog, not a route) | live |
| `/search`, `/browse` (modals) | resource search/browse (modal dialogs) | live |
| `/bundles` | curated resource sequences | shell live, "No bundles found" |
| `/courses` | classroom courses listing | live (legacy) |
| `/hub` | site activity: news, events, articles, updates, quotes, newsletter archive, posters | live, largely dormant |
| `/your-mathematical-classroom` group | teacher-facing: bundles, resources-in-action, blog, webinars, 2017 A level | live (legacy) |
| `/how-to-guide` | user guide incl. videos | live |
| `/about`, `/about/website` | project + technical self-documentation | live |
| `/terms`, `/cookie-policy`, `/privacy-policy` | legal | live |

## Scale measured from the public API (2026-10-22)

| Measure | Count |
|---|---|
| Stations (topics) | 29 (24 with resources, 4 under construction returning 401 on their APIs, 1 station id 7 absent) |
| Public resources (sum over stations) | **855** |
| — Review questions (type 10) | 569 (66%) |
| — Designed teaching resources | 286 across 13 other types |
| Station key questions | 113 |
| Lines (curriculum threads) | 5 |
| Pervasive ideas | 6 |
| Resource types | 14 |
| Duplicate slugs across stations | 0 (slug namespace is station-scoped and clean) |

## Why SyllabAI cares (working hypothesis, to validate in later phases)

1. **Review-question corpus**: 569 exam questions digitised *with* section
   structure (question/suggestion/solution), exam provenance and per-question
   metadata — a reference model for how SyllabAI's Smart Mark corpus rows
   could be structured (see `syllabai` spec §Smart Mark).
2. **Pedagogy layer above the questions**: key questions, pervasive ideas,
   resource levels (Introducing → Developing), teacher support pages — a
   mature model of "teaching wrapper" that SyllabAI's tutor layer could
   imitate.
3. **Taxonomy design**: mathematical organisation (tubemap) separate from
   syllabus mapping — directly relevant to the CIE/Edexcel spine work in
   `syllabai-v2` (T-SM-ROLLOUT) as a cross-mapping pattern.
4. **Authoring pipeline**: markdown + LaTeX source → HTML + PDF from one
   source, authored in an admin UI — comparable problem space to
   `syllabai-parser`/content pipeline, with an honest retrospective worth
   reading before choosing our own authoring formats.
