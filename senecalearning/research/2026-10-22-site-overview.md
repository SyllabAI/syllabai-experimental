# Site overview — Seneca Learning

**Captured**: 2026-10-22 · sources: app shell HTML, `/env.js`, App Store
listing, public help centre, public company profiles (see repo for URLs).

## Identity

| Field | Value |
|---|---|
| Product | Seneca — "Learn 2x Faster" homework & revision platform |
| Legal entity | Seneca Learning Ltd (UK, incorporated 16 Sep 2016; platform launched 2017) |
| Founders | Stephen Wilks, Lukas Feddern (met at Oxford) |
| HQ | London (WeWork, 123 Buckingham Palace Road, SW1W 9SH) |
| Owner | **GoStudent** (acquired February 2022) |
| Contact | learnmore@seneca.io · +44 2070978853 · DUNS 222072026 |
| Scale claims | 15M+ students (og:description says "over 15 million"; App Store 14M), 300k+ teachers, 6,000+ schools |
| Markets | UK (primary), DE/AT (Studienkreis variant), ES/FR/IT localisations, BR (Plurall white-label), International (iGCSE/IAL/IB) |

## What the product is

A freemium, curriculum-linked revision/homework platform: short
explanation → immediate active-recall question loops, with cognitive-science
framing (spaced repetition, retrieval practice, interleaving, forgetting
curve). Monetisation: free core content; **Premium** subscriptions for
students/parents; school/teacher contracts; tutoring marketplace ("find
tutors"); and **B2B white-label** — the same SPA powers
`learning.gostudent.org` (GoStudent) and Studienkreis (DE/AT), plus Plurall
(Brazil) via OIDC. An AI layer is now central to the pitch: **AI-marked
questions**, an AI tutor (**"Amelia"**), and an AI **Revision Planner**
(personalised weekly study plan, GCSE/A-level years, with catch-up
sessions and break rewards — help centre, Aug 2026).

## Product surfaces (from app routes + help centre taxonomy)

1. **Student platform** — dashboard, course adding, learning sessions,
   memory-strength bars, XP/streaks/leaderboards, tournaments & challenges,
   Revision Planner, premium upsell (`/dashboard/what-is-premium`).
2. **Teacher platform** — classes, assignments ("set automatically marked
   adaptive homework"), progress tracking, school analytics, MIS sync,
   target grades, report cards.
3. **Parent platform** — `/parent/*` monitoring overview, parent quiz,
   tutoring offers.
4. **AI layer** — chatbot service endpoints (query/explain/
   explain-wrong-answer/exam-question-conversation), short-answer AI
   marking, text-to-speech.

## Evidence the platform is exam-qualification driven

Marketing nav enumerates A Level, GCSE, KS3, iGCSE, International A Level,
IB Diploma courses per subject — the same qualification-spine shape as
SyllabAI's curriculum KG (our 4CH1 pilot sits exactly in their iGCSE
Chemistry lane). Their Premium upsell and "what-is-premium" route confirm
feature entitlement is a first-class product concern — directly comparable
to SyllabAI's DC3 re-attempt economics.

## Cognitive-science claim & research posture

Seneca cites a randomised controlled trial (1,120 Year-9 pupils; Seneca
group mean 8.39 vs 5.15 / 4.08 comparison arms) as its efficacy anchor, and
maintains an "Evidence Seneca works" page. For Paper B (SyllabAI system
design), note the pattern: **product claims backed by a pre-registered-ish
RCT on a specific year group** — the same structure as our Cycle-1 pilot.

## Competitor set (public framing)

Quizlet, BBC Bitesize, Tassomai, Sparx Maths. For SyllabAI the interesting
contrast: all of these are content-first or drill-first; Seneca is the
closest to our "diagnosis + grounded tutoring + learner modelling +
assessment" stack (minus grounded citations, which none of them claim).
