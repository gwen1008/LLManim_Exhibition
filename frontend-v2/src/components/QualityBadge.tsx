import type { JudgeResult } from '../types'

interface Props {
  result: JudgeResult | null
}

export default function QualityBadge({ result }: Props) {
  if (!result) return null

  const isPass = result.verdict === 'PASS'

  return (
    <div className={`flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium ${
      isPass
        ? 'bg-emerald-900/40 border border-emerald-800 text-emerald-400'
        : 'bg-amber-900/30 border border-amber-800 text-amber-400'
    }`}>
      <span className="text-base">{isPass ? '✓' : '!'}</span>
      <span>{isPass ? '影片生成成功' : '影片品質偏低，建議調整描述後重新生成'}</span>
    </div>
  )
}
