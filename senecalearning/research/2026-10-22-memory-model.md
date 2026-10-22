# Memory Model — memory service schema + stats proficiency / spaced repetition

**Date:** 2026-10-22 (Phase 2, session 4) · **Method:** baseline `GET /api/memories`
before any study (`{"items":[]}`), one live Adaptive session, then re-read
`/api/memories` + `GET /api/stats/sections` and diff. Plus static analysis of the
classroom UI ("Spaced Repetition recommendations" controls).

---

## 1. Two distinct stores — don't conflate them

| Store | Host | Holds | Lifetime |
|---|---|---|---|
| **memory service** | `memory.app.senecalearning.com` | *palace deposits*: which (course, section) pairs have been memorised, and where they "live" on the world map | permanent unlock/collectible |
| **stats service** | `stats.app.senecalearning.com` | *learning state*: proficiency, scores, spacing counter, study time, per-section events | rolling, updated per session |

Seneca's marketing "Memory" (the palace) is a **gamified ledger of completed
sections**, NOT the spaced-repetition scheduler. The scheduler state
(`proficiency`, `spacing`) lives in the **stats** service. SyllabAI's BKT + forgetting
curve model maps to the stats-service shape below, not the palace.

## 2. memory service — captured schema

### Read — `GET https://memory.app.senecalearning.com/api/memories`

Response after one completed session (verbatim, `userId` never appears — memories are
resolved from the `access-key` JWT):

```json
{
  "items": [
    {
      "id": "657b836a-6576-49d6-9551-1ae15d17e215",
      "courseId": "967b4370-21e8-11e8-8c0c-d79041e9c8a6",
      "sectionId": "0fde17b0-21e9-11e8-8c0c-d79041e9c8a6",
      "locationId": "5c1f19e5-4a48-4c32-b461-2e9592148db4",
      "timeEarned": "2026-10-22T02:06:46Z",
      "courseName": "Chemistry: Edexcel iGCSE",
      "sectionTitle": "States of Matter",
      "location": {
        "id": "5c1f19e5-4a48-4c32-b461-2e9592148db4",
        "name": "Riddarholmen Cathedral",
        "countryName": "Sweden",
        "imageURL": "seneca-image-cdn:///memory-location-images/11thFebOnwards/Riddarholmen%20Cathedral%2C%20Sweden-min.jpg",
        "latitude": 59.324681,
        "longitude": 18.064578
      }
    }
  ]
}
```

- One memory item = one **(courseId, sectionId)** pair + palace `locationId` +
  earn timestamp. Re-studying a section presumably re-uses/updates the same item
  (keyed by course+section).
- `location` embeds a custom CDN scheme (`seneca-image-cdn:///…`) resolved by the app,
  plus real lat/long — the world map UI pins memories at geographic coordinates.
- Write path: `POST /api/memories` `{courseId, courseName, sectionId, sectionTitle,
  locationId, timeEarned}` → `201` (see session-lifecycle doc §3). The
  `locationId` is chosen from a 2-option UI at session end.
- Negative probes: `GET /api/memories/up-next` → 404 (no scheduler endpoint here —
  confirms §1). No delete observed in client bundle.

## 3. stats service — the real spaced-repetition model

### `GET https://stats.app.senecalearning.com/api/stats/sections?includeHardestQuestionsOnlyStats=true&courseId={courseId}`

Captured per-section record (redacted):

```jsonc
{
  "stats": [{
    "userId": "…", "sectionId": "0fde17b0-…", "courseId": "967b4370-…",
    "sessionsCompleted": 1,
    "totalStudyTime": 159,                    // seconds
    "lastStudied": 1792634806,                // epoch seconds
    "sessionModulesStudied": 5,
    "sessionModulesCorrect": 2,
    "averageScore": 0.89,
    "averageSessionScore": 0.89,
    "lastScore": 0.89, "bestScore": 0.89, "worstScore": 0.89,
    "spacing": 1,                             // ← spaced-repetition interval counter
    "recentSectionEvents": [
      {"averageScore": 0.89,
       "endingSectionProficiency": 0.495,     // BKT posterior after that session
       "startingSectionProficiency": 0,       // BKT prior before it
       "timeFinished": 1792634806}
    ],
    "proficiency": 0.495,                     // current knowledge state
    "hardestQuestionsSessionsCompleted": 0,   // separate counters per mode family
    "hardestQuestionsTotalStudyTime": 0,
    "hardestQuestionsSessionModulesStudied": 0,
    "hardestQuestionsSessionModulesCorrect": 0,
    "moduleIdsStudied": ["86b828c0-…", "86b828c7-…", "86b828c2-…", "86b828c3-…", "86b828c4-…"]
  }]
}
```

### Interpretation (BKT + forgetting curve)

- **`proficiency`** ∈ [0,1] — per-section knowledge estimate. One adaptive session
  with score 0.89 moved it 0 → **0.495** (and the same posterior was already
  client-computed in the session emit, so stats-service values are derived from the
  emitted session record — stats is a projection, not an independent model).
- **`spacing: 1`** — the interval counter the scheduler bumps after each successful
  review (classic expanding-interval SR; the classroom UI has a
  "Show Spaced Repetition recommendations" toggle that was disabled with empty state —
  recommendations activate once memories exist across sections).
- **`recentSectionEvents[]`** — the per-session (prior → posterior) transition log:
  exactly the evidence stream needed to refit a BKT/IRT model offline.
- Mode-scoped counters (`hardestQuestions*`) keep separate mastery tracks per study
  mode.

### Daily stats

`GET /api/stats?date=<ISO>&aggregationLevel=day` returned 404 with our params on the
stats host (the working daily call seen in traffic was scoped slightly differently —
query params captured live: `date=2026-10-22T01:50:57.482Z&aggre…` truncated in hook;
the `xp.app…/api/xp/me?date=` endpoint is the reliable daily-XP source:

```json
{"totalUserXp":214,"yearlyUserXp":214,"monthlyUserXp":214,"weeklyUserXp":214,
 "dailyUserXp":214,
 "userLevel":{"level":2,"currentLevelXpThreshold":200,"nextLevelXpThreshold":350}}
```

## 4. Where the recommendations come from

Classroom "For you" tab (section-overview) showed, pre-study: **New Topic
recommendations** (next sections, ~30 XP each) with toggles for Spaced Repetition /
Wrong Answers / Hardest Questions / Exam Questions recommendation sources (all
disabled until data exists). Post-study the same section now has
`sessionsCompleted: 1` — the recommendation engine reads `stats/sections` +
`memories`. (Deeper recommendation contract left for a future pass; needs multi-section
history.)

## 5. SyllabAI relevance

- **Split stores** (collectible ledger vs. learning state) is a clean separation
  SyllabAI can adopt for its own "memory palace" style motivation layer without
  polluting the BKT store.
- The **`recentSectionEvents` (prior → posterior, per session) log** is the exact
  shape SyllabAI's `bkt_mastery` evolution table should expose — it makes mastery
  auditable and re-trainable.
- **`spacing` as a first-class column** next to proficiency = minimal viable
  forgetting-curve scheduler; SyllabAI's existing `memory` model (BKT mastery +
  `next_review_at`) can be expressed in exactly this projection shape.
- The palace mechanic (2-option location choice + map micro-question + `memoryXp`
  reward) is a cheap, high-retention engagement loop worth prototyping in
  SyllabAI's XP system.
