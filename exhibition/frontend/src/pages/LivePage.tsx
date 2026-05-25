import { useEffect, useRef, useState } from "react";
import { getTask, postGenerate } from "../api/client";
import type { TaskResponse } from "../types";

interface RunState {
  taskId: string | null;
  task: TaskResponse | null;
  error: string | null;
}

const EMPTY: RunState = { taskId: null, task: null, error: null };

function ProgressPanel({
  label,
  run,
  color,
}: {
  label: string;
  run: RunState;
  color: "red" | "green";
}) {
  const c = color === "red" ? "border-red-700 bg-red-950/20" : "border-green-700 bg-green-950/20";
  const bar = color === "red" ? "bg-red-500" : "bg-green-500";
  const text = color === "red" ? "text-red-400" : "text-green-400";

  return (
    <div className={`border-2 ${c} rounded-xl p-4 flex-1`}>
      <div className={`font-bold text-sm mb-3 ${text}`}>{label}</div>

      {!run.taskId && !run.error && (
        <div className="text-gray-600 text-sm">等待送出…</div>
      )}

      {run.error && (
        <div className="text-red-400 text-sm">{run.error}</div>
      )}

      {run.task && (
        <div className="space-y-3">
          <div className="text-xs text-gray-400">
            狀態：
            <span className={`ml-1 font-medium ${
              run.task.status === "done"
                ? "text-green-400"
                : run.task.status === "failed"
                ? "text-red-400"
                : "text-yellow-400"
            }`}>
              {run.task.status}
            </span>
          </div>

          <div>
            <div className="flex justify-between text-xs text-gray-400 mb-1">
              <span>{run.task.progress.stage}</span>
              <span>{run.task.progress.percent}%</span>
            </div>
            <div className="bg-gray-800 rounded-full h-2">
              <div
                className={`${bar} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${run.task.progress.percent}%` }}
              />
            </div>
          </div>

          {run.task.status === "failed" && run.task.error && (
            <div className="bg-red-950/50 border border-red-800 rounded p-2 text-xs text-red-300 font-mono break-all">
              {run.task.error}
            </div>
          )}

          {run.task.status === "done" && run.task.artifacts.video_url && (
            <video
              src={run.task.artifacts.video_url}
              controls
              autoPlay
              className="w-full rounded bg-black aspect-video"
            />
          )}

          {run.task.status === "done" &&
            run.task.artifacts.vision_verdict &&
            run.task.artifacts.vision_verdict.verdict !== "ERROR" && (
            <div className="text-xs">
              <span className="text-gray-400">Vision QA: </span>
              <span
                className={
                  run.task.artifacts.vision_verdict.verdict === "PASS"
                    ? "text-green-400"
                    : "text-red-400"
                }
              >
                {run.task.artifacts.vision_verdict.verdict}
              </span>
            </div>
          )}

          {run.task.artifacts.logs && run.task.artifacts.logs.length > 0 && (
            <div className="bg-black/50 rounded p-2 max-h-32 overflow-y-auto">
              {run.task.artifacts.logs.map((log, i) => (
                <div key={i} className="text-xs text-gray-400 font-mono">
                  {log}
                </div>
              ))}
            </div>
          )}

          <div className="text-xs text-gray-600">{Math.floor(run.task.duration_sec)}s elapsed</div>
        </div>
      )}
    </div>
  );
}

export function LivePage() {
  const [available, setAvailable] = useState<boolean | null>(null);
  const [topic, setTopic] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [opusRun, setOpusRun] = useState<RunState>(EMPTY);
  const [sysRun, setSysRun] = useState<RunState>(EMPTY);
  const opusInterval = useRef<ReturnType<typeof setInterval> | null>(null);
  const sysInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  // Probe if /api/generate is available (200 = live, 501 = not implemented)
  useEffect(() => {
    fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic: "__probe__", mode: "opus_only" }),
    })
      .then((r) => setAvailable(r.status !== 501))
      .catch(() => setAvailable(false));
  }, []);

  function poll(taskId: string, setter: typeof setOpusRun, intervalRef: typeof opusInterval) {
    intervalRef.current = setInterval(async () => {
      try {
        const task = await getTask(taskId);
        setter((prev) => ({ ...prev, task }));
        if (task.status === "done" || task.status === "failed") {
          clearInterval(intervalRef.current!);
        }
      } catch (e) {
        setter((prev) => ({ ...prev, error: String(e) }));
        clearInterval(intervalRef.current!);
      }
    }, 2000);
  }

  async function handleSubmit() {
    if (!topic.trim()) return;
    setSubmitting(true);
    setOpusRun(EMPTY);
    setSysRun(EMPTY);

    try {
      const [opusRes, sysRes] = await Promise.all([
        postGenerate(topic, "opus_only"),
        postGenerate(topic, "full_system"),
      ]);

      if (!opusRes || !sysRes) {
        setAvailable(false);
        return;
      }

      setOpusRun({ taskId: opusRes.task_id, task: null, error: null });
      setSysRun({ taskId: sysRes.task_id, task: null, error: null });
      poll(opusRes.task_id, setOpusRun, opusInterval);
      poll(sysRes.task_id, setSysRun, sysInterval);
    } catch (e) {
      setOpusRun({ taskId: null, task: null, error: String(e) });
    } finally {
      setSubmitting(false);
    }
  }

  if (available === false) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🚧</div>
          <h2 className="text-2xl font-bold text-gray-300 mb-2">Live 模式尚未開放</h2>
          <p className="text-gray-500">後端 /api/generate 尚未實作（501）</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-extrabold text-center mb-2">Live 對比生成</h1>
        <p className="text-gray-400 text-center mb-8">輸入數學主題，即時觀看兩個系統生成影片</p>

        <div className="flex gap-3 mb-10 max-w-xl mx-auto">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="輸入數學主題，例如：畢氏定理"
            className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500"
          />
          <button
            onClick={handleSubmit}
            disabled={submitting || !topic.trim()}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed px-5 py-2.5 rounded-lg font-medium transition-colors"
          >
            {submitting ? "生成中…" : "生成"}
          </button>
        </div>

        <div className="flex gap-4">
          <ProgressPanel label="Opus 一發直出" run={opusRun} color="red" />
          <ProgressPanel label="本系統（5-Agent Pipeline）" run={sysRun} color="green" />
        </div>
      </div>
    </div>
  );
}
