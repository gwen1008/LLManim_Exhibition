import { useEffect, useMemo, useState } from "react";
import { AlertCircle, Inbox } from "lucide-react";
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
    // showcase 項無 Opus 對比，所有對比數據只看對比項
    const cmp = items.filter((i) => !i.showcase_only);
    const cmpTotal = cmp.length;
    const showcaseCount = total - cmpTotal;
    const opusFail = cmp.filter((i) => !i.opus_metrics?.render_success).length;
    const sysFail = cmp.filter((i) => !i.system_metrics.render_success).length;
    // 影片長度比：只在對比項上，系統 vs opus
    const opusDur = cmp
      .map((i) => i.opus_metrics?.video_duration_sec)
      .filter((v): v is number => typeof v === "number");
    const sysDur = cmp
      .map((i) => i.system_metrics.video_duration_sec)
      .filter((v): v is number => typeof v === "number");
    const opusAvg = opusDur.length > 0 ? opusDur.reduce((a, b) => a + b, 0) / opusDur.length : 0;
    const sysAvg = sysDur.length > 0 ? sysDur.reduce((a, b) => a + b, 0) / sysDur.length : 0;
    const ratio = opusAvg > 0 ? sysAvg / opusAvg : 0;
    return { total, cmpTotal, showcaseCount, opusFail, sysFail, ratio };
  }, [items]);

  if (!stats) return null;

  return (
    <div className="mt-6 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm">
      <div className="inline-flex items-baseline gap-1.5">
        <span className="text-emerald-300 font-bold tabular-nums text-lg">
          {stats.showcaseCount}
        </span>
        <span className="text-gray-400">部能力展示</span>
      </div>
      <span className="text-gray-700" aria-hidden="true">·</span>
      <div className="inline-flex items-baseline gap-1.5">
        <span className="text-rose-300 font-bold tabular-nums text-lg">
          {stats.opusFail}/{stats.cmpTotal}
        </span>
        <span className="text-gray-400">對比中直出失敗</span>
      </div>
      <span className="text-gray-700" aria-hidden="true">·</span>
      <div className="inline-flex items-baseline gap-1.5">
        <span className="text-emerald-300 font-bold tabular-nums text-lg">
          {stats.cmpTotal - stats.sysFail}/{stats.cmpTotal}
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
    // showcase 項無 Opus 對比，不計入對比類統計
    const cmp = items.filter((i) => !i.showcase_only);
    const opusFail = cmp.filter((i) => !i.opus_metrics?.render_success).length;
    const bothOk = cmp.filter(
      (i) => i.opus_metrics?.render_success && i.system_metrics.render_success
    ).length;
    return { all: items.length, opus_fail: opusFail, both_success: bothOk };
  }, [items]);

  const showcaseItems = useMemo(() => items.filter((i) => i.showcase_only), [items]);
  const comparisonItems = useMemo(() => items.filter((i) => !i.showcase_only), [items]);

  const filtered = useMemo(() => {
    if (filter === "opus_fail")
      return items.filter((i) => !i.showcase_only && !i.opus_metrics?.render_success);
    if (filter === "both_success")
      return items.filter(
        (i) => !i.showcase_only && i.opus_metrics?.render_success && i.system_metrics.render_success
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
            從一句話，到
            <span className="text-emerald-300">會說話的數學動畫</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-200 mb-2 inline-flex flex-wrap items-center justify-center gap-2">
            <span className="text-emerald-300 font-semibold">本系統（Multi-Agent Pipeline）</span>
            <span className="text-gray-500">·</span>
            <span className="text-gray-300">能力展示</span>
            <span className="text-gray-500">＋</span>
            <span className="text-rose-300">Opus 裸跑對比</span>
          </p>
          <p className="text-gray-400 text-sm mt-4 max-w-2xl mx-auto leading-relaxed">
            上半部「系統能力展示」：把數學主題交給完整 pipeline（Translator → Planner → RAG → Coder → VisionQA → Reflexion），
            自動生成帶旁白與字幕的動畫。下半部「Opus 裸跑對比」：相同 Prompt 下，零樣本 Opus（僅給「請寫一個 ManimCE 場景」、不給範例、不修正）與本系統的並排對照。
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
            {filter === "all" ? (
              <div className="space-y-12">
                {showcaseItems.length > 0 && (
                  <section aria-labelledby="sec-showcase">
                    <div className="mb-5 border-l-4 border-emerald-500 pl-3">
                      <h2 id="sec-showcase" className="text-2xl font-bold text-white">
                        系統能力展示
                      </h2>
                      <p className="text-gray-400 text-sm mt-1">
                        本系統自動生成的數學動畫，展現對複雜題型的視覺化能力
                      </p>
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {showcaseItems.map((item) => (
                        <ComparisonCard key={item.id} item={item} />
                      ))}
                    </div>
                  </section>
                )}
                {comparisonItems.length > 0 && (
                  <section aria-labelledby="sec-comparison">
                    <div className="mb-5 border-l-4 border-rose-500 pl-3">
                      <h2 id="sec-comparison" className="text-2xl font-bold text-white">
                        Opus 裸跑 vs 本系統
                      </h2>
                      <p className="text-gray-400 text-sm mt-1">
                        相同 Prompt 下，零樣本 Opus 與本系統 5-Agent Pipeline 的並排對比
                      </p>
                    </div>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                      {comparisonItems.map((item) => (
                        <ComparisonCard key={item.id} item={item} />
                      ))}
                    </div>
                  </section>
                )}
              </div>
            ) : filtered.length === 0 ? (
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
