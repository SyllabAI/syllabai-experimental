'use client';

import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { ArrowLeft, BookOpenCheck, ClipboardCheck, Map, GraduationCap, Loader2, Sparkles, ShieldCheck } from 'lucide-react';
import { TOOLS, type ToolId } from '@/lib/presets';
import { LessonPlanForm, RubricForm, SowForm, ClarifyForm } from '@/components/toolkit/forms';
import { LessonPlanView, RubricView, SowView, ClarifyView } from '@/components/toolkit/renderers';
import { FidelityPanel } from '@/components/toolkit/fidelity-panel';
import type { LessonPlanOutput, RubricOutput, SowOutput, ClarifyOutput } from '@/lib/schemas';

interface GenState {
  status: 'idle' | 'loading' | 'done' | 'error';
  output?: Record<string, unknown>;
  elapsedMs?: number;
  attempts?: number;
  error?: string;
}

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  BookOpenCheck, ClipboardCheck, Map, GraduationCap,
};

const SUBMIT_TYPE: Record<ToolId, string> = {
  'lesson-plan-generator': 'lesson-plan',
  'rubric-generator': 'rubric',
  'sow-generator': 'sow',
  'clarify-challenge': 'clarify',
};

const STAGES = [
  { at: 0, label: 'Submitting to generator…' },
  { at: 3000, label: 'Processing (model drafting structure)…' },
  { at: 15000, label: 'Processing (populating all contract fields)…' },
  { at: 40000, label: 'Still working — large documents take up to 2 min…' },
  { at: 90000, label: 'Almost there — validating JSON contract…' },
];

export default function Home() {
  const [tool, setTool] = useState<ToolId | null>(null);
  const [gen, setGen] = useState<GenState>({ status: 'idle' });
  const [stage, setStage] = useState(0);
  const [used, setUsed] = useState(0);

  const meta = TOOLS.find((t) => t.id === tool);

  const onGenerate = useCallback(async (data: Record<string, unknown>) => {
    if (!tool) return;
    setGen({ status: 'loading' });
    setStage(0);
    setUsed((u) => Math.min(u + 1, 5));
    const timer = setInterval(() => setStage((s) => Math.min(s + 1, STAGES.length - 1)), 3000);
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ toolType: SUBMIT_TYPE[tool], data }),
      });
      const json = await res.json();
      if (!json.success) throw new Error(json.error || 'generation failed');
      setGen({ status: 'done', output: json.output, elapsedMs: json.elapsedMs, attempts: json.attempts });
    } catch (e) {
      setGen({ status: 'error', error: e instanceof Error ? e.message : String(e) });
    } finally {
      clearInterval(timer);
    }
  }, [tool]);

  const openTool = (id: ToolId) => { setTool(id); setGen({ status: 'idle' }); };

  // ---------------- home ----------------
  if (!tool) {
    return (
      <main className="min-h-screen bg-[#0E1420] text-white flex flex-col">
        <div className="mx-auto w-full max-w-5xl flex-1 px-5 py-12 sm:py-16">
          <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-white/50">
            <ShieldCheck className="h-3.5 w-3.5" /> SyllabAI research · educator-ai recreation
          </div>
          <h1 className="text-3xl font-bold leading-tight sm:text-4xl">My Teaching Toolkit — Recreated</h1>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-white/65 sm:text-base">
            A working reconstruction of the four ZNotes educator-ai generators, built from the reverse-engineered
            contract (form presets, submit/poll protocol, output schemas — captured live 2026-10-22).
            Every output is validated field-by-field against the real captured structure. Prompts and content are
            original; only the interface contract is mirrored.
          </p>

          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {TOOLS.map((t) => {
              const Icon = ICONS[t.icon] ?? Sparkles;
              return (
                <button key={t.id} onClick={() => openTool(t.id)}
                  className="group rounded-xl border border-white/10 bg-white/[0.04] p-5 text-left transition-colors hover:bg-white/[0.09]">
                  <div className="flex items-center gap-3">
                    <span className="grid h-10 w-10 place-items-center rounded-lg" style={{ backgroundColor: `${t.color}22` }}>
                      <Icon className="h-5 w-5" style={{ color: t.color }} />
                    </span>
                    <div>
                      <div className="font-semibold">{t.title}</div>
                      <div className="text-xs text-white/50">{t.subtitle}</div>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-2 text-[11px] text-white/40">
                    <Badge variant="outline" className="border-white/15 text-white/60">{t.type}</Badge>
                    <span className="font-mono">{t.color}</span>
                    <span className="ml-auto opacity-0 transition-opacity group-hover:opacity-100">Open →</span>
                  </div>
                </button>
              );
            })}
          </div>

          <div className="mt-10 grid gap-3 text-xs text-white/50 sm:grid-cols-3">
            <div className="rounded-lg border border-white/10 p-3">
              <b className="text-white/80">Parity by construction.</b> Same presets (16 assignment types, marks 4–25,
              20 emphasis areas), same submit shape <code className="font-mono">{`{type,userId,data}`}</code>, same computed rubric scores.
            </div>
            <div className="rounded-lg border border-white/10 p-3">
              <b className="text-white/80">Exactness proven, not claimed.</b> A built-in validator diffs each output
              against type-shape anchors from 4 real responses pulled from the production API.
            </div>
            <div className="rounded-lg border border-white/10 p-3">
              <b className="text-white/80">Known divergence.</b> Prose is model-dependent (ZNotes: Claude-class backend
              per <code className="font-mono">originalUrl</code>; here: GLM). Structure is identical; wording varies — as it does
              between ZNotes runs too.
            </div>
          </div>
        </div>
        <footer className="mt-auto border-t border-white/10 py-4 text-center text-[11px] text-white/35">
          Research prototype · contract metadata only, no ZNotes content reproduced · quota UX mirrored for parity (no real quota)
        </footer>
      </main>
    );
  }

  // ---------------- tool workspace ----------------
  return (
    <main className="min-h-screen bg-[#F6F7F9] text-foreground flex flex-col">
      <header className="sticky top-0 z-20 border-b bg-[#0E1420] text-white">
        <div className="mx-auto flex w-full max-w-7xl items-center gap-3 px-5 py-3">
          <Button variant="ghost" size="icon" className="text-white/80 hover:bg-white/10 hover:text-white" onClick={() => setTool(null)}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div className="min-w-0">
            <div className="truncate text-sm font-semibold">{meta?.title}</div>
            <div className="truncate text-[11px] text-white/50">recreated · type <code className="font-mono">{meta?.type}</code></div>
          </div>
          <div className="ml-auto hidden items-center gap-2 sm:flex">
            <Badge variant="outline" className="border-white/20 text-white/70">Free prompts used {used}/5 <span className="text-white/40">(parity mirror)</span></Badge>
            <Badge variant="outline" className="border-white/20 font-mono text-white/70">POST /api/generate</Badge>
          </div>
        </div>
      </header>

      <div className="mx-auto grid w-full max-w-7xl flex-1 gap-5 px-5 py-6 lg:grid-cols-[420px_1fr]">
        <section className="lg:sticky lg:top-[73px] lg:self-start">
          <Card>
            <CardContent className="p-5">
              <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold">
                <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: meta?.color }} />
                Configuration <span className="font-normal text-muted-foreground">— presets mirrored from ZNotes</span>
              </h2>
              {tool === 'lesson-plan-generator' && <LessonPlanForm onGenerate={onGenerate} busy={gen.status === 'loading'} />}
              {tool === 'rubric-generator' && <RubricForm onGenerate={onGenerate} busy={gen.status === 'loading'} />}
              {tool === 'sow-generator' && <SowForm onGenerate={onGenerate} busy={gen.status === 'loading'} />}
              {tool === 'clarify-challenge' && <ClarifyForm onGenerate={onGenerate} busy={gen.status === 'loading'} />}
            </CardContent>
          </Card>
        </section>

        <section className="space-y-4">
          {gen.status === 'idle' && (
            <Card><CardContent className="grid min-h-[300px] place-items-center p-10 text-center">
              <div>
                <Sparkles className="mx-auto mb-3 h-8 w-8 text-muted-foreground/40" />
                <p className="text-sm text-muted-foreground">Configure the form and generate.<br />
                Output renders here in the same tab structure as ZNotes, with a fidelity report underneath.</p>
              </div>
            </CardContent></Card>
          )}
          {gen.status === 'loading' && (
            <Card><CardContent className="grid min-h-[300px] place-items-center p-10 text-center">
              <div className="space-y-3">
                <Loader2 className="mx-auto h-8 w-8 animate-spin text-muted-foreground" />
                <p className="text-sm font-medium">{STAGES[stage].label}</p>
                <p className="text-xs text-muted-foreground">ZNotes does this via responseId + 20s polling; we await directly.</p>
              </div>
            </CardContent></Card>
          )}
          {gen.status === 'error' && (
            <Card className="border-rose-200"><CardContent className="p-6">
              <p className="text-sm font-semibold text-rose-700">Generation failed</p>
              <p className="mt-1 text-sm text-muted-foreground">{gen.error}</p>
            </CardContent></Card>
          )}
          {gen.status === 'done' && gen.output && (
            <>
              <Card className="py-1"><CardContent className="p-4 sm:p-6">
                {tool === 'lesson-plan-generator' && <LessonPlanView out={gen.output as unknown as LessonPlanOutput} />}
                {tool === 'rubric-generator' && <RubricView out={gen.output as unknown as RubricOutput} />}
                {tool === 'sow-generator' && <SowView out={gen.output as unknown as SowOutput} />}
                {tool === 'clarify-challenge' && <ClarifyView out={gen.output as unknown as ClarifyOutput} />}
              </CardContent></Card>
              <FidelityPanel toolType={SUBMIT_TYPE[tool]} output={gen.output} elapsedMs={gen.elapsedMs} />
            </>
          )}
        </section>
      </div>

      <footer className="mt-auto border-t bg-white py-4 text-center text-[11px] text-muted-foreground">
        Research recreation of a public-facing AI feature · original prompts & content · structure validated against live-captured anchors
      </footer>
    </main>
  );
}
