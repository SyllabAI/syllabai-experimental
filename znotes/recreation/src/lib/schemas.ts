// Output types reconstructed from live capture of the 4 educator-ai
// generators (phase 2, 2026-10-22). Field names are the exact contract.

// ---------- lesson-plan ----------
export interface LessonPlanOutput {
  overview: {
    subject: string;
    topic: string;
    duration: number;
    teachingStyle: string | null;
    learningObjectives: string[];
    initialPrompts: string[];
  };
  lessonPlan: {
    starterActivity: {
      description: string;
      duration: number;
      materials: string[];
      instructions: string[];
    };
    mainActivities: {
      description: string;
      duration: number;
      materials: string[];
      instructions: string[];
      differentiation: { support: string[]; core: string[]; extension: string[] };
    }[];
    plenary: {
      description: string;
      duration: number;
      materials: string[];
      instructions: string[];
      teacherFollowUp: string[];
      successIndicators: string[];
    };
  };
  reflectionSuggestions: string[];
  differentiationAndSEN: {
    differentiation: { support: string[]; core: string[]; extension: string[] };
    senSupport: string[];
  };
  crossCurricularLinks: string[];
  assessmentQuestions: string[];
  additionalNotes: string[] | string;
}

// ---------- rubric ----------
export interface RubricOutput {
  metadata: {
    subject: string;
    topic: string;
    assignmentType: string;
    taskDescription: string;
    assessmentType: string;
    assessor: string;
    marksPerCriterion: number;
  };
  overview: {
    assignmentPurpose: string;
    submissionFormat: string;
    criteriaAssessed: number;
    performanceScale: string;
  };
  rubric: {
    criteria: {
      name: string;
      criterionIntent: string;
      levels: {
        advanced: RubricLevel;
        proficient: RubricLevel;
        basic: RubricLevel;
        emerging: RubricLevel;
      };
    }[];
  };
  moderationGuidance: string[];
}
export interface RubricLevel { score: number; description: string; feedback: string; }

// ---------- sow ----------
export interface SowOutput {
  subject: string;
  topic: string;
  overarchingObjectives: string[];
  lessons: {
    lessonNumber: number;
    title: string;
    duration: number;
    learningObjectives: string[];
    activities: { title: string; description: string; duration: number; resources: string[] }[];
    assessment: string[];
    differentiation: { support: string[]; core: string[]; extension: string[] };
    scaffoldingStrategies: string[];
    reflectionPrompts: string[];
    crossCurricularLinks: string[];
    stretchTasks: string[];
  }[];
  metadata: { author: string; createdAt: string; version: string };
}

// ---------- clarify / challenge (Learning Coach) ----------
export interface ClarifyOutput {
  topic: string;
  main_argument: string;
  key_concepts: { title: string; importance: string; description: string }[];
  critical_details: string[];
  applications_in_practice: { example: string; description: string }[];
  thinking_prompt: string;
  connections: { concept: string; relationship: string }[];
}

export type AnyOutput = LessonPlanOutput | RubricOutput | SowOutput | ClarifyOutput;
