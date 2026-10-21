# Technical architecture — stack, rendering, authoring pipeline

**Captured**: 2026-10-22 · sources: live HTML/JS, `/about/website`, `main.min.js` (224 KB) endpoint scan

## Frontend stack (verified from served HTML)

| Layer | Technology |
|---|---|
| SPA framework | **AngularJS 1.4.7** (`data-ng-app="cmCore"`), angular-resource, angular-sanitize |
| DOM helpers | jQuery 2.1.4, js-cookie 2.1.1, jquery.devbridge-autocomplete 1.2.24 |
| Math rendering | **MathJax 2.7.1**, config `TeX-AMS-MML_HTMLorMML` |
| Markdown (client) | markdown-it 8.3.1 (used for user notes/comments) |
| Fonts | Open Sans (Google Fonts) |
| CSS | single bundle `/static/css/main.min.css?v=2` |
| JS bundles | `/static/js/main.min.js` (app core, 224 KB) + page-type bundles e.g. `/static/js/public/resource.min.js` (13 KB) |
| Offline | **ServiceWorker** + web app manifest (`/static/app-manifest/manifest.webmanifest`); "network-first, fall back to cache" |
| Analytics | gtag.js `G-EB3PK96QD8` |

Architecture shape: **server-side pre-rendered HTML, progressively enhanced
by Angular**. Page titles, navigation and full content are present in the raw
HTML (curl-able without JS); Angular then wires up modals (map/search/browse),
user features, collections and comments. This dual nature is why plain HTTP
captures work for content and the API works for metadata.

There is also a role-gated **admin toolbar** (`adminData.showTools` in the
shell) exposing authoring tools to staff accounts.

## Backend (inferred + self-documented)

- Content stored in a **MySQL database**; images uploaded to server
  filesystem (stated on `/about/website`).
- REST API under `/api/*` — **215 distinct endpoints** referenced in
  `main.min.js` (catalogue in `2026-10-22-api-catalogue.md`).
- Auth model: anonymous read of public content APIs; session cookie for user
  features (collections, notes, comments); staff-gated authoring/admin
  APIs (`/api/content/:identifier` returns `LoginRequired` 401 to anon).
- Endpoints follow a consistent resource-nested pattern
  (`/api/resources/:resourceId/{key-questions,lines,tags,…}`) — strongly
  normalised backend entities, matching the MySQL schema.

## The authoring → delivery pipeline (self-documented on /about/website)

This is the highest-value page on the site for us; quoted/summarised:

1. Resources are **written online in an admin section** by resource
   designers; content stored in MySQL; images on server filesystem.
2. Delivery must be both **HTML (online) and PDF (print)**; browser print
   was deemed too inflexible.
3. Source format is **Markdown with mathematics as LaTeX** inside it.
4. **Custom XML/HTML tags are processed before the Markdown** to express
   features Markdown lacks: toggleable sections, highlighted
   questions/comments, alternative output for the printable version, etc.
   The same tags emit different HTML and LaTeX.
5. **Pandoc** converts Markdown → HTML (site, math via MathJax) and → LaTeX
   → PDF (per-resource printables and user-generated booklets).
6. Their own retrospective: *"working with Markdown programmatically is
   quite difficult due to whitespace being significant, so it may have been
   better to use a restricted subset of HTML rather than Markdown."*
7. Booklet generation (combined PDFs from a user's resource collection)
   reuses the LaTeX pipeline; not intended for large collections; links in
   resources point back to the website; navigational pages are deliberately
   not offered as PDFs.

Why this matters for SyllabAI: the same dual-target need (web + print) exists
in our content pipeline; their answer (single markdown+LaTeX source, custom
pre-processor tags, Pandoc) is a proven but candidly-costed design, and the
retrospective is an argument for structured/semantic source over
whitespace-sensitive markdown for anything machine-processed.

## Interactivity

- **GeoGebra applets** embedded as resources/sections (e.g.
  `geogebra-constructions-quadratic`), plus static interactive graphs.
- Interactivity is flagged in metadata (`interactivityLabels`,
  `resource-interactivity-labels` APIs; `resource-interactivity-labels` on
  each resource) so search/browse can filter "interactive" resources.
- MUST/MAY/CAN'T card-sorts etc. are delivered as **printable card PDFs**
  (download links inside problem sections) — low-tech, classroom-first.

## URL & asset scheme (verified 2026-10-22)

- `/` — SPA home (35 KB server-rendered shell).
- `/{station}` — station page (e.g. `/quadratics`, 31 KB).
- `/{station}/{slug}` — designed resource; `/{station}/r####` — review
  question; `/{station}/r####/solution` → 200; teacher support lives at
  `/{station}/{slug}-teacher-support` → 200.
- `/pervasive-ideas/{slug}`, `/resource-types`, `/bundles`, `/hub`,
  `/courses`, `/webinars`, `/blog`, `/how-to-guide`, `/about`,
  `/about/website`, legal pages.
- No `/sitemap.xml` (404); no public robots.txt restrictions observed.
- Full pattern table with observed status codes:
  `2026-10-22-url-schemes.md`.

## Ops signals

- Content is effectively **frozen 2016–2017** (updatedDate distribution);
  the hub/news surfaces are dormant — a completed, maintained-in-amber
  product, not an active build.
- Image pipeline endpoints (`/api/images/:virtualPath/generate`) suggest
  on-demand image resizing with a virtual-path abstraction.
- Long-running task infrastructure (`long-running-tasks`, statuses/types)
  exists for admin batch jobs — consistent with the print/booklet pipeline.

## Risks/limits of the reverse engineering so far

- Admin/authoring APIs are auth-gated; the admin UI itself is not reachable
  — pipeline knowledge above comes from their own documentation, not
  inspection.
- Search endpoint `/api/search/:keyphrase` returned empty results in tests
  (`{"results":[],"totalRows":0}`); the real search UI likely posts
  different queries — to investigate in the crawl phase.
- The tubemap SVG rendering code (map positions, text angles) lives in
  client bundles; not yet analysed in detail.
