import { STAGE_ORDER, STAGE_LABELS, STAGE_DESC, type StageMap, type StageName, type StageStatus } from '../types'

interface Props {
  stages: StageMap
}

function StepIcon({ status }: { status: StageStatus }) {
  if (status === 'done') {
    return (
      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-emerald-600 text-white text-sm font-bold">
        ✓
      </span>
    )
  }
  if (status === 'running') {
    return (
      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-indigo-600">
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
      </span>
    )
  }
  if (status === 'error') {
    return (
      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-red-600 text-white text-sm font-bold">
        ✗
      </span>
    )
  }
  return (
    <span className="flex h-7 w-7 items-center justify-center rounded-full border-2 border-slate-700 bg-slate-800" />
  )
}

function currentRunningStage(stages: StageMap): StageName | null {
  return STAGE_ORDER.find(s => stages[s] === 'running') ?? null
}

export default function PipelineStages({ stages }: Props) {
  const doneCount = STAGE_ORDER.filter(s => stages[s] === 'done').length
  const pct = Math.round((doneCount / STAGE_ORDER.length) * 100)
  const running = currentRunningStage(stages)

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 space-y-5">
      {/* Current step description */}
      <div className="text-sm text-slate-400 min-h-5">
        {running
          ? <span className="text-indigo-400">{STAGE_DESC[running]}…</span>
          : doneCount === STAGE_ORDER.length
            ? <span className="text-emerald-400">所有步驟已完成</span>
            : '準備中'
        }
      </div>

      {/* Step indicators */}
      <div className="flex items-center gap-1 overflow-x-auto pb-1">
        {STAGE_ORDER.map((s, i) => (
          <div key={s} className="flex items-center gap-1 shrink-0">
            <div className="flex flex-col items-center gap-1.5">
              <StepIcon status={stages[s]} />
              <span className={`text-xs whitespace-nowrap ${
                stages[s] === 'running' ? 'text-indigo-400 font-medium' :
                stages[s] === 'done'    ? 'text-emerald-500' :
                stages[s] === 'error'   ? 'text-red-400' :
                'text-slate-600'
              }`}>
                {STAGE_LABELS[s]}
              </span>
            </div>
            {i < STAGE_ORDER.length - 1 && (
              <div className={`h-px w-8 mb-5 shrink-0 transition-colors duration-500 ${
                stages[STAGE_ORDER[i + 1]] !== 'idle' ? 'bg-emerald-700' : 'bg-slate-800'
              }`} />
            )}
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div className="h-1.5 rounded-full bg-slate-800">
        <div
          className="h-1.5 rounded-full bg-indigo-500 transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
