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
