import { STAGE_ORDER, STAGE_LABELS, type StageMap, type StageStatus } from '../types'

interface Props {
  stages: StageMap
}

function Pill({ label, status }: { label: string; status: StageStatus }) {
  const base = 'flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-all duration-300'
  const styles: Record<StageStatus, string> = {
    idle:    'bg-slate-800 text-slate-500',
    running: 'bg-blue-600 text-white',
    done:    'bg-green-600 text-white',
    error:   'bg-red-600 text-white',
  }
  const icons: Record<StageStatus, React.ReactNode> = {
    idle:    <span className="h-2 w-2 rounded-full bg-slate-600" />,
    running: <span className="h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent" />,
    done:    <span>✓</span>,
    error:   <span>✗</span>,
  }

  return (
    <div className={`${base} ${styles[status]}`}>
      {icons[status]}
      {label}
    </div>
  )
}

export default function PipelineStages({ stages }: Props) {
  const doneCount = STAGE_ORDER.filter(s => stages[s] === 'done').length
  const pct = Math.round((doneCount / STAGE_ORDER.length) * 100)

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5 space-y-4">
      <div className="flex flex-wrap gap-2">
        {STAGE_ORDER.map(s => (
          <Pill key={s} label={STAGE_LABELS[s]} status={stages[s]} />
        ))}
      </div>
      <div className="space-y-1">
        <div className="flex justify-between text-xs text-slate-500">
          <span>Progress</span>
          <span>{pct}%</span>
        </div>
        <div className="h-2 rounded-full bg-slate-800">
          <div
            className="h-2 rounded-full bg-blue-500 transition-all duration-500"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  )
}
