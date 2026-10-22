# API catalogue — public REST surface

**Captured**: 2026-10-22 · method: endpoint strings extracted from
`https://undergroundmathematics.org/static/js/main.min.js` (AngularJS
`$resource` definitions), then live-tested. 215 endpoints referenced in
total; grouped below. Raw list kept in the worklog; the groups below are the
reverse-engineering-relevant subset.

## Auth model

- **Anonymous read** works for the public content/metadata endpoints
  (tested OK).
- **Session-gated**: user features (collections, notes, comments, trials).
- **Staff-gated**: authoring/admin (content CRUD, publishing, history,
  analytics dashboards). `/api/content/:identifier` → 401
  `LoginRequired` for anonymous calls.
- The four under-construction stations return **401** on their station
  sub-resources (`/api/stations/{id}/resources|key-questions|lines`) —
  i.e. unpublished stations are *not merely hidden*, their read paths are
  auth-fenced.

## Verified public (anonymous, 200) — the useful scrape surface

| Endpoint | Returns |
|---|---|
| `/api/stations` | all 29 stations: id, friendlyId, title, guiding question, map position/angle, publish/hidden/underConstruction flags, timestamps |
| `/api/stations/{id}/resources/all` | full resource records for a station (schema in content-model note) |
| `/api/stations/{id}/key-questions` | station key questions (slug + question) |
| `/api/stations/{id}/lines` | lines through the station |
| `/api/stations/{id}/nearby` | map "nearby stations" relations |
| `/api/lines/detail` | 5 lines with colour, order, member stationIds |
| `/api/pervasive-ideas` | 6 pervasive ideas |
| `/api/resource-types/converted` | 14 types with full descriptions |
| `/api/resource-list` | filtered/paged resource list (returned 25 in test — default page, not the full corpus) |
| `/api/search/{keyphrase}` | search results (returned empty in our test — needs UI-equivalent params) |
| `/api/analytics`, `/api/analytics/total`, `/api/analytics/resources`, `/api/analytics/cities` | public site-activity counters used by the hub |

## Endpoint groups present in the client bundle (auth-gated or user-scoped)

**Content/authoring** — `/api/content/:identifier` (+`/converted`,
`/lock`, `/unlock`, `/force-unlock`, `/warnings`), `/api/history/:id`,
`/api/history/restore/:saveId`, `/api/metadata-history/:id`,
`/api/find-and-replace`, `/api/long-running-tasks*`,
`/api/publish-statuses`, `/api/update-{types,importances}`.

**Resources (write + relations)** — `/api/resources/:id` (+`/clone`,
`/replace`, `/update-printable-cache`); per-resource relation CRUD:
`key-questions`, `keyphrases`, `lines`, `tags`, `interactivity-labels`,
`malcolm-swan-categories`, `related-pervasive-ideas`, `related-resources`,
`resource-extras`, `resource-sections`, `teacher-notes`, `contributors`,
`review-question-info`, `assets/:name`.

**Taxonomies** — `/api/resource-section-types`, `/api/resource-levels`,
`/api/review-question-types`, `/api/review-question-info-entries`,
`/api/keyphrase-types`, `/api/contribution-types`,
`/api/teacher-perspective-categories`,
`/api/malcolm-swan-categories` (classic classroom-challenge taxonomy),
`/api/station-nearby-types`, `/api/url-redirect-types`,
`/api/copyright-licences`, `/api/resource-sources`.

**User features** — `/api/bookmarks*` (groups, pairs, notes, lite, many,
download), `/api/comments*` (recent, per-item, accept/reject moderation),
`/api/resource-trials*` + `/api/resource-trial-requests*` (teacher trial
booking), `/api/champion-applications*` (champion programme),
`/api/glossary`, `/api/help-items` + `/api/help-sections`.

**Site pages & hub** — `/api/extra-site-pages` (+sections, includes),
`/api/news-items`, `/api/events`, `/api/featured-events`,
`/api/conference-days`, `/api/webinars`, `/api/newsletters` (+content),
`/api/quotes/public`, `/api/articles`, `/api/useful-links`,
`/api/useful-downloads`, `/api/features`, `/api/pedagogy-page-overviews`
(+properties), `/api/new-a-level`, `/api/recent-updates`.

**Media** — `/api/images/:virtualPath` (+`/generate`, `/clear`,
`/image-sources-parent`).

## Notable schema signals

- `/api/resources/:resourceId/sections` + `resource-section-types`: page
  sections are typed entities — confirms the "sections as data" model that
  the markdown pre-processor tags compile into.
- `malcolm-swan-categories` on resources: they tag tasks with the
  Swan/Burton *learning difficulties* taxonomy — a fifth, research-derived
  tagging axis (misconception-oriented), reinforcing the pervasive-ideas
  finding.
- `teacher-perspectives` with categories/stations/resource-types facets:
  the "Resource in action" layer is structured data, not prose pages.
- `copyright-licences` as a first-class entity; every resource can carry a
  licence record — rights are modelled, not assumed.
- `url-redirects` with types: URL stability is managed explicitly (relevant
  given content frozen since 2016).

## Scrape-relevant pagination note

`/api/resource-list` pages; the reliable full-corpus path is
`/api/stations` → loop `/api/stations/{id}/resources/all` (what
`resources/api/all-resources.json` contains). Rate limiting: none observed
at research volume (~30 calls, ~0.4 s spacing); keep it polite.

## Phase-3b correction (2026-10-22, live-tested at corpus scale)

The grouping above put the per-resource relation paths under
"Resources (write + relations)" among auth-gated endpoints. **That is wrong
for reads**: every per-resource relation GET is anonymously public, and they
are the clean membership source for the relation graph.

Verified at full scale (855 resources × 6 axes = 5,130 calls, ~0.35 s
spacing, descriptive UA, 0 failures, no rate limiting observed):

| Endpoint (per resource) | Anonymous GET | Edges captured |
|---|---|---|
| `/api/resources/{id}/key-questions` | 200 | 1,530 (843 resources have ≥1) |
| `/api/resources/{id}/lines` | 200 | 1,272 (844 resources) |
| `/api/resources/{id}/related-pervasive-ideas` | 200 | 331 (250 resources) |
| `/api/resources/{id}/related-resources` | 200 | 306 raw / 290 unique — relationship vocabulary: `Around`, `Back`, `Forward` |
| `/api/resources/{id}/keyphrases` | 200 | 2,286 (783 resources) |
| `/api/resources/{id}/tags` | 200 | 300 (225 resources; `relevanceScore` weight) |

Taxonomy status refined:

- `/api/tags` — public (11 process-skill tags) — committed as
  `resources/api/tags.json`.
- `/api/interactivity-labels` — public (2: card-sort, geogebra) — committed
  as `resources/api/interactivity-labels.json`.
- `/api/keyphrases` (+ `/api/keyphrases/{id}`) — 401 `LoginRequired`
  (list and single alike): keyphrase memberships are public but their
  labels are not. Graph carries numeric keyphrase nodes flagged
  `labelResolved: false`.
- `/api/glossary` — public (term suggestions; not a keyphrase map).

`/api/resource-list` addendum: its `page`/`pageSize`/`perPage` params are
**ignored** — every response is the same first 25 rows (25 hard-paged);
`totalRows: 843`. Only 25 unique records are reachable. For those 25, the
embedded `lines` arrays match the per-resource capture exactly (0
mismatches), which cross-validates the capture. 843 equals the count of
resources with key-question memberships, suggesting the list is
tubemap-scoped, not a full-corpus list (855). Evidence:
`resources/derived/relations/`, graph meta in
`resources/derived/relation-graph.json`.
