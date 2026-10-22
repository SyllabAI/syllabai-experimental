# Reverse-engineering plan — ZNotes (znotes.org)

**Status legend**: [x] done · [~] in progress · [ ] open
**Captured**: 2026-10-22 (Phase 1)

## Objective

Produce a structural understanding of ZNotes — product surface, content
model, API contract, and above all the **educator "My Teaching Toolkit"**
(4 AI resource generators) — sufficient to (a) inform SyllabAI teacher-tool
design (form ergonomics, option presets, grounded generation, async UX,
quota gating, export formats) and (b) position a possible metadata-level
study of their chapter taxonomy. ZNotes is a freemium login-walled platform
whose notes content is its product: **recon-first, account-second**, and
authenticated work is metadata-only by the IP rules in
`docs/IP-AND-COPYRIGHT-NOTES.md`.

## Phases

### Phase 1 — Identification, public recon & static reconstruction `[x]` (2026-10-22)

- [x] Company identity, scale, product surface, boards/levels covered
      (research/2026-10-22-site-overview.md)
- [x] Frontend stack fingerprint (Vite SPA, chunk architecture, CloudFront
      asset host) + API host + auth protocol
      (research/2026-10-22-technical-architecture.md)
- [x] Sitemap taxonomy census (239 URLs; CAIE IGCSE 42, IB DP 31, AS 18 …)
- [x] **My Teaching Toolkit static reconstruction** — the 4 generators with
      full form schemas, option presets, validation rules, request payloads,
      async polling protocol, quota model, export machinery
      (research/2026-10-22-teaching-toolkit.md)
- [x] Evidence captures: sitemap.xml, robots.txt, home/educators/subjects
      HTML, chunk manifest, toolkit registry JSON (resources/captures/)
- [x] Chunk corpus fetched locally for analysis (99 chunks, 5.8 MB) — not
      committed; reproducible via resources/scripts/fetch-app-bundles.sh

### Phase 2 — Authenticated educator walkthrough `[x]` (2026-10-22)

**Resolution of the blocker**: the supplied password includes a **leading
dash** — `-7WVK4?rkV%y2GH` (15 chars). With it, `POST /v2/auth/login`
succeeds; account "HNA 011" @ "ABC International School" (teacher),
teaching Science (CAIE Checkpoint) + Biology (IB DP). All four generators
were driven live and every static-reconstruction claim verified.

- [x] Login session confirmed: email+password path works; session
      preserved locally (never committed)
- [x] Toolkit panel live: `/content/dashboard` sidebar → "My Teaching
      Toolkit"; 4 tool cards render exactly as the registry predicted
- [x] **Wizard step 0 discovered** (static analysis missed it): every
      tool opens a Subject* → Module* wizard before its form. Subject
      dropdown = the FULL board/level/subject catalogue (not restricted
      to taught subjects); Biology (CAIE IGCSE) modules = Theory /
      Alternative to Practical / Topic Explainer / Past Paper Walkthrough /
      Model Answers
- [x] Live quota: "5 out of 5 Free prompts left" → 4 → 3 → 2 → 1 as the
      four generations were submitted (one per tool; server reconciles
      the counter on submit response immediately)
- [x] Async UX verified: "Your resource is being generated … You can
      continue working" + "Continue working" button; resources appear on
      the "Your resources" shelf; toasts fire on completion
- [x] **Lesson plan output verified live**: Overview / Lesson Plan /
      Assessment / Additional tabs; Overview carries Topic/Subject/
      Duration/Homework/Teaching Style/Student Ability/Assessment
      Preference + Learning Objectives = **the verbatim CAIE 0610
      syllabus outcomes for the chapter** (grounding proven — the
      objectives are corpus content, not AI-invented); Lesson Plan tab
      shows timed Starter Activity (7 min) with Materials + Instructions
- [x] **Rubric output verified live — with a correction**: metadata
      renders (Assignment Type `lab-report` slug, Assessment Type
      `summative-assessment`, **Assessor: Teacher**, Purpose, Submission
      Format) and the performance scale is **computed from
      marksPerCriterion** — Emerging (2) → Basic (4) → Proficient (6) →
      Advanced (8) for marks=8. The static bundle labels
      (exceptional/advancing/basic/emerging) are the *render defaults*,
      not the server's scale. Observed quirk: "Criteria Assessed: 1"
      despite 3 criteria selected — server consolidated the requested
      criteria into fewer rows (data point, not blocking)
- [x] **SOW output verified live**: Topic/Subject header + "Unit
      Objectives: 4" count + table (Lesson Number | Duration | Learning
      Objectives | KEY ACTIVITIES AND RESOURCES) with per-lesson
      activities incl. Resources lists
- [x] **Learning Coach output verified live — richer than static
      analysis showed**: result renders **6 tabs** — Main Argument /
      Key Concepts / Critical Details / Applications In Practice /
      Thinking Prompt / Connections — plus Topic/Subject/Audience meta
- [x] Exports verified live: "Export as PDF / DOCS / CSV / JSON"
- [x] Regenerate behaviour verified: re-opens the form (does NOT
      auto-consume a prompt)

### Phase 3 — Content-model & pedagogy synthesis `[ ]`
> 2026-10-22 addition: a **recreation of the 4 toolkit generators** was built and
> verified at 100% structural fidelity against live-captured output anchors
> (`research/2026-10-22-recreation.md`, `recreation/`). New intel: backend model
> family is Claude-class (`originalUrl: "znotes-claude"`); rubric level scores are
> computed client-side at 100/75/50/25 % of marksPerCriterion.

- [ ] Chapter → notes-cards model vs question bank (`/v1/questionBank`,
      `/api/randomQuestions/5/{id}`) — how quizzes and cards relate
- [ ] ZSlides pipeline (notes → slide decks) as far as publicly observable
- [ ] Student AI assistant surface (`/api/knowledge/query`,
      `/api/newbot/query`, `/chat-history`) — request shape, token budget,
      message-count gating (`/v1/updateMessageCount`)
- [ ] Content QA process (7-step pipeline publicised by ZNotes) mapped to
      SyllabAI's teacher-validation workbench concepts

### Phase 4 — SyllabAI synthesis & graduation `[ ]`

- [ ] SyllabAI relevance memo finalised (research/…-syllabai-relevance.md)
- [ ] Decision memo: which toolkit contracts to adopt for the T-TEACH track
      (option-preset ergonomics, grounded objectives, async UX, export set)
- [ ] Graduation PR(s) drafted for of-record repos if adopted
