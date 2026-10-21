# URL schemes — verified patterns

**Captured**: 2026-10-22 · method: live HTTP GET/HEAD probes (status codes below observed, not assumed).

## Verified resource URL patterns

| Pattern | Status | Notes |
|---|---|---|
| `/{station}` | 200 | station page, e.g. `/quadratics`; station pages list ~20 named resources + all `r####` review questions |
| `/{station}/{slug}` | 200 | designed resource, e.g. `/quadratics/discriminating` |
| `/{station}/r{ref}` | 200 | review question, e.g. `/quadratics/r5059` (slug = `r{ref}`) |
| `/{station}/r{ref}/solution` | **200** | review-question solution page |
| `/{station}/{slug}-teacher-support` | **200** | teacher support as sibling URL, e.g. `/quadratics/discriminating-teacher-support` |
| `/pervasive-ideas/{slug}` | 200 | e.g. `/pervasive-ideas/invariance` |

## Probed and NOT valid (404) — do not crawl these shapes

| Pattern | Status |
|---|---|
| `/{station}/{slug}/resource-in-action` | 404 |
| `/{station}/{slug}-in-action` | 404 |
| `/resources-in-action/{slug}` | 404 |
| `/{station}/r{ref}/teacher-notes` | 404 |

"Resource in action" and "Teacher notes" render as tabs/sections on the
resource page (and the `-teacher-support` sibling), not as separate routes;
the exact RIA URL shape remains open — resolve during the full crawl by
harvesting actual anchor hrefs from station pages rather than guessing.

## Top-level routes observed on the homepage

```
/about  /blog  /bundles  /courses  /how-to-guide  /hub
/mathematical-classroom  /pervasive-ideas-explanation  /resource-types
/resources-in-action  /webinars
/terms  /cookie-policy  /privacy-policy
```

Plus the 29 station routes and 6 pervasive-idea routes; `/sitemap.xml` → 404,
so the station→resource URL map must be built from API + page harvest (which
is what `../resources/api/all-resources.json` gives us: station + slug per
resource; canonical URL = `/{station.friendlyId}/{resource.friendlyName}`).

## Page-size notes (for crawl budgeting)

- Home 35 KB; station page ~31 KB; designed resource ~21 KB; review question
  ~15 KB (server-rendered HTML, no JS needed for content).
- Estimated full-content crawl of 855 resources + solutions + teacher
  support ≈ low thousands of requests at ~15–35 KB — tens of MB, trivially
  feasible; be polite (spacing, UA string).
