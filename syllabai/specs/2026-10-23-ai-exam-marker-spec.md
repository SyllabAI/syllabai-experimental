# SyllabAI AI Exam Marker — product & engineering spec (draft v0.1)

| | |
|---|---|
| Status | DRAFT v0.1 — operator review; not yet an ADR |
| Date | 2026-10-23 |
| Origin | Option (b) of the exam-mate AI arc: build our own marker, informed by the competitor's behavioral contract and our 10-point gap analysis |
| Companions | `exam-mate/research/2026-10-23-ai-marker-gem-spec.md` (extracted contract + gaps) · `2026-10-23-exam-mate-ai-features.md` · `2026-10-23-exam-mate-ai-persona-internals.md` |

**Clean-room note.** This spec is derived from *behavioral* analysis of a
competitor product (public landing copy, observed chat choreography, a
self-described workflow) and from our own corpus realities. It contains no
third-party prompt text, and the product must never ship any: our
architecture differs categorically (structured pipeline vs free-form
chat), so there is nothing to copy even if we wanted to. The reusable
asset is behavioral insight — what to promise teachers, where thin
wrappers break — and that is what this spec encodes.

## 0. Summary and design goals

### 0.1 The product in one paragraph

SyllabAI AI Exam Marker ingests a question paper PDF, its official mark
scheme PDF, and one PDF per student script. It first compiles a
structured, **teacher-confirmed marking contract**: a question tree with
mark allocations reconciled between QP and MS, criterion rows normalized
to the board's mark-type vocabulary, routing rules for optional
questions, and syllabus topic tags for every question. It then marks
every script **criterion-by-criterion, with evidence quotes taken from
both the mark scheme and the student's answer**, attaches a per-mark
confidence, and routes anything uncertain to a human review queue. It
finally produces per-student reports, class analytics computed in
deterministic code, and machine-readable exports. A grade appears only
when a provenance-tracked grade-boundary table is available — the system
never invents a grade, never invents a mark, and never emits an award it
cannot show evidence for. The LLM does reading and judgement; all
arithmetic, aggregation and formatting happen in ordinary code.

### 0.2 The baseline we must beat

Behavioral summary of the competitor marker (see companion notes for the
full evidence), and where this spec takes the opposite side:

| Competitor behavior (observed) | Consequence for teachers | SyllabAI answer |
|---|---|---|
| Single generic persona; no subject knowledge anywhere in the product | Generic feedback; zero syllabus awareness | Per-syllabus topic tagging grounded in our 186.8k-image corpus and `subject_taxonomy.json` |
| Requires an "Estimated Grade" with no boundary data of any kind | Grades are whistles; can disagree across a class | Grade rendered only from a provenance-tracked boundary table; otherwise an explicit empty state |
| Reads marks only from QP-printed "(N marks)" strings | Silently breaks wherever totals live only in the MS | MS-first allocation, QP cross-check, reconciliation warnings surfaced to the teacher |
| Awards without any evidence linkage | Teacher cannot audit why a mark was given or lost | Every award cites a criterion row plus quoted MS and student evidence |
| "Weak Topics" by LLM free association | Topic feedback not comparable across exams | Topics are syllabus reference codes; aggregates computed in code |
| Chat-only delivery; reports are copy-paste markdown | No records, no exports, no integration | JSON / CSV / PDF exports from day one; reports rendered from stored data |
| No confidence or failure protocol | Illegible answers get confident nonsense | Per-mark confidence; review queue; flagged items never silently scored |
| Rigid conversational hard gates | Chatty, sequential, no bulk control | Forms, tables and queues; bulk operations; chat optional later and never load-bearing |

### 0.3 Design goals

- **G1 — Evidence-linked marking.** Every awarded mark cites the matched
  criterion row and quotes the student's evidence. An award without
  evidence is a bug, not a style choice.
- **G2 — Grounded analytics.** Topic-level findings come from syllabus
  reference codes attached to questions, and every numeric aggregate is
  computed in code from stored mark records.
- **G3 — Honest grading.** Grades exist only with boundary provenance.
  Absence of data is shown as absence, never improvised.
- **G4 — Teacher in command.** The teacher confirms the compiled
  structure, adjudicates the review queue, and can override any mark with
  a recorded reason. The product's stance is "AI-assisted marking,
  teacher-confirmed".
- **G5 — Model-agnostic core.** All model access goes through one adapter
  interface; prompts and schemas are versioned in the repo and gated by
  the evaluation suite (§8).
- **G6 — Export-first.** JSON dump, CSV gradebook and PDF reports are
  first-class outputs, not afterthoughts.
- **G7 — Privacy by default.** Minimal PII, one-click pseudonymization,
  retention controls, and no use of student content for model training.
- **G8 — Clean-room discipline.** Behavioral notes in, prompt text never;
  no competitor string constants in product or repo.

### 0.4 Non-goals (v1)

Proctoring or plagiarism adjudication beyond duplicate/collusion
*flagging*; write-back into school LMS/SIS systems (export files only);
syllabus-level grade aggregation across multiple components (we grade the
marked component; roll-up is an M4 goal); a mobile capture pipeline; and
student-facing views — in v1 the teacher is the only user of the marker.

## 1. Architecture

```
              +------------------------------------------------------+
              |                   teacher web app                    |
              |  intake | structure confirm | review queue | reports |
              +-----------+-----------------------------+------------+
                          |                             |
               +----------v----------+       +----------v----------+
               |   marking service   |       |  analytics service  |
               |  (async worker q)   |       |  (pure functions)   |
               +---+-------------+---+       +----------^----------+
                   |             |                      |
        +----------v---+  +------v---------+    MarkRecords in,
        | LLM adapter  |  | PDF/vision     |    aggregates out;
        | (provider-   |  | pipeline       |    no LLM in the
        |  agnostic)   |  | (pages, OCR)   |    aggregation path
        +------+-------+  +----------------+
               |
   +-----------v-------------------------------------------+
   | corpus services                                       |
   | - topic tags  (subject_taxonomy + topical corpus)     |
   | - boundary tables (ingested, with provenance)         |
   | - calibration packs (per question type)               |
   +-------------------------------------------------------+
```

| Component | Responsibility | Notes |
|---|---|---|
| Teacher web app | All human touchpoints; renders reports from data | Next.js; student content only on server paths |
| Marking service | Runs the §3 pipeline stages 3.2–3.5 as queued jobs | Resumable; per-stage checkpoints; idempotent per submission |
| Analytics service | §3.7–3.8 aggregates, ranking, stats | Pure functions over MarkRecords; snapshot per report |
| LLM adapter | §4 interface; provider selection, retries, schema enforcement | Temperature 0 for extraction/marking; every call logged |
| PDF/vision pipeline | Page rendering, text-layer extraction, vision OCR fallback | Page images cached in object storage |
| Corpus services | Topic-tag priors, boundary tables, calibration packs | Served from the 132-subject mirror + ingested boundary docs |
| Storage | Postgres for entities; object storage for PDFs/pages | Marks are append-only after lock (I5) |

Every LLM call is recorded (prompt-template version, payload hash, model,
latency, cost, outcome) so any report can be replayed and any prompt
change can be regression-tested against the same inputs.

## 2. Data model

Core entities: `Exam`, `QuestionNode`, `CriterionRow`, `RoutingRule`,
`BoundaryTable`, `Student`, `Submission`, `MarkRecord`, `ReviewItem`,
`AuditEvent`. Sketches for the three load-bearing shapes:

**QuestionNode** — one question or part, from structure compilation:

```json
{
  "id": "q1b",
  "path": "Q1(b)",
  "parent": "q1",
  "marksPrinted": 3,
  "marksMsSum": 3,
  "marksSource": "ms",
  "topicRefs": ["E2.3"],
  "commandWord": "Calculate",
  "responseType": "short_numeric",
  "flags": []
}
```

**CriterionRow** — one markable line of the compiled mark scheme:

```json
{
  "id": "q1b:c2",
  "question": "q1b",
  "marks": 1,
  "type": "A",
  "text": "cao 7.5 with correct substitution seen",
  "alternatives": ["7.5 from correct method"],
  "ecfFrom": "q1a:c1"
}
```

**MarkRecord** — one student × one question, the unit of evidence:

```json
{
  "student": "s01",
  "question": "q1b",
  "awarded": 2,
  "max": 3,
  "criteria": [
    {"criterion": "q1b:c1", "awarded": 1,
     "msEvidence": "M1: 3x = 15 seen",
     "answerEvidence": "\"3x = 15\""},
    {"criterion": "q1b:c2", "awarded": 1,
     "msEvidence": "A1: x = 5",
     "answerEvidence": "\"x = 5\""},
    {"criterion": "q1b:c3", "awarded": 0,
     "msEvidence": "B1: answer in km/h",
     "answerEvidence": "\"5\" (no unit)", "note": "unit omitted"}
  ],
  "confidence": 0.61,
  "flags": ["low_confidence"],
  "reviewState": "pending",
  "adjustmentOf": null
}
```

**Invariants (enforced at write time):**

- **I1** Totals and every aggregate are computed in code from
  MarkRecords; the model is never asked for, and never returns, totals.
- **I2** Every MarkRecord cites criterion rows; each criterion decision
  carries non-empty `msEvidence` and `answerEvidence` strings.
- **I3** `awarded <= max` per question; `max` is the reconciled MS/QP
  value or a recorded teacher override.
- **I4** A grade is rendered only with a boundary-provenance string
  attached.
- **I5** After an exam is locked, MarkRecords are append-only: any change
  is a new record with `adjustmentOf`, reviewer and reason.
- **I6** `confidence` is mandatory; below threshold it automatically
  creates a ReviewItem.

## 3. Marking pipeline

Eleven stages. Stages 3.2–3.5 are queued jobs; everything else is
request-scoped. Each stage lists its inputs, outputs and failure
behavior, so it can be built and tested independently.

### 3.1 Intake and identity

**Inputs:** QP PDF, MS PDF, N student-script PDFs. **Output:** `Exam`
row, `Submission` rows, storage keys.

- Student identity is **explicit mapping, not filename magic**: the
  teacher maps each uploaded file to a student via autocomplete (or bulk
  pastes a roster). Filenames are a *suggestion* only. This deliberately
  reverses the competitor's contract, where the filename is the identity
  mechanism and a misnamed file silently mislabels a child's report.
- Duplicates: identical content hash is rejected with a pointer to the
  existing submission; near-duplicate text similarity creates a
  collusion-watch flag for the teacher to judge — flagging only, never
  auto-punishment.
- Pseudonymize mode: students are stored and rendered as S01, S02, …;
  display names optional per exam. Default ON for accounts marked as
  teaching minors, otherwise one click away.
- Upload hygiene: minimum resolution / page-count sanity checks; a
  phone-photo warning (glare, skew) with a "continue anyway" escape.

### 3.2 Structure compilation (QP parse + MS-first reconciliation)

**Inputs:** QP pages, MS pages. **Outputs:** `QuestionNode[]`,
`CriterionRow[]`, reconciliation report.

1. `extractStructure` over QP pages yields the question tree: paths,
   printed marks, command words, response-type guesses.
2. `extractScheme` over MS pages yields criterion rows per question with
   types and per-criterion marks.
3. **Reconciliation runs in code, never in the model:** per question,
   `sum(criterion marks)` is compared against QP-printed marks; children
   are summed against parents; the exam total against the printed total.
   The **MS is the source of truth** (it is where boards actually
   allocate marks); QP-printed values are the cross-check. Every
   mismatch becomes a visible warning on the structure-confirm screen —
   the exact failure mode that silently breaks the competitor's
   QP-first contract (boards that print totals only in the MS) is here a
   first-class, resolved-by-a-human condition.
4. The teacher confirms or edits the structure. Edits are recorded as
   `teacher_override` and win over both sources. Confirmed structure is
   the marking contract; nothing marks before confirmation.

### 3.3 Criterion compilation

**Inputs:** confirmed QuestionNodes, raw criterion rows. **Outputs:**
normalized CriterionRows, RoutingRules, topic tags.

- Mark-type registry per board: CIE (M/A/B and friends), Edexcel
  (M/A/B/K/C), OCR, AQA, IB markbands for extended writing. Unknown
  types degrade to a generic `criterion` with a warning, never to a
  guess.
- **Routing rules** compiled and confirmed by the teacher: choose-N-of-M
  groups (CIE "answer two of three"), alternative parts, best-of
  selections. The routing engine decides *which* questions count toward
  the total; unchosen attempts are still marked (feedback is free) but
  excluded from totals per the rule.
- **ECF chains**: `ecfFrom` links captured from MS wording ("error
  carried forward", "follow their…"); the engine applies propagated
  penalties in code, per MS rule text, not per model mood.
- **Topic tagging**: candidate tags come from (a) topical-corpus priors
  via question-text similarity against our topic-organized mirror, then
  (b) LLM classification against the syllabus context. Tags are shown on
  the structure screen for a quick teacher scan — because *this* tag
  quality is what later makes "weak topics" trustworthy.

### 3.4 Answer extraction

**Inputs:** submission page images + text layers, confirmed question
tree. **Outputs:** `AnswerRegion[]` per student with per-region
confidence.

- A layout pass maps answer regions to question paths; handwritten and
  typed responses are treated identically (vision extraction either way).
- An illegible or missing region yields `answer = null` plus an
  `illegible` flag. **We never guess a blank.** The competitor has no
  such protocol; this is the difference between a flagged question and a
  confidently fabricated zero.
- Out-of-order answers and extra sheets: when the layout pass cannot
  place a region, a small mapping UI asks "where does Q3(b) continue?"
  instead of inventing an alignment.
- Region images (crop) are kept for the review UI so the teacher sees
  exactly what the model saw.

### 3.5 Marking engine

**Inputs:** per question — question text, criterion rows, routing
context, student answer regions, calibration pack; per student — nothing
else. **Output:** strict-JSON MarkRecord per question.

- **One call per question × student** (not one call per script): keeps
  payloads small, failures isolated, retries cheap, and the eval suite
  composable.
- Strategy per `responseType`:
  - `mcq` — deterministic string match; no model call at all.
  - `short_numeric` — unit and alternative-form handling from
    CriterionRow.alternatives.
  - `short_text` — per-criterion keyword/semantic match.
  - `structured` — per-criterion decisions (the workhorse).
  - `extended` — markband/levels application: level chosen per criterion
    group with a justification quoting the script; band descriptors come
    from the MS pages, not from model priors.
- **Evidence rule (I2)** is the core prompt contract: for each criterion
  the model must return `awarded`, `msEvidence` (quote of the matched MS
  line) and `answerEvidence` (quote of the student's text). A decision
  without both quotes is rejected by the schema validator and retried.
- A **self-check pass** is folded into the same call: after drafting
  decisions, the model re-reads criterion rows against its own draft and
  corrects — cheap consistency without a second round-trip.
- Temperature 0; schema-constrained output; retry ×2 on schema violation,
  then dead-letter with a flag rather than a fabricated mark.
- **Confidence** is computed from extraction confidence, criterion-match
  margins, and self-check stability; below threshold (default 0.70) it
  triggers a ReviewItem (I6).
- ECF post-pass applies chain penalties in code after all marks for the
  chain exist.

### 3.6 Review queue

**Inputs:** ReviewItems from 3.2 (reconciliation), 3.4 (illegible), 3.5
(low confidence), 3.1 (collusion watch). **Output:** adjudicated marks.

- The UI shows the cropped student answer region beside the criterion
  rows and the model's proposed decision with its evidence — the teacher
  accepts, adjusts (with reason, recorded), or escalates.
- Bulk actions for repeat patterns (e.g., "this unit omission applies to
  all students").
- Queue-zero is the release gate: reports render with an "unreviewed
  marks" banner otherwise. This queue is the product's trust engine —
  the teacher sees the model be right (or corrects it) at the exact
  granularity where trust is built.

### 3.7 Aggregation and analytics (pure code)

Totals, percentages, per-question facility (class mean ÷ max), topic
aggregates via `topicRefs`, common-mistake clusters (grouped by
criterion-level failure plus misconception tags), ranks, high/low/mean/
median — all deterministic functions over MarkRecords, snapshotted with
the report for reproducibility. The model contributes *categorizations*
(misconception tags) but never numbers. This is the direct inversion of
the competitor's design, where the model both marks and narrates
statistics in one breath.

### 3.8 Grading and boundaries

- Lookup by (board, syllabus, session, component) in `BoundaryTable`.
  Hit: grade rendered with its provenance line, e.g. "Grade boundaries:
  CIE 0580, June 2023, Paper 2 threshold table (ingested 2026-10-23)".
- Miss: **no grade is shown**; the UI states why and offers two
  remedies — ingest a table, or paste a custom one (provenance recorded
  as `teacher-supplied`). An estimate without boundaries is exactly the
  failure we documented; we do not reproduce it with extra steps.
- Until M4 multi-component roll-up exists, grades are labeled
  "indicative — single component".

### 3.9 Reports and exports

- **Per-student report** rendered from stored data (template lives in
  the app layer, never in a model's system prompt): header with total
  and grade-if-provenanced; question-by-question table with criteria and
  evidence; "why marks were lost" assembled from evidence quotes;
  improvement actions keyed to topicRefs; weak-topics list computed from
  topic aggregates.
- **Class report**: summary table (student, marks, %, grade-if-any,
  rank), difficulty analysis from facility values, topic performance,
  common mistakes from clusters, stats.
- **Exports**: versioned JSON dump (full MarkRecord graph), CSV
  gradebook, PDF reports from our own generator (patterns already
  decoded during the Build-Exam research), and an optional per-student
  PDF for parents.

### 3.10 Privacy and safety

Minimal PII (§3.1); retention configurable per account; student content
never used for model training — provider endpoints must be
no-training/no-retention tier, verified in the adapter config; LLM call
logs store payload *hashes*, not raw student content; exports carry the
same pseudonymization state as the UI. The product copy says plainly:
"AI-assisted marking, teacher-confirmed" — positioning honesty is part of
safety.

### 3.11 Cost and scale sketch

A 12-question paper × 30 students ≈ 1 structure call + 1 scheme call +
30 layout calls + ~360 mark calls (MCQs excluded). With small payloads
and temperature 0 this is a modest per-exam spend; mark calls are cached
by (question, answer-region hash) so re-marks and re-runs are cheap.
Provider pricing belongs in the ops doc, not here.

## 4. LLM service design

### 4.1 Adapter interface

One interface, five operations; the marking pipeline knows nothing about
providers:

```
extractStructure(pages)                 -> QuestionNode[]      (§3.2)
extractScheme(pages, questionTree)      -> CriterionRow[]      (§3.2)
mapAnswers(pages, questionTree)         -> AnswerRegion[]      (§3.4)
markQuestion(markPayload)               -> MarkRecord          (§3.5)
tagTopics(questionText, syllabusCtx)    -> TopicRef[]          (§3.3)
```

### 4.2 Payload principles

- **P1** System prompts carry only the invariant contract (roles, schema,
  evidence rule). All exam-specific material travels in the payload.
- **P2** Outputs are schema-constrained JSON; free prose is never parsed.
- **P3** Temperature 0 for every extraction/marking call.
- **P4** The model is never asked to total, average or rank anything
  (I1) — those are code paths.
- **P5** Each mark payload embeds 2–4 calibration examples of the same
  response type (mined from our corpus, §6), so consistency is bought
  per-call rather than hoped for from a persona.
- **P6** Prompts, schemas and provider configs are versioned in the repo;
  changes ship only through the eval gate (§8).
- **P7** Call logs store hashes and outcomes, never raw student content
  (§3.10).

### 4.3 Failure behavior

| Failure | Detection | Response |
|---|---|---|
| Garbage vision (blur, skew) | Low extraction confidence | `illegible` flag; review queue; never guessed |
| Schema-violating model output | Validator | Retry ×2, then dead-letter + flag (no fabricated mark) |
| Provider outage | Adapter | Queue pauses, resumes idempotently |
| Hallucinated criterion id | FK check vs confirmed structure | Reject + retry; metric tracked in eval |
| Routing ambiguity (two Q3(b)s) | Layout pass | Mapping UI fallback (§3.4) |

## 5. Teacher experience

Exam states: `draft → structure_confirmed → marking → review → locked`
(reports unlocked at review-complete; locked freezes marks into the
append-only regime).

Journey: 1) create exam, upload QP+MS; 2) review the compiled structure
— reconciliation warnings on top, topic tags editable inline; 3) upload
scripts; 4) map files to students (roster paste welcome); 5) mark —
progress live, resumable; 6) work the review queue; 7) read reports; 8)
export.

Deliberate contrast with the competitor: no conversational gates, no
"name yourself / name the exam" choreography, nothing load-bearing in a
chat transcript. The marker is a tool with state, not a persona with
moods. (An optional assistant chat can arrive later — for "why did this
lose a mark?" queries over stored evidence — but it reads the pipeline's
outputs; it never *is* the pipeline.)

## 6. Corpus leverage (the unfair advantage)

- **Topic grounding.** The topical mirror already organizes real
  questions by syllabus topic across 132 subjects; `subject_taxonomy.json`
  gives the stable code vocabulary. Question-tag priors come from
  similarity against that corpus before any LLM classification, and the
  UGM spine exports show the pattern for full syllabus-statement trees
  where we have them.
- **Calibration packs.** Real QP/MS pairs supply worked criterion
  examples per response type and per board vocabulary — the competitor's
  personas have none (few-shot absence was one of our ten documented
  gaps).
- **Evaluation gold sets.** The same corpus yields real papers for gold
  sets; teacher-authored variant scripts supply the student side (§8).
- **Boundary ingestion workstream.** Grade-threshold documents are
  published per session by CIE/Edexcel/OCR; we ingest them with source
  URL and retrieval date as provenance. IB thresholds are less public —
  so the teacher-supplied boundary path must be first-class, not an
  afterthought. (Honesty note: our current archive is QP/MS images;
  boundary tables are a separate, small ingestion effort, not something
  we already hold.)

## 7. Roadmap

| Milestone | Scope | Eval gate |
|---|---|---|
| **M1 — walking skeleton** | Typed-text PDFs only; one board (CIE IGCSE); numeric/short/structured types; teacher-pasted boundaries; JSON export | Per-criterion agreement ≥ 0.80 on the first gold set; fabricated-award rate = 0 |
| **M2 — vision + analytics** | Handwritten marking; topic-tag UI and grounded class analytics; PDF reports | Hallucination rate 0 on handwritten gold set; review-queue precision ≥ 0.7 |
| **M3 — full contract** | Extended-response bands; ECF chains; routing rules; boundary ingestion service | Cohen's kappa ≥ target on essay gold set; reconciliation false-warning rate < 5% |
| **M4 — scale out** | Multi-component roll-up; LMS export formats; cross-exam student progress | Roll-up matches manual computation on synthetic multi-paper fixture |

M1's single-board scope is a feature: the mark-type registry, MS layout
quirks and calibration packs are board-specific, and pretending otherwise
is how generic markers end up generic.

## 8. Evaluation plan

- **Gold sets** to start: 5 subjects × 2 papers × 10 scripts, teacher-
  marked with criterion-level ground truth. Scripts are authored
  variants (correct, partially correct, method-error, blank, illegible)
  so every branch of the engine is exercised.
- **Metrics:**

| Metric | Definition | Target (M1) |
|---|---|---|
| Per-criterion agreement | Exact match vs teacher ground truth | ≥ 0.80 |
| Total-mark MAE | Mean absolute error of exam totals | ≤ 2 marks |
| Grade accuracy | Where boundaries exist | ≥ 0.9 exact, 0 near-miss |
| Fabricated-award rate | Awards lacking evidence quotes or valid criterion ids | **0** (hard gate) |
| Review-queue precision | Flagged marks that were genuinely uncertain | ≥ 0.70 |
| Silence rate | Marks rendered without review despite teacher override | ≤ 1% |

- **Regression harness:** any prompt/model/schema change replays the
  stored call-log inputs and must not regress agreement without an
  explicit, recorded trade-off decision.

## 9. Risks and open questions

1. **Handwritten vision quality** — phone photos will be the norm, not
   the exception. Mitigations: resolution guidance, blur rejection,
   review queue. Open: does M1 accept scans only?
2. **Board rubric variance** — the registry work is real labor; IB
   markbands and CIE M/A marks are different beasts. M1's single-board
   scope contains this.
3. **Boundary data acquisition** — public but distributed; needs a small
   harvester plus provenance records. IB remains a gap.
4. **Cost at scale** — per-call caching and payload discipline should
   hold; revisit if extended-response payloads grow.
5. **Teacher trust** — the review queue is the wedge; acceptance rate is
   the trust KPI. If teachers override constantly, the product is not
   working regardless of raw accuracy.
6. **Minors and data protection** — pseudonymize default for under-16
   cohorts; open question for the operator: retention defaults.
7. **Competitive hygiene** — we publish behavior-derived notes only;
   no prompt text in product, repo, or marketing. G8 is a standing rule,
   not a one-time cleanup.

## 10. Worked example (abbreviated end-to-end trace)

Setup: CIE IGCSE-style mock, Paper 2 excerpt — 3 questions, 9 marks;
boundaries pasted by the teacher (provenance: `teacher-supplied`).

Structure (confirmed): Q1(a) 2 marks [M1 substitution, A1 answer];
Q1(b) 3 marks [M1, A1, B1 unit]; Q2 4 marks [structured, tag `E2.3`].
Reconciliation: clean, no warnings.

Student S01, Q1(b): script shows `3x = 15`, `x = 5`, no unit. MarkRecord
as sketched in §2: awarded 2/3, confidence 0.61 → ReviewItem. Teacher
sees the crop beside the three criterion rows, accepts the proposal in
one click. The M1/A1/B1 unit decision and both evidence quotes are now
part of the audit trail.

Report fragment (rendered from data, not generated):

```
S01 — Mock Paper 2            Total 7/9 (78%)   Grade: n/a*
  Q1(b)  2/3 — unit omitted (B1 not earned)
         MS: "B1: answer expressed in km/h"
         Script: "x = 5" (no unit given)
* Grade withheld: no boundary table for this session.
  Supply one to grade this paper.

Class: facility 0.42 on Q1(b) — weakest item;
       topic E2.3 class mean 61% → flagged for reteach.
```

Every number above is computed; every claim above is quotable. That
sentence is the product.

## Appendix A — competitor contract → our component map

Behavioral mapping from the extracted contract (no third-party text
reproduced; see companion notes):

| Their step (behavioral) | Our component | Upgrade |
|---|---|---|
| Greet, collect teacher/exam names | Exam record + states (§5) | No role-play; durable objects |
| Gate: upload QP, then MS | §3.2 structure compilation | MS-first reconciliation vs QP-only reading |
| Gate: all student PDFs, filename = name | §3.1 intake + identity mapping | Explicit mapping; duplicates and collusion flags |
| Marks only from QP-printed values | §3.2 reconciliation | MS source-of-truth + cross-check + warnings |
| Per-student marking, "beautiful report" | §3.5 engine + §3.9 rendered reports | Evidence quotes; template in code |
| Estimated grade (no boundaries) | §3.8 boundaries service | Provenance or absence; never invented |
| Class analysis in chat | §3.7 analytics service | Computed, snapshotted, exportable |
| Chat-only persistence | §2 data model + exports | Postgres; JSON/CSV/PDF out |

