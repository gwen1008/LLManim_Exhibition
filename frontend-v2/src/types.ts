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
  rag:     '搜尋資料',
  planner: '規劃腳本',
  audio:   '生成旁白',
  coder:   '製作動畫',
  render:  '渲染影片',
  judge:   '品質確認',
}

export const STAGE_DESC: Record<StageName, string> = {
  rag:     '搜尋相關數學知識',
  planner: '拆解概念、規劃動畫流程',
  audio:   '生成講解旁白',
  coder:   '撰寫動畫程式碼',
  render:  '渲染輸出影片',
  judge:   '確認影片品質',
}
