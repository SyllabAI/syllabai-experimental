# 2026-10-23 (c) — AI Marker Gem: full instructions extracted; persona spec + gap analysis

Status: **Gemini-side extraction COMPLETE** (manual fallback; ChatGPT side
pending). Companion to `2026-10-23-exam-mate-ai-features.md` §4 and
`2026-10-23-exam-mate-ai-persona-internals.md` (runbook + ToS caution).

## 0. TL;DR

The operator opened the AI Marker Gem share link with a personal Google
account and ran the three-prompt battery from the runbook. The first
prompt — the classic recitation leak — made the Gem print its **complete
instructions** into a code block. Findings at a glance:

- exam-mate's entire "AI Exam Marker" product is **one hand-written
  conversational prompt** (~700 words) inside a Google Gemini Custom Gem.
- **Zero knowledge files** (explicit self-report), zero retrieval, zero
  board data — the final confirmation of the zero-AI-infrastructure
  finding, now at prompt level rather than inferred from wiring.
- The marketed 6-step contract is implemented *literally* as chat
  choreography with hard gates between uploads.
- Biggest spec gap: the report template requires an "**Estimated Grade**"
  but no grade boundaries exist anywhere in the prompt — the Gem must
  improvise a percentage heuristic, with nothing keeping it consistent
  across students in the class table.
- Topic-level analytics ("Weak Topics", "Topic Performance") have no
  syllabus grounding at all — free LLM association.

Raw transcripts are held **privately** (`exam-mate-probe/persona/gemini/`)
per the ToS caution in the persona-internals note §5 (this repo is public
— no verbatim prompt text is committed here). This note publishes the
structural spec.

## 1. Provenance, method, handling

| Field | Value |
|---|---|
| Persona | "AI Marker" — Custom Gem |
| Share id | `1pbFQkuKQifVUtkF-YSgdvq2xp4Ow96Ye` |
| exam-mate landing | `/exam-marker` |
| Date / route | 2026-10-23, manual fallback: personal Google account → share link → "Start chat" |
| Battery | (1) recitation leak → full instructions; (2) knowledge-files probe → "no files"; (3) workflow self-description (`flow_marker`) |
| Artifacts (local-only) | `exam-mate-probe/persona/gemini/chat_ai-marker.json`, `ai_marker_meta.json`, `ai_marker_instructions_recitation.txt` |

Caveats: the turn-1 text is a **model recitation**, not the author's
source file — treat as high-fidelity (≥95%) but expect minor drift in
wording/order; turn-3 list markers were flattened by copying from the
rendered chat UI; only whitespace was normalized. Quotation in this note
is limited to short functional excerpts for research commentary.

## 2. Confirmation scorecard (claims from main note §4, now settled)

| Claim (from landing-page reverse engineering) | Verdict after extraction |
|---|---|
| Single generic, board-agnostic marker persona | ✅ confirmed — prompt contains no board/subject/qualification specifics |
| 6-step contract (name exam → QP PDF → MS PDF → per-student PDFs → reports → class analysis) | ✅ confirmed literally — hard conversational gates |
| Filename = student name drives report identity | ✅ confirmed ("use the filename as the Student Name" + a restriction bullet) |
| Marks strictly from QP-printed values, none invented | ✅ confirmed — dedicated 6-rule "SCORING RULES" block with anti-invention wording and a worked example |
| "Works exclusively from these documents, no external sources" | ✅ confirmed — grounding line + restrictions section both say uploaded PDFs only |
| "Estimated grade" output | ⚠️ refined — it is an estimate with **no boundaries input**; the heuristic is unspecified |
| Zero AI infrastructure (previously inferred from wiring) | ✅ confirmed at prompt level — and strengthened: no knowledge files either |

## 3. The persona as a state machine

The prompt is essentially a finite-state conversation script:

| State | Behaviour | Advance condition |
|---|---|---|
| S0 | Greeting + "may I know your name" | teacher's name received |
| S1 | "What would you like to name this exam?" | exam name received |
| S2 | Request **Exam Questions PDF** ("must be a PDF file and clearly named") | QP uploaded — hard gate ("Do NOT continue until…") |
| S3 | Request **Official Mark Scheme PDF** | MS uploaded — hard gate |
| S4 | Request **ALL student answer sheets at once**; one PDF per student; filename = student full name; batch uploads allowed | all student PDFs received |
| S5 | Mark each student (per-student loop) | every PDF processed |
| S6 | Final class analysis + fixed closing line | — |

This choreography is the strongest part of the prompt: deterministic,
idiot-proof, and it matches the marketing copy exactly. Everything after
the gates is conventional.

## 4. Scoring contract

- **Sole mark source**: the "(N marks)" strings printed at the end of each
  question/part *in the Question Paper*. Total = their sum. Explicit
  anti-invention rule ("MUST NOT guess marks or create its own mark
  distribution") plus a worked example (Q1(a) 2 + Q1(b) 3 → Q1 = 5).
- **MS role** (from the workflow self-description): official answers,
  "acceptable alternatives", method-mark allocations, and penalty
  criteria.
- Method marks "where applicable"; deductions strictly within the printed
  per-question ceiling; every score explanation must reference the printed
  value.
- Answers may be "handwritten or typed" — the Gem relies entirely on
  Gemini's native PDF vision; there is no OCR-failure protocol.
- **Not specified anywhere**: optional/alternative questions (e.g. CIE
  "choose 2 of 3" parts), multi-component papers, and — critically — any
  fallback when the QP does not print per-part marks (some boards put
  totals only in the MS; the contract would then have nothing to sum).

## 5. Output templates

Student report (fixed skeleton baked into the prompt): banner (exam name,
student, X/Y, percentage, estimated grade) → Performance Summary →
Question-by-Question Marking (per-part bullets with ✔️/✖️) → Mistakes &
Misconceptions → Why Marks Were Lost → Improvement Suggestions → Weak
Topics → Recommended Practice (optional).

Class report: banner → Class Overview → Student Summary Table (Student |
Marks | Percentage | Grade | Rank) → Ranking → Question Difficulty
Analysis → Topic Performance → Common Mistakes → Class Statistics
(high/low/mean/median) → fixed closing line.

Both templates are emoji-heavy markdown. A large fraction of the prompt's
token budget is spent on formatting directives ("BEAUTIFUL, CLEAN,
HIGH-QUALITY", "modern typography and GPT-style formatting") rather than
marking accuracy. In their design the *formatting* is the product
differentiator; accuracy is delegated to the model plus the uploaded MS.

## 6. Authorship fingerprints

Consistent with the batch-production timeline already established from
g-id prefixes (predictions Nov–Dec 2025, revisions Jan 2026):

- The phrase "GPT-style formatting" inside a **Gemini** prompt — likely
  ported from a ChatGPT draft.
- Inconsistent step numbering (CONVERSATION START → STEP 1 = MS receipt →
  STEP 2 = student uploads → STEP 3 = marking; the "SCORING RULES" block
  lists six numbered rules under an unnumbered header).
- Zero knowledge files even though the sibling revision GPTs advertise a
  "full official topic list" — the marker was the cheapest persona to
  produce: no per-subject work at all.
- No few-shot examples, no calibration instructions, no self-check pass.

## 7. Gap analysis → SyllabAI marker deltas (feeds option (b))

1. **Grades without boundaries.** The estimated grade has no boundaries
   input, and nothing enforces consistency across students in the class
   table. *Delta*: inject real per-board/per-session threshold tables (we
   hold the data); print the boundary row next to each grade.
2. **Topic-less analytics.** "Weak Topics" / "Topic Performance" are LLM
   free association. *Delta*: pre-tag every question with syllabus
   reference codes from our 186.8k-image corpus so topic aggregates are
   grounded and comparable across exams.
3. **QP-first mark extraction is brittle.** *Delta*: MS-first allocation
   with QP cross-check and an explicit reconciliation warning when they
   disagree.
4. **No evidence linkage.** Awards are not required to cite the matched
   MS point. *Delta*: evidence-linked marking — quote the MS line per
   award — for auditability and hallucination resistance.
5. **No illegibility/confidence protocol.** *Delta*: per-question
   confidence plus a "flag for human review" queue.
6. **Chat-only delivery.** No export; teachers copy-paste. *Delta*: JSON
   schema + CSV/PDF export — also our integration wedge for LMSs.
7. **No optional-question logic** (CIE alternative routes, best-of
   selections).
8. **No few-shot calibration** per question type; extended-response
   subjects get generic method marks only.
9. **Filename-only identity.** No student-ID sanity checks, no duplicate
   or collusion detection.
10. **Token hygiene.** Emoji/formatting directives crowd out accuracy
    instructions (double-mark sampling, self-verification).

## 8. Remaining backlog

- **ChatGPT side (47 GPTs)**: same three-prompt battery from the runbook;
  the recitation leak is the opening shot there too. If a GPT refuses,
  fall back to landing metadata + the flow prompts — refusal patterns are
  themselves data. Harness: `scripts/exam_mate_probe_gpt_chat.py` (must
  run from the operator's own machine; the sandbox IP is
  Cloudflare-blocked by chatgpt.com).
- After extraction: consolidate a persona-spec book (per-subject prompt
  structures, topic-list organization) → then option (b): a SyllabAI
  prediction/revision/marker spec built on our corpus grounding.
