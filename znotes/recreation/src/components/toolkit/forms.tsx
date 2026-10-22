'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import {
  ASSIGNMENT_TYPES, ASSESSMENT_TYPES_RUBRIC, ASSESSMENT_TYPES_LESSON_PLAN,
  CRITERIA, MARKS_PER_CRITERION, TEACHING_STYLES, TEACHING_APPROACHES_SOW,
  STUDENT_ABILITY, DIFFICULTY_LEVELS, EMPHASIS_AREAS, AUDIENCES, BOARDS,
  DEMO_GROUNDINGS,
} from '@/lib/presets';

export interface FormProps {
  onGenerate: (data: Record<string, unknown>) => void;
  busy: boolean;
}

const selCls = 'bg-white/70';

export function LessonPlanForm({ onGenerate, busy }: FormProps) {
  const [subject, setSubject] = useState('Biology');
  const [topic, setTopic] = useState('Enzymes');
  const [duration, setDuration] = useState(45);
  const [objectives, setObjectives] = useState<string[]>(DEMO_GROUNDINGS.Enzymes);
  const [homework, setHomework] = useState('No');
  const [teachingStyle, setTeachingStyle] = useState<string>('Teacher-led');
  const [ability, setAbility] = useState<string>('Mixed Ability');

  return (
    <div className="space-y-4">
      <div className="rounded-lg bg-muted/60 border p-3 text-xs leading-relaxed text-muted-foreground">
        <b className="text-foreground">Grounding behavior parity:</b> ZNotes auto-attaches the chapter&apos;s
        syllabus <i>outcomes</i> as <code>learningObjectives</code> and the model must reuse them verbatim.
        Paste your own outcomes below (or keep the demo set).
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Subject</Label><Input className={selCls} value={subject} onChange={(e) => setSubject(e.target.value)} /></div>
        <div className="space-y-1.5"><Label>Topic</Label><Input className={selCls} value={topic} onChange={(e) => setTopic(e.target.value)} /></div>
      </div>
      <div className="space-y-1.5">
        <Label>Lesson duration: <span className="font-mono font-semibold text-foreground">{duration} min</span> <span className="text-muted-foreground">(ZNotes range 30–60)</span></Label>
        <Slider min={30} max={60} step={5} value={[duration]} onValueChange={(v) => setDuration(v[0])} />
      </div>
      <div className="space-y-1.5">
        <Label>Learning objectives (grounding, used verbatim) — {objectives.length} items</Label>
        <Textarea rows={6} className="font-mono text-xs" value={objectives.join('\n')}
          onChange={(e) => setObjectives(e.target.value.split('\n').filter((x) => x.trim()))} />
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div className="space-y-1.5"><Label>Teaching style</Label>
          <Select value={teachingStyle} onValueChange={setTeachingStyle}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent>{TEACHING_STYLES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Ability</Label>
          <Select value={ability} onValueChange={setAbility}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent>{STUDENT_ABILITY.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Homework</Label>
          <Select value={homework} onValueChange={setHomework}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent><SelectItem value="Yes">Yes</SelectItem><SelectItem value="No">No</SelectItem></SelectContent>
          </Select>
        </div>
      </div>
      <Button className="w-full" disabled={busy} onClick={() => onGenerate({
        subject, topic, duration, learningObjectives: objectives, homework,
        teachingStyle: teachingStyle || null, studentAbility: ability || null, assessmentPreference: null,
      })}>{busy ? 'Generating…' : 'Generate Lesson Plan'}</Button>
    </div>
  );
}

export function RubricForm({ onGenerate, busy }: FormProps) {
  const [subject, setSubject] = useState('Biology');
  const [topic, setTopic] = useState('Enzymes');
  const [assignmentType, setAssignmentType] = useState<string>('Lab Report');
  const [assessmentType, setAssessmentType] = useState<string>('Summative Assessment');
  const [taskDescription, setTaskDescription] = useState('Write a lab report investigating the effect of temperature on catalase activity in potato tissue, including hypothesis, method, results and evaluation.');
  const [marks, setMarks] = useState(8);
  const [criteria, setCriteria] = useState<string[]>(['Knowledge & Understanding', 'Accuracy', 'Application']);

  const toggle = (c: string) => setCriteria((prev) =>
    prev.includes(c) ? prev.filter((x) => x !== c) : prev.length < 4 ? [...prev, c] : prev);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Subject</Label><Input className={selCls} value={subject} onChange={(e) => setSubject(e.target.value)} /></div>
        <div className="space-y-1.5"><Label>Topic</Label><Input className={selCls} value={topic} onChange={(e) => setTopic(e.target.value)} /></div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Assignment type (16 presets)</Label>
          <Select value={assignmentType} onValueChange={setAssignmentType}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent className="max-h-72">{ASSIGNMENT_TYPES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Assessment type</Label>
          <Select value={assessmentType} onValueChange={setAssessmentType}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent className="max-h-72">{ASSESSMENT_TYPES_RUBRIC.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
      </div>
      <div className="space-y-1.5"><Label>Task description</Label>
        <Textarea rows={3} value={taskDescription} onChange={(e) => setTaskDescription(e.target.value)} />
      </div>
      <div className="space-y-1.5">
        <Label>Marks per criterion: <span className="font-mono font-semibold text-foreground">{marks}</span> <span className="text-muted-foreground">(presets 4/5/8/10/12/20/25)</span></Label>
        <div className="flex gap-2">
          {MARKS_PER_CRITERION.map((m) => (
            <button key={m} onClick={() => setMarks(m)}
              className={`h-9 w-11 rounded-md border text-sm font-mono transition-colors ${marks === m ? 'bg-foreground text-primary-foreground border-foreground' : 'bg-white/70 hover:bg-accent'}`}>{m}</button>
          ))}
        </div>
        <p className="text-xs text-muted-foreground">Level scores are computed client-side (advanced 100% · proficient 75% · basic 50% · emerging 25%) — same rule ZNotes applies.</p>
      </div>
      <div className="space-y-1.5">
        <Label>Criteria assessed — {criteria.length} selected (up to 4)</Label>
        <div className="flex flex-wrap gap-1.5 max-h-44 overflow-y-auto rounded-md border p-2.5 bg-white/50">
          {CRITERIA.map((c) => (
            <Badge key={c} variant={criteria.includes(c) ? 'default' : 'outline'}
              className="cursor-pointer select-none" onClick={() => toggle(c)}>{c}</Badge>
          ))}
        </div>
      </div>
      <Button className="w-full" disabled={busy || criteria.length === 0} onClick={() => onGenerate({
        subject, topic, assignmentType, taskDescription, assessmentType, marksPerCriterion: marks, criteria,
      })}>{busy ? 'Generating…' : 'Generate Rubric'}</Button>
    </div>
  );
}

export function SowForm({ onGenerate, busy }: FormProps) {
  const [subject, setSubject] = useState('Biology');
  const [topic, setTopic] = useState('Enzymes');
  const [board, setBoard] = useState<string>('CAIE');
  const [level, setLevel] = useState('IGCSE');
  const [totalLessons, setTotalLessons] = useState(2);
  const [lessonDuration, setLessonDuration] = useState(60);
  const [difficulty, setDifficulty] = useState<string>('Intermediate');
  const [emphasis, setEmphasis] = useState<string[]>(['Scientific Thinking', 'Practical Skills', 'Metacognition']);
  const [prefs, setPrefs] = useState('');

  const toggle = (c: string) => setEmphasis((prev) =>
    prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Subject</Label><Input className={selCls} value={subject} onChange={(e) => setSubject(e.target.value)} /></div>
        <div className="space-y-1.5"><Label>Topic</Label><Input className={selCls} value={topic} onChange={(e) => setTopic(e.target.value)} /></div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Board</Label>
          <Select value={board} onValueChange={setBoard}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent>{BOARDS.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Level</Label><Input className={selCls} value={level} onChange={(e) => setLevel(e.target.value)} /></div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5">
          <Label>Lessons: <span className="font-mono font-semibold text-foreground">{totalLessons}</span> <span className="text-muted-foreground">(1–5)</span></Label>
          <Slider min={1} max={5} step={1} value={[totalLessons]} onValueChange={(v) => setTotalLessons(v[0])} />
        </div>
        <div className="space-y-1.5">
          <Label>Lesson duration: <span className="font-mono font-semibold text-foreground">{lessonDuration} min</span> <span className="text-muted-foreground">(30–180)</span></Label>
          <Slider min={30} max={180} step={15} value={[lessonDuration]} onValueChange={(v) => setLessonDuration(v[0])} />
        </div>
      </div>
      <div className="space-y-1.5"><Label>Difficulty</Label>
        <Select value={difficulty} onValueChange={setDifficulty}>
          <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
          <SelectContent>{DIFFICULTY_LEVELS.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
        </Select>
      </div>
      <div className="space-y-1.5">
        <Label>Emphasis areas (20 presets) — {emphasis.length} selected</Label>
        <div className="flex flex-wrap gap-1.5 max-h-40 overflow-y-auto rounded-md border p-2.5 bg-white/50">
          {EMPHASIS_AREAS.map((c) => (
            <Badge key={c} variant={emphasis.includes(c) ? 'default' : 'outline'}
              className="cursor-pointer select-none" onClick={() => toggle(c)}>{c}</Badge>
          ))}
        </div>
      </div>
      <div className="space-y-1.5"><Label>User preferences (optional)</Label>
        <Textarea rows={2} value={prefs} onChange={(e) => setPrefs(e.target.value)} placeholder="e.g. include regular low-stakes quizzing" />
      </div>
      <Button className="w-full" disabled={busy} onClick={() => onGenerate({
        subject, topic, board, level, totalLessons, lessonDuration,
        difficultyLevel: difficulty, emphasisAreas: emphasis, userPreferences: prefs,
      })}>{busy ? 'Generating…' : `Generate Scheme of Work (${totalLessons} lesson${totalLessons > 1 ? 's' : ''})`}</Button>
    </div>
  );
}

export function ClarifyForm({ onGenerate, busy }: FormProps) {
  const [mode, setMode] = useState<'clarify' | 'challenge'>('clarify');
  const [audience, setAudience] = useState<string>('Teacher');
  const [subject, setSubject] = useState('Biology');
  const [inputText, setInputText] = useState('Enzymes are biological catalysts. The lock-and-key model says the substrate fits the active site exactly, but the induced-fit model says the active site changes shape slightly as the substrate binds. Enzymes denature above their optimum temperature because the tertiary structure of the active site is lost. pH changes also affect the shape of the active site.');

  return (
    <div className="space-y-4">
      <div className="space-y-1.5">
        <Label>Mode</Label>
        <div className="grid grid-cols-2 gap-2">
          <button onClick={() => setMode('clarify')}
            className={`rounded-lg border p-3 text-left transition-colors ${mode === 'clarify' ? 'border-[#49B081] bg-[#49B081]/10' : 'bg-white/70 hover:bg-accent'}`}>
            <div className="text-sm font-semibold">Clarify</div>
            <div className="text-xs text-muted-foreground">Explain the idea clearly</div>
          </button>
          <button onClick={() => setMode('challenge')}
            className={`rounded-lg border p-3 text-left transition-colors ${mode === 'challenge' ? 'border-[#49B081] bg-[#49B081]/10' : 'bg-white/70 hover:bg-accent'}`}>
            <div className="text-sm font-semibold">Challenge</div>
            <div className="text-xs text-muted-foreground">Stretch & stress-test it</div>
          </button>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5"><Label>Audience</Label>
          <Select value={audience} onValueChange={setAudience}>
            <SelectTrigger className={selCls}><SelectValue /></SelectTrigger>
            <SelectContent>{AUDIENCES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
          </Select>
        </div>
        <div className="space-y-1.5"><Label>Subject</Label><Input className={selCls} value={subject} onChange={(e) => setSubject(e.target.value)} /></div>
      </div>
      <div className="space-y-1.5">
        <Label>Concept / passage <span className="text-muted-foreground">(ZNotes also allows selecting a saved note card)</span></Label>
        <Textarea rows={6} value={inputText} onChange={(e) => setInputText(e.target.value)} />
      </div>
      <Button className="w-full" disabled={busy || !inputText.trim()} onClick={() => onGenerate({
        mode, audience, inputText, subject,
      })}>{busy ? 'Generating…' : `Generate ${mode === 'clarify' ? 'Clarification' : 'Challenge'}`}</Button>
    </div>
  );
}
