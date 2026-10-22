# ZNotes "My Teaching Toolkit" — the 4 AI resource generators (Phase 1 static reconstruction)

**Captured**: 2026-10-22, from the public app bundles (anonymous recon —
no account used). Sources: main bundle (`app-D0RKGZIv.js`), dashboard
chunk (`index-D157Rw1H.js`), shared-components chunk
(`styles-Cbdz7pEk.js`), boost chunk (`index-t7YzLEaD.js`), educators
chunk (`educators-C4gTZwu-.js`). Field lists and payloads below are
decompiled from minified code and are reliable to field-name level;
server-side validation may differ slightly.

---

## 0. What "My Teaching Toolkit" is

The teacher-facing AI resource generator: a **dashboard panel**
(`/content/dashboard?panel=educator-ai`) presenting **four tools** —
"AI+ Tools ⚡" — each generating one teaching resource type from a form.
It is Boost-monetised (5 free prompts lifetime, 100 with Boost Plus) and
**grounded in ZNotes' own content graph**: every tool takes the
subject/module context and its Topic dropdown lists the *chapters of the
selected subject* (from `/v1/chapters/withCards/dashboard`).

### The 4 tools (registry verbatim from the bundle)

| # | id = `type` | UI title | Icon colour | One-liner (i18n) |
|---|---|---|---|---|
| 1 | `lesson-plan-generator` | Lesson Plan Generator | `#E25881` | "Create comprehensive lesson plans with learning objectives" |
| 2 | `rubric-generator` | Rubric Developer | `#F89900` | "Create clear criteria for any assignment or project" |
| 3 | `sow-generator` | Curriculum Mapper | `#26B3E8` | "Generate full-term schemes of work with clarity" |
| 4 | `clarify-challenge` | Learning Coach | `#49B081` | "Clarify confusing topics or push your thinking further" |

(The same quartet is marketed on `/for/educators`, the landing page
"AI-powered teaching workflow" section, and the `/boost/educator` SKU
page — three surfaces, one registry.)

---

## 1. The generation pipeline (shared by all 4)

### 1.1 Submit

```
POST https://api.znotes.org/api/znotes-educator-ai
Content-Type: application/json

{ "type": "<tool-type>",            // one of the 4 registry ids
  "userId": "<user._id>",           // session user
  "data": { ...tool payload } }     // per-tool schema in §2
```

Client-side guard: `type` must be in the valid-set (`dx`); quota checked
pre-submit (§1.4); button label "Generate" → "Generating…".

### 1.2 Async response + polling

```
→ { "responseId": "<id>", "status": "pending" | "processing", ... }
```

- The client starts a poller: **`GET /api/educator-ai/responses/{responseId}`
  every 20 s, hard timeout 5 min.**
- Status lifecycle: `pending | processing | success | error`.
- On `success`/`error` the poller stops and fires window event
  `educator-ai-response-completed` `{responseId, responseData}`; on
  `success` a toast "*{topic or tool title}* is ready! Click to view."
  deep-links to `/?panel=educator-ai&responseId={id}`.
- On submit the event `educator-ai-resource-created` refreshes the
  "Your resources" list:
  `GET /api/educator-ai/responses?userId={id}&limit=50`.
- UX contract (i18n `dashEduAi_generatingInstruction`): "You can continue
  working — we'll notify you when it's ready or you can open it later
  from Your Resources." (fire-and-forget with a history shelf).
- Legacy responses (no `status` field) render as completed.

### 1.3 Context auto-fill

- `subject`/`subjectId`, `module`/`moduleId` resolved from (in order):
  the dashboard's selected subject-module → props → **URL path sniffing**
  (`/{board}/{level}/{subject}/...`, skipping `dashboard|content|skills|
  booster|register|login|profile|settings` prefixes) → subject data
  fallback (`boardSlug`/`levelSlug`).
- Chapter dropdowns are the platform's own chapters
  (`key = chapter.name`); lesson plans additionally read the chapter's
  **`outcomes`** array and send it verbatim as `learningObjectives` —
  i.e. objectives are **corpus-grounded, not AI-invented**.

### 1.4 Quota / entitlement model

- Constants: `Qn = { FREE: 5, PLUS: 100 }`.
- Counters on the user's `userInteraction` record:
  `educatorAiUsageCount` (period) and a lifetime counter; Boost-Plus
  status = `boosterInfo.planType === "boosterPlus"`.
- Remaining = `PLUS − usage` for Plus; else `max(0, FREE − lifetime)`.
- Exhaustion toast: *"You have used all your free prompts. Upgrade to
  Plus booster for 100 prompts!"* / Plus cap: *"You have reached your
  Plus booster limit of 100 prompts."*
- The submit response returns the updated `userInteraction`, so the UI
  decrements immediately.
- Upgrade surface: `/boost/educator` (Boost Plus SKU page lists the same
  4 tool cards).

### 1.5 Results, exports, regeneration

- Result views are per-tool components (§2.6) with **Regenerate**
  (re-opens the form, consuming another prompt).
- **Exports, all client-side** (`docx` + `JSZip` in-bundle):
  PDF / DOCX / CSV / JSON from the result object — for lesson plans the
  export payload is `{lessonPlan, headerMeta}`; for rubrics
  `{criteria}`; clarify exports the body; SOW exports the table.

---

## 2. The four generators — forms, payloads, outputs

### 2.1 Lesson Plan Generator (`lesson-plan-generator`)

**Form fields**

| Field | Req | Control | Options / constraints |
|---|---|---|---|
| Topic Name | ✔ | select | chapters of the subject (`chapter.name`) |
| Duration | ✔ | number | **30–60 minutes** ("cannot exceed 60") |
| Teaching Style | – | select | Teacher-led, Student-centred, Inquiry-based, Discussion-based, Project-based Learning (PBL), Collaborative Learning, Hands-on / Practical, Flipped Classroom, Blended Learning |
| Student Ability | – | select | Mixed Ability, Developing, Intermediate, Advanced |
| Assessment Preference | – | select | Formative Assessment, Summative Assessment, Observation, Oral Questioning, Quiz, Exit Ticket, Peer Assessment, Self Assessment, Performance Task |
| Homework Required | – | select | Yes / No (defaults "No") |

**Payload**

```json
{ "subject": "<name>", "subjectId": "<id>",
  "module": "<name>", "moduleId": "<id>",
  "topic": "<chapter name>",
  "duration": 45,
  "learningObjectives": ["<chapter.outcomes — auto-attached>"],
  "teachingStyle": "Inquiry-based | ... (optional)",
  "studentAbility": "mixed-ability|developing|intermediate|advanced (optional)",
  "assessmentPreference": "Quiz | ... (optional)",
  "homework": "Yes" | "No" }
```

**Output** (`output.lessonPlan`, or `output.lessonOptions[0]` — the API
may return multiple candidate plans, UI takes the first):
`overview` block (topic, subject, level, board, duration, objectives)
+ `starterActivity {duration, description, materials[], instructions[]}`
+ `mainActivities[] {duration, description, materials[], instructions[],
differentiation{core|… support tiers}}` + plenary + homework sections;
rendered as a timed activity sheet with a differentiation table.

### 2.2 Curriculum Mapper (`sow-generator` — "scheme of work")

**Form fields**

| Field | Req | Control | Options / constraints |
|---|---|---|---|
| Topic Name | ✔ | select | chapters |
| Total Lessons | ✔ | number | **1–5** ("cannot exceed 5") |
| Lesson Duration | ✔ | number | **30–180 minutes** |
| Difficulty Level | ✔ | select | Foundation, Intermediate, Advanced (sent lowercase) |
| Teaching Approach | – | select | Traditional, Inquiry-Based, Project-Based Learning, Collaborative Learning, Problem-Based Learning, Discussion-Based, Practical / Hands-on, Blended Learning |
| Emphasis Areas | ✔ | multi-select | Critical Thinking, Problem Solving, Creativity, Communication, Collaboration, Digital Literacy, Research Skills, Inquiry Skills, Real-world Applications, Practical Skills, Scientific Thinking, Mathematical Reasoning, Literacy, Numeracy, Sustainability, Global Citizenship, Ethics, Careers & Future Skills, Independent Learning, Metacognition |

**Payload**

```json
{ "subject": "...", "subjectId": "...", "module": "...", "moduleId": "...",
  "topic": "...", "board": "<board slug>", "level": "<level slug>",
  "totalLessons": 4, "lessonDuration": 60,
  "userPreferences": { "difficultyLevel": "intermediate",
                       "emphasisAreas": ["Critical Thinking", "..."],
                       "teachingApproach": "optional" } }
```

**Output**: `output.overarchingObjectives[]` (unit objectives) +
`output.lessons[] {lessonNumber, title, duration, learningObjectives[],
activities[] {title, description, resources[]}, crossCurricularLinks[]}`
— rendered as a scheme-of-work table (lesson number cell, duration,
objectives list, "KEY ACTIVITIES AND RESOURCES" column with
cross-curricular links footer).

### 2.3 Rubric Developer (`rubric-generator`)

**Form fields**

| Field | Req | Control | Options / constraints |
|---|---|---|---|
| Assignment Type | ✔ | select | Essay, Research Project, Presentation, Poster, Lab Report, Report, Practical Investigation, Case Study, Debate, Portfolio, Creative Writing, Prototype / Design Task, Problem-Solving Task, Reflection, Group Project, Multimedia Project |
| Task Description | ✔ | textarea (4 rows) | "Describe what students are being asked to produce…" |
| Topic Name | ✔ | select | chapters |
| Assessment Type | ✔ | select | Formative Assessment, Summative Assessment, Observation, Oral Questioning, Quiz, Exit Ticket, Peer Assessment, Self Assessment, Performance Task, Teacher Assessment |
| Marks Per Criterion | ✔ | select | **4, 5, 8, 10, 12, 20, 25** (validated 1–100 numeric) |
| Assessment Criteria | ✔ | multi-select | Knowledge & Understanding, Accuracy, Application, Analysis, Evaluation, Critical Thinking, Problem Solving, Creativity, Communication, Organisation, Research, Use of Evidence, Presentation, Teamwork, Practical Skills, Reflection |

**Payload**

```json
{ "subject": "...", "subjectId": "...", "module": "...", "moduleId": "...",
  "assignmentType": "Lab Report",
  "taskDescription": "...",
  "assessmentType": "Summative Assessment",
  "topic": "...",
  "marksPerCriterion": 8,
  "criteria": ["Analysis", "Use of Evidence"] }
```

**Output** (propTypes verified): `output.metadata` (topic, subject,
assignmentType, assessmentType, **assessor**, marksPerCriterion,
assignmentPurpose, submissionFormat, criteriaAssessed,
performanceScale) + `output.rubric.criteria[] {name, levels{…}}` —
levels render as **Exceptional / Advancing / Basic / Emerging** columns
(each with marks implied by `marksPerCriterion`) + a **Moderation
Guidance** list. Rendered as a striped assessment matrix.

### 2.4 Learning Coach (`clarify-challenge`)

**Form fields**

| Field | Req | Control | Options / constraints |
|---|---|---|---|
| Clarify or Challenge | ✔ | select | **clarify** → "Clarify Confusing Topics"; **challenge** → "Challenge Your Thinking & Push it Further" |
| Audience | ✔ | select | Beginner, Intermediate, Advanced, **Teacher, Parent** |
| Input method | ✔ | radio | **text** ("Enter Text") / **notes** ("Select topic from Notes") |
| Your text | (text) | textarea (6 rows) | "Paste or type the academic content you want clarified or challenged" |
| Select Topic | (notes) | select | notes cards of the chapter/module — sends the **full card content** (`title + content`) |

**Payload**

```json
{ "subject": "...", "subjectId": "...", "module": "...", "moduleId": "...",
  "type": "clarify" | "challenge",
  "audience": "beginner|intermediate|advanced|teacher|parent",
  "inputText": "<typed text OR full notes-card content>" }
```

**Output**: explanatory body (`clarify-result`) with meta header
(type/subject/audience) — a grounded explanation/exploration document;
same export set.

### 2.5 Cross-tool invariants

- Every tool payload carries `subject/subjectId/module/moduleId` — the
  generators cannot be used detached from the platform's taxonomy.
- Every tool is **one-shot async** with regenerate-as-new-prompt.
- Client-side validation mirrors server assumptions (ranges hard-coded).
- UI vocabulary consistent: "Generate" → "Generating…" → toast "ready!"
  → "Your resources" shelf ("No resources yet. Create your first
  resource using the tools above!" empty state; `limit=50` history).

### 2.6 Surrounding teacher dashboard (context)

Panels observed in i18n/route table: My Subjects / My Teaching Subjects,
My Teaching Toolkit (`educator-ai`), My Teaching Progress, My School
Learning Analytics (`schooldashboard`), My Professional Development
(`my-development`), My Students' Uni Goals (`my-uni`), gradebook,
assignments (+ `/content/assignments/preview`), Test Builder strings,
target-grades service, report-card strings — the toolkit sits inside a
full teacher LMS shell, but the AI generators are the only
`/api/znotes-educator-ai` consumers.

---

## 3. Requirements summary (what a client must satisfy to reproduce)

1. Authenticated teacher session (`POST /v2/auth/login` → session with
   `user._id`; login offers email+password or Google).
2. `POST /api/znotes-educator-ai` with `{type, userId, data}` and the
   per-tool `data` schema above (unknown `type` rejected client-side).
3. Subject/module/chapter context from `/v1/boards`,
   `/v1/modules?subject=`, `/v1/chapters/withCards/dashboard`.
4. Poll `GET /api/educator-ai/responses/{responseId}` (20 s cadence,
   5 min cap) until `success`/`error`; render per-tool output schema
   (§2.x); list via `GET /api/educator-ai/responses?userId=&limit=50`.
5. Entitlement: free 5 prompts (lifetime) / Plus 100; enforce pre-submit
   and update counters from the response's `userInteraction`.
6. Exports: PDF/DOCX/CSV/JSON generated in-browser from result objects.

**Not yet verified live** (Phase 2 blocker: credential rejection — see
README): exact server-side validation limits, generation latency,
response retention/TTL, and whether `lessonOptions` implies a
pick-one-among-N UX variant.
