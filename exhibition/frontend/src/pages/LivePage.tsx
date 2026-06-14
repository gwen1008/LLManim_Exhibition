import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { Construction, Loader2, Send, Sparkles, X } from "lucide-react";
import { getTask, postGenerate } from "../api/client";
import type { TaskResponse } from "../types";

const TASK_TIMEOUT_SEC = 360;

function friendlyError(err: unknown): string {
  const msg = String(err);
  if (msg.includes("404")) return "任務遺失（後端可能已重啟），請重新送出";
  if (msg.includes("Failed to fetch")) return "無法連線到後端";
  return msg.replace(/^Error:\s*/, "");
}

interface RunState {
  taskId: string | null;
  task: TaskResponse | null;
  error: string | null;
}

const EMPTY: RunState = { taskId: null, task: null, error: null };

function LogPanel({ logs }: { logs: string[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [logs]);
  return (
    <div
      ref={ref}
      role="log"
      aria-live="polite"
      aria-atomic="false"
      className="bg-black/50 rounded p-2 max-h-48 overflow-y-auto border border-gray-800/60"
    >
      {logs.map((log, i) => (
        <div
          key={i}
          className="text-xs text-gray-300 font-mono tabular-nums whitespace-pre-wrap break-all"
        >
          {log}
        </div>
      ))}
    </div>
  );
}

function ProgressPanel({
  label,
  run,
  color,
  onCancel,
}: {
  label: string;
  run: RunState;
  color: "rose" | "emerald";
  onCancel?: () => void;
}) {
  const c =
    color === "rose"
      ? "border-rose-800/70 bg-rose-950/20"
      : "border-emerald-800/70 bg-emerald-950/20";
  const bar = color === "rose" ? "bg-rose-500" : "bg-emerald-500";
  const text = color === "rose" ? "text-rose-300" : "text-emerald-300";

  return (
    <section
      aria-label={label}
      className={`border ${c} rounded-xl p-4 flex-1 min-w-0`}
    >
      <div className={`font-bold text-sm mb-3 ${text}`}>{label}</div>

      {!run.taskId && !run.error && (
        <div className="text-gray-500 text-sm">等待送出…</div>
      )}

      {run.error && (
        <div role="alert" className="text-rose-300 text-sm">
          {run.error}
        </div>
      )}

      {run.task && (
        <div className="space-y-3">
          <div className="flex items-center justify-between gap-2">
            <div className="text-xs text-gray-300">
              狀態：
              <span
                className={`ml-1 font-medium ${
                  run.error
                    ? "text-gray-500 line-through"
                    : run.task.status === "done"
                    ? "text-emerald-300"
                    : run.task.status === "failed"
                    ? "text-rose-300"
                    : "text-amber-300"
                }`}
              >
                {run.task.status}
                {run.error && (
                  <span className="ml-1 text-rose-300 no-underline">（追蹤已中斷）</span>
                )}
              </span>
            </div>
            {onCancel && (run.task.status === "queued" || run.task.status === "running") && (
              <button
                type="button"
                onClick={onCancel}
                className="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-gray-800 hover:bg-gray-700 text-gray-300 text-[11px] font-medium border border-gray-700 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 cursor-pointer"
                aria-label="取消任務"
              >
                <X className="size-3" aria-hidden="true" />
                取消
              </button>
            )}
          </div>

          <div>
            <div className="flex justify-between text-xs text-gray-300 mb-1">
              <span>{run.task.progress.stage}</span>
              <span className="tabular-nums">{run.task.progress.percent}%</span>
            </div>
            <div
              role="progressbar"
              aria-valuenow={run.task.progress.percent}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label={`${label} 進度`}
              className="bg-gray-800 rounded-full h-2 overflow-hidden"
            >
              <div
                className={`${bar} h-2 rounded-full transition-[width] duration-500 ease-out`}
                style={{ width: `${run.task.progress.percent}%` }}
              />
            </div>
          </div>

          {run.task.status === "failed" && run.task.error && (
            <div
              role="alert"
              className="bg-rose-950/50 border border-rose-800/60 rounded p-2 text-xs text-rose-200 font-mono break-all"
            >
              {run.task.error}
            </div>
          )}

          {run.task.status === "done" && run.task.artifacts.video_url && (
            <video
              src={run.task.artifacts.video_url}
              controls
              playsInline
              className="w-full rounded bg-black aspect-video"
              aria-label={`${label} 結果影片`}
            />
          )}

          {run.task.status === "done" &&
            run.task.artifacts.vision_verdict &&
            run.task.artifacts.vision_verdict.verdict !== "ERROR" && (
              <div className="text-xs">
                <span className="text-gray-300">Vision QA: </span>
                <span
                  className={
                    run.task.artifacts.vision_verdict.verdict === "PASS"
                      ? "text-emerald-300 font-semibold"
                      : "text-rose-300 font-semibold"
                  }
                >
                  {run.task.artifacts.vision_verdict.verdict}
                </span>
              </div>
            )}

          {run.task.logs && run.task.logs.length > 0 && <LogPanel logs={run.task.logs} />}

          <div className="text-xs text-gray-500 tabular-nums">
            {Math.floor(run.task.duration_sec)}s elapsed
          </div>
        </div>
      )}
    </section>
  );
}

export function LivePage() {
  const [available, setAvailable] = useState<boolean | null>(null);
  const [topic, setTopic] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [sysRun, setSysRun] = useState<RunState>(EMPTY);
  const sysInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: "__probe__", mode: "full_system" }),
    })
      .then((r) => setAvailable(r.status !== 501))
      .catch(() => setAvailable(false));
  }, []);

  useEffect(() => {
    return () => {
      if (sysInterval.current) clearInterval(sysInterval.current);
    };
  }, []);

  function poll(taskId: string, setter: typeof setSysRun, intervalRef: typeof sysInterval) {
    if (intervalRef.current) clearInterval(intervalRef.current);
    const startedAt = Date.now();
    let consecutiveFailures = 0;
    const MAX_FAILURES = 5; // 容忍 ~10s 連續失敗（如 uvicorn reload）
    const handle = setInterval(async () => {
      const elapsed = (Date.now() - startedAt) / 1000;
      if (elapsed > TASK_TIMEOUT_SEC) {
        clearInterval(handle);
        intervalRef.current = null;
        setter((prev) => ({
          ...prev,
          error: `任務逾時（>${TASK_TIMEOUT_SEC}s），已停止追蹤`,
        }));
        return;
      }
      try {
        const task = await getTask(taskId);
        consecutiveFailures = 0;
        setter((prev) => ({ ...prev, task, error: null }));
        if (task.status === "done" || task.status === "failed") {
          clearInterval(handle);
          intervalRef.current = null;
        }
      } catch (e) {
        consecutiveFailures += 1;
        if (consecutiveFailures >= MAX_FAILURES) {
          clearInterval(handle);
          intervalRef.current = null;
          setter((prev) => ({ ...prev, error: friendlyError(e) }));
        }
      }
    }, 2000);
    intervalRef.current = handle;
  }

  function cancelRun(setter: typeof setSysRun, intervalRef: typeof sysInterval) {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setter((prev) => ({ ...prev, error: "已取消（後端任務可能仍在執行）" }));
  }

  async function handleSubmit(e?: React.FormEvent) {
    e?.preventDefault();
    if (!topic.trim() || submitting) return;
    if (sysInterval.current) clearInterval(sysInterval.current);
    setSubmitting(true);
    setSysRun(EMPTY);

    try {
      const sysRes = await postGenerate(topic, "full_system");

      if (!sysRes) {
        setAvailable(false);
        return;
      }

      setSysRun({ taskId: sysRes.task_id, task: null, error: null });
      poll(sysRes.task_id, setSysRun, sysInterval);
    } catch (err) {
      const msg = friendlyError(err);
      setSysRun({ taskId: null, task: null, error: msg });
    } finally {
      setSubmitting(false);
    }
  }

  if (available === null) {
    return (
      <div className="min-h-dvh bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center text-gray-400 flex flex-col items-center gap-3">
          <Loader2 className="size-8 animate-spin text-emerald-400" aria-hidden="true" />
          <span className="text-sm">檢查後端狀態中…</span>
        </div>
      </div>
    );
  }

  if (available === false) {
    return (
      <div className="min-h-dvh bg-gray-950 flex items-center justify-center px-4">
        <div className="text-center">
          <Construction className="size-14 mx-auto mb-4 text-amber-400" aria-hidden="true" />
          <h2 className="text-2xl font-bold text-gray-100 mb-2">Live 模式尚未開放</h2>
          <p className="text-gray-400">後端 <code className="font-mono text-gray-300">/api/generate</code> 尚未實作（501）</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-dvh bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-extrabold text-center mb-2 flex items-center justify-center gap-2">
          <Sparkles className="size-7 text-emerald-400" aria-hidden="true" />
          <span>Live 即時生成</span>
        </h1>
        <p className="text-gray-300 text-center mb-8">輸入數學主題，本系統即時生成教學動畫影片</p>

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
            disabled={submitting || !topic.trim()}
            className="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-slate-950 disabled:opacity-50 disabled:cursor-not-allowed px-5 py-2.5 rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-300 min-h-11 cursor-pointer"
          >
            {submitting ? (
              <Loader2 className="size-4 animate-spin" aria-hidden="true" />
            ) : (
              <Send className="size-4" aria-hidden="true" />
            )}
            {submitting ? "生成中…" : "生成"}
          </button>
        </form>

        <div className="max-w-2xl mx-auto">
          <ProgressPanel
            label="本系統（5-Agent Pipeline）"
            run={sysRun}
            color="emerald"
            onCancel={() => cancelRun(setSysRun, sysInterval)}
          />
        </div>
      </div>
    </div>
  );
}
