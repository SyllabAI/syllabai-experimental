# URL schemes — Seneca Learning

**Captured**: 2026-10-22 · sources: bundle route strings, AASA, PWA
manifest, App Store metadata.

## Web app routes (SPA, client-side)

| Route | Surface |
|---|---|
| `/login`, `/sign-up` | auth |
| `/dashboard` | student home |
| `/dashboard/assignments/todo` | student assignment queue |
| `/dashboard/courses/add` | add a course (enrolment picker) |
| `/dashboard/what-is-premium` | premium upsell (excluded from app deep links — web-only, see AASA) |
| `/classroom` | in-app classroom view |
| `/session` | a learning session (the core loop) |
| `/multi-section/end-session` | multi-section session wrap-up |
| `/teacher` | teacher platform |
| `/parent`, `/parent/monitoring/overview`, `/parent/tutoring`, `/parent/what-is-premium` | parent platform |
| `?min-version=latest` | escape hatch to force latest PWA assets (versions.js) |

## Mobile deep links

- **iOS universal links** (AASA, `/.well-known/apple-app-site-association`):
  app IDs `4393Y7QA5R.com.senecalearning.{dev,edge,app}` — three release
  channels (dev/edge/prod) all claiming `*` paths except
  `NOT /what-is-premium` and `NOT /what-is-premium/parent`. The explicit
  NOT-exclusion of the premium page from native links is a deliberate
  funnel choice (keep purchase flow on web for Stripe/monitoring).
- **Android**: `/.well-known/assetlinks.json` + Play id
  `com.senecalearning.app`; TWA support chunks (`useAndroidTWA`).
- PWA: `start_url ./index.html`, standalone display, theme `#3574cf`;
  push scope `/firebase-cloud-messaging-push-scope/` with
  `/firebase-messaging-sw.js` worker.

## Content CDN URL patterns observed

- App assets: `https://app.senecalearning.com/assets/{name}-{hash}.js|css`
  (hashed, immutable).
- Images: `https://image.cdn.app.senecalearning.com/...` and
  `https://image-v2.cdn.app.senecalearning.com/...` (two CDN generations).
- Course content: `https://course-cdn-v2.app.senecalearning.com/...`
  (path pattern unresolved — Phase 2, needs auth).
- Partner/static S3 buckets (from CSP): `seneca-images-v1`,
  `studienkreis-pdf-resources-processed-v1`, `certificate-pdfs-v1`,
  `chatbot-upload-images-production-v1` (all `s3.eu-west-1.amazonaws.com`);
  sharing image `https://d17hukvrbysd4e.cloudfront.net/rsz_sharinglinkimage.png`.
- Certificates: `certificate-pdfs-v1` — Seneca issues downloadable
  certificates (per help centre, XP/milestones).

## Marketing site notes

`senecalearning.com` serves per-locale roots (`/en-GB`, `/en-gb`, …) and is
SEO-heavy: one landing page per subject/qualification (A Level, GCSE, KS3,
iGCSE, IAL, IB) — 100+ nav-linked course pages observed in the search
index. Help centre on `help.senecalearning.com` (Intercom-style articles,
6 locales).
