# Auth model — Seneca Learning

**Captured**: 2026-10-22 · sources: `env.js`, bundle mining (`auth-*.js`,
`signInWithEmailAndPassword-*.js`, `firebase-*.js`, `signInState-*.js`),
live probes. No authentication was attempted beyond anonymous endpoint
probes.

## Primary identity: AWS Cognito

| Field | Value (from env.js — public client config, not a secret) |
|---|---|
| User pool | `eu-west-1_5sGUjs8Wq` (Ireland) |
| App client id | `5e9bhjn9pn9tf41hrr7s1rqhr4` |
| Custom endpoint | `https://identity.app.senecalearning.com` (Cognito custom auth domain, used instead of `cognito-idp` direct) |
| API facade | `https://authentication.app.senecalearning.com` |
| Retry policy | `retryCount: 0` on the auth service config |

Endpoint surface seen in bundles (all paths live on the `identity` host):

- `/v1/token` — token issue/exchange
- `/v1/recaptchaParams` + `/v2/recaptchaConfig` — reCAPTCHA bootstrapping
  (visible chunks: `recaptcha`, `password-ab*.js` for policy validation)
- `/v2/passwordPolicy` — server-driven password rules

**Live probe (anonymous GET)**: `identity.app…` answers these paths with a
structured `400 BadRequest {"code":"BadRequest","type":"client"}` while
`authentication.app…` returns generic 404 — confirming the identity host
owns the Cognito-protocol surface and the authentication host is a
separate app-level API. Correct verbs are POST (untested; Phase 2 with an
account).

JWTs then ride the `Authorization` header to every service (CORS allow-list
confirms `Authorization` + `X-Amz-Security-Token` accepted — the latter
hints some services also accept SigV4/IAM, likely service-to-service).

## Secondary identity layer: Firebase

| Project | Purpose |
|---|---|
| `seneca-auth-production` (authDomain `auth.app.senecalearning.com`, apiKey `AIzaSyDXmCdeFZFJbQOtl6xupkxZw-lIOKuJQKg`) | main client project: **FCM push messaging** (VAPID), Google Analytics (`G-VKRZ4QY04D`), storage bucket `seneca-auth-production.appspot.com`, Google sign-in bridging (`signInWithRedirectTarget` chunk) |
| `seneca-auth-production-oidc` | **OIDC federation project shared by Plurall and GoStudent variants** — `adapta.plurall.net` and `learning.gostudent.org` authenticate via this second Firebase project; auth domain `auth.oidc.app.senecalearning.com` |

So the architecture is: **Cognito owns the Seneca-native identity;
Firebase/OIDC brokers the white-label partner identities** (and owns
messaging/analytics for everyone). Email+password signup is reCAPTCHA
protected; Google SSO present; Microsoft identity association file also
published (`/.well-known/microsoft-identity-association.json`) for
Entra-based school SSO.

## Session/transport auth

- Bearer Cognito JWT per service call; `correlationId`, `user-region`,
  `user-language` custom headers on every request (CORS list).
- WebSocket (`wss://session-ws.app.…`) presumably authenticates on
  connect with the same token (Phase 2 item).
- Anonymous access: every probed API path returned 401/404 — **no public
  read surface**; even course metadata requires auth. (Contrast: UGM's
  fully anonymous API.)

## Mobile app identity

- iOS: App Store id `1631302657`, AASA at
  `/.well-known/apple-app-site-association` (three bundle ids:
  `.dev`, `.edge`, `.app` — staged release channels; all paths allowed
  except `/what-is-premium*` which is web-only by design).
- Android: `com.senecalearning.app` (Play) + `assetlinks.json` for TWA
  deep links.

## Phase 2 credential ask

To map the authenticated contract (token flow shape, JWT claims,
course/session/memory payloads) we need **one throwaway student account**.
Operator decision required per `docs/IP-AND-COPYRIGHT-NOTES.md`. Signup
will need an email + reCAPTCHA solve (interactive); if the operator
provides credentials, capture plan: login → save token shape (redacted) →
hit the phase-2 endpoint list with metadata-only capture, ≤1 req/s.
