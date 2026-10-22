// Original prompt engineering for the 4 recreated generators.
// NOTE: ZNotes' server-side prompts are a black box; these prompts were
// written from scratch and calibrated to the OBSERVED output contract
// (key paths, array sizes, length profiles) captured live on 2026-10-22.

const JSON_ONLY = 'Respond with a single valid JSON object and nothing else. No markdown fences, no commentary.';

export interface LessonPlanInput {
  subject: string; topic: string; duration: number;
  learningObjectives: string[]; homework: string;
  teachingStyle?: string | null; studentAbility?: string | null;
  assessmentPreference?: string | null;
}

export function lessonPlanPrompt(d: LessonPlanInput) {
  const objectives = d.learningObjectives.length
    ? d.learningObjectives
    : [`Understand the core ideas of ${d.topic}`];
  return [
    `You are an expert secondary-school lesson designer for ${d.subject}.`,
    JSON_ONLY,
    `Design ONE lesson on "${d.topic}" lasting exactly ${d.duration} minutes.`,
    `LEARNING OBJECTIVES (use these VERBATIM as overview.learningObjectives, in this order, no rewording):`,
    objectives.map((o, i) => `${i + 1}. ${o}`).join('\n'),
    `Required JSON shape (all keys mandatory, exact casing):`,
    `{
  "overview": { "subject": string, "topic": string, "duration": ${d.duration}, "teachingStyle": string|null, "learningObjectives": string[] (VERBATIM list above), "initialPrompts": string[3] (engaging opening questions) },
  "lessonPlan": {
    "starterActivity": { "description": string (~180 chars), "duration": int (5-10), "materials": string[2-3], "instructions": string[4-5] (each 1-2 sentences) },
    "mainActivities": [ 2-3 items: { "description": string (~150 chars), "duration": int (materials+instructions as below), "materials": string[2-3], "instructions": string[4-6], "differentiation": { "support": string[2], "core": string[2], "extension": string[2] } } ],
    "plenary": { "description": string (~150 chars), "duration": int (5-10), "materials": string[2], "instructions": string[4-5], "teacherFollowUp": string[3], "successIndicators": string[4] }
  },
  "reflectionSuggestions": string[5] (each ~110 chars, teacher reflection after the lesson),
  "differentiationAndSEN": { "differentiation": { "support": string[4-5], "core": string[4], "extension": string[4-5] }, "senSupport": string[4-5] (concrete SEN/EAL accommodations) },
  "crossCurricularLinks": string[3] (each ~60-80 chars, name the other subject),
  "assessmentQuestions": string[4-6] (exam-style questions testing the objectives),
  "additionalNotes": string[3] or string (safety, equipment, context notes)
}`,
    `Timing rule: starterActivity.duration + sum(mainActivities[].duration) + plenary.duration must equal exactly ${d.duration}.`,
    d.teachingStyle ? `Preferred teaching style: ${d.teachingStyle}.` : '',
    d.studentAbility ? `Class ability: ${d.studentAbility}.` : '',
    `Homework requested: ${d.homework}. If "No", do not include homework anywhere.`,
    `Tone: practical, specific, classroom-ready. Descriptions 2-4 sentences; instructions imperative.`,
  ].filter(Boolean).join('\n');
}

export interface RubricInput {
  subject: string; topic: string; assignmentType: string;
  taskDescription: string; assessmentType: string;
  marksPerCriterion: number; criteria: string[];
}

export function rubricPrompt(d: RubricInput) {
  return [
    `You are an expert assessment designer. You write analytical rubrics for school assessment.`,
    JSON_ONLY,
    `Rubric for a ${d.assignmentType} in ${d.subject} on "${d.topic}".`,
    `Task description: ${d.taskDescription}`,
    `Assessment type: ${d.assessmentType}. Each criterion is worth ${d.marksPerCriterion} marks.`,
    `Criteria to assess (one rubric row each, EXACT names): ${JSON.stringify(d.criteria)}`,
    `Required JSON shape (all keys mandatory, exact casing):`,
    `{
  "metadata": { "subject": string, "topic": string, "assignmentType": string, "taskDescription": string (reuse, ~130 chars), "assessmentType": string, "assessor": "Teacher", "marksPerCriterion": ${d.marksPerCriterion} },
  "overview": { "assignmentPurpose": string (~95 chars), "submissionFormat": string (~85 chars, concrete format of what students hand in), "criteriaAssessed": ${d.criteria.length}, "performanceScale": "Emerging -> Basic -> Proficient -> Advanced" },
  "rubric": { "criteria": [ one per criterion: { "name": string (exact criterion name), "criterionIntent": string (~110 chars, what this criterion measures), "levels": { "advanced": { "description": string (~300-380 chars), "feedback": string (~100 chars, feedback a teacher would write) }, "proficient": { same fields, description ~300 chars }, "basic": { same, ~330 chars }, "emerging": { same, ~280 chars } } } ] },
  "moderationGuidance": string[2] (how two markers should align, ~150-190 chars each)
}`,
    `Do NOT include "score" fields; they are computed by the app.`,
    `Level ladder: advanced = excellent command, proficient = secure, basic = adequate with gaps, emerging = limited/starting. Descriptions must be observable and specific to ${d.assignmentType.toLowerCase()} work, not generic.`,
  ].join('\n');
}

export interface SowInput {
  subject: string; topic: string; board: string; level: string;
  totalLessons: number; lessonDuration: number;
  difficultyLevel: string; emphasisAreas: string[]; userPreferences: string;
}

export function sowPrompt(d: SowInput) {
  const perLesson = Math.round(d.lessonDuration);
  return [
    `You are an expert head of department writing a scheme of work.`,
    JSON_ONLY,
    `Scheme of work: ${d.totalLessons} lesson(s) of ${perLesson} minutes each for ${d.level} ${d.subject} (${d.board}), topic "${d.topic}". Difficulty: ${d.difficultyLevel}.`,
    d.emphasisAreas.length ? `Emphasis areas to weave in: ${d.emphasisAreas.join(', ')}.` : '',
    d.userPreferences ? `Teacher preferences: ${d.userPreferences}` : '',
    `Required JSON shape (all keys mandatory, exact casing):`,
    `{
  "subject": string, "topic": string,
  "overarchingObjectives": string[3-4] (course-level goals, ~70 chars each),
  "lessons": [ exactly ${d.totalLessons} items: {
    "lessonNumber": int (1-based), "title": string (~55 chars), "duration": ${perLesson},
    "learningObjectives": string[3-4] (measurable, "By the end... students can..." style, ~70 chars),
    "activities": [3-5 items: { "title": string (~40 chars), "description": string (~200-270 chars), "duration": int, "resources": string[3-4] } ]  // activity durations must sum to ${perLesson}
    ,
    "assessment": string[3-4] (~70 chars each, concrete checks for understanding),
    "differentiation": { "support": string[3-4], "core": string[3], "extension": string[3] },
    "scaffoldingStrategies": string[3-4] (~70 chars),
    "reflectionPrompts": string[3] (~75 chars, questions the teacher asks students),
    "crossCurricularLinks": string[3] (~60-80 chars, name the other subject),
    "stretchTasks": string[3] (~85 chars, beyond-spec challenge)
  } ],
  "metadata": { "author": "Curriculum Planning Expert", "createdAt": "YYYY-MM-DD", "version": "1.0" }
}`,
    `Lessons must build progressively (later lessons assume earlier ones).`,
  ].filter(Boolean).join('\n');
}

export interface ClarifyInput {
  mode: 'clarify' | 'challenge'; audience: string;
  inputText: string; subject: string;
}

export function clarifyPrompt(d: ClarifyInput) {
  const verb = d.mode === 'clarify'
    ? 'EXPLAIN the passage clearly, unpacking difficult ideas step by step'
    : 'CHALLENGE the passage: extend it, stress-test it, surface misconceptions, and push understanding further';
  const audienceNote = d.audience === 'Teacher'
    ? 'for a teacher who will re-teach this content'
    : d.audience === 'Parent'
      ? 'for a parent supporting learning at home, plain language, minimal jargon'
      : `for a ${d.audience.toLowerCase()} student`;
  return [
    `You are an expert learning coach for ${d.subject}.`,
    JSON_ONLY,
    `Task: ${verb}, ${audienceNote}.`,
    `PASSAGE:"""${d.inputText}"""`,
    `Required JSON shape (all keys mandatory, exact casing, snake_case exactly as shown):`,
    `{
  "topic": string (~60-75 chars, a descriptive title for the document),
  "main_argument": string (~200-240 chars, the single central claim of the passage, one strong sentence pair),
  "key_concepts": [4-6 items: { "title": string (~30 chars), "importance": "Core" or "Supporting", "description": string (~150-260 chars) } ]  // cover EVERY mechanism in the passage; models named in the passage get their own entries
  ,
  "critical_details": string[3] (~120-140 chars each, precise facts/examinable details that must not be lost),
  "applications_in_practice": [3 items: { "example": string (~40 chars), "description": string (~200-290 chars, concrete classroom/exam/real-world application) } ],
  "thinking_prompt": string (~250-280 chars, ONE rich question + guidance that pushes the audience to reason further),
  "connections": [3 items: { "concept": string (~25 chars, another topic in ${d.subject} or beyond), "relationship": string (~200-230 chars, how it links and why it matters) } ]
}`,
    d.mode === 'challenge'
      ? 'For challenge mode, key_concepts descriptions should also flag common misconceptions and edge cases.'
      : 'For clarify mode, key_concepts descriptions should build from simple to precise.',
  ].join('\n');
}
