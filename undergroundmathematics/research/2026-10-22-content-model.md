# Content model — resources, sections, review questions, provenance

**Captured**: 2026-10-22 · data: `../resources/api/all-resources.json` (855 records), HTML captures of exemplar pages

## Resource record schema (from `/api/stations/{id}/resources/all`)

Every resource object carries:

| Field | Meaning |
|---|---|
| `id` | internal numeric id |
| `ref` | public ref — review questions use `R{ref}` (e.g. R5059); teaching resources use `T{ref}`-style refs in page footers |
| `friendlyName` | URL slug — `r6180` for review questions, prose slugs (`discriminating`) for designed resources |
| `title` | display title (all 855 unique) |
| `description` | one-paragraph teacher-facing summary |
| `stationId` / `_station` | owning station (single-owner model; cross-station reach via lines) |
| `resourceTypeId` | one of 14 types (see below) |
| `resourceLevel` | `Introducing` / `Developing` / null — pedagogical stage |
| `oldSiteId` | predecessor-site id (`Q255`, `C3_RT6_3`) — 600/855 mapped |
| `acknowledgement` | exam/source provenance text (UCLES paper, QP code, year, question numbers, permission line) |
| `sourceUrl`, `resourceSourceId`, `copyrightLicenceId` | source linkage (7 distinct source ids in use) |
| `publishStatus`, `hidden`, `displayAtStation`, `underConstructionWarning` | visibility flags — all 855 `Public`, 0 hidden |
| `displayAtStation` | **346 resources are `false`** — they exist as sub/attached resources (teacher-support pages, suggestions, solutions, in-action variants) rather than station-listed items |
| `associatedResourceId` | pairing of related resources |
| `quickNotes`, `createdDate`, `updatedDate`, `createdByUserId`, `updatedByUserId` | authoring metadata |

## Two species of resource

**1. Review questions (569, 66%)** — the historical-exam corpus.

- Slug `r####`, public ref `R####`.
- Sourced from real past papers; the acknowledgement field records exact
  provenance, e.g. (R5059, "When is 12x^2+7x-10 negative?"):
  *"UCLES O level Additional Mathematics 2, QP 420/2, 1962, Q7(ii), 7(iii).
  Question reproduced by kind permission of Cambridge Assessment Group
  Archives. The question remains Copyright University of Cambridge Local
  Examinations Syndicate (UCLES), All rights reserved."*
- Papers stretch back to the 1960s; 398/569 carry machine-readable `oldSiteId`
  links to the pilot site.
- Page anatomy: **Question → Suggestion → Solution** (three toggleable
  sections), plus "Previous/Next" in-station navigation, station + lines
  footer, printable PDF, teacher notes.
- `resourceLevel` is null for review questions — levels apply to designed
  resources only.

**2. Designed teaching resources (286)** — the pedagogy layer, 13 types:

| Type (id) | Count | Role (from `/resource-types`) |
|---|---|---|
| Building blocks (1) | 44 | introduce concepts/techniques, foundations for later work |
| Rich example (2) | 12 | standard techniques or arguments, invitations to explore scope |
| Scaffolded task (3) | 20 | structured progression, scaffolds later removed |
| Many ways problem (4) | 29 | one problem, multiple solution routes |
| Package of problems (5) | 29 | related problem sets around one idea |
| Problem requiring decisions (6) | 10 | choose approach/tools before computing |
| Investigation (7) | 19 | open exploration |
| Fluency exercise (8) | 24 | practice with variation |
| Food for thought (9) | 44 | provocations, snippets, discussion starters |
| Go and think about it... (11) | 7 | pointers to external/extended problems |
| Bigger picture (12) | 36 | context, history, connections beyond A level |
| Resource in action (13) | 12 | classroom narrative with teacher moves |
| Support (14) | (attached) | teacher-support material |

Levels: **Introducing 59, Developing 227** — a two-stage gradient matching
the low-threshold high-ceiling philosophy (no "Advanced" tier: challenge comes
from the task, not the tier).

## Section structure inside a resource page

Named resources (e.g. `/quadratics/discriminating`, "Package of problems")
render as:

- Header: station breadcrumb, resource type, title, add-to-collection /
  notes actions, printable PDF, fullscreen toggle.
- Tabs/sections: **Problem · Suggestion · Solution · Interactive graph ·
  Teacher support · Resource in action** (tabs vary by resource; each is a
  separately-authored collapsible section — the "custom XML tags" in their
  authoring pipeline, e.g. toggleable sections).
- Body: markdown + LaTeX (MathJax-rendered), e.g. MUST/MAY/CAN'T statement
  cards, downloadable card-sort PDFs, GeoGebra applets
  (`geogebra-constructions-quadratic` is itself a resource).
- Footer: acknowledgement/provenance, "Last updated", station, lines.

## The wrapper features around content

- **Resource collections** (bookmarks): users group resources into
  collections; the system can generate a combined PDF booklet via the
  LaTeX pipeline (explicitly "not designed to be used for large numbers").
- **Notes** per user per resource; **comments/discussion** per resource
  (moderated — `comments/:id/accept|reject` endpoints).
- **Teacher notes** are first-class content (`teacher-notes` API),
  generated per resource.
- **Bundles** — curated sequences with a goal ("take students on a
  particular mathematical journey"); the feature ships but is empty live.
- **Resources in action** — a dedicated layer documenting classroom use:
  narrative + student-thinking commentary (`teacher-perspectives` API with
  categories, resource-types and stations facets).

## Provenance & rights model (summary)

- University of Cambridge owns the site content (© + database right).
- Exam questions remain © UCLES, used "by kind permission" of Cambridge
  Assessment Group Archives, with per-resource acknowledgement strings.
- Their licensing page (`/terms#copyright`) frames reuse permissions for
  users; see `../docs/IP-AND-COPYRIGHT-NOTES.md` for what this means for us.

## SyllabAI takeaways

1. The review-question record (`ref` + provenance + sections + level + links)
   is close to a canonical **mark-row-compatible question schema**; the
   acknowledgement field shows how exam provenance is carried per item.
2. **Suggestions as a separate section** (between problem and solution) is a
   pedagogically motivated middle layer — a natural fit for SyllabAI's
   tutor scaffolding ("hint before solution").
3. `displayAtStation=false` for 40% of records shows their model separates
   *content objects* from *navigation surfaces* — sub-resources (solutions,
   teacher support) are resources too, just not station-listed.
4. Type + level + key-questions + pervasive-ideas is a compact but complete
   pedagogical tagging system; SyllabAI could adopt the shape with its own
   exam-board mapping on top.
