export interface ArmMetrics {
  render_success: boolean;
  video_duration_sec: number | null;
  code_lines: number | null;
  gen_time_sec: number | null;
  notes?: string;
  // Opus 裸跑：餵錯誤重試到第幾次成功
  attempts?: number;
  // 本系統：RefiningLoop 迭代次數（0 = 一次到位）
  iterations?: number;
}

export interface GalleryItem {
  id: string;
  topic: string;
  topic_en: string;
  topic_prompt?: string;
  // showcase_only 為 true 時：純系統展示（無 Opus 對比），前端只渲染系統單欄
  showcase_only?: boolean;
  opus_video_url?: string;
  system_video_url: string;
  opus_metrics?: ArmMetrics;
  system_metrics: ArmMetrics;
}

export interface GalleryResponse {
  items: GalleryItem[];
  generated_at: string;
}

export interface Agent {
  name: string;
  model: string;
  role: string;
}

export interface StatsResponse {
  total_videos_generated: number;
  total_video_minutes: number;
  total_cost_usd: number;
  total_compute_minutes: number;
  total_compute_hours: number;
  total_tokens: number;
  // Vision QA — overall + by category
  vision_qa_pass_rate: number;
  vision_qa_pass_elementary: number;
  vision_qa_pass_middle: number;
  vision_qa_elem_n: [number, number];
  vision_qa_mid_n: [number, number];
  // GT — judged-only
  gt_match_rate_judged: number;
  gt_match_true: number;
  gt_match_false: number;
  gt_match_unjudged: number;
  gt_judged_n: number;
  // FJ Math
  fj_math_avg: number;
  fj_math_n: number;
  // Reflexion split
  iter1_count: number;
  iter1_pass_count: number;
  iter1_pass_rate: number;
  iter_multi_count: number;
  iter_multi_pass_count: number;
  iter_multi_fail_count: number;
  iter_multi_pass_rate: number;
  iter_avg: number;
  iter_max: number;
  iter_distribution: Record<string, number>;
  // Per-video
  cost_avg_usd: number;
  duration_avg_sec: number;
  code_lines_avg: number;
  video_duration_avg_sec: number;
  tokens_avg: number;
  // Static
  refining_loop_max_iterations: number;
  benchmark_pass_rate: string;
  fj_fail_count: number;
  fail_rate: number;
  agents: Agent[];
}

export interface TaskProgress {
  stage: string;
  percent: number;
}

export interface TaskArtifacts {
  planner_json?: Record<string, unknown>;
  code?: string;
  vision_verdict?: { verdict: string; issues: string[] };
  video_url?: string;
  bj_score?: number;
  render_error?: string;
}

export type TaskStatus = "queued" | "running" | "done" | "failed";

export interface TaskResponse {
  status: TaskStatus;
  progress: TaskProgress;
  artifacts: TaskArtifacts;
  duration_sec: number;
  error: string | null;
  logs?: string[];
}
