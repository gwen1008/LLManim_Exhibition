export interface OpusMetrics {
  render_success: boolean;
  render_duration_sec: number;
  code_lines: number;
  deprecated_api_count: number;
  notes?: string;
}

export interface SystemMetrics {
  render_success: boolean;
  render_duration_sec: number;
  code_lines: number;
  deprecated_api_count: number;
  bj_score: number;
  refining_iterations: number;
}

export interface GalleryItem {
  id: string;
  topic: string;
  topic_en: string;
  opus_video_url: string;
  system_video_url: string;
  opus_metrics: OpusMetrics;
  system_metrics: SystemMetrics;
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
  benchmark_pass_rate: string;
  gt_match_rate: number;
  bj_average_score: number;
  total_videos_generated: number;
  refining_loop_max_iterations: number;
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
  logs?: string[];
}

export type TaskStatus = "queued" | "running" | "done" | "failed";

export interface TaskResponse {
  status: TaskStatus;
  progress: TaskProgress;
  artifacts: TaskArtifacts;
  duration_sec: number;
  error: string | null;
}
