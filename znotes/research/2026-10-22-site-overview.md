# ZNotes — site overview (Phase 1)

**Captured**: 2026-10-22 (anonymous public surface + bundle analysis)

## Identity & scale

- **ZNotes Education Limited** — "For Students. By Students." Free
  revision-notes platform founded around peer-authored content; notes are
  written by top-performing students, moderated and expert-reviewed
  (publicised 7-step QA: application → interviews → training → co-creation
  → moderation → publication → expert review).
- Claimed scale: **6 million students**, 80,000 teachers (educators page);
  50K+ on Discord; iOS app shipped 2025 (App Store: "ZNotes: Study Notes &
  Revision", v1.0.15 as of Oct 2026), Android app exists.
- Mission-driven/free-first: notes are free; monetisation is **ZNotes
  Boost** (freemium: unlimited PDFs, ZSlides, AI tokens, custom themes)
  plus school packages ("For Schools" landing page with discounted Boost
  bundles, skills-building workshops).

## Product surface

| Surface | What it is | Access |
|---|---|---|
| Notes | Chapter-wise revision notes per syllabus | free, web + app |
| Videos | Topical + past-paper walkthrough videos | free |
| Quizzes | 3000+ chapter-wise questions | free |
| Flashcards | Per-topic card decks | free |
| Study groups | Discord communities per subject | free |
| ZNotes AI | Personal study assistant over the notes | message-capped free tier |
| ZSlides | Ready-made slide decks generated from notes | Boost |
| PDF exports | Downloadable note PDFs | 3/month free, unlimited Boost |
| **Teaching Toolkit** | **4 educator AI generators (see teaching-toolkit memo)** | 5 free prompts, 100 with Boost Plus |
| Uni Guide | University admissions guides (uni-guides/) | free |
| Skills | Skills/careers content (skills/) | free |

## Boards & levels (sitemap census, 239 URLs)

CAIE: IGCSE (42 subjects), AS-Level (18), A2-Level (13), O-Level (8),
Checkpoint (4) · IB: Diploma Programme (31), MYP (9) · Edexcel: IGCSE (9),
International A-Level (9), GCSE (1) · AQA A-Level (1) · OxfordAQA IAS (1)
· College Board AP (6) · CBSE XI/XII (2) · FBISE HSSC-2 (1) · WAEC WASSCE (3)
· plus university-admission resources (ECAT, SAT, Oxford, language exams).

Subject families span sciences (Bio/Chem/Physics/CS), maths, humanities
(Econ/Business/Law/History/Geography/Sociology/Psychology), languages,
Pakistan Studies/Islamiyat, Food & Nutrition, D&T, Combined Science.

## URL structure

- Content: `/{board}/{level}/{subject}/[module]/[chapter]` (e.g.
  `/caie/igcse/chemistry-0620/...`) — board/level/subject slugs are also
  read client-side to pre-select toolkit context.
- Auth: `/login/`, `/register/{student,educator}/`, `/password/reset/:token`.
- Dashboard: `/content/dashboard` with panel query param
  (`?panel=educator-ai|gradebook|schooldashboard|my-uni|my-development`).
- Commerce: `/boost` (+ `/boost/educator`, `/boost/student`),
  `/subscription`, booster campaigns (`ask-parent`, `claim`).
- Edu-landing: `/for/educators/`, `/for/schools/`.
- Community/join: `/join/{ambassador,contributor,expert,intern,partner}`,
  `/contribution`, `/donate`, `/impact`, `/team`, `/testimonials`.

## Registration roles

`/register/student/` and `/register/educator/` are distinct flows; the
dashboard is role-aware (sidebar strings include "My Teaching Subjects",
"My Teaching Progress", "My Teaching Toolkit", "My School Learning
Analytics", "My Professional Development", "My Students' Uni Goals",
gradebook, assignments, Test Builder ("class-scoped" language appears in
i18n), target grades, report cards — a fairly full teacher LMS surface).

## Business model observations relevant to SyllabAI

1. **Free notes → paid productivity**: the free tier covers content
   consumption; everything *generative or export-heavy* (PDFs, ZSlides,
   AI tokens, toolkit prompts) is quota-gated and upgraded via Boost.
2. **Prompt-count entitlement**: the toolkit's FREE=5 (lifetime) vs
   PLUS=100 counters is one of the cleanest observable examples of
   per-action AI entitlement gating — directly comparable to SyllabAI's
   DC3 re-attempt economics work.
3. **Teacher funnel**: educators get their own landing, registration,
   Boost-Plus SKU and dashboard panels; school-wide packages ride the
   "For Schools" page. Teacher-side monetisation is a distinct lane from
   student Boost.
