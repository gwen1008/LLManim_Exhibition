import { useEffect, useMemo, useState } from "react";
import { AlertCircle, ArrowRight, Inbox } from "lucide-react";
import { getGallery } from "../api/client";
import { ComparisonCard } from "../components/ComparisonCard";
import type { GalleryItem } from "../types";

type Filter = "all" | "opus_fail" | "both_success";

function CardSkeleton() {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden animate-pulse">
      <div className="px-4 py-3 border-b border-gray-800 flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="h-5 bg-gray-800 rounded w-3/4" />
          <div className="h-3 bg-gray-800 rounded w-1/3 mt-2" />
        </div>
        <div className="h-5 w-20 bg-gray-800 rounded-full shrink-0" />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2">
        <div className="aspect-video bg-gray-800" />
        <div className="aspect-video bg-gray-800 sm:border-l border-t sm:border-t-0 border-gray-900" />
      </div>
      <div className="px-4 py-3 space-y-2">
        <div className="h-3 bg-gray-800 rounded w-1/2 ml-auto" />
        <div className="h-3 bg-gray-800 rounded" />
        <div className="h-3 bg-gray-800 rounded w-5/6" />
        <div className="h-3 bg-gray-800 rounded w-4/6" />
        <div className="h-8 bg-gray-800 rounded mt-3" />
      </div>
    </div>
  );
}

function HeroStats({ items }: { items: GalleryItem[] }) {
  const stats = useMemo(() => {
    const total = items.length;
    if (total === 0) return null;
    const opusFail = items.filter((i) => !i.opus_metrics.render_success).length;
    const sysFail = items.filter((i) => !i.system_metrics.render_success).length;
    const opusDur = items
      .map((i) => i.opus_metrics.video_duration_sec)
      .filter((v): v is number => typeof v === "number");
    const sysDur = items
      .map((i) => i.system_metrics.video_duration_sec)
      .filter((v): v is number => typeof v === "number");
    const opusAvg = opusDur.length > 0 ? opusDur.reduce((a, b) => a + b, 0) / opusDur.length : 0;
    const sysAvg = sysDur.length > 0 ? sysDur.reduce((a, b) => a + b, 0) / sysDur.length : 0;
    const ratio = opusAvg > 0 ? sysAvg / opusAvg : 0;
    return { total, opusFail, sysFail, ratio };
  }, [items]);

  if (!stats) return null;

  return (
    <div className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm">
      <div className="inline-flex items-baseline gap-1.5">
        <span className="text-rose-300 font-bold tabular-nums text-lg">
          {stats.opusFail}/{stats.total}
        </span>
        <span className="text-gray-400">直出失敗</span>
      </div>
      <span className="text-gray-700" aria-hidden="true">·</span>
      <div className="inline-flex items-baseline gap-1.5">
        <span className="text-emerald-300 font-bold tabular-nums text-lg">
          {stats.total - stats.sysFail}/{stats.total}
        </span>
        <span className="text-gray-400">本系統成功</span>
      </div>
      {stats.ratio > 0 && (
        <>
          <span className="text-gray-700" aria-hidden="true">·</span>
          <div className="inline-flex items-baseline gap-1.5">
            <span className="text-emerald-300 font-bold tabular-nums text-lg">
              {stats.ratio.toFixed(1)}×
            </span>
            <span className="text-gray-400">平均影片長度</span>
          </div>
        </>
      )}
    </div>
  );
}

function FilterTabs({
  value,
  onChange,
  counts,
}: {
  value: Filter;
  onChange: (v: Filter) => void;
  counts: Record<Filter, number>;
}) {
  const tabs: { key: Filter; label: string }[] = [
    { key: "all", label: "全部" },
    { key: "opus_fail", label: "直出失敗對比" },
    { key: "both_success", label: "兩邊都成功" },
  ];
  return (
    <div
      role="tablist"
      aria-label="篩選對比類型"
      className="flex flex-wrap gap-2 mb-6"
    >
      {tabs.map((t) => {
        const active = value === t.key;
        return (
          <button
            key={t.key}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => onChange(t.key)}
            className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors min-h-9 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 cursor-pointer ${
              active
                ? "bg-emerald-500 text-slate-950 border border-emerald-400"
                : "bg-gray-900 text-gray-300 border border-gray-800 hover:border-gray-700 hover:text-white"
            }`}
          >
            <span>{t.label}</span>
            <span
              className={`tabular-nums text-[10px] px-1.5 py-0.5 rounded ${
                active ? "bg-slate-950/20 text-slate-950" : "bg-gray-800 text-gray-400"
              }`}
            >
              {counts[t.key]}
            </span>
          </button>
        );
      })}
    </div>
  );
}

export function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<Filter>("all");

  useEffect(() => {
    getGallery()
      .then((data) => setItems(data.items))
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  const counts: Record<Filter, number> = useMemo(() => {
    const opusFail = items.filter((i) => !i.opus_metrics.render_success).length;
    const bothOk = items.filter(
      (i) => i.opus_metrics.render_success && i.system_metrics.render_success
    ).length;
    return { all: items.length, opus_fail: opusFail, both_success: bothOk };
  }, [items]);

  const filtered = useMemo(() => {
    if (filter === "opus_fail") return items.filter((i) => !i.opus_metrics.render_success);
    if (filter === "both_success")
      return items.filter(
        (i) => i.opus_metrics.render_success && i.system_metrics.render_success
      );
    return items;
  }, [items, filter]);

  return (
    <div className="min-h-dvh bg-gray-950 text-white">
      {/* Hero */}
      <section className="relative bg-gradient-to-b from-gray-900 to-gray-950 border-b border-gray-800 px-6 py-16 text-center overflow-hidden">
        <div
          aria-hidden="true"
          className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(34,197,94,0.10),transparent_60%)]"
        />
        <div className="relative max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            同樣的 Prompt，
            <span className="text-rose-300">差距有多大？</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-200 mb-2 inline-flex flex-wrap items-center justify-center gap-2">
            <span className="text-rose-300 font-semibold">Opus 裸跑（zero-shot）</span>
            <ArrowRight className="size-4 text-gray-500" aria-hidden="true" />
            <span className="text-emerald-300 font-semibold">本系統（Multi-Agent Pipeline）</span>
          </p>
          <p className="text-gray-400 text-sm mt-4 max-w-2xl mx-auto leading-relaxed">
            每組影片使用完全相同的數學主題。左邊：把 topic 直接丟給 Opus，僅給「請寫一個 ManimCE 場景」最小指令、不給範例、不給 Planner 藍圖、不修正。
            右邊：完整 pipeline（Translator → Planner → RAG → Coder → VisionQA → Reflexion）。
          </p>
          {!loading && !error && <HeroStats items={items} />}
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 py-10">
        {loading && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" aria-busy="true" aria-label="載入中">
            {Array.from({ length: 4 }).map((_, i) => (
              <CardSkeleton key={i} />
            ))}
          </div>
        )}

        {error && (
          <div
            role="alert"
            className="bg-rose-950/40 border border-rose-800/60 rounded-lg p-6 text-center text-rose-300 flex flex-col items-center gap-2"
          >
            <AlertCircle className="size-6" aria-hidden="true" />
            <span>資料載入失敗：{error}</span>
          </div>
        )}

        {!loading && !error && items.length === 0 && (
          <div className="text-center text-gray-400 py-20 flex flex-col items-center gap-3">
            <Inbox className="size-10 text-gray-600" aria-hidden="true" />
            <span>尚無資料</span>
          </div>
        )}

        {!loading && !error && items.length > 0 && (
          <>
            <FilterTabs value={filter} onChange={setFilter} counts={counts} />
            {filtered.length === 0 ? (
              <div className="text-center text-gray-500 py-16 flex flex-col items-center gap-3">
                <Inbox className="size-10 text-gray-700" aria-hidden="true" />
                <span>此分類下沒有對比項目</span>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {filtered.map((item) => (
                  <ComparisonCard key={item.id} item={item} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
