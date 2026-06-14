import { useState, useRef } from 'react'
import TopicInput from './components/TopicInput'
import PipelineStages from './components/PipelineStages'
import VideoPlayer from './components/VideoPlayer'
import QualityBadge from './components/QualityBadge'
import { STAGE_ORDER, type StageMap, type JudgeResult, type StageEvent } from './types'

const IDLE_STAGES: StageMap = Object.fromEntries(
  STAGE_ORDER.map(s => [s, 'idle'])
) as StageMap

export default function App() {
  const [stages, setStages] = useState<StageMap>(IDLE_STAGES)
  const [videoPath, setVideoPath] = useState<string | null>(null)
  const [judgeResult, setJudgeResult] = useState<JudgeResult | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const esRef = useRef<EventSource | null>(null)

  const handleSubmit = async (topic: string) => {
    setStages(IDLE_STAGES)
    setVideoPath(null)
    setJudgeResult(null)
    setError(null)
    setIsRunning(true)
    esRef.current?.close()

    let taskId: string
    try {
      const res = await fetch('/animate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      })
      if (!res.ok) throw new Error(`伺服器錯誤 (${res.status})`)
      const data = await res.json() as { task_id: string }
      taskId = data.task_id
    } catch (e) {
      setError(e instanceof Error ? e.message : '無法連線，請稍後再試')
      setIsRunning(false)
      return
    }

    const es = new EventSource(`/animate/${taskId}/stream`)
    esRef.current = es

    es.onmessage = (e: MessageEvent<string>) => {
      const event = JSON.parse(e.data) as StageEvent

      if (event.type === 'ping' || !event.stage || !event.status) return

      setStages(prev => ({ ...prev, [event.stage!]: event.status! }))

      if (event.stage === 'render' && event.status === 'done' && event.video_path) {
        setVideoPath(event.video_path)
      }

      if (event.stage === 'judge' && event.status === 'done' && event.verdict && event.scores) {
        setJudgeResult({
          verdict: event.verdict,
          score: event.score ?? 0,
          scores: event.scores,
        })
        es.close()
        setIsRunning(false)
      }

      if (event.status === 'error') {
        setError('生成過程發生錯誤，請重新嘗試')
        es.close()
        setIsRunning(false)
      }
    }

    es.onerror = () => {
      setError('連線中斷，請重新整理頁面')
      es.close()
      setIsRunning(false)
    }
  }

  const hasOutput = videoPath !== null || judgeResult !== null

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-3xl px-4 py-14 space-y-8">

        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">LLManim</h1>
          <p className="text-slate-400">輸入任何數學概念，AI 自動生成一支完整的動畫講解影片</p>
        </div>

        {/* Input */}
        <TopicInput onSubmit={handleSubmit} disabled={isRunning} />

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-800 bg-red-900/30 px-4 py-3 text-sm text-red-400">
            {error}
          </div>
        )}

        {/* Progress */}
        {(isRunning || hasOutput) && (
          <PipelineStages stages={stages} />
        )}

        {/* Output */}
        {hasOutput && (
          <div className="space-y-3">
            <VideoPlayer videoPath={videoPath} />
            <QualityBadge result={judgeResult} />
          </div>
        )}
      </div>
    </div>
  )
}
