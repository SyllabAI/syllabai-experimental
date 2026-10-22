// Schema-fidelity validator: extracts a type-shape from a generated output and
// diffs its KEY STRUCTURE against anchors derived from real captured responses
// (content-free). "Exact" = same key paths, same types, arrays of same item
// shape. Array lengths vary run-to-run (LLM non-determinism) and are not
// required to match.

export type Shape =
  | { kind: 'object'; fields: Record<string, Shape> }
  | { kind: 'array'; items: Shape }
  | { kind: 'leaf'; type: string };

export function extractShape(value: unknown): Shape {
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    const fields: Record<string, Shape> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      fields[k] = extractShape(v);
    }
    return { kind: 'object', fields };
  }
  if (Array.isArray(value)) {
    return { kind: 'array', items: extractShape(value[0] ?? null) };
  }
  if (value === null) return { kind: 'leaf', type: 'null' };
  return { kind: 'leaf', type: typeof value };
}

// Anchors: key paths (+ leaf types) observed in the REAL captured outputs.
// Array item paths use `[]` segments; `*` = any leaf type (strings/ints both
// appear for numeric fields run-to-run).
const A = 'array', O = 'object';
export const ANCHORS: Record<string, Record<string, string>> = {
  'lesson-plan': {
    'overview': O, 'overview.subject': 'string', 'overview.topic': 'string',
    'overview.duration': '*', 'overview.teachingStyle': '*',
    'overview.learningObjectives': A, 'overview.learningObjectives[]': 'string',
    'overview.initialPrompts': A, 'overview.initialPrompts[]': 'string',
    'lessonPlan': O,
    'lessonPlan.starterActivity': O, 'lessonPlan.starterActivity.description': 'string',
    'lessonPlan.starterActivity.duration': '*', 'lessonPlan.starterActivity.materials': A,
    'lessonPlan.starterActivity.materials[]': 'string', 'lessonPlan.starterActivity.instructions': A,
    'lessonPlan.starterActivity.instructions[]': 'string',
    'lessonPlan.mainActivities': A, 'lessonPlan.mainActivities[]': O, 'lessonPlan.mainActivities[].description': 'string',
    'lessonPlan.mainActivities[].duration': '*', 'lessonPlan.mainActivities[].materials': A,
    'lessonPlan.mainActivities[].materials[]': 'string',
    'lessonPlan.mainActivities[].instructions': A,
    'lessonPlan.mainActivities[].instructions[]': 'string',
    'lessonPlan.mainActivities[].differentiation': O,
    'lessonPlan.mainActivities[].differentiation.support': A,
    'lessonPlan.mainActivities[].differentiation.support[]': 'string',
    'lessonPlan.mainActivities[].differentiation.core': A,
    'lessonPlan.mainActivities[].differentiation.core[]': 'string',
    'lessonPlan.mainActivities[].differentiation.extension': A,
    'lessonPlan.mainActivities[].differentiation.extension[]': 'string',
    'lessonPlan.plenary': O, 'lessonPlan.plenary.description': 'string',
    'lessonPlan.plenary.duration': '*', 'lessonPlan.plenary.materials': A,
    'lessonPlan.plenary.materials[]': 'string', 'lessonPlan.plenary.instructions': A,
    'lessonPlan.plenary.instructions[]': 'string',
    'lessonPlan.plenary.teacherFollowUp': A, 'lessonPlan.plenary.teacherFollowUp[]': 'string',
    'lessonPlan.plenary.successIndicators': A, 'lessonPlan.plenary.successIndicators[]': 'string',
    'reflectionSuggestions': A, 'reflectionSuggestions[]': 'string',
    'differentiationAndSEN': O, 'differentiationAndSEN.differentiation': O,
    'differentiationAndSEN.differentiation.support': A,
    'differentiationAndSEN.differentiation.support[]': 'string',
    'differentiationAndSEN.differentiation.core': A,
    'differentiationAndSEN.differentiation.core[]': 'string',
    'differentiationAndSEN.differentiation.extension': A,
    'differentiationAndSEN.differentiation.extension[]': 'string',
    'differentiationAndSEN.senSupport': A, 'differentiationAndSEN.senSupport[]': 'string',
    'crossCurricularLinks': A, 'crossCurricularLinks[]': 'string',
    'assessmentQuestions': A, 'assessmentQuestions[]': 'string',
    'additionalNotes': '*',
  },
  rubric: {
    'metadata': O, 'metadata.subject': 'string', 'metadata.topic': 'string',
    'metadata.assignmentType': 'string', 'metadata.taskDescription': 'string',
    'metadata.assessmentType': 'string', 'metadata.assessor': 'string',
    'metadata.marksPerCriterion': '*',
    'overview': O, 'overview.assignmentPurpose': 'string',
    'overview.submissionFormat': 'string', 'overview.criteriaAssessed': '*',
    'overview.performanceScale': 'string',
    'rubric': O, 'rubric.criteria': A, 'rubric.criteria[]': O, 'rubric.criteria[].name': 'string',
    'rubric.criteria[].criterionIntent': 'string', 'rubric.criteria[].levels': O,
    'rubric.criteria[].levels.advanced': O, 'rubric.criteria[].levels.advanced.score': '*',
    'rubric.criteria[].levels.advanced.description': 'string',
    'rubric.criteria[].levels.advanced.feedback': 'string',
    'rubric.criteria[].levels.proficient': O, 'rubric.criteria[].levels.proficient.score': '*',
    'rubric.criteria[].levels.proficient.description': 'string',
    'rubric.criteria[].levels.proficient.feedback': 'string',
    'rubric.criteria[].levels.basic': O, 'rubric.criteria[].levels.basic.score': '*',
    'rubric.criteria[].levels.basic.description': 'string',
    'rubric.criteria[].levels.basic.feedback': 'string',
    'rubric.criteria[].levels.emerging': O, 'rubric.criteria[].levels.emerging.score': '*',
    'rubric.criteria[].levels.emerging.description': 'string',
    'rubric.criteria[].levels.emerging.feedback': 'string',
    'moderationGuidance': A, 'moderationGuidance[]': 'string',
  },
  sow: {
    'subject': 'string', 'topic': 'string',
    'overarchingObjectives': A, 'overarchingObjectives[]': 'string',
    'lessons': A, 'lessons[].activities': A, 'lessons[].activities[]': O, 'lessons[].lessonNumber': '*', 'lessons[].title': 'string',
    'lessons[].duration': '*', 'lessons[].learningObjectives': A,
    'lessons[].learningObjectives[]': 'string',
    'lessons[].activities': A, 'lessons[].activities[].title': 'string',
    'lessons[].activities[].description': 'string', 'lessons[].activities[].duration': '*',
    'lessons[].activities[].resources': A, 'lessons[].activities[].resources[]': 'string',
    'lessons[].assessment': A, 'lessons[].assessment[]': 'string',
    'lessons[].differentiation': O, 'lessons[].differentiation.support': A,
    'lessons[].differentiation.support[]': 'string', 'lessons[].differentiation.core': A,
    'lessons[].differentiation.core[]': 'string', 'lessons[].differentiation.extension': A,
    'lessons[].differentiation.extension[]': 'string',
    'lessons[].scaffoldingStrategies': A, 'lessons[].scaffoldingStrategies[]': 'string',
    'lessons[].reflectionPrompts': A, 'lessons[].reflectionPrompts[]': 'string',
    'lessons[].crossCurricularLinks': A, 'lessons[].crossCurricularLinks[]': 'string',
    'lessons[].stretchTasks': A, 'lessons[].stretchTasks[]': 'string',
    'metadata': O, 'metadata.author': 'string', 'metadata.createdAt': 'string',
    'metadata.version': 'string',
  },
  clarify: {
    'topic': 'string', 'main_argument': 'string',
    'key_concepts': A, 'key_concepts[]': O, 'key_concepts[].title': 'string',
    'key_concepts[].importance': 'string', 'key_concepts[].description': 'string',
    'critical_details': A, 'critical_details[]': 'string',
    'applications_in_practice': A, 'applications_in_practice[]': O, 'applications_in_practice[].example': 'string',
    'applications_in_practice[].description': 'string',
    'thinking_prompt': 'string',
    'connections': A, 'connections[]': O, 'connections[].concept': 'string',
    'connections[].relationship': 'string',
  },
};

export interface FidelityRow {
  path: string;
  expected: string; // object | array | leaf type
  actual: string | null;
  ok: boolean;
}

function pathsOf(value: unknown, prefix = ''): { path: string; type: string }[] {
  const out: { path: string; type: string }[] = [];
  if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
    out.push({ path: prefix || '$', type: 'object' });
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out.push(...pathsOf(v, prefix ? `${prefix}.${k}` : k));
    }
  } else if (Array.isArray(value)) {
    out.push({ path: prefix, type: 'array' });
    if (value.length > 0) {
      out.push(...pathsOf(value[0], `${prefix}[]`));
    }
  } else {
    out.push({ path: prefix, type: value === null ? 'null' : typeof value });
  }
  return out;
}

export interface FidelityResult {
  score: number; // 0-100
  rows: FidelityRow[];
  missing: string[];
  extra: string[];
  typeMismatch: FidelityRow[];
}

export function checkFidelity(toolType: string, output: unknown): FidelityResult {
  const anchor = ANCHORS[toolType] ?? {};
  const actualPaths = new Map<string, string>();
  for (const p of pathsOf(output)) {
    if (p.path !== '$') actualPaths.set(p.path, p.type);
  }
  const rows: FidelityRow[] = [];
  const missing: string[] = [];
  const extra: string[] = [];
  const typeMismatch: FidelityRow[] = [];

  for (const [path, expected] of Object.entries(anchor)) {
    const actual = actualPaths.get(path) ?? null;
    // for arrays with items, if generation produced empty array the [] path is absent
    let ok: boolean;
    if (actual === null) {
      const parent = path.endsWith('[]') ? path.slice(0, -2) : null;
      const parentIsArray = parent ? actualPaths.get(parent) === 'array' : false;
      ok = parentIsArray && expected === 'string'; // empty array: item paths vacuously ok
      if (!ok) { missing.push(path); rows.push({ path, expected, actual, ok: false }); continue; }
      rows.push({ path, expected, actual: '(empty array)', ok: true });
      continue;
    }
    ok = expected === '*' ? actual !== 'null' : actual === expected;
    if (!ok) typeMismatch.push({ path, expected, actual, ok: false });
    rows.push({ path, expected, actual, ok });
  }
  const anchorKeys = new Set(Object.keys(anchor));
  for (const p of actualPaths.keys()) {
    if (!anchorKeys.has(p)) extra.push(p);
  }
  const okCount = rows.filter((r) => r.ok).length;
  const score = rows.length ? Math.round((okCount / rows.length) * 100) : 0;
  return { score, rows, missing, extra, typeMismatch };
}
