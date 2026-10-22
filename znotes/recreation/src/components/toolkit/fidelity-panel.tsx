'use client';

import { useMemo } from 'react';
import { checkFidelity, type FidelityResult } from '@/lib/fidelity';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export function FidelityPanel({ toolType, output, elapsedMs }: {
  toolType: string; output: unknown; elapsedMs?: number;
}) {
  const [open, setOpen] = useState(true);
  const result: FidelityResult = useMemo(() => checkFidelity(toolType, output), [toolType, output]);

  const grade = result.score === 100 ? 'EXACT' : result.score >= 90 ? 'NEAR-EXACT' : 'DIVERGENT';
  const gradeCls = result.score === 100
    ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
    : result.score >= 90
      ? 'bg-amber-100 text-amber-800 border-amber-300'
      : 'bg-rose-100 text-rose-800 border-rose-300';

  return (
    <div className="rounded-lg border bg-white">
      <button className="flex w-full items-center justify-between gap-3 p-4 text-left" onClick={() => setOpen(!open)}>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">Schema Fidelity vs real ZNotes capture</span>
            <Badge variant="outline" className={gradeCls}>{grade}</Badge>
          </div>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {result.rows.filter((r) => r.ok).length}/{result.rows.length} contract paths match ·
            type {result.typeMismatch.length === 0 ? 'clean' : `${result.typeMismatch.length} mismatches`} ·
            {result.extra.length === 0 ? ' no extra keys' : ` ${result.extra.length} extra keys`}
            {elapsedMs ? ` · generated in ${fmt(elapsedMs)}` : ''}
          </p>
        </div>
        {open ? <ChevronUp className="h-4 w-4 shrink-0 text-muted-foreground" /> : <ChevronDown className="h-4 w-4 shrink-0 text-muted-foreground" />}
      </button>
      {open && (
        <div className="border-t p-4">
          <div className="mb-3 flex items-center gap-3">
            <Progress value={result.score} className="h-2 flex-1" />
            <span className="font-mono text-sm font-semibold">{result.score}%</span>
          </div>
          <div className="max-h-64 overflow-y-auto rounded-md border">
            <table className="w-full text-left text-xs">
              <thead className="sticky top-0 bg-muted/90 backdrop-blur">
                <tr>
                  <th className="px-2.5 py-1.5 font-medium">Contract path</th>
                  <th className="px-2.5 py-1.5 font-medium">Expected</th>
                  <th className="px-2.5 py-1.5 font-medium">Actual</th>
                  <th className="px-2.5 py-1.5 font-medium w-10"></th>
                </tr>
              </thead>
              <tbody className="font-mono">
                {result.rows.map((r) => (
                  <tr key={r.path} className={`border-t ${r.ok ? 'bg-white' : 'bg-rose-50'}`}>
                    <td className="px-2.5 py-1">{r.path}</td>
                    <td className="px-2.5 py-1 text-muted-foreground">{r.expected}</td>
                    <td className="px-2.5 py-1 text-muted-foreground">{r.actual ?? '—'}</td>
                    <td className={`px-2.5 py-1 font-sans font-bold ${r.ok ? 'text-emerald-600' : 'text-rose-600'}`}>{r.ok ? '✓' : '✗'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {result.missing.length > 0 && (
            <p className="mt-2 text-xs text-rose-600">Missing: {result.missing.join(', ')}</p>
          )}
          <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
            Anchors were derived from 4 real responses captured live from the production API
            (content stripped, structure kept). Array lengths vary run-to-run for any LLM —
            including ZNotes&apos; own — so length is intentionally not compared; item shape is.
          </p>
        </div>
      )}
    </div>
  );
}

const fmt = (ms: number) => `${(ms / 1000).toFixed(1)}s`;
