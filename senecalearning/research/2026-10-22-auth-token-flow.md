# Auth token flow — verified with a live account (Phase 2, session 1)

**Captured**: 2026-10-22 · method: headless-browser login (operator-provided
teacher account), fetch/XHR instrumentation in page context, token decoded
locally with claims redacted. **No credentials or tokens are committed.**

## The verified flow

```
Firebase email/password (sign_in_provider: "password")
  → Firebase ID token (JWT RS256, kid 904b0f91…)
      iss: https://securetoken.google.com/<firebase-project>
      aud: <firebase-project-id> (seneca-auth-production)
      claims: sub/user_id, email, email_verified, auth_time, iat, exp (1h)
  → sent to every backend service as the CUSTOM HEADER  access-key: <ID token>
      + correlationId: {epochMs}::{uuid4}
      + X-Amz-Date: {yyyyMMddTHHmmssZ}   (timestamp header, not SigV4 —
                                          no signature/hdr list present)
      + user-region: GB   (on some services)
```

Corrections to Phase 1 inferences:

1. The primary auth is **Firebase**, not Cognito — the SPA's session JWT is
   a Firebase ID token. The Cognito config in `env.js`
   (`eu-west-1_5sGUjs8Wq`) remains real but is not what the logged-in SPA
   sends; treat Cognito as legacy or per-flow secondary until proven
   otherwise.
2. There is **no `Authorization: Bearer` header** — the token rides the
   custom `access-key` header (hence the CORS allow-list entry `access-key`
   spotted in Phase 1).
3. `X-Amz-Date` + `access-key` looked like SigV4 in Phase 1; live capture
   shows a bare timestamp + JWT — **no request signing observed**.

## Service auth matrix (live, same token+headers)

| Service | Path tried | Result | Reading |
|---|---|---|---|
| class | `/api/enrollments/me/classes`, `/api/classes/me` | **200** | accepts Firebase token |
| assignments | `/api/teacher/me/assignments*` | **200** | accepts |
| memory | `/api/memories` | **200** | accepts |
| xp | `/api/xp/me?date=` | **200** | accepts (400 w/o `date`) |
| feature-flags | `/api/flags` | **200** | accepts |
| course-cdn-v2 | `/api/courses?limit=3000` | **200 anonymous** (correlationId only) | catalogue is public; detail payloads CloudFront-signed |
| course (API) | `/api/courses/{id}` | **401 Unauthorized** | does NOT accept this token — different auth (Cognito? signed flow?) |
| session | `/api/sessions` | 403 Missing Authentication Token | session-scoped auth, unresolved |
| tournaments | `/api/tournaments` | 401 Invalid or missing access-key | region/scope mismatch or different token type — unresolved |

So **the fleet is not uniform**: Firebase-token services vs
differently-authed services (course API, session, tournaments). Mapping the
second family is the top Phase 2 leftover; the browser must be watched
while actually opening a course/session to see which token/flow they use.

## Token hygiene

- Tokens live only in `/tmp/seneca_token.txt` (machine-local) and page
  memory; 1-hour expiry (`exp`), refresh silent via Firebase SDK.
- Nothing committed: captures contain response bodies and redacted header
  shapes only. Saved auth state JSON also stays out of the repo.
