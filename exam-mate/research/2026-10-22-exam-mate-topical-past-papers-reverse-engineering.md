# 2026-10-22 — exam-mate.com TOPICAL PAST PAPERS: full reverse-engineering

Target: `https://www.exam-mate.com/` — the TOPICAL PAST PAPERS feature
(navigation id 1, route `/topicalpastpapers`).
Everything below was verified empirically against the live site on 2026-10-22
(scripts in `scripts/exam_mate_*.py`, probe artifacts under `exam-mate-probe/`).

## 1. Stack fingerprint

| Layer | Finding |
|---|---|
| Backend | Laravel (cookies `XSRF-TOKEN` + `exam_mate_session`, `/livewire/*` endpoints) |
| Frontend | Livewire **v2** (protocol marker `"v": "acj"` in every component fingerprint) + Alpine.js + Turbolinks-flavoured boot (`window.livewire_token`, `deferLoadingAlpine`) |
| CSRF | Not a meta tag — `window.livewire_token = '...'` inline boot script |
| Web server | Apache (HTTP/2), `cf-edge-cache: no-cache` header (some CDN in play, but challenge is app-origin) |
| Analytics | Pirsch (`api.pirsch.io/hit`, 403 from datacenter IPs — ignore) |
| Static assets | `/storage/...` (logos), question images under `/questions/{folder}/{qid}/` |
| Livewire components on the topical page | `new-exam-modal`, `new-question-list-modal`, `filter-box.topical-filter-box`, `list.questions-list`, `viewer.question-viewer` |

## 2. The WAF ("One moment, please...") — fully decoded

Every HTML **and asset** request from a non-clearanced client gets an
interstitial challenge page (~7 KB) titled "One moment, please...".

Mechanism (deobfuscated from the served obfuscated JS):

1. The page runs 7 fingerprint checks against a registry object:

```js
{
  webdriverCheck:        'webdriver' in window || !!navigator.webdriver,
  userAgentCheck:        /headless|bytespider/i.test(navigator.userAgent),
  appVersionCheck:       /headless/i.test(navigator.appVersion),
  pluginArraySpoofing:   PluginArray.prototype !== navigator.plugins.__proto__ (and per-plugin proto check),
  mimeTypeArraySpoofing: MimeTypeArray.prototype !== navigator.mimeTypes.__proto__,
  noLanguage:            !navigator.language || navigator.languages.length === 0,
  zeroOuterDimensions:   window.outerHeight === 0 && window.outerWidth === 0,
}
```

2. **If any check fails** → XHR `GET /z0f76a1d14fd21a8fb5fd0d03e0fdc3d3cedae52f
   ?id=a6105c0a611b41b08f1209506350279e&ts=<page-ts>&wsidchk=<n>&pdata=<enc>&cttl=0
   &failedChecks=<name,...>` → server answers **404 empty** → page reloads after
   5 s → loop forever. (This is the headless-browser death loop.)
   Note the *different* hex id (`a6105c0a61…`) on the failure branch — the two
   ids distinguish flagged vs clean submissions server-side.
3. **If all checks pass** → a hidden form is built and GET-submitted to the same
   `/z0f76…` endpoint with `wsidchk` (a JSFuck-style per-page constant pair
   summed to one number), `id` = `7fa3b767c460b54a2be4d49030b349c7`, `ts` = fresh
   per-page timestamp, `pdata` = `https%3A%2F%2Fwww.exam-mate.com`, `cttl=0`.
   Server answers **302 → / ** and sets the clearance cookie.

Clearance cookie: **`wssplashchk`** (host `.www.exam-mate.com`, ~1 h expiry).
With it, plain `curl` fetches HTML fine. Two practical caveats:

- The WAF also fingerprints **TLS/HTTP headers on XHR POSTs**: python-requests
  with a valid cookie still got splashed on Livewire POSTs. Browser-context
  requests (`page.evaluate fetch` / Playwright `context.request`) pass.
- The clearance is re-checked periodically; a fixed-fingerprint Chromium gets
  re-cleared automatically (the challenge self-solves in ~3–5 s).

Bypass recipe (implemented in `exam_mate_client.py`): launch Chromium with
`--disable-blink-features=AutomationControlled`, real-Chrome UA (no
"Headless"), and init-script patches `navigator.webdriver → undefined`,
`window.outerWidth/outerHeight → non-zero`. **Do not** spoof
`navigator.plugins` with a plain array — the prototype-identity check catches
that (cost us one debugging cycle).

## 3. Feature architecture (how TOPICAL PAST PAPERS works)

Route: `/topicalpastpapers` (default state = CIE IGCSE / Additional
Mathematics 0606).

### 3.1 State model (Livewire)

`filter-box.topical-filter-box` public properties:

```
eventKey, categoryName ("IGCSE"), subjectName ("Additional Mathematics(0606)"),
categoryID, subjectID, chapterID, topicID,
paperIDs[], years[], zoneIDs[], topicIDs[], chapterIDs[], seasons[],
levelID, paperType, difficulty, isMCQ, isWorksheet, country
```

`list.questions-list`:

```
examID, eventKey, filters{categoryID, subjectID, topics[], papers[], years[],
zones[], seasons[], levelID}, page, paginators{page}, order (DESC),
randomNumQuestions (20), + a mirror of the filter properties
```

`viewer.question-viewer`: `examID, questionID, eventKey, showAnswer, showButtons`.

### 3.2 Interaction graph

- Boards: 21 categories via `wire:click="$set('categoryID', N)"`.
  Full harvested map (id → label): 56 MYP1, 57 MYP2, 58 MYP3, 59 MYP 4,5,
  7 DIPLOMA (IB), 3 CIE IGCSE, 12 CIE O-LEVEL, 5 CIE A-LEVEL, 4 Edexcel IGCSE,
  21 Edexcel IGCSE (9-1), 6 Edexcel A-LEVEL, 14 OCR GCSE (9-1), 19 OCR AS,
  16 OCR A-LEVEL, 15 AQA GCSE, 18 AQA AS, 17 AQA A-LEVEL, 53 TYT (YKS),
  54 AYT (YKS), 55 YDT (YKS), 13 SPM.
- Subjects: `$set('subjectID', N)` — the filter-box re-renders (full HTML
  response, ~40 KB) with the subject's **topic list, zones, papers, seasons,
  years**. Clicking the *already-default* subject returns a 223-byte
  no-op response (html:null + `subjectChanged` dispatch) — that asymmetry
  confused two earlier probes.
- The filter-box render embeds `x-init="$dispatch('filterResults')"`; the
  questions-list declares `listeners: ["filterResults", "examQuestionsUpdated"]`.
- Applying filters: a button inside the filter-box with
  `x-on:click="$wire.filter(window.location.pathname.split('/')[1], $wire.section ?? '')"`
  (class `filter-button filterBtn`). Checkbox filters are
  `wire:model.defer` (topics[], zones[], years[], papers[], seasons[]) —
  deferred until the apply button fires `$wire.filter(...)`.
- Pagination: `wire:click="gotoPage(N)"` / `nextPage` / `toggleOrder` /
  `randomSelect` on `list.questions-list` (25 questions per page, hard cap
  observed 200 pages; the Random panel caps `randomNumQuestions` at 75).

### 3.3 The gold: question cards carry their full payload

Every question row (`li#qid-<id>-<eventKey>`) embeds a complete JSON payload in
its `onclick` attribute:

```js
selectQuestion(60043,1,'{"question_images":["https://www.exam-mate.com/questions/21400/61890/21400_q_61890_10_1.png",
 "https://.../21400_q_61890_10_2.png"],
 "answer_images":["https://.../21400_a_61890_10_1.png"],
 "mcq_answer":"A","question_text":"","answer_text":"","topics":"Functions, Modolus"}')
```

So one paginated list response yields 25 complete question records — no
per-question fetches needed. Image URL pattern:
`/questions/{qfolder}/{qid}/{qfolder}_{q|a}_{qid}_{n}_{m}.png`.

### 3.4 URL scheme (deep links)

The filter-box emits `rewrite-url` with the canonical URL:

```
/topicalpastpapers/{CategoryLabel}-{categoryID}/{SubjectLabel}-{subjectID}
e.g. /topicalpastpapers/IGCSE-3/Additional_Mathematics(0606)-11
```

The label slugs are cosmetic (spaces → underscores; wrong labels work) —
the numeric ids drive the state. **Caveat:** a deep-link page renders the
filter-box perfectly but seeds `list.questions-list` with
`filters.subjectID` as a **string** (`"201"`) and the list renders
**0 questions** — a server-side type seeding bug we confirmed repeatedly.
The default route (`/topicalpastpapers`, no params) seeds ints and works.

## 4. The gating model (what is free, what is metered)

- Structural navigation (category `$set`, subject `$set`, deep-link loads) —
  **free**, no observed limits. This is how the full taxonomy was harvested.
- Serving the question list (`list.questions-list` renders, pagination,
  filter/apply) — **metered per Laravel session**. When the allowance is spent,
  every list call returns HTTP **403**:

```json
{"validation":{},"error":["Your request has been denied. You might have hit
the request limit or don't have an active subscription."]}
```

- One fresh anonymous session comfortably served the **full 1,333-question
  list** of Add Mathematics 0606 (54 pages) plus overhead before the wall.
- The UI copy confirms the monetization: "Not Subscribed — Questions are not
  downloadable" (question images are viewable but gated for bulk export).
- Direct `$set('subjectID', N)` on the list component (skipping the filter-box)
  → HTTP 500. There is no clean public path to force a non-default subject's
  list from an anonymous session — subject switching beyond the default did
  not yield list reloads through clicks, apply, manual `filterResults`
  dispatches, session reloads, or deep-links (see §5).

## 5. What resisted (open threads, honestly documented)

1. **Non-default subject list reload.** After `$set('subjectID')`, the
   filter-box re-renders but the questions-list does not re-query (its POST
   never fires; the `filterResults` x-init dispatch did not reach it in our
   environment). The apply button then re-renders the list with 0 rows
   (filters arrive as strings from the deep-link path or the list keeps stale
   state). A subscription login is the likely intended path; all anonymous
   avenues were exhausted.
   **UPDATE (same day, logged-in session):** with any authenticated account
   (verified against an account whose subscription status shows "You are
   not subscribed"), both the **apply button** after a subject switch AND
   **deep-link navigation** serve the non-default subject's list correctly —
   badge, rows and pagination all live (Edexcel IGCSE 4CH1: 40 questions;
   4CH0: 419; CIE 0620: 6,398). The blocker is therefore anonymous-session
   -specific, and **active subscription is NOT required for list serving** —
   the "not subscribed" gate only blocks worksheet/export features and the
   MCQ Papers product. Login route: `/login` (plain Laravel form POST,
   `email`/`password`/`remember`; authenticated session = `exam_mate_session`
   cookie, reuse via client state restore).
2. **Livewire replay chaining** works (request `serverMemo` → response
   `serverMemo`), but chained `gotoPage` occasionally 500s when the chained
   memo goes stale after a WAF re-clearance; the DOM `nextPage` walk is the
   robust fallback and was used for the full 54-page harvest.
3. `wssplashchk` lifetime is ~1 h but re-challenges can appear earlier on
   asset fetches; the client heals by re-loading any page (auto-solve).

## 6. Reproduction pointers

- Client + WAF bypass: `scripts/exam_mate_client.py`
- Challenge solver (Node shim, for the record): `scripts/exam_mate_solve.js`
- Catalog + questions crawler: `scripts/exam_mate_crawler.py`
- Taxonomy harvester (all subjects): `scripts/exam_mate_taxonomy.py`
- Probe artifacts (challenge HTML, wire captures, protocol dumps):
  `/home/z/my-project/exam-mate-probe/` (working dir, not committed in full)
