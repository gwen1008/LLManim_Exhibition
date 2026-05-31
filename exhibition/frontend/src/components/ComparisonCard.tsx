import { useRef, useState } from "react";
import { CheckCircle2, ChevronRight, FileText, Pause, Play, Trophy, XCircle } from "lucide-react";
import type { GalleryItem, ArmMetrics } from "../types";
import { FairnessDisclaimer } from "./FairnessDisclaimer";

function WinnerBadge({ winner }: { winner: "system" | "opus" | null }) {
  if (!winner) return null;
  const isSystem = winner === "system";
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${
        isSystem
          ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/40"
          : "bg-rose-500/15 text-rose-300 border-rose-500/40"
      }`}
    >
      <Trophy className="size-3" aria-hidden="true" />
      {isSystem ? "本系統勝" : "裸跑勝"}
    </span>
  );
}

interface Props {
  item: GalleryItem;
}

function fmt(v: number | string | null | undefined, suffix = ""): string {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") {
    const s = Number.isInteger(v) ? v.toString() : v.toFixed(1);
    return s + suffix;
  }
  return String(v) + suffix;
}

function MetricRow({
  label,
  opusVal,
  sysVal,
  lowerIsBetter = true,
  neutral = false,
}: {
  label: string;
  opusVal: string;
  sysVal: string;
  lowerIsBetter?: boolean;
  neutral?: boolean;
}) {
  const opusNum = parseFloat(opusVal);
  const sysNum = parseFloat(sysVal);
  const valid = !isNaN(opusNum) && !isNaN(sysNum) && opusVal !== "—" && sysVal !== "—";
  const opusBetter =
    !neutral && valid ? (lowerIsBetter ? opusNum < sysNum : opusNum > sysNum) : false;
  const sysBetter = !neutral && valid && !opusBetter && opusNum !== sysNum;
  const baseColor = neutral ? "text-gray-200" : "text-gray-400";

  return (
    <div className="flex justify-between text-xs py-1">
      <span className="text-gray-300">{label}</span>
      <div className="flex gap-4 tabular-nums">
        <span
          className={`w-20 text-right ${
            opusBetter ? "text-emerald-400 font-semibold" : valid && !neutral ? "text-rose-300" : baseColor
          }`}
        >
          {opusVal}
        </span>
        <span
          className={`w-20 text-right ${
            sysBetter ? "text-emerald-400 font-semibold" : valid && !neutral ? "text-rose-300" : baseColor
          }`}
        >
          {sysVal}
        </span>
      </div>
    </div>
  );
}

function RenderBadge({ success }: { success: boolean }) {
  const Icon = success ? CheckCircle2 : XCircle;
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold ${
        success
          ? "bg-emerald-900/40 text-emerald-300 border border-emerald-700/60"
          : "bg-rose-900/40 text-rose-300 border border-rose-700/60"
      }`}
    >
      <Icon className="size-3" aria-hidden="true" />
      {success ? "成功" : "失敗"}
    </span>
  );
}

export function ComparisonCard({ item }: Props) {
  const om: ArmMetrics = item.opus_metrics;
  const sm: ArmMetrics = item.system_metrics;
  const opusVideoRef = useRef<HTMLVideoElement>(null);
  const sysVideoRef = useRef<HTMLVideoElement>(null);
  const [syncPlaying, setSyncPlaying] = useState(false);

  let winner: "system" | "opus" | null = null;
  if (om.render_success !== sm.render_success) {
    winner = sm.render_success ? "system" : "opus";
  }

  const canSync = om.render_success && sm.render_success;

  const handleSyncToggle = async () => {
    const a = opusVideoRef.current;
    const b = sysVideoRef.current;
    if (!a || !b) return;
    if (syncPlaying) {
      a.pause();
      b.pause();
      setSyncPlaying(false);
      return;
    }
    a.currentTime = 0;
    b.currentTime = 0;
    setSyncPlaying(true);
    try {
      await Promise.all([a.play(), b.play()]);
    } catch {
      setSyncPlaying(false);
    }
  };

  return (
    <article
      className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden shadow-lg shadow-black/20 hover:border-gray-700 transition-colors"
      aria-labelledby={`card-${item.id}-title`}
    >
      <header className="px-4 py-3 border-b border-gray-800 flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h3 id={`card-${item.id}-title`} className="text-white font-semibold text-base leading-snug">
            {item.topic}
          </h3>
          <p className="text-gray-500 text-xs mt-0.5 font-mono">{item.id}</p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <WinnerBadge winner={winner} />
          {canSync && (
            <button
              type="button"
              onClick={handleSyncToggle}
              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-[11px] font-bold uppercase tracking-wider transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 cursor-pointer min-h-8"
              aria-label={syncPlaying ? "暫停同步播放" : "同步播放兩部影片"}
            >
              {syncPlaying ? (
                <Pause className="size-3" aria-hidden="true" />
              ) : (
                <Play className="size-3" aria-hidden="true" />
              )}
              <span>同步播放</span>
            </button>
          )}
        </div>
      </header>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-0">
        {/* Baseline side */}
        <div className="border-b sm:border-b-0 sm:border-r border-gray-800">
          <div className="bg-rose-950/40 px-3 py-1.5 text-center">
            <span className="text-rose-300 text-[11px] font-bold uppercase tracking-wider">
              Opus 裸跑 · Zero-Shot
            </span>
          </div>
          <div className="relative bg-black aspect-video">
            {om.render_success ? (
              <video
                ref={opusVideoRef}
                src={item.opus_video_url}
                poster={`/static/thumbs/opus/${item.id}.jpg`}
                controls
                playsInline
                className="w-full h-full object-contain"
                preload="metadata"
                onPause={() => setSyncPlaying(false)}
                onEnded={() => setSyncPlaying(false)}
                aria-label={`Opus 裸跑影片 — ${item.topic}`}
              />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 px-3">
                <XCircle className="size-9 text-rose-400" aria-hidden="true" />
                <span className="text-rose-300 text-sm font-medium">Render Failed</span>
                {om.notes && (
                  <span className="text-gray-500 text-[11px] text-center line-clamp-2">
                    {om.notes.split("\n").slice(-1)[0]}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        {/* System side */}
        <div>
          <div className="bg-emerald-950/40 px-3 py-1.5 text-center">
            <span className="text-emerald-300 text-[11px] font-bold uppercase tracking-wider">
              本系統（5-Agent Pipeline）
            </span>
          </div>
          <div className="relative bg-black aspect-video">
            {sm.render_success ? (
              <video
                ref={sysVideoRef}
                src={item.system_video_url}
                poster={`/static/thumbs/system/${item.id}.jpg`}
                controls
                playsInline
                className="w-full h-full object-contain"
                preload="metadata"
                onPause={() => setSyncPlaying(false)}
                onEnded={() => setSyncPlaying(false)}
                aria-label={`本系統影片 — ${item.topic}`}
              />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
                <XCircle className="size-9 text-rose-400" aria-hidden="true" />
                <span className="text-rose-300 text-sm font-medium">Render Failed</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="px-4 py-3">
        <div className="grid grid-cols-[1fr_auto] gap-4 text-xs mb-2">
          <span className="sr-only">指標</span>
          <div className="flex gap-4">
            <span className="w-20 text-right text-rose-300 font-medium">裸跑</span>
            <span className="w-20 text-right text-emerald-300 font-medium">本系統</span>
          </div>
        </div>

        <div className="space-y-0">
          <div className="flex justify-between text-xs py-1">
            <span className="text-gray-300">Render 結果</span>
            <div className="flex gap-4 items-center">
              <span className="w-20 inline-flex justify-end">
                <RenderBadge success={om.render_success} />
              </span>
              <span className="w-20 inline-flex justify-end">
                <RenderBadge success={sm.render_success} />
              </span>
            </div>
          </div>
          <MetricRow
            label="影片時長"
            opusVal={fmt(om.video_duration_sec, "s")}
            sysVal={fmt(sm.video_duration_sec, "s")}
            lowerIsBetter={false}
          />
        </div>

        {item.topic_prompt && (
          <details className="mt-2 group [&>summary]:list-none [&>summary::-webkit-details-marker]:hidden">
            <summary className="text-xs text-gray-400 cursor-pointer hover:text-gray-300 select-none inline-flex items-center gap-1.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 rounded">
              <ChevronRight className="size-3 transition-transform group-open:rotate-90" aria-hidden="true" />
              <FileText className="size-4" aria-hidden="true" />
              原始 Prompt
            </summary>
            <p className="mt-1 text-xs text-gray-300 leading-relaxed">{item.topic_prompt}</p>
          </details>
        )}

        <FairnessDisclaimer />
      </div>
    </article>
  );
}
