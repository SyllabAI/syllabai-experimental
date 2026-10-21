# Technical architecture — app.senecalearning.com

**Captured**: 2026-10-22 · method: response-header analysis, app shell
HTML, `/env.js`, `/versions.js`, `manifest.json`, 290-chunk bundle corpus
mined locally (bundles not committed — see IP notes).

## Delivery topology

```
browser
  │  https://app.senecalearning.com            (SPA shell, S3 + CloudFront)
  │  https://course-cdn-v2.app.…               (course content CDN)
  │  https://localisation.app.…                (Localize widget CDN)
  │  https://{service}.app.senecalearning.com  (~40 API microservices, AWS API Gateway)
  │  wss://session-ws.app.…                    (live session WebSocket)
  │  relay.app.…                               (Sentry tunnel)
  ▼
AWS (Cognito eu-west-1, S3 buckets eu-west-1 for images/PDFs/certs, Lambda-ish chatbot function URLs)
```

- Static origin: S3 (`x-amz-server-side-encryption`, `server: None` hidden)
  behind **CloudFront**; `no-cache` on the shell so deploys land instantly.
- API hosts return uniform JSON errors `{"message":"Not Found"}` (404) /
  `{"message":"Unauthorized"}` (401) — classic API Gateway + custom
  (Lambda) authorizer behaviour. CORS allow-list pins the app origin, and
  permits `Authorization, X-Api-Key, X-Amz-Security-Token, access-key,
  correlationId, user-region, user-language` — i.e. Cognito JWTs, custom
  correlation IDs and regional routing are part of the contract.
- The `user-region` request header + a `regions-*.js` chunk + a
  geolocation service imply **multi-region data routing** (likely for
  GDPR/school contracts).

## Frontend stack (fingerprinted)

| Concern | Finding |
|---|---|
| Framework | React 19-era SPA; `react-dom`, `react-redux`, `immer`, `reselect`, Redux `ReducerRegistry` (registry-slice pattern) |
| Data | **TanStack Query** (`useQuery`, `useMutation`, `useQueries`, `queryOptions`) alongside Redux; `apiStates` helper module |
| Router | typed-router helpers (`useTypedSearchParams`, `useTypedState`) |
| Build | **Rolldown** (`rolldown-runtime-*.js`) — Rust-based bundler; 290 chunks, granular per-feature code-splitting; versioned asset hashes |
| Versioning | `window.Seneca.version = "4.6.264"`; `/versions.js` force-upgrade machinery (cache purge + SW unregister below `AUTO_UPDATE_VERSION 4.6.0`; `?min-version=latest` escape hatch) |
| PWA | `manifest.json`, service worker, push via **Firebase Cloud Messaging** (VAPID key in env.js), iOS TWA (assetlinks + AASA, App Store id 1631302657), localforage offline storage, update toasts |
| Fonts | Mulish (self-hosted woff2) |
| Localisation | Localize widget (`localisation.app.…` CDN) — runtime DOM translation, 6 locales (help-centre locales: en, pt-BR, fr, de, es, vi) |
| Observability | Sentry (DSN + **tunnel** through `relay.app.…`), Microsoft Clarity, GTM |
| Analytics/marketing | GA4, Doubleclick, LinkedIn, TikTok, Facebook, Bing pixels |
| Payments | Stripe (`pk_live_11CE1Pa7Fy7Fmg0fNv98clBm`), js.stripe.com frames |
| Support | Intercom (`fwcflxs6`), Calendly, Loom embeds |
| Content media | Giphy/Tenor (memes in lessons), YouTube, Mux video, Sanity CMS CDN (marketing content) |

## White-label / multi-variant architecture

One codebase, origin-sniffed variants (chunks: `useAppVariant`,
`useIsStudienkreisApp`, `useIsGoStudentLearningApp`, `isGoStudentLearningApp`):

| Variant | Domain | Notes |
|---|---|---|
| Seneca | app.senecalearning.com | default |
| GoStudent Learning | learning.gostudent.org; `gostudent` origin sniff; GoStudent logo/splash | owner's brand |
| Studienkreis | DE/AT variant; dedicated PDF bucket `studienkreis-pdf-resources-processed-v1.s3…` | German partner |
| Plurall (Adapta) | `adapta.plurall.net`; **separate OIDC Firebase project** (`seneca-auth-production-oidc`), Plurall help-centre API + shared cookie | Brazil |
| iOS dev/edge builds | `com.senecalearning.dev` / `.edge` / `.app` in AASA | staged rollout channels |

Splash-screen JS even picks logo CSS by origin — cheap-and-effective
theming rather than per-variant builds.

## Notable engineering choices (SyllabAI-relevant)

1. **`env.js` as runtime config**: a single fetched JS object wires every
   service host, feature flags (separate feature-flags *service*), Sentry,
   Stripe, Firebase, GTM — no rebuild to re-point infrastructure. Cheap
   and operationally excellent; see `research/2026-10-22-service-map.md`.
2. **Force-upgrade machinery** (`versions.js`): cache apocalypse recovery
   for stale service workers after school holidays ("after the Summer"),
   with a query-param escape hatch — real-world PWA fleet management we
   should imitate if/when the hub ships PWA.
3. **Sentry tunnel**: first-party relay to dodge ad-blockers eating error
   reports.
4. **Granular chunking**: 290 chunks with feature-named modules
   (`classLeaderboardsService`, `anonymousQuizStorage`,
   `enrichEQWithGenerationSeed`, `sessionsCompletedCounter`) — the chunk
   graph itself is a feature map; `resources/captures/chunk-list.txt` keeps it.
5. **`enrichEQWithGenerationSeed`** + `anonymousQuizStorage`: evidence of
   **procedurally seeded exam-question variants** and pre-auth quiz
   attempts — directly comparable to SyllabAI question-generation plans.
6. Dual data layers: Redux for session UI state, TanStack Query for
   server state, localforage for offline — a pragmatic hybrid.
