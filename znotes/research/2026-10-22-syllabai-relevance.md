# ZNotes → SyllabAI relevance memo (Phase 1)

**Captured**: 2026-10-22. Companion to `2026-10-22-teaching-toolkit.md`.

## What ZNotes does that SyllabAI should study

### 1. Generation grounded in the platform's own content graph (adopt)
Every toolkit request carries `subject/subjectId/module/moduleId`, Topic
dropdowns enumerate the corpus's chapters, and lesson plans auto-attach
the chapter's stored `outcomes` as `learningObjectives`. The teacher
never types free-form objectives; the AI elaborates from curated ones.
**SyllabAI mapping**: our T-TEACH generators should take (course → unit →
chapter) context the same way, and pull objectives from the curriculum
KG rather than asking the model to invent them. This is the same
"grounded, no-invented-content" instinct as our anchored tutor, applied
to teacher tools.

### 2. One endpoint + type discriminator (study, then decide)
`POST /api/znotes-educator-ai {type, userId, data}` with four payload
schemas beats four bespoke endpoints operationally, at the cost of a
union-typed contract. For SyllabAI v2, a single `POST /educator-ai`
with a discriminated union (zod-validated per `type`) would mirror this
while keeping our typed-contract culture. Their `responseId` queue with
20 s polling and a 5-min timeout is a simple pattern for any generation
we run async (Smart Mark currently runs synchronous; a toolkit-style
queue may suit bulk operations like full-book flips).

### 3. Prompt-count entitlements (direct DC3 comparator)
`FREE: 5` (lifetime) vs `PLUS: 100` per-period, counters on the user
record (`educatorAiUsageCount`, lifetime variant), enforced client-side
pre-submit with server reconciliation from the submit response. The
clean observable lesson: **entitlement is a counter the server returns
with every action response**, not a separate entitlement lookup. Maps
onto DC3's "the mark row carries the ordinal; the gate reads the
policy" — same shape: the action response carries the updated state.

### 4. Fire-and-forget UX with a history shelf (adopt)
"You can continue working — we'll notify you when it's ready or open it
later from Your Resources." + toast deep-link
`/?panel=educator-ai&responseId=` + `limit=50` history. Async work never
blocks the dashboard and every artifact has a stable deep link. Cheap to
adopt in the hub for any long-running teacher operation.

### 5. Export quadruple PDF/DOCX/CSV/JSON, rendered client-side (consider)
`docx`+`JSZip` shipped to the browser, zero server render. For SyllabAI
the export set worth matching is PDF/DOCX/JSON (CSV rarely fits our
nested schemas); client-side generation would keep Vercel functions
lean, at the cost of bundle weight (~1 MB of lib for docx+jszip).

### 6. Option-preset ergonomics (adopt the vocabulary)
Their preset lists are good defaults for teaching-tool forms: assignment
types (16), assessment types (10), marks-per-criterion (4/5/8/10/12/20/25
— a realistic mark-budget ladder), difficulty ladder (Foundation/
Intermediate/Advanced), emphasis areas (20 21st-century skills), teaching
approaches (8-9). SyllabAI's Test Builder / assignment forms can reuse
these ladders rather than inventing new ones.

### 7. Audience-differentiated explanation (interesting for the tutor)
Learning Coach's **audience selector** (Beginner/Intermediate/Advanced/
**Teacher/Parent**) over the same content is a crisp, checkable way to
do differentiated output. The clarify/challenge split ("make it clear"
vs "push thinking further") is also a nice bounded alternative to an
open-ended tutor chat — potentially a good fit for a "study mode" in the
hub that parents/teachers can steer.

## What to avoid / risks

1. **Lifetime free quota of 5** is aggressive; it gates discovery of the
   feature itself. SyllabAI's $0-cost architecture can afford a more
   generous trial band, but the lesson stands: count prompts, not tokens.
2. **Client-side-only quota enforcement** (pre-submit check) — the
   server must remain the authority; their model (counter returned with
   each response) makes that feasible without extra round-trips.
3. **No visible citation/provenance surface** on generated outputs (as
   far as static analysis shows): outputs render with metadata but no
   chapter/card anchoring is exposed to the teacher. SyllabAI should
   keep our anchored-provenance standard (trace IDs of record) in any
   generator we build — it's a differentiator over ZNotes.
4. Their toolkit is **detached from assessment data** (no class/marks
   context in any payload — generation is syllabus-driven only).
   SyllabAI's edge: generation that reads the learner model (misconception
   heat, mastery state) is the step ZNotes hasn't taken.

## Bottom line

ZNotes validates the thesis that **teacher AI tools sell Boost** and that
the winning shape is *form-based, corpus-grounded, async, quota-gated,
export-heavy*. The full contract is now documented at field level in
`2026-10-22-teaching-toolkit.md`; the immediate SyllabAI-side follow-ups
are (a) a T-TEACH design note comparing our planned generator contracts
against §2 of that memo, and (b) a DC3-comparison footnote using their
FREE/PLUS counter mechanics.
