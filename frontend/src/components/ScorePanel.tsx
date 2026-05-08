import type { JudgeResult } from '../types'

interface Props {
  result: JudgeResult | null
}

const SCORE_LABELS: Record<keyof JudgeResult['scores'], string> = {
  math_correctness:   'Math Accuracy',
  visual_clarity:     'Visual Clarity',
  concept_alignment:  'Concept Alignment',
}

function ScoreBar({ value }: { value: number }) {
  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-1.5 rounded-full bg-slate-800">
        <div
          className="h-1.5 rounded-full bg-blue-400 transition-all duration-700"
          style={{ width: `${Math.min(100, Math.round(value))}%` }}
        />
      </div>
      <span className="w-10 text-right text-sm font-mono text-slate-300">
        {value.toFixed(2)}
      </span>
    </div>
  )
}

export default function ScorePanel({ result }: Props) {
  if (!result) return null

  const isPass = result.verdict === 'PASS'

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900">
      <div className="px-4 py-3 border-b border-slate-800 text-sm font-medium text-slate-400">
        Quality Report
      </div>
      <div className="p-4 space-y-4">
        <div className={`flex items-center justify-between rounded-lg px-4 py-3 ${isPass ? 'bg-green-900/40 border border-green-700' : 'bg-red-900/40 border border-red-700'}`}>
          <span className="text-sm font-semibold text-slate-300">Verdict</span>
          <span className={`text-lg font-bold ${isPass ? 'text-green-400' : 'text-red-400'}`}>
            {isPass ? '✅ PASS' : '❌ FAIL'}
          </span>
        </div>

        <div className="space-y-3">
          {(Object.keys(result.scores) as Array<keyof JudgeResult['scores']>).map(key => (
            <div key={key} className="space-y-1">
              <div className="flex justify-between text-xs text-slate-500">
                <span>{SCORE_LABELS[key]}</span>
              </div>
              <ScoreBar value={result.scores[key]} />
            </div>
          ))}
        </div>

        <div className="pt-1 border-t border-slate-800 flex items-center justify-between">
          <span className="text-sm text-slate-500">Overall Score</span>
          <span className="text-xl font-bold text-slate-100">{result.score.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}
