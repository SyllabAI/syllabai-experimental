# Captures manifest — senecalearning

**Captured**: 2026-10-22 · all items fetched anonymously from public
endpoints with a descriptive UA. Sizes approximate.

## Committed

| Path | What | Source URL |
|---|---|---|
| `env/env.js` (9.4 KB) | the app's full runtime service config — the Phase 1 crown jewel | `https://app.senecalearning.com/env.js` |
| `env/versions.js` (2.4 KB) | PWA force-upgrade machinery | `https://app.senecalearning.com/versions.js` |
| `env/manifest.json` (0.5 KB) | PWA manifest | `https://app.senecalearning.com/manifest.json` |
| `env/apple-app-site-association.json` | iOS universal links (3 bundle ids) | `https://app.senecalearning.com/.well-known/apple-app-site-association` |
| `headers/app-senecalearning-headers.txt` | response headers + CSP of the app shell | `https://app.senecalearning.com/` (HEAD/GET) |
| `chunk-list.txt` | 290 JS chunk paths from the module graph | extracted from `index-*.js` + `routes-*.js` |
| `extracted-paths.json` | API paths + config strings mined from all chunks | local analysis |
| `extracted-paths-2.json` | second-pass extraction (template literals, resource names, app routes) | local analysis |

## Not committed (re-fetchable; see `scripts/fetch-app-bundles.sh`)

| Path (local only) | What | Why excluded |
|---|---|---|
| `js/*.js` (290 files, ~4.6 MB) | the full minified app bundle corpus | Seneca's minified proprietary code; kept locally for analysis only, per IP notes. Chunk manifest + extractions capture the intel. |

## Live-probe log (Phase 1)

| Request | Result |
|---|---|
| `GET /` (app shell) | 200, CloudFront HKG, S3 origin, full CSP recorded |
| `OPTIONS chatbot /api/query` | 200; CORS pinned to app origin; `Authorization`+`correlationId`+`user-region`+`user-language` expected; methods `OPTIONS,POST` |
| `POST chatbot /api/query` (anonymous, `{}` body) | 401 `{"message":"Unauthorized"}` |
| `GET course /courses`, `/v1/courses`, `/`, `course-cdn-v2 /courses.json` | 404 `{"message":"Not Found"}` |
| `GET identity /v1/token`, `/v2/passwordPolicy`, `/v2/recaptchaConfig` | 400 structured `BadRequest` (protocol-aware host) |
| `GET authentication /v2/passwordPolicy`, `/v2/recaptchaConfig`, `/v1/token` | 404 generic (not the protocol host) |
| `GET /.well-known/apple-app-site-association` | 200, captured |
| `GET /assets/ServiceClientRegistry-*.js.map` | 200 but SPA-fallback HTML — source maps NOT published |

## Phase 2 additions (2026-10-22, live session)

| Path | What | Source |
|---|---|---|
| `courses-taxonomy.jsonl` (713 KB, 2,761 rows) | slim course taxonomy: courseId, name, tier, visibility, regions, section counts, TTS | `course-cdn-v2…/api/courses?limit=3000&maxVisibility=HIDDEN` (full 3.9 MB dump local only) |
| `feature-flags.json` (3.4 KB) | static + release flag set of record | `feature-flags…/api/flags` |
| `class-me-redacted.json` | teacher class record (`/api/classes/me`), userId redacted | live session |
| `xp-me-shape.json` | XP response shape (levels, buckets) | `xp…/api/xp/me?date=` |

Live session log (kept local, not committed): fetch/XHR instrumentation
capture with signed headers; token in `/tmp/seneca_token.txt` only.

## Phase 2 session 3 additions (2026-10-22, assignment creation + Resource Hub)

| Path | What | Source |
|---|---|---|
| `assignments/README.md` + 4 exemplars | full assignment CRUD payload set (create/update/class-view, redacted) | live UI funnel + fetch instrumentation |
| `resource-hub/README.md` | categorisation + schema guide for the catalogue | this session |
| `resource-hub/tags-taxonomy-slim.json` | 132-tag taxonomy (74 subjects, 21 age groups, 12 boards, price/pathway/tier) | `tags…/api/tags` |
| `resource-hub/subject-resource-counts.csv` | 74 subjects × 3 types = 207,629 resources | `tutor-resources…/api/v2/query-resources` aggregations |
| `resource-hub/chemistry-resources-metadata.jsonl.gz` | every Chemistry resource, metadata only (18,306 rows; examQuestion stems nulled) | same, paginated |
| `resource-hub/all-subjects-sample-metadata.jsonl.gz` | ≤200/type sample for 69 other subjects (18,890 rows; examQuestion stems nulled) | same |
| `resource-hub/edexcel-igcse-chemistry-*.json` | 14-course family records + 872 sections + readable tree of the Free course | `course…/api/courses/queryCourses` (types=[section]) |
| `scripts/resourcehub-download*.py`, `scripts/sections-download.py`, `scripts/build-repo-artifacts.py` | reproducible pipeline for the above | — |

Not committed (local-only, per IP notes): raw `query-resources`
responses incl. question bodies, mark schemes and generation scripts
(`probe-results/rh3/local-only-full-payloads/`).
