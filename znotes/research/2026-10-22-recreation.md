# Recreation of the educator-ai generators — feasibility proven

**Date:** 2026-10-22
**Question:** can the four "My Teaching Toolkit" generators be recreated so outputs
match the real thing? **Answer: yes — structure exactly, content equivalently.**

## What was done

A working recreation was built and tested end-to-end (Next.js app, LLM-backed).
Prior to building, the four REAL responses produced in phase 2 were retrieved from
the production API via the list endpoint (`GET /api/educator-ai/responses?userId=…&limit=50`)
— stored server-side, retrievable at zero quota cost. These served as gold-standard
anchors.

## Key new intel

- `originalUrl: "znotes-claude"` appears on the clarify response object → the backend
  model family is Claude-class. (Field discovered only in live data; not visible in bundles.)
- Rubric level scores are computed, not generated: advanced=marks, proficient=75%,
  basic=50%, emerging=25% of marksPerCriterion (observed marks=8 → 8/6/4/2). The
  recreation reproduces this rule client-side.
- `sow` output metadata is fixed persona strings: author "Curriculum Planning Expert",
  version "1.0".
- `lesson-plan` inputMetadata carries nullable teachingStyle/studentAbility/
  assessmentPreference and homework "Yes"/"No".
- Server honors the submitted criteria count (overview.criteriaAssessed matched the
  submitted list); the "1 despite 3 selected" quirk seen in phase 2 was UI-side only.

## Fidelity results (recreation vs real anchors)

Content-free type-shape anchors were derived from the 4 real responses and a
validator diffs every contract path (keys, nesting, leaf types, array item shapes):

| generator    | contract paths | result |
|--------------|---------------|--------|
| lesson-plan  | 60/60         | EXACT (100%) |
| rubric       | 37/37         | EXACT (100%) |
| sow          | 38/38         | EXACT (100%) |
| clarify      | 18/18         | EXACT (100%) |

Generation latency ~12–22 s per document (vs ZNotes async: responseId + 20 s polling,
5 min cap). SOW activity durations were constrained to sum to lesson duration — a
property the real outputs also satisfy.

## What "exact" means here — honest breakdown

1. **Structure/schema: exact.** Every key path, nesting level, leaf type and array
   item shape matches the real outputs. Proven by the validator, repeatable per run.
2. **Grounding behavior: exact.** Lesson-plan learning objectives are the verbatim
   syllabus outcomes attached from the chapter — recreated with the same mechanism.
3. **Computed fields: exact.** Rubric scores follow the same 100/75/50/25 % rule.
4. **Prose content: equivalent, not identical.** The server-side prompt is a black
   box and the backend model is Claude-class; the recreation uses original prompts on
   GLM. Word-level output necessarily differs — but so does output between two runs
   on ZNotes itself (LLM non-determinism). Length/tone/array-size profiles were
   calibrated to the observed distributions.

## IP posture

- No ZNotes prompt text exists publicly and none was copied (server-side, unknowable).
- Prompts in `recreation/` are original writing, calibrated to observable structure.
- Anchors file (`resources/captures/educator-ai-output-schemas.json`) is content-free
  (type shapes + integer lengths only).
- Form presets (option lists like "Essay", "Lab Report") are functional interface
  facts, not creative expression.
- Generated demo content is original, produced by the recreation itself.

## Recreation source

`recreation/` contains the complete runnable Next.js app (see its README):
- `src/lib/presets.ts` — form option lists (mirrored) + score rule
- `src/lib/schemas.ts` — the four output TypeScript contracts
- `src/lib/anchors.ts`+`fidelity.ts` — real-capture anchors + validator
- `src/lib/prompts.ts` — original schema-locked prompt engineering
- `src/app/api/generate/route.ts` — submit endpoint (single-shot, JSON extraction,
  one self-heal retry; post-processes rubric scores + sow metadata like ZNotes does)
- `src/components/toolkit/` — preset-accurate forms, ZNotes-style tabbed output
  renderers, in-UI fidelity panel
- demo outputs + fidelity checks in `recreation/verification/`

## Verification log (2026-10-22)

- clarify: HTTP 200, 17.9 s, attempt 1, 18/18 EXACT
- rubric: HTTP 200, 19.4 s, attempt 1, 37/37 EXACT, scores 8/6/4/2
- lesson-plan: HTTP 200, 21.0 s, attempt 1, 60/60 EXACT, timing sums 5+15+15+10=45
- sow: HTTP 200, 20.1 s, attempt 1, 38/38 EXACT, activity sums 60+60
- Browser walkthrough: home grid, Learning Coach golden path (EXACT 18/18 in UI),
  Lesson Plan golden path (EXACT 60/60 in UI, verbatim objectives), no console errors.
