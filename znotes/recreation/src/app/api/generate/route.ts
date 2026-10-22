import { NextRequest, NextResponse } from 'next/server';
import ZAI from 'z-ai-web-dev-sdk';
import {
  lessonPlanPrompt, rubricPrompt, sowPrompt, clarifyPrompt,
  LessonPlanInput, RubricInput, SowInput, ClarifyInput,
} from '@/lib/prompts';
import { levelScores } from '@/lib/presets';

export const maxDuration = 300;

function extractJson(text: string): unknown {
  const cleaned = text.trim()
    .replace(/^```(?:json)?\s*/i, '')
    .replace(/\s*```$/i, '')
    .trim();
  try { return JSON.parse(cleaned); } catch { /* fallthrough */ }
  const s = cleaned.indexOf('{');
  const e = cleaned.lastIndexOf('}');
  if (s !== -1 && e > s) return JSON.parse(cleaned.slice(s, e + 1));
  throw new Error('Model did not return parseable JSON');
}

type ToolType = 'lesson-plan' | 'rubric' | 'sow' | 'clarify';

function buildPrompt(toolType: ToolType, data: Record<string, unknown>): string {
  switch (toolType) {
    case 'lesson-plan': return lessonPlanPrompt(data as unknown as LessonPlanInput);
    case 'rubric': return rubricPrompt(data as unknown as RubricInput);
    case 'sow': return sowPrompt(data as unknown as SowInput);
    case 'clarify': return clarifyPrompt(data as unknown as ClarifyInput);
  }
}

// Post-processing that mirrors client-side computations observed in ZNotes
function postProcess(toolType: ToolType, output: Record<string, unknown>, data: Record<string, unknown>) {
  if (toolType === 'rubric') {
    const marks = Number(data.marksPerCriterion) || 8;
    const scores = levelScores(marks);
    const rubric = output.rubric as { criteria?: { levels?: Record<string, Record<string, unknown>> }[] } | undefined;
    for (const c of rubric?.criteria ?? []) {
      for (const [lvl, score] of Object.entries(scores)) {
        if (c.levels?.[lvl]) c.levels[lvl].score = score;
      }
    }
  }
  if (toolType === 'sow') {
    const meta = output.metadata as Record<string, unknown> | undefined;
    if (meta) {
      meta.author = 'Curriculum Planning Expert';
      meta.version = '1.0';
      if (!meta.createdAt || typeof meta.createdAt !== 'string') {
        meta.createdAt = new Date().toISOString().slice(0, 10);
      }
    }
  }
  return output;
}

export async function POST(req: NextRequest) {
  const started = Date.now();
  try {
    const body = await req.json();
    const toolType = body.toolType as ToolType;
    const data = body.data as Record<string, unknown>;
    if (!['lesson-plan', 'rubric', 'sow', 'clarify'].includes(toolType)) {
      return NextResponse.json({ success: false, error: 'unknown toolType' }, { status: 400 });
    }

    const zai = await ZAI.create();
    const messages = [
      { role: 'assistant' as const, content: buildPrompt(toolType, data) },
      { role: 'user' as const, content: 'Generate the JSON document now. Output JSON only.' },
    ];

    let attempt = 0;
    let output: Record<string, unknown> | null = null;
    let lastError = '';

    while (attempt < 2 && !output) {
      attempt += 1;
      const msgs = attempt === 1
        ? messages
        : [
            ...messages,
            { role: 'user' as const, content: `Your previous output failed validation (${lastError}). Re-output the complete corrected JSON now.` },
          ];
      const completion = await zai.chat.completions.create({
        messages: msgs,
        thinking: { type: 'disabled' },
      });
      const raw = completion.choices[0]?.message?.content ?? '';
      try {
        const parsed = extractJson(raw) as Record<string, unknown>;
        if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
          throw new Error('not an object');
        }
        output = parsed;
      } catch (e) {
        lastError = e instanceof Error ? e.message : String(e);
      }
    }

    if (!output) {
      return NextResponse.json(
        { success: false, error: `generation failed after ${attempt} attempts: ${lastError}` },
        { status: 502 },
      );
    }

    const final = postProcess(toolType, output, data);
    return NextResponse.json({
      success: true,
      output: final,
      elapsedMs: Date.now() - started,
      attempts: attempt,
      meta: { toolType, generatedAt: new Date().toISOString(), backend: 'GLM via z-ai-web-dev-sdk' },
    });
  } catch (err) {
    return NextResponse.json(
      { success: false, error: err instanceof Error ? err.message : String(err) },
      { status: 500 },
    );
  }
}
