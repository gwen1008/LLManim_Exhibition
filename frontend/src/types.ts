export type StageName = 'rag' | 'planner' | 'audio' | 'coder' | 'render' | 'judge'
export type StageStatus = 'idle' | 'running' | 'done' | 'error'

export interface Scores {
  math_correctness: number
  visual_clarity: number
  concept_alignment: number
}

export interface JudgeResult {
  verdict: 'PASS' | 'FAIL'
  score: number
  scores: Scores
}

export interface StageEvent {
  stage?: StageName
  status?: StageStatus
  type?: string
  verdict?: 'PASS' | 'FAIL'
  score?: number
  scores?: Scores
  video_path?: string
}

export type StageMap = Record<StageName, StageStatus>

export const STAGE_ORDER: StageName[] = ['rag', 'planner', 'audio', 'coder', 'render', 'judge']

export const STAGE_LABELS: Record<StageName, string> = {
  rag: 'RAG',
  planner: 'Planner',
  audio: 'Audio',
  coder: 'Coder',
  render: 'Render',
  judge: 'Judge',
}
