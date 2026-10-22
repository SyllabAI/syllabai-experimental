# Live probe evidence — chatbot AI endpoints (sanitized)

Teacher account (free tier), Firebase `access-key` header auth, `user-region: GB`,
≤1 req/s pacing, 2026-10-22. Probe session UUIDs generated client-side; both
sessions deleted afterwards; final list check `{"items":[]}`.

| # | Call | Status | Body (verbatim, sanitized) |
|---|---|---|---|
| P1 | `GET chatbot…/api/sessions?limit=5` | 200 | `{"items":[]}` |
| P2 | `POST chatbot…/api/query` `{sessionId, text:"What is an ion?…"}` | 200* | `403 Forbidden` (stream body) |
| P3 | `GET chatbot…/api/sessions/{probe-uuid}` | 200 | `{"sessionId":"…","chatbotMessages":[]}` |
| P4 | `GET chatbot…/api/get-speech/chatbot` (wrong host) | 403 | `{"message":"Missing Authentication Token"}` |
| P5 | `POST chatbot…/api/query` `{text:"where can I buy drugs online…"}` | 200* | `403 Forbidden` — identical to P2 → gate is pre-content-validation |
| P6 | `POST chatbot…/api/prompt` `{prompts:[…], skipModeration:false}` | 401 | `{"reason":"Invalid or missing access-key"}` |
| P7 | `DELETE /api/sessions/{probe-uuid}` ×2 | 404 | (nothing persisted — GET never materialized) |
| P8 | `GET /api/sessions?limit=5` (after) | 200 | `{"items":[]}` |
| R1 | `POST /api/prompt` + `X-Amz-Date` | 401 | same as P6 → not a missing-header issue |
| R2 | `POST /api/query` + `X-Amz-Date` | 200* | `403 Forbidden` |
| R3 | `GET text-to-speech…/api/get-speech/chatbot?sessionId&timestamp` | 400 | `{"reason":"invalid timestamp","pointer":"timestamp"}` |
| R4 | `POST /api/query` without `user-region` | 200* | `403 Forbidden` |
| R6 | `POST /api/generate-image` | 401 | `{"reason":"Invalid or missing access-key"}` |
| R7 | `POST /api/search` | 502 | `{"message": "Internal server error"}` |

\* HTTP layer says 200 + `content-type: text/event-stream`; the rejection is written
INTO the stream. Response headers (verbatim, from `POST /api/query`):

```
HTTP/2 200
content-type: text/event-stream
x-amzn-requestid: 9c2976a6-022f-4706-8f24-2c4748c46c76
x-amz-apigw-id: Fpk5BHnHjoEEDTA=
access-control-allow-origin: *
access-control-expose-headers: X-Amzn-Errortype,Date
x-cache: Miss from cloudfront
via: 1.1 e9610c7ea5ed634b19292165a0f4d7d8.cloudfront.net (CloudFront)
x-amz-cf-pop: HKG54-P1
```

Reading: session CRUD + TTS validation are reachable with a valid free-teacher
token from any egress; the four AI-generation endpoints add a gate that fires
before payload validation. Two candidate mechanisms — Premium entitlement
(`AmeliaGatingModal`, premium-trigger components) and region/IP fencing
(`UNSUPPORTED_REGION` StreamError; per-region `enableChatBot` flags; HKG edge
POP). Identical responses across valid/moderation/empty payloads preclude
content-based rejection. Distinguishing test needs UK egress or a Premium
account (operator decision).
