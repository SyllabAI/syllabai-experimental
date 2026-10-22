# 2026-10-23 — exam-mate.com: paper viewers, Build Exam/Worksheet + PDF export

Target: the two feature families requested for reverse-engineering:

1. **"Build Exam or Worksheet"** (`/myexams`, `/list`) with its **export-to-PDF modes**
2. **The paper viewers** — how per-paper content is served, and how QP / Mark-Scheme
   is chosen (both the yearly past-papers viewer and the topical question viewer)

Everything below was verified empirically against the live site on 2026-10-23
with the fixed-fingerprint Chromium pipeline (`scripts/exam_mate_client.py`).
Probe artifacts: `/home/z/my-project/exam-mate-probe/` (01–33 numbered captures:
HTML, screenshots, wire-traffic JSON, sample PDFs). Probe scripts used for this
session: `scripts/exam_mate_probe_viewers_builder.py` (consolidated; committed).

Predecessor: `research/2026-10-22-exam-mate-topical-past-papers-reverse-engineering.md`
(stack fingerprint, WAF bypass, topical list/card payload — all still accurate).

## 0. Session context changes vs 2026-10-22

- Sandbox wipe #3: PAT + login session were lost; a **fresh free account** was
  registered through `/register` (plain Laravel form POST: `name`, `email`,
  `password`, `password_confirmation`, `terms`, `designation`, `timezone`).
  **Registration logs you in immediately — no e-mail verification wall.**
  "Only 2 active sessions are allowed per account" is enforced server-side;
  restored `exam_mate_session` cookies from a saved state did **not** survive
  into a new browser context — always log in inside the working context.
- Anonymous list serving on `/pastpapers` **works** (category/subject `$set`,
  filter apply, paper list). On `/topicalpastpapers` it remained blocked for
  non-default subjects (see predecessor §5.1 — still true).

## 1. Feature map (nav → routes)

| Nav entry | Route | Access |
|---|---|---|
| Yearly Past Papers (Free) | `/pastpapers` | anonymous browsing + **anonymous PDF download** |
| Topical Past Papers | `/topicalpastpapers` | anonymous (default subject), login for others |
| Smart Quiz MCQ Papers | `/mcq` | paid product |
| Online Exam Builder ("Build Exam or Worksheet") | `/myexams` | login (build+PDF export = paid package) |
| Build Question List (Free) | `/list` | login (free; PDF export gated, see §5) |
| Topical eBooks (Worksheets) | `/topicalpastpapers_books` | public shop |
| Solved Past Papers | `/solved_pastpapers` | public shop |
| AI features | `/prediction-exam`, `/revision`, `/exam-marker`, `/mockexam` | login, free |
| Question Bank / Golden Notes / Testprep | `/questionbank`, `/golden_notes`, `/testprep` | login, free |
| My Generated Pdfs | `/mypdfs` | login — landing page of every PDF export |
| Pricing: Build Exam / Extra PDF / Remove branding / Schools | `/exams/pricing`, `/extra_pdf/pricing`, `/remove_branding/pricing`, `/school/pricing` | public |

## 2. Viewer A — Yearly Past Papers (`/pastpapers`) — PDF-tab viewer

### 2.1 Livewire components

| Component | Role | `serverMemo.data` (captured) |
|---|---|---|
| `filter-box.past-papers-filter-box` | board/subject/paper/season/year/zone filters | `eventKey, categoryName, subjectName, categoryID, subjectID, chapterID, topicID, paperIDs[], years[], zoneIDs[], topicIDs[], chapterIDs[], seasons[], levelID, paperType, difficulty, isMCQ, isWorksheet, country` (same shape as topical) |
| `list.pastpapers-list` | the paper list + selection | `selectedPastPaper[], filters{categoryID, subjectID, chapterID, chapters[], topicID, topics[], year, years[], paperID, papers[], season, seasons[], zoneID, zones[], levelID, grade, isMCQ, isWorksheet}, page, paginators{page}, order, randomNumQuestions, random, seed` |
| `viewer.pastpaper-viewer` | the tabbed PDF viewer | `selectedPastPaper[], showButtons: true` |

Fingerprints use `{"id","name","locale","path","method","v":"acj"}` — same wire
protocol as the topical page (v2.12 snapshot style; POST body is FLAT:
`{fingerprint, serverMemo, updates[]}` — **not** nested under `snapshot`).

### 2.2 Interaction flow

1. Category: `wire:click="$set('categoryID', N)"` (same 21-board set as topical;
   /pastpapers list starts at CIE O-LEVEL 11, then IGCSE 3, 12, 5, 20, 4, 21, 6 …).
2. Subject: `$set('subjectID', N)` — note the subject id space **differs from
   topical** (pastpapers 11 = Accounting 9-1(0985) while topical 11 = Add Maths
   0606; Add Maths is `subjectID 11` only within category 3's own list … actually
   the same id (11) resolves to different labels per feature — treat the two
   taxonomies as independent).
3. Apply: `.filter-button` fires `$wire.filter('pastpapers', section)` —
   the button carries `x-bind:disabled="!$wire.isAuthenticated"` for anonymous
   users, but a plain JS `el.click()` bypasses the disabled state and the list
   **does** re-query anonymously (verified: full paper list of 0606).
4. Paper rows: `<li id="pid-{rowID}" wire:click="selectPastpaper({rowID})">
   <span>0606/23_Summer_2026</span></li>` under `ul#paper-list
   x-init="selectFirstPaper()"` — **first paper auto-loads**.
5. Prev/Next: `selectPreviousPaper({rowID})` / `selectNextPaper({rowID})` JS.

### 2.3 The viewer itself (the answer to "Qp/MS choosable")

`selectPastpaper` re-renders `viewer.pastpaper-viewer` with a Bootstrap tab set:

| Tab | id | Content |
|---|---|---|
| Question | `#questions-tab` (active) | `<iframe src="{QP pdf}">` + `Download PDF` button (`target="_blank"`) |
| Answer | `#answers-tab` | `<iframe src="{MS pdf}">` + `Download PDF` |
| Extra Files | `#extra-tab` | empty for most papers (no extra files observed) |

So **QP/MS choice = client-side tab switch; both PDFs are pre-loaded as
iframes**. No per-page image API: the yearly viewer is **PDF-native**, the
browser's own PDF plugin provides paging/zoom.

### 2.4 PDF URLs (freely downloadable, anonymous, with WAF clearance only)

```
/media/pastpapers/{mediaID}/{filename}.pdf
CIE:      0606_s26_qp_21.pdf / 0606_s26_ms_21.pdf      (qp 600830, ms 600831)
Edexcel:  0985-Accounting-(9-1)-June-2026-Question-Paper--22.pdf
          0985-Accounting-(9-1)-June-2026-Mark-Scheme--22.pdf  (600363/600364)
```

- `mediaID` is a **per-file id** (QP and MS are separate entries, usually
  adjacent); the paper **row id** (`selectPastpaper` argument, e.g. 48827/48595)
  is a different id space (the papers table PK).
- Downloaded anonymously through the browser context: HTTP 200, `%PDF-1.4`,
  e.g. 148 KB for 0606_s26_qp_21.pdf. No login, no subscription check — only
  the WAF clearance cookie is needed.
- Naming follows CIE's own file convention for CIE; human-readable slugs for
  publisher boards.

### 2.5 Deep links

`/pastpapers/{CategoryLabel}-{categoryID}/{SubjectLabel}-{subjectID}` (same slug
cosmetics as topical; e.g. `/pastpapers/IGCSE-3/Additional_Mathematics(0606)-11#`).

## 3. Viewer B — Topical question viewer (image-based, recap + additions)

Unchanged from the predecessor note (§3.3): the topical list embeds the full
payload per question in `selectQuestion(qid, eventKey, '{json}')` with
`question_images[]`, `answer_images[]`, `mcq_answer`, `topics`. The
`viewer.question-viewer` (`examID, questionID, eventKey, showAnswer,
showButtons`) swaps **QP images ↔ MS images** via `showAnswer` — this is the
image-based QP/MS switch. In the builder editors (§4) the SAME component is
instantiated twice (`questions-tab1/2`, `answers-tab1/2` viewer tabs).

Image URL patterns (both confirmed in editors):

```
/questions/{qfolder}/{qid}/{qfolder}_{q|a}_{qid}_{n}_{m}.png    (standard topical)
/media/questions/{qid}/{label}.png                              (Turkish YKS-TYT media scheme)
```

## 4. Build Exam or Worksheet (`/myexams`) + Build Question List (`/list`)

### 4.1 Key structural discovery: lists and exams are one model

- `POST`-less creation via Livewire modals on the respective index pages:
  `wire:click="createExam"` (`#new-exam-modal`, `wire:model="examName"`) and
  `wire:click="createList"` (`#new-list-modal`, `wire:model="listName"`,
  validated server-side — "The list name field is required.").
- Creating list #1 gave `/list/228944`; creating exam #1 gave
  `/myexams/228945` — **sequential ids, same backing table**. The export
  component inside BOTH editors is literally `components.exam.exam-export-component`.
  A "question list" is an exam row with a different flag.

### 4.2 Editor layout (`/list/{id}` ≡ `/myexams/{id}`)

Top tabs: `#add` → `#view` → `#settings` → `#export` (plus viewer tabs
`questions-tab1/2`, `answers-tab1/2`). 38 nested Livewire components on the page.

**#add** — question picker = the topical filter UI embedded
(`filter-box` clone: curriculum/subject/topic/paper/year/season/zone,
`wire:model.defer` arrays, `toggleOrder()`, `randomSelect` +
`randomNumQuestions`) and 25 rows/page, each row:

- `wire:click="toggle()"` — add/remove the question to/from the exam
  (element ids `add-q-exam` / `remove-q-exam` per row; 300-row cap shown by the
  **`SELECTED QUESTIONS {n} / 300`** badge — its own nested component).
- `$emit('questionSelected', qid, eventKey)` — opens the image viewer.

**#view** — selected questions panel (drag-order via dragula:
`/assets/libs/dragula/dragula.min.js` is loaded on the editor page).

**#settings** — the full PDF-generation contract, as `state.*` properties
(`wire:model.defer="state.X"`), grouped in cards:

| Card | Fields |
|---|---|
| Share Settings (both lists & exams) | `state.is_public` (Public), `state.share_answers` (Share Answers), share link input → **`/myexams/{id}/share`** (public share viewer; redirects to `/` while `is_public` is off) |
| Header & Footer Questions | `state.header_left`, `state.header_center`, `state.header_right`, `state.footer_left`, `state.footer_right`, `state.show_page_number`, `state.page_num_start_at`, `state.question_num_start_at` (Alpine counter, 1–999) |
| Header & Footer Answers (exam editor) | same set, separate PDF; samples `header_footer_sample.pdf` / `header_footer_a_sample.pdf` |
| Cover Settings (exam editor; `cover_settings_sample.pdf`) | `state.cover_school_name`, `cover_teacher_name`, `cover_subject`, `cover_date`, `cover_time`, `cover_duration`, `cover_total_marks`, `cover_instructions`, `logo` (Dropify upload → school logo) |
| misc | `state.show_question_details` (prints the `(0606/23_Winter_2022_Q10) — Topic` captions under each question, as seen in the samples) |

Save via `wire:click="update()"` ("Save Settings").

**#export** — `components.exam.exam-export-component`, self-refreshing with
`wire:poll.10s.visible` (polls the build table while the tab is visible —
**the tab must be active or the table never updates**). Four cards:

| Mode | wire method | Sample | Layout |
|---|---|---|---|
| **MODE 1** | `exportMode1` | `/storage/mode1_sample.pdf` | "many questions per page" (compact worksheet) |
| **MODE 2** | `exportMode2` | `/storage/mode2_sample.pdf` | "one question per page" (exam-style) |
| **ANSWERS** | `exportAnswers` | `/storage/answer_sample.pdf` | separate answer-key PDF, "many answers per page" |
| **COVER** | (export cover) | `/storage/cover_sample.pdf` | cover sheet — **marked "Free"** (no quota deduction observed in UI) |

Each button wraps a JS confirm: *"Are you sure you want to export your exam to
PDF? Doing so will deduct 1 pdf from your monthly limit."* — i.e. **export
modes 1/2/answers share one monthly PDF allowance** (they are separate
artifacts of the same deduction).

Built files land in a table (`Name of File / Status / Type / Size / Created
at / Download`) refreshed by the poll, and the account-wide library is
`/mypdfs` ("My Generated Pdfs").

### 4.3 Sample-PDF forensics (layout contract, from the actual files)

- Page header: `"{Board} {Syllabus} {Exam name}"` (e.g. "Cambridge IGCSE
  Additional Mathematics 0606 Test 10"); user-defined left/center/right
  header + footer text; page numbers with configurable start.
- Question caption line: `{n} - ({paper_ref}) - {Topic}` (driven by
  `show_question_details`).
- Fixed footer branding: `Powered By : www.exam-mate.com` (+ year range
  `2012-20…`) — this is what the paid "Remove Branding" add-on strips
  (`/remove_branding/pricing`, USD 10/mo).
- COVER: exam-mate logo header, Student Name/Number/Class/Score boxes,
  Teacher/Subject/Date/Time/Duration/Total Marks, bulleted Instructions.
- The QP/MS content is embedded as **images** (the topical PNGs) inside the
  generated PDF, not as text — the PDF is a layout wrapper around the same
  `/questions/...` images.

### 4.4 Export gating (verified live, free account)

| Tier | UI quota | Observed behaviour |
|---|---|---|
| Anonymous | — | `/myexams`, `/list`, `/mypdfs` → 302 `/login` |
| Logged-in free | `0 / 1 PDF(s) built` | `exportMode1`, `exportMode2`, `exportAnswers` all return **HTTP 500** from `components.exam.exam-export-component` (Laravel error page as effects.html) — the free-tier export path is **not functional**; the 500 (rather than a 403) suggests an unhandled null-subscription crash server-side. COVER export is advertised "Free" (not tested to completion). |
| Paid packages (`/exams/pricing`) | Parents 5 PDFs/mo USD 20/1mo·110/6·200/12·380/24; Teachers 10 PDFs/mo USD 25/130/240/450; Schools 20–30 PDFs/mo, 10–20 accounts USD 1100–2200 | "Questions Per PDF **20**" (parents/teachers) / **30** (schools) — a hard cap of questions per generated PDF |
| Extra PDF add-on | USD 1/PDF (1/3/5/10 packs) | "only applies to users who already have an active build exam package… no time limitation" |
| Remove Branding | USD 10/1mo … 120/12mo | strips the `Powered By : exam-mate` footer |

Year filters inside the editor's question picker show padlocks on recent years
(2026/2025 "Unlock" → `/topicalpastpapers/pricing`) — free accounts may only
add questions from older years.

### 4.5 Registration + session notes (for future automation)

- `/register`: plain form POST, instant auth, no email verification observed;
  designation + timezone are collected but do not gate anything tested.
- Login: `/login` POST (`email`, `password`, `remember`) → 302
  `/topicalpastpapers`. Session cookie `exam_mate_session`; 2-sessions-per-
  account limit; **do not reuse state across fresh browser contexts** —
  re-login in the working context instead (state restore passed the WAF but
  the app session was rejected).
- Livewire POST format on these pages (v2.12 flat): `{fingerprint{id,name,
  locale,path,method,v:"acj"}, serverMemo{data...}, updates[{type:
  "callMethod"|"syncInput", payload{...}}]}` — same replay rules as the topical
  crawler (`exam_mate_crawler.lw_list_call`).

## 5. What resisted (open threads)

1. **Actual PDF generation internals** — the export endpoint 500s for
   non-subscribers, so the built-file URL pattern (`/mypdfs/{id}` download
   link format, status transitions in the build table) remains unobserved.
   With any subscribed session, run `exportMode1` on a 2-question exam and
   capture: POST response effects, one poll cycle of the table, and the
   final file URL.
2. **COVER export** — advertised free; not driven to completion (expected to
   work even on free tier — worth confirming).
3. **Share view (`/myexams/{id}/share`)** with `is_public` ON — expected to
   render a read-only viewer (QP/MS tabs); unverified (needs a second
   browser context or logout to view anonymously).
4. **Extra Files tab** — empty for all sampled papers; unknown which papers
   ship extra files (inserts/formula sheets?) and their URL pattern.
5. `/solved_pastpapers` viewer — shop page only; per-paper solved viewer not
   probed.
6. The wire `updates[].type` observed on /pastpapers was `callMethod` only;
   checkbox `syncInput` batches (`paperIDs[]` etc.) were not captured — low
   risk (same pattern as topical), but confirm before scripting filters.

## 6. Reproduction pointers

- Consolidated probe script (viewers + builder + export, this session):
  `scripts/exam_mate_probe_viewers_builder.py`
- Client + WAF bypass: `scripts/exam_mate_client.py`; crawler patterns:
  `scripts/exam_mate_crawler.py`
- Probe artifacts (local working dir, not committed): `~/exam-mate-probe/`
  — `01_home.*` … `33_*`: page HTMLs, screenshots, `06_pp_wire_traffic.json`,
  `28/29_export_wire.json`, `mode1/mode2/answer/cover_sample.pdf`,
  `qp_test.pdf` (anonymous download proof).
- Research account: `~/exam-mate-probe/research_account.json` (throwaway,
  disposable inbox, no purchases; 0600, never commit).
