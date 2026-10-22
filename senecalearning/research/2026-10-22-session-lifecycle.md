# Session Lifecycle — session-ws Protocol + Session Emit + XP

**Date:** 2026-10-22 (Phase 2, session 4) · **Method:** live Adaptive study session on
`Chemistry: Edexcel iGCSE → States of Matter` (leaf section) as teacher account, with
in-page `fetch` + `WebSocket` instrumentation; frame ledger + REST payloads captured
verbatim.

---

## 1. session-ws WebSocket protocol

### Connection

```
wss://session-ws.app.senecalearning.com?access-key=<Firebase JWT>&sessionId=<uuid>
```

- Opened by the session player when a study session starts (route
  `/classroom/course/{courseId}/section/{sectionId}/session`).
- **Auth rides the query string**, not a header — the same Firebase ID token used in
  the `access-key` REST header is passed as `?access-key=…` (JWT visible in URL;
  servers/CDN logs see it — an implementation detail SyllabAI should NOT copy; use
  `Sec-WebSocket-Protocol` or first-message auth).
- One socket per session (`sessionId` is generated client-side, UUIDv4).

### Frame inventory (full capture, one complete session)

| # | Dir | Frame |
|---|---|---|
| 1 | OUT | `{"action":"start-session","data":{…}}` |
| 2–5 | OUT | `{"action":"keep-connection-alive"}` (~every 30–60 s) |
| 6 | IN | `{"action":"session-xp","data":{…}}` (after session emit) |

**The socket is lifecycle/signalling only — zero answer data flows through it.**
All answer evidence is buffered client-side (Redux) and flushed by a single REST emit
at session end (§2). Frames:

```jsonc
// OUT on open
{"action":"start-session","data":{
  "userId": "<uuid>",
  "sessionId": "63f02348-41c2-480c-9529-32c8a4d9c8c1",
  "courseId": "967b4370-21e8-11e8-8c0c-d79041e9c8a6",
  "sectionId": "0fde17b0-21e9-11e8-8c0c-d79041e9c8a6",
  "sessionTimeStarted": "2026-10-22T02:03:11+00:00"
}}

// OUT every ~30-60s
{"action":"keep-connection-alive"}

// IN after the client POSTs the finished session (§2) — the only server push seen
{"action":"session-xp","data":{
  "type": "session",
  "userId": "…", "sessionId": "…", "courseId": "…", "sectionId": "…",
  "sectionIds": ["…"],
  "newXp": 29,
  "userLevel": {"level": 2, "currentLevelXpThreshold": 200, "nextLevelXpThreshold": 350},
  "breakdown": {"completionXp": 12, "scoreXp": 9, "memoryXp": 8},
  "assignmentXp": 0,
  "independentXp": 29,
  "totalUserXp": 214, "totalCourseXp": 29,           // + yearly/monthly/weekly/daily mirrors
  "reward": {"type": "avatar", "avatarId": "0ede5ab5-…"},
  "session": {"sessionId": "…"}
}}
```

**XP formula decoded:** `session XP = completionXp + scoreXp + memoryXp`
(12 + 9 + 8 = 29 here; completion is fixed per session, score scales with session
score 0.89, memoryXp is the palace-deposit bonus — see §3). Levels: thresholds
200 → 350 → … (level 2 at capture). Random cosmetic reward (avatar) granted alongside.

Sentry telemetry in the app bundle corroborates the socket's role: a
`complete-session-ws-response-duration` custom measurement (sampled 0.2%) times the
emit→xp round-trip.

## 2. Session end — `POST https://session.app.senecalearning.com/api/session`

One shot, fired when the learner finishes (or abandons-but-confirms) the session.
`200` on success. This is **the entire answer ledger** — full-document emit, no
incremental syncing, matching the offline-first client design (the earlier
`emitSession`/`emitQuizSession` client methods in `signOut-B19aTuAB.js`:
`POST /api/session` [200, 400] and `POST /api/session/quiz` [200, 400] for quiz-type
sessions).

### Request (captured, redacted)

```jsonc
{
  "platform": "seneca",
  "clientVersion": "4.6.264",
  "userId": "<uuid>",
  "session": {
    "sessionId": "63f02348-…", "courseId": "967b4370-…",
    "timeStarted": "2026-10-22T02:03:11+00:00",
    "timeFinished": "2026-10-22T02:06:46Z",
    "startingProficiency": 0,                    // BKT prior for this section
    "endingProficiency": 0.495,                  // BKT POSTERIOR — computed client-side
    "startingCourseProficiency": 0,
    "endingCourseProficiency": 0.0023798076923076924,
    "endingCourseScore": 0.0036475409836065576,
    "sessionScore": 0.89,
    "completed": true,
    "modulesCorrect": 2, "modulesIncorrect": 1,
    "averageScore": 0.89,
    "modulesGaveUp": 1,
    "modulesStudied": 5, "modulesTested": 3,
    "sessionType": "adaptive",                   // adaptive | quiz | wrong-answers | hardest-questions | exam-questions
    "sectionIds": ["0fde17b0-…"],
    "contentIds": [],
    "options": {"hasHardestQuestionContent": false}
  },
  "modules": [ /* full per-module ledger, in play order */ ]
}
```

**Notable:** the client computes and submits `endingProficiency` itself — the
knowledge-tracing update (0 → 0.495 after one 0.89-score session) happens in the
SPA, and the server trusts it. SyllabAI's server-side update (per its docs) is
strictly more trustworthy; Seneca's choice optimises for offline play.
(Session-5 addendum: the *durable* client model is an exponential forgetting
curve + fractional spacing counter, not BKT — exact formulas in
`2026-10-22-memory-math.md`; the in-session posterior formula itself remains
unrecovered, §5 there.)

### Module ledger entry shape (5 modules captured)

Common keys: `sessionId, moduleOrder, moduleId, timeStarted, timeFinished, gaveUp,
submitted, completed, moduleType, testingActive, content, score, moduleScore?,
userAnswer?, moduleDifficulty, courseId, sectionId, contentId`.

| moduleType | testingActive | what it is |
|---|---|---|
| `concept` | false | notes/lesson card (content echoed: `title`, `explanation`, `examples[] {title, example, image{url,fallbackUrl}}` — image URLs are `image-v2.cdn.app.senecalearning.com/courseImages/…` with Cloudinary-style transforms `f_cover,h_400,w_600`) |
| `image-list` | true | label-the-image + attached MC. `userAnswer: {multipleChoice:{index:3}, list:["gas","",""]}`, `moduleScore: {score:1, multipleChoice:{score:1,inputScores:[true]}, list:{score:1,hits:[false,true,false],inputScores:[true]}}` |
| `mindmap` | true | the "Switch the toggles" pairing widget (gave-up path observed: `gaveUp:true, submitted:false, score:0.67` — partial credit for toggles set correctly before abandoning) |
| `multiple-choice` | true | plain MC, `userAnswer: {index:…}`-family, per-input `inputScores[]` |

Scoring is **fine-grained and client-computed**: `score` (0–1) plus `moduleScore`
with per-blank `hits[]` / `inputScores[]` booleans. `pretest: "SOMETIMES"` flags
interleaved repeats (adaptive re-asking the same concept with re-shuffled options —
observed live: same question, different option order on second pass).

### Quiz-mode variant

`POST /api/session/quiz` (same envelope; quiz sessions reference the quiz `contentId`
rather than course section modules — client method `emitQuizSession`).

## 3. Memory palace deposit — `POST https://memory.app.senecalearning.com/api/memories`

Immediately after the session emit, the client fires:

```json
{
  "courseId": "967b4370-…",
  "courseName": "Chemistry: Edexcel iGCSE",
  "sectionId": "0fde17b0-…",
  "sectionTitle": "States of Matter",
  "locationId": "5c1f19e5-4a48-4c32-b461-2e9592148db4",
  "timeEarned": "2026-10-22T02:06:46Z"
}
```

→ `201`. The UI flow right before it: **"Choose where to store your memory"** — a
choice of 2 real-world locations (Castle Combe UK / Riddarholmen Cathedral Sweden),
then an interactive **map micro-question** ("Do you know where Riddarholmen Cathedral,
Sweden is?" → click the world map → "You scored 48!") before the deposit. This is
Seneca's method-of-loci gamification: each studied section becomes a "memory"
pinned to a place. The deposit itself is what earns the `memoryXp` component
in the session-xp breakdown.

## 4. Related REST touched by the session player

| Call | Purpose |
|---|---|
| `GET /api/stats?date=<ISO>&aggregationLevel=day` (stats.app…) | daily XP/usage header |
| `GET /api/stats/sections?includeHardestQuestionsOnlyStats=true&courseId=…` | per-section spaced-repetition state (see `2026-10-22-memory-model.md`) |
| `GET /api/weekly-plan/me?weekStartDate=2026-10-19` | weekly study plan widget |
| `POST /api/get-speech/module` (422 on our modules) | TTS narration for lesson content |
| `POST /api/quizzes/generate` family | Magic Quiz (see sibling doc) |

## 5. Mode chooser (session start UI)

Adaptive (free) · Quiz (**premium-locked in UI**) · Wrong Answers (needs history) ·
Hardest Questions · Exam Questions. `sessionType` in the emit enum mirrors this.

## 6. SyllabAI relevance

- **Offline-first + single-shot emit** is a proven pattern for flaky school Wi-Fi:
  buffer everything client-side, one `POST` on completion, server idempotent on
  `sessionId`.
- **Client-computed BKT posterior** is Seneca's trade-off (trusting the client);
  SyllabAI already plans server-side BKT — but keeping the *ledger shape*
  (`userAnswer` + per-input `moduleScore` with `hits[]`) gives explainable
  per-blank evidence to feed it.
- **WS for signalling only** (session open + XP push), REST for state — simple and
  robust; SyllabAI can replicate without streaming answers.
- **XP breakdown as data** (`completion/score/memory`) is a clean motivation model;
  the memory-palace deposit + `memoryXp` couples retention mechanics to reward.
