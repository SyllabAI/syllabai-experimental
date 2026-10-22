// Presets mirrored from ZNotes educator-ai form options
// Source: static bundle analysis (toolkit-registry.json), live-verified phase 2
// These are functional interface option lists.

export const ASSIGNMENT_TYPES = [
  'Essay', 'Research Project', 'Presentation', 'Poster', 'Lab Report',
  'Report', 'Practical Investigation', 'Case Study', 'Debate', 'Portfolio',
  'Creative Writing', 'Prototype / Design Task', 'Problem-Solving Task',
  'Reflection', 'Group Project', 'Multimedia Project',
] as const;

export const ASSESSMENT_TYPES_RUBRIC = [
  'Formative Assessment', 'Summative Assessment', 'Observation',
  'Oral Questioning', 'Quiz', 'Exit Ticket', 'Peer Assessment',
  'Self Assessment', 'Performance Task', 'Teacher Assessment',
] as const;

export const ASSESSMENT_TYPES_LESSON_PLAN = [
  'Formative Assessment', 'Summative Assessment', 'Observation',
  'Oral Questioning', 'Quiz', 'Exit Ticket', 'Peer Assessment',
  'Self Assessment', 'Performance Task',
] as const;

export const CRITERIA = [
  'Knowledge & Understanding', 'Accuracy', 'Application', 'Analysis',
  'Evaluation', 'Critical Thinking', 'Problem Solving', 'Creativity',
  'Communication', 'Organisation', 'Research', 'Use of Evidence',
  'Presentation', 'Teamwork', 'Practical Skills', 'Reflection',
] as const;

export const MARKS_PER_CRITERION = [4, 5, 8, 10, 12, 20, 25] as const;

export const TEACHING_STYLES = [
  'Teacher-led', 'Student-centred', 'Inquiry-based', 'Discussion-based',
  'Project-based Learning (PBL)', 'Collaborative Learning',
  'Hands-on / Practical', 'Flipped Classroom', 'Blended Learning',
] as const;

export const TEACHING_APPROACHES_SOW = [
  'Traditional', 'Inquiry-Based', 'Project-Based Learning',
  'Collaborative Learning', 'Problem-Based Learning', 'Discussion-Based',
  'Practical / Hands-on', 'Blended Learning',
] as const;

export const STUDENT_ABILITY = [
  'Mixed Ability', 'Developing', 'Intermediate', 'Advanced',
] as const;

export const DIFFICULTY_LEVELS = ['Foundation', 'Intermediate', 'Advanced'] as const;

export const EMPHASIS_AREAS = [
  'Critical Thinking', 'Problem Solving', 'Creativity', 'Communication',
  'Collaboration', 'Digital Literacy', 'Research Skills', 'Inquiry Skills',
  'Real-world Applications', 'Practical Skills', 'Scientific Thinking',
  'Mathematical Reasoning', 'Literacy', 'Numeracy', 'Sustainability',
  'Global Citizenship', 'Ethics', 'Careers & Future Skills',
  'Independent Learning', 'Metacognition',
] as const;

export const AUDIENCES = [
  'Beginner', 'Intermediate', 'Advanced', 'Teacher', 'Parent',
] as const;

export const BOARDS = ['CAIE', 'Edexcel', 'IB', 'AQA', 'OCR'] as const;

// Rubric performance-level score rule, inferred from live capture:
// marks=8 -> advanced 8 / proficient 6 / basic 4 / emerging 2  (100/75/50/25 %)
export function levelScores(marks: number) {
  const r = (f: number) => Math.max(1, Math.round(marks * f));
  return { advanced: marks, proficient: r(0.75), basic: r(0.5), emerging: r(0.25) };
}

export type ToolId = 'lesson-plan-generator' | 'rubric-generator' | 'sow-generator' | 'clarify-challenge';

export interface ToolMeta {
  id: ToolId;
  type: string; // submit payload `type`
  title: string;
  subtitle: string;
  color: string; // brand color as observed
  icon: string; // lucide icon name hint
}

export const TOOLS: ToolMeta[] = [
  { id: 'lesson-plan-generator', type: 'lesson-plan', title: 'Lesson Plan Generator', subtitle: 'Duration-driven plan with verbatim outcome groundings', color: '#E25881', icon: 'BookOpenCheck' },
  { id: 'rubric-generator', type: 'rubric', title: 'Rubric Developer', subtitle: 'Criterion × 4-level scale, scores computed from marks', color: '#F89900', icon: 'ClipboardCheck' },
  { id: 'sow-generator', type: 'sow', title: 'Curriculum Mapper', subtitle: 'Multi-lesson scheme of work with differentiation', color: '#26B3E8', icon: 'Map' },
  { id: 'clarify-challenge', type: 'clarify', title: 'Learning Coach', subtitle: 'Clarify or Challenge a concept for any audience', color: '#49B081', icon: 'GraduationCap' },
];

// Demo grounding set for the lesson-plan generator (our own outcome-style
// phrasings for a public CAIE IGCSE Biology topic; substitute your own).
export const DEMO_GROUNDINGS: Record<string, string[]> = {
  Enzymes: [
    'Describe enzymes as proteins that function as biological catalysts',
    'Explain enzyme action in terms of the lock-and-key and induced-fit models',
    'Describe the effect of temperature and pH on enzyme activity',
    'Explain enzyme denaturation in terms of changes to the active site',
    'Investigate and describe practical tests for enzyme activity',
    'Explain the specificity of enzymes for their substrates',
    'Describe the role of enzymes in metabolism, including anabolic and catabolic reactions',
  ],
};
