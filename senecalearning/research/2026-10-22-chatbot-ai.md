# Seneca Chatbot ("Amelia" AI Assistant) — Reverse Engineering

**Session 8 · 2026-10-22 · authenticated teacher pass + full 1,920-chunk static sweep**

Companion artifacts: `resources/captures/chatbot/` (sanitized probe evidence), API
catalogue session-8 table. Methods: (1) static extraction over the complete chunk
graph — expanded from 290 to **1,920 chunks** by taking the recursive `assets/*.js`
import closure (the chat UI is dynamically imported and absent from the entry/routes
closure used in earlier sessions); (2) live authenticated probes with the operator's
teacher account, ≤1 req/s, captures sanitized before commit.

---

## 1. Service topology

| Host | Role |
|---|---|
| `chatbot.app.senecalearning.com` | chatbot service: 4 streaming AI endpoints, 6 JSON endpoints, session CRUD, file upload |
| `text-to-speech.app.senecalearning.com` | TTS narration for modules *and* chatbot messages (separate service, separate gateway) |
| `identity.app.senecalearning.com` | Firebase ID token issuance (unchanged from auth note) |

The four AI endpoints are declared in `/env.js` under
`chatbotService.functionURL.{query,explain,explainWrongAnswer,examQuestionConversation}`
— same host, plain paths; the "functionURL" name is a leftover from when they were
direct Lambda function URLs. Today they sit behind API Gateway + CloudFront
(`x-amzn-requestid`, `x-amz-apigw-id`, `via: …cloudfront.net` headers observed).

## 2. ChatbotServiceClient — complete surface (14 methods)

Decoded from the minified client class (`signOut-*.js` module `Ke`). Two request
styles coexist:

- **Raw-fetch streaming style** (returns `response.body`, a `ReadableStream`): the
  four AI endpoints. Headers set manually: `correlationId`, `Content-Type:
  application/json`, `access-key` (Firebase ID token), `user-region` (default `GB`).
- **makeRequest JSON style** (adds `X-Amz-Date`, structured `{reason,pointer}` errors):
  everything else.

| Method | Wire call | Notes |
|---|---|---|
| `query(body, accessKey, region)` | `POST /api/query` | **stream**; main "Ask Amelia" chat |
| `explain(body, accessKey)` | `POST /api/explain` | **stream** |
| `explainWrongAnswer(body, accessKey, region)` | `POST /api/explain-wrong-answer` | **stream**; in-session wrong-answer coach |
| `examQuestionConversation(body, accessKey, region)` | `POST /api/exam-question-conversation` | **stream**; chat about an exam question |
| `prompt({prompts, skipModeration})` | `POST /api/prompt` | JSON; 400 → `InappropriateContentError` |
| `generatePrompts(body)` | `POST /api/generate-prompts` | JSON; notes/quiz prompt generation |
| `search(body)` | `POST /api/search` | JSON |
| `generateImage({prompt, orientation})` | `POST /api/generate-image` | JSON; 400 moderated, 401 unauthorised |
| `createUploadUrl(contentType)` | `POST /api/files/upload-url` | `201 {uploadUrl:{fields,url}, key}` — S3 pre-signed POST |
| `fetchSessions({limit, lastKey})` | `GET /api/sessions?limit&lastKey` | chat list, cursor pagination |
| `fetchSessionMessages(sessionId)` | `GET /api/sessions/{id}` | `{sessionId, chatbotMessages[]}` |
| `renameSession({sessionId, title})` | `PATCH /api/sessions/{id}` | `{title}`; 200/400/404 |
| `deleteSession(sessionId)` | `DELETE /api/sessions/{id}` | `204` on success |
| `fetchSessionMessageAdmin({userId, sessionId, timestamp})` | `GET /api/admin/sessions/{id}/message?userId&timestamp` | admin surface, 200/400/404 |

Live-verified shapes (teacher token, free tier):

- `GET /api/sessions?limit=5` → `200 {"items":[]}`
- `GET /api/sessions/{unknown-uuid}` → `200 {"sessionId":"<id>","chatbotMessages":[]}`
  (server synthesizes an empty view rather than 404), while
  `DELETE /api/sessions/{unknown-uuid}` → `404` (strict).

## 3. Streaming protocol — *not* SSE events

Despite `content-type: text/event-stream`, the body is **plain UTF-8 text chunks**
of the model answer (markdown, rendered incrementally via the bundled `marked`
parser). Client loop (from `useSubmitQuestion-*` / `ResultsCard-*` chunks):

```js
const stream = await chatbotService.query(payload, token, region);
const reader = stream.pipeThrough(new TextDecoderStream).getReader();
let acc = '';
for (;;) {
  const {value, done} = await reader.read();
  if (value !== undefined) {
    if (value === StreamErrors.INAPPROPRIATE_CONTENT) throw ...;
    if (Object.values(StreamErrors).includes(value)) throw ...;
    acc += value;
  }
  onReplyStreaming(acc);
  if (done) { onReplyStreamed(acc); break; }
}
```

**Error signalling = error-as-body.** The server writes one of the literal
`StreamErrors` enum strings as (part of) the stream and closes:

| Enum member | Literal stream text | Client behaviour |
|---|---|---|
| `INAPPROPRIATE_CONTENT` | `400 Bad request: inappropriate content` | throw, show safety message |
| (unnamed 413) | `413 Content too large: conversation length limit hit` | **graceful**: `onSuccess({text, finished:true, lengthLimitHit:true})` |
| `INVALID_BODY_FIELD_TEXT` | `422 Invalid body field: text` | throw |
| `INVALID_BODY` | `422 Invalid body` | throw |
| `UNSUPPORTED_REGION` | `Unsupported region` | throw |
| `UNKNOWN` | `Something went wrong in response stream` | throw |
| `FILE_RESOURCE_NOT_FOUND` | `File resource not found` | throw |

There is no `data:` framing, no event names, no `keep-alive` comments — chunks are
appended verbatim. Simple, gzip-friendly, and trivially portable (SyllabAI can adopt
the pattern or improve it with real SSE events without changing the product).

## 4. Model + RAG constants (client-bundled server config)

From the shared errors chunk (`errors-*.js`, exported as chatbot constants):

```
SERVICE_NAME                        = 'chatbot-service'
MODEL_GPT4_OMNI                     = 'gpt-4o'
MODEL_GPT4_OMNI_MINI                = 'gpt-4o-mini'
TEMPERATURE                         = 0.1
MAX_MODEL_GPT4_OMNI_COMPLETION_TOKENS = 4096
MAX_RESPONSE_TOKENS                 = 700
MAX_QUERY_WORDS                     = 500        (UI hard warning at >500 words)
TOKENS_PER_WORD                     = 4/3
MAX_REQUEST_TOKENS                  = MAX_QUERY_WORDS × 4/3 ≈ 666
MAX_EMBEDDINGS_CONTEXT_TOKENS       = 300
MAX_FILES = 1, MAX_SIZE_BYTES = 5,242,880      (one image per message, 5 MB)
```

Interpretation: RAG over Seneca course content with a ~300-token retrieval context
per turn, gpt-4o family, temperature 0.1 (near-deterministic tutoring answers),
700-token response cap. Marketing copy confirms the grounding: *"…answer all your
questions about any course in Seneca. Using state of the art AI technology, trained
on Seneca [content]"*. Contrast with SyllabAI's planned Groq→Gemini Flash→OpenRouter
cascade: Seneca buys reliability/grounding at premium-token cost; the cascade can
differentiate on latency + cost per token.

## 5. Request payloads (client-side construction, minified-decoded)

**Amelia chat (`query`)** — submit handler builds
`{sessionId, text, image?}` (`image` = S3 `key` from `createUploadUrl`, first of the
`fileKeys[]`; UI limits to 1 image). Session IDs are client-generated UUIDs; a new
chat posts with a fresh UUID and the server materializes it.

**In-session wrong-answer coach (`explainWrongAnswer`)** — full payload observed in
`registerComponents-*`:

```js
{
  courseId, courseName, sessionId,            // chatbot session id
  userProperties: { yearGroup },
  question:      { text },                    // or {question, correctAnswer, userAnswer}
  correctAnswer: { text },                    // built per module type (MC/wordfill/word)
  userAnswer:    { text },
}
```

Answer text is composed per module type, e.g. word-fill:
`"Wrong word: <user>  Word that fits better: <correct>"`. Gating metadata rides the
UI (`gatingType: EXPLAIN_ANSWER`, `remainingInvocation`), not the payload.

**TTS** — `GET text-to-speech…/api/get-speech/chatbot?sessionId&timestamp` →
`{items:[{audioUrl, speechMarks}]}`; per-message pre-generated audio keyed by
message timestamp, `speechMarks` drive mouth/typing animation. Live probe confirmed
validation contract: missing/odd timestamp → `400 {"reason":"invalid timestamp","pointer":"timestamp"}`
(same `{reason,pointer}` InvalidArgumentError shape as tutor-resources).

**Files** — `POST /api/files/upload-url {contentType}` → pre-signed S3 POST
(`fields` + `url` + `key`); browser POSTs `FormData` directly to S3; the `key` then
rides the next chat message. Upload analytics event: `ameliaImgUploadToStorage`.

## 6. Product surface — "Amelia AI Assistant"

- Persona: **Amelia** ("Amelia AI Assistant"); time-of-day greeting ("Good morning,
  {name}, how can I help?"); course-scoped route `CLASSROOM.COURSE.ASK_AMELIA.CHAT`.
- Input affordances: text, voice (speech recognition), 1 image; 500-word warning;
  acceptable-use-policy link; personal-information warning copy.
- Answers render as streaming markdown; per-message feedback options; TTS playback;
  transcript appending (`appendTranscript-*` chunk) for follow-ups.
- Session management UI: list with titles, rename modal, delete modal ("Delete this
  chat? … You won't be able to access it again."), conversation-length graceful stop.
- Gating: `AmeliaGatingModal` — *"Your own personal tutor to support, explore and
  guide with Seneca Premium. Plus so much more…"*; premium-trigger components wrap
  the in-session coach; analytics `AmeliaGating{Shown,Dismiss,CtaClicked}`.

## 7. Freemium quota — AI features as XP rewards

`FreemiumRewardFeature` enum: `explainMyAnswer`, `examQuestion`, `wrongAnswers`,
`hardestQuestions`. Reward types: `avatar` | `freemium`. The hook
`useExplainMyAnswerAccess` computes
`remainingInvocation = premium ? Infinity : data?.explainMyAnswer ?? 0` — i.e. the
free tier earns AI invocations as **XP level-up rewards**, surfaced on the dashboard
as claimable reward cards ("Claim a free reward" → invite-parent flow for more).
This is a gamified entitlement loop: study → XP → level → more AI quota → study.
Directly portable to SyllabAI as an engagement mechanic.

## 8. Live gating findings (free teacher account, sandbox egress)

| Probe | Result |
|---|---|
| `GET /api/sessions?limit=5` | `200 {"items":[]}` — token accepted |
| `GET /api/sessions/{uuid}` | `200` empty messages view — token accepted |
| `POST /api/query` (valid payload) | HTTP **200**, `content-type: text/event-stream`, stream body = `403 Forbidden` |
| `POST /api/query` (moderation-probe text) | identical stream body `403 Forbidden` — rejection fires **before** content validation |
| `POST /api/prompt` | `401 {"reason":"Invalid or missing access-key"}` (with/without `X-Amz-Date`) |
| `POST /api/generate-image` | `401 {"reason":"Invalid or missing access-key"}` |
| `POST /api/search` | `502 {"message":"Internal server error"}` (endpoint exists; payload shape unverified) |
| `GET text-to-speech…/get-speech/chatbot` | `400 {"reason":"invalid timestamp","pointer":"timestamp"}` — validation reached |

Diagnosis: the AI-generation endpoints enforce an additional gate that the session
CRUD endpoints do not. Two candidate mechanisms, not mutually exclusive:

1. **Entitlement** — Amelia is a Premium package feature (`AmeliaGatingModal`,
   premium-trigger wrapping, "Invalid or missing access-key" on the JSON-style AI
   endpoints for a free account).
2. **Region/IP fence** — CloudFront served this sandbox from `x-amz-cf-pop: HKG54`;
   the client ships a `UNSUPPORTED_REGION` StreamError and per-region
   `enableChatBot` flags (GB/DE/AT/FR/ES/IT true, US absent), and the streaming
   rejection is a bare gateway-style `403 Forbidden` written into an otherwise-200
   SSE response.

The identical body across valid/moderation/empty payloads shows the gate is
pre-validation; distinguishing entitlement vs IP fence requires either UK egress or
a Premium account (operator decision, not pursued).

## 9. SyllabAI takeaways

1. **Streaming**: raw-text-chunks + error-as-body is beautifully simple but
   conflates transport with payload; SyllabAI should use real SSE events
   (`{type:"delta"|"error"|"done"}`) — same UX, debuggable contract.
2. **Server-side entitlement**: SyllabAI's free-tier quotas must be enforced
   server-side (Seneca's client-visible `remainingInvocation` is advisory; their
   server clearly enforces too — our 401/403 proves it — but the *count* lives
   client-side between requests).
3. **XP-rewarded AI quota** is a proven engagement loop worth adapting: study
   streaks literally purchase tutor usage.
4. **RAG sizing**: 300-token retrieval context is aggressively small — a deliberate
   cost choice; SyllabAI's per-specification retrieval can afford more context per
   turn and still undercut gpt-4o pricing via the Groq/Gemini cascade.
5. **Admin/observability**: session-message admin endpoint exists (compliance
   surface); SyllabAI should plan the equivalent safeguarding view from day one.
6. **Cost guardrails in client constants** (max words/tokens/temperature) are a
   leak of server config — keep SyllabAI's tuning server-side.

## Probe hygiene

Both probe sessions were `DELETE`d (404s confirmed nothing persisted); final
`GET /api/sessions` → `{"items":[]}` — account clean. No assignments, classes,
or student data touched. JWT stayed in `/tmp/seneca_token.txt` (removed after
session); raw probe bodies live in local `probe-results/chatbot/` (git-ignored);
only sanitized, token-free exemplars are committed under `resources/captures/chatbot/`.
