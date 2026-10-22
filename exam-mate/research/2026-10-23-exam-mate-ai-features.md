# 2026-10-23 — exam-mate.com "exam-mate AI" features: how they actually work

Targets (from the nav's "exam-mate AI" group, all labelled Free):

1. **AI Exam Prediction** — `/prediction-exam`
2. **AI Revision Assistant** — `/revision`
3. **AI Exam Marker** — `/exam-marker`
(+ sibling `/mockexam` for disambiguation — it is **not** AI, see §4.)

Probe: `scripts/exam_mate_probe_ai.py` (modes `recon` / `interact` / `sweep` /
`gem`), artifacts `~/exam-mate-probe/4x_*` `5x_*` `6_*` `ai_gpt_catalog.json`
(local only). Committed catalog copy:
`research/2026-10-23-ai-gpt-catalog.json`.

## 0. Executive finding

**There is no AI infrastructure on exam-mate's side.** All three "AI" features
are landing pages that funnel the visitor into *consumer chatbot personas*
hosted by third parties:

| Feature | Actual backend | Where the persona lives |
|---|---|---|
| AI Exam Prediction | **ChatGPT custom GPTs**, one per subject | `chatgpt.com/g/g-…` (31 GPTs) |
| AI Revision Assistant | **ChatGPT custom GPTs**, one per subject | `chatgpt.com/g/g-…` (16 GPTs) |
| AI Exam Marker | **Google Gemini Gem** (a single generic one) | `gemini.google.com/gem/1pbFQkuKQifVUtkF-YSgdvq2xp4Ow96Ye` |

- exam-mate never proxies an AI request: zero XHR/fetch to any AI API from
  these pages (wire capture shows only the two Livewire `$set` round-trips per
  selection); the only third-party script on the landing pages is pirsch.io
  analytics.
- Using any of the three requires the *visitor's own* consumer AI account
  (ChatGPT / Google). "Free for limited time" badges on exam-mate's pages
  cost exam-mate nothing per use — the compute is OpenAI's/Google's.
- The landing pages themselves are **fully public** (no login, no WAF-gated
  content beyond the usual clearance): subject → GPT-URL resolution happens
  anonymously.

## 1. Common landing-page mechanism (prediction & revision)

Both pages share one pattern; only the component name differs
(`filter-box.prediction-exam` vs `filter-box.revision`):

1. Page renders a card: "Curriculum: Select Category / Subject: Select
   Subject / **Lets GO!**" — the GO anchor is `class="btn btn-primary w-100
   disabled" href="#"` until a subject is chosen.
2. Board click → Livewire `callMethod $set ['categoryID', N]`; subject click →
   `callMethod $set ['subjectID', M]` (v2.12 flat protocol, 200 OK each).
3. After the subject `$set` round-trip the server **re-renders the anchor with
   the real href** — the subject→GPT mapping lives server-side (a DB table),
   never shipped to the client. GO then has `href="https://chatgpt.com/g/g-…"
   target="_blank"` and the disabled class drops.
4. Subject rows are pre-rendered in the page DOM for all categories (88 rows
   on IGCSE etc., hidden by the closed dropdown); `el.click()` works even
   while the dropdown is closed.

Subject id space: the AI pages carry their own taxonomy (`3:11` = Additional
Maths 0606, `21:613` = Edexcel Biology 4BI1, `7:542` = IB Math AA …) —
independent of /pastpapers and /topicalpastpapers id spaces (third taxonomy).
133 (categoryID, subjectID) pairs enumerated in total.

## 2. AI Exam Prediction (`/prediction-exam`)

### 2.1 Flow (page's own 7-step description, condensed)

Configure paper type → AI generates exam-style questions shown in one view
(no answers/hints) → student uploads each answer as photos/scans per question
number (re-upload allowed, latest wins) → "Finish" locks the exam → AI marks
with worked solutions, step-by-step reasoning, mark allocation, examiner-style
comments → performance report (score, predicted level, strengths/weaknesses,
targeted revision plan).

### 2.2 Coverage — 31 per-subject GPTs (of 133 subjects)

| Board (category) | GPTs | Subjects |
|---|---|---|
| CIE IGCSE (`3`) | 11 | 0606 AddMaths, 0610 Bio, 0620 Chem*, 0455 Econ, 0470 Hist*, 0580 Maths, 0607 IntlMaths, 0625 Phys, 0970/0971/0972 9-1 sciences |
| CIE A-LEVEL (`5`) | 8 | 9700, 9701, 9702, 9708, 9709 Pure1 / Pure2-3 / Mech, 9231 |
| Edexcel IGCSE 9-1 (`21`) | 4 | 4BI1, 4CH1, 4MA1, 4PM1 |
| OCR GCSE 9-1 (`14`) | 7 | J247/J248/J249/J250 science A/B, J560 Maths |
| IB (`7`) | 1 | Math AA |
| AQA GCSE/AS/A (`15/18/17`), OCR A-LEVEL (`16`), SPM (`13`) | 0 | GO stays `disabled href="#"` |

\* two cross-wiring bugs, see §5.

### 2.3 GPT URL anatomy

```
https://chatgpt.com/g/{g-id}-{slug}
slug = [board-]level-subject(code)-exam-prediction-ai   e.g.
  igcse-additional-maths-0606-exam-prediction-ai
  edexcel-igcse-biology-9-1-4bi1-ai-exam
  ocr-gcse-9-1-math-j560-ai-prediction-exam
  a-level-pure-maths1-9709-exam-prediction-ai
  ib-math-aa-exam-prediction-ai
```

The first 8 hex of the g-id ≈ creation epoch: `0x6918…`≈late-Nov 2025,
`0x6957-6969…`≈Dec 2025 — the prediction GPTs were batch-created across a
~6-week window, i.e. hand-made personas, not generated.

## 3. AI Revision Assistant (`/revision`)

Same landing mechanism (`filter-box.revision`). The page's 6-step pitch: pick
curriculum+subject → GO opens "your dedicated AI Revision Assistant in a new
tab" → it asks your name, then shows the full official topic list (theory /
research methods / evaluation / exam-style questions / A* killers) →
examiner-standard revision (key points, definitions, keywords, common
mistakes, command-term training) → modes (full topic revision, exam-style
Qs, hard/A* questions, timed pressure mode, printable mock exams) → session
summary + weak areas + next-step guidance.

**Coverage — 16 GPTs**, a *different* board mix than prediction:

| Board | GPTs | Subjects |
|---|---|---|
| Edexcel IGCSE 9-1 (`21`) | 6 | 4BI1, 4CH1, 4MA1, 4MB1, 4PH1, 4PM1 |
| IB Diploma (`7`) | 10 | Bio/Phys/Chem (2025 syllabus), Math AA/AI, Econ, Psych, Global Politics, Philosophy, World Religions |

Slug convention: `exam-mate-{board}-{subject}-revision` (e.g.
`exam-mate-ib-diploma-biology-revision`). g-ids `0x696f…` ≈ mid-Jan 2026 —
a second, later batch than the predictions.

## 4. AI Exam Marker (`/exam-marker`) — the Gemini Gem

No subject filter at all: a single generic marker. "Lets GO!" is a **static
anchor** (not disabled, no Livewire needed):

```
https://gemini.google.com/gem/1pbFQkuKQifVUtkF-YSgdvq2xp4Ow96Ye?usp=sharing
```

Anonymous fetch → 302 to `gemini.google.com/app?usp=sharing` (generic app
page): the Gem's instructions/chat need a Google account, so the persona
prompt itself is not observable without one (open thread §6.1). The page's
own 6-step workflow is explicit about the contract:

1. Start a marking session, name the exam.
2. Upload **Exam Questions PDF** + **Official Mark Scheme PDF** ("works
   exclusively from these documents, no external sources").
3. Upload student answer sheets — **one PDF per student, filename = student
   full name** (drives report labelling).
4. Per student the AI: extracts answers, compares with the MS, awards marks
   strictly per the marks printed on the question paper, applies method
   marks, flags errors/misconceptions; "No marks are invented, adjusted, or
   estimated."
5. Per-student report: total/percentage/estimated grade, question-by-question
   breakdown, explanations for lost marks, misconceptions, improvement
   actions.
6. Final **class analysis**: rankings, high/low/mean/median, question
   difficulty, topic-level performance, class-wide common mistakes.

`/mockexam` disambiguation: same nav region but human service — "Our
qualified teachers will grade your exam", an APPLY NOW form, no AI.

## 5. Data-quality observations in exam-mate's own wiring

- `3:24` **History(0470)** resolves to the Biology 9-1 (0970) prediction GPT
  (`g-69576e03d3a48191b1c73b2096d2654d`, slug `igcse-biology-9-1-0970-…`) —
  copy-paste duplication in their mapping table.
- `3:16` **Chemistry(0620)** "prediction" href slug is
  `exam-mate-igcse-chemistry-revision` — a *revision* GPT cross-linked into
  the prediction column.
- `21:616` Physics 4PH1 has a revision GPT but no prediction GPT (asymmetric
  coverage).
- Take-away: the mapping table is maintained by hand and lightly QA'd.

## 6. Open threads

1. **Persona internals** — the actual system prompts / knowledge files of the
   GPTs and the Gem require a personal ChatGPT / Google account to open
   (sandbox IPs are Cloudflare-blocked by chatgpt.com and Gem share links
   need sign-in). If ever obtained, the likely content: a marking-rubric
   prompt + per-subject syllabus/topic-list uploads (their "official topic
   list" claim).
2. Whether GPTs are updated per exam session (the "prediction" framing
   implies season-specific knowledge) — observable only by chatting.
3. Any analytics tying GO clicks to accounts (pirsch is the only tracker; no
   exam-mate-side endpoint is called at GO — the anchor is a plain
   target="_blank" link, so no click attribution server-side beyond page
   views).

## 7. Reproduction pointers

- `python3 -u exam_mate_probe_ai.py recon` — anonymous+auth dumps of all four
  routes (`4x_*.html/.png/.dom.json/.wire.json`).
- `… interact` — category+subject click-through showing GO href materialize
  (`5x_*`).
- `… sweep prediction|revision` — full 133-subject walk, checkpoints into
  `ai_gpt_catalog.json` after every subject (safe to interrupt/resume).
- `… gem` — Gem/GPT landing attempts (`6_*.html/.json`).
- Client fix this session: `exam_mate_client._log_xhr` now tolerates binary
  POST bodies (chatgpt.com firehose requests crashed the response listener).
- Wire replay pattern (same as predecessor note §4.5): flat v2.12 body
  `{fingerprint, serverMemo, updates:[{type:"callMethod", payload:{method:
  "$set", params:["subjectID", 11]}}]}` against
  `/livewire/message/filter-box.prediction-exam`.

## 8. Implications for SyllabAI

- The moat is **prompt + syllabus-knowledge packaging per subject**, not AI
  infra; every artifact here (per-subject persona, QP/MS-driven marking
  contract, class analytics spec) is directly implementable on our own stack
  — and our 186.8k-image QP/MS corpus is far richer grounding than what a
  hand-typed GPT knowledge file holds.
- The per-subject GPT id space (31+16 URLs) is a ready-made feature-coverage
  checklist of which board/subject combos exam-mate considers commercially
  interesting (CIE/Edexcel/OCR GCSE + IB).
