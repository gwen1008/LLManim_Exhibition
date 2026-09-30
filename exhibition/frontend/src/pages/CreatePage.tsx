import { useEffect, useRef, useState } from "react";
import { Check, Loader2, Send, Sparkles, X } from "lucide-react";
import { getTask, postGenerate } from "../api/client";
import type { TaskResponse } from "../types";

const TASK_TIMEOUT_SEC = 360;
const POLL_MS = 2000;
const MAX_FAILURES = 5;

type Mode = "opus_only" | "full_system";
type StageStatus = "idle" | "running" | "done" | "error";

interface StageDef {
  label: string;
  desc: string;
  // Percent threshold emitted by the runner ([STAGE] key|pct)
  start: number;
}

// naked_opus.py: coder|20, render|65
const OPUS_STAGES: StageDef[] = [
  { label: "製作動畫", desc: "撰寫動畫程式碼", start: 1 },
  { label: "渲染影片", desc: "渲染輸出影片", start: 65 },
];

// full_system_lite_runner.py: rag|10, planner|15, coder|35, refining|55, judge|85
const SYSTEM_STAGES: StageDef[] = [
  { label: "搜尋資料", desc: "搜尋相關數學知識", start: 1 },
  { label: "規劃腳本", desc: "拆解概念、規劃動畫流程", start: 15 },
  { label: "製作動畫", desc: "撰寫動畫程式碼", start: 35 },
  { label: "渲染影片", desc: "渲染並修正影片", start: 55 },
  { label: "品質確認", desc: "確認影片品質", start: 85 },
];

type Color = "rose" | "emerald";

const THEME: Record<Color, { card: string; title: string; accent: string; bar: string; ring: string; line: string }> = {
  rose: {
    card: "border-rose-800/70 bg-rose-950/20",
    title: "text-rose-300",
    accent: "text-rose-300",
    bar: "bg-rose-500",
    ring: "bg-rose-500/20 ring-rose-500 text-rose-300",
    line: "bg-rose-700",
  },
  emerald: {
    card: "border-emerald-800/70 bg-emerald-950/20",
    title: "text-emerald-300",
    accent: "text-emerald-300",
    bar: "bg-emerald-500",
    ring: "bg-emerald-500/20 ring-emerald-500 text-emerald-300",
    line: "bg-emerald-700",
  },
};

interface RunState {
  running: boolean;
  task: TaskResponse | null;
  error: string | null;
}

const EMPTY: RunState = { running: false, task: null, error: null };

function stagesFromTask(defs: StageDef[], task: TaskResponse | null): StageStatus[] {
  if (!task || task.status === "queued") return defs.map(() => "idle");
  if (task.status === "done") return defs.map(() => "done");
  const pct = task.progress.percent;
  let idx = 0;
  defs.forEach((d, i) => {
    if (pct >= d.start) idx = i;
  });
  return defs.map((_, i) =>
    i < idx ? "done" : i === idx ? (task.status === "failed" ? "error" : "running") : "idle"
  );
}

function friendlyError(err: unknown): string {
  const msg = String(err);
  if (msg.includes("404")) return "任務遺失，請重新送出";
  if (msg.includes("Failed to fetch")) return "無法連線，請稍後再試";
  return "生成過程發生錯誤，請重新嘗試";
}

function StepIcon({ status, color }: { status: StageStatus; color: Color }) {
  if (status === "done") {
    return (
      <span className="flex size-7 items-center justify-center rounded-full bg-emerald-600 text-white">
        <Check className="size-4" aria-hidden="true" />
      </span>
    );
  }
  if (status === "running") {
    return (
      <span className={`flex size-7 items-center justify-center rounded-full ring-2 ${THEME[color].ring}`}>
        <Loader2 className="size-4 animate-spin" aria-hidden="true" />
      </span>
    );
  }
  if (status === "error") {
    return (
      <span className="flex size-7 items-center justify-center rounded-full bg-rose-600 text-white">
        <X className="size-4" aria-hidden="true" />
      </span>
    );
  }
  return <span className="size-7 rounded-full border-2 border-gray-700 bg-gray-800" />;
}

function RunPanel({
  label,
  defs,
  run,
  color,
}: {
  label: string;
  defs: StageDef[];
  run: RunState;
  color: Color;
}) {
  const t = THEME[color];
  const stages = stagesFromTask(defs, run.task);
  const doneCount = stages.filter((s) => s === "done").length;
  const pct = Math.round((doneCount / defs.length) * 100);
  const runningIdx = stages.indexOf("running");
  const videoUrl = run.task?.status === "done" ? run.task.artifacts.video_url : undefined;
  const verdict = run.task?.status === "done" ? run.task.artifacts.vision_verdict?.verdict : undefined;

  let statusText: React.ReactNode = "等待送出…";
  if (runningIdx >= 0) statusText = <span className={t.accent}>{defs[runningIdx].desc}…</span>;
  else if (doneCount === defs.length) statusText = <span className="text-emerald-400">所有步驟已完成</span>;
  else if (run.task?.status === "queued") statusText = run.task.progress.stage;
  else if (run.running) statusText = "準備中";

  return (
    <section aria-label={label} className={`border ${t.card} rounded-xl p-5 flex-1 min-w-0 space-y-4`}>
      <div className={`font-bold text-sm ${t.title}`}>{label}</div>

      <div className="text-sm text-gray-400 min-h-5" aria-live="polite">
        {statusText}
      </div>

      <ol className="flex items-center gap-1 overflow-x-auto pb-1">
        {defs.map((d, i) => (
          <li key={d.label} className="flex items-center gap-1 shrink-0">
            <div className="flex flex-col items-center gap-1.5">
              <StepIcon status={stages[i]} color={color} />
              <span
                className={`text-xs whitespace-nowrap ${
                  stages[i] === "running"
                    ? `${t.accent} font-medium`
                    : stages[i] === "done"
                    ? "text-emerald-500"
                    : stages[i] === "error"
                    ? "text-rose-400"
                    : "text-gray-600"
                }`}
              >
                {d.label}
              </span>
            </div>
            {i < defs.length - 1 && (
              <div
                className={`h-px w-6 mb-5 shrink-0 transition-colors duration-500 ${
                  stages[i + 1] !== "idle" ? t.line : "bg-gray-800"
                }`}
              />
            )}
          </li>
        ))}
      </ol>

      <div
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`${label} 進度`}
        className="h-1.5 rounded-full bg-gray-800"
      >
        <div className={`h-1.5 rounded-full ${t.bar} transition-[width] duration-500`} style={{ width: `${pct}%` }} />
      </div>

      {run.error && (
        <div role="alert" className="rounded-lg border border-rose-800 bg-rose-900/30 px-3 py-2 text-sm text-rose-300">
          {run.error}
        </div>
      )}

      {videoUrl && (
        <div className="rounded-xl overflow-hidden border border-gray-800 bg-black">
          <video key={videoUrl} src={videoUrl} controls playsInline className="w-full aspect-video" />
        </div>
      )}

      {verdict && verdict !== "ERROR" && (
        <div
          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium ${
            verdict === "PASS"
              ? "bg-emerald-900/40 border border-emerald-800 text-emerald-400"
              : "bg-amber-900/30 border border-amber-800 text-amber-400"
          }`}
        >
          <span>{verdict === "PASS" ? "✓" : "!"}</span>
          <span>{verdict === "PASS" ? "影片品質通過" : "影片品質偏低"}</span>
        </div>
      )}
    </section>
  );
}

function useRun(mode: Mode) {
  const [run, setRun] = useState<RunState>(EMPTY);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  function stop(error: string | null = null) {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = null;
    setRun((prev) => ({ ...prev, running: false, error }));
  }

  function poll(taskId: string) {
    const startedAt = Date.now();
    let failures = 0;
    intervalRef.current = setInterval(async () => {
      if ((Date.now() - startedAt) / 1000 > TASK_TIMEOUT_SEC) {
        stop("生成時間過長，請稍後再試");
        return;
      }
      try {
        const t = await getTask(taskId);
        failures = 0;
        // failed reports percent=100; keep last known percent so the failing stage is marked
        setRun((prev) => ({
          ...prev,
          task: t.status === "failed" ? { ...t, progress: prev.task?.progress ?? t.progress } : t,
        }));
        if (t.status === "failed") stop("生成過程發生錯誤");
        else if (t.status === "done") stop();
      } catch (e) {
        failures += 1;
        if (failures >= MAX_FAILURES) stop(friendlyError(e));
      }
    }, POLL_MS);
  }

  async function start(topic: string) {
    if (intervalRef.current) clearInterval(intervalRef.current);
    setRun({ running: true, task: null, error: null });
    try {
      const res = await postGenerate(topic, mode);
      if (!res) {
        stop("即時生成目前未開放");
        return;
      }
      poll(res.task_id);
    } catch (err) {
      stop(friendlyError(err));
    }
  }

  return { run, start };
}

export function CreatePage() {
  const [topic, setTopic] = useState("");
  const opus = useRun("opus_only");
  const sys = useRun("full_system");
  const busy = opus.run.running || sys.run.running;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const val = topic.trim();
    if (!val || busy) return;
    opus.start(val);
    sys.start(val);
  }

  return (
    <div className="min-h-dvh bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-extrabold text-center mb-2 flex items-center justify-center gap-2">
          <Sparkles className="size-7 text-emerald-400" aria-hidden="true" />
          <span>Live 對比生成</span>
        </h1>
        <p className="text-gray-300 text-center mb-8">輸入數學主題，即時觀看兩個系統生成影片</p>

        <form onSubmit={handleSubmit} className="flex gap-3 mb-10 max-w-xl mx-auto" aria-label="生成表單">
          <label htmlFor="topic-input" className="sr-only">
            數學主題
          </label>
          <input
            id="topic-input"
            type="text"
            autoComplete="off"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="輸入數學主題，例如：畢氏定理"
            className="flex-1 min-w-0 bg-gray-900 border border-gray-700 rounded-lg px-4 py-2.5 text-white placeholder-gray-400 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/40 min-h-11"
          />
          <button
            type="submit"
            disabled={busy || !topic.trim()}
            className="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-slate-950 disabled:opacity-50 disabled:cursor-not-allowed px-5 py-2.5 rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-300 min-h-11 cursor-pointer"
          >
            {busy ? <Loader2 className="size-4 animate-spin" aria-hidden="true" /> : <Send className="size-4" aria-hidden="true" />}
            {busy ? "生成中…" : "生成"}
          </button>
        </form>

        <div className="flex flex-col md:flex-row gap-4">
          <RunPanel label="Opus 裸跑（Zero-Shot）" defs={OPUS_STAGES} run={opus.run} color="rose" />
          <RunPanel label="本系統（5-Agent Pipeline）" defs={SYSTEM_STAGES} run={sys.run} color="emerald" />
        </div>
      </div>
    </div>
  );
}
