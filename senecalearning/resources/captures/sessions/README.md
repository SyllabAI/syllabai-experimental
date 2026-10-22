# Session lifecycle captures — redacted

**Captured**: 2026-10-22 (Phase 2 session 4) · one real **Adaptive** study session on
`Chemistry: Edexcel iGCSE → States of Matter` (leaf section `0fde17b0-…`,
course `967b4370-…`) walked end-to-end on the teacher account with in-page
`fetch`+`WebSocket` instrumentation. `userId` values redacted; the Firebase JWT never
stored (it rode the WS query string only in RAM; scrubbed from frame captures).
Lesson/question content bodies truncated per the IP notes "title rule" extension —
structure kept, bodies shortened.

| File | What |
|---|---|
| `session-ws-frames.jsonl` | full WS frame ledger for one session: `start-session` OUT, `keep-connection-alive` heartbeat OUT ×3, `session-xp` IN (the only server push; contains the XP formula breakdown `completionXp+scoreXp+memoryXp` and level thresholds) |
| `session-emit-request-redacted.json` | verbatim `POST https://session.app.senecalearning.com/api/session` request body: session envelope with **client-computed BKT posterior** (`startingProficiency 0 → endingProficiency 0.495`) + full 5-module answer ledger (`moduleType`, `userAnswer`, `score`, `moduleScore` with per-input `hits[]`) |
| `module-answer-samples.json` | the 3 tested modules' `userAnswer`/`moduleScore` pairs extracted cleanly (image-list, mindmap/toggles gave-up partial credit, multiple-choice) |
| `memory-items-after.json` | `GET https://memory.app.senecalearning.com/api/memories` read model after first session: one memory item = (courseId, sectionId) + palace `location` {name, country, lat/long, `seneca-image-cdn:///` image ref} |
| `stats-section-redacted.json` | `GET https://stats.app.senecalearning.com/api/stats/sections` record: `proficiency: 0.495`, **`spacing: 1`** (SR interval counter), `recentSectionEvents[]` (prior→posterior log), mode-scoped counters, `moduleIdsStudied[]` |

Related research: `research/2026-10-22-session-lifecycle.md` (protocol +
emit contract), `research/2026-10-22-memory-model.md` (schema interpretation).

Account state after capture: 1 completed session, 1 memory deposit, XP 214 (level 2);
0 assignments; no class changes.
