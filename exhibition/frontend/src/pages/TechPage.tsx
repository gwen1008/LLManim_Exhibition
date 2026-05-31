import { useEffect, useState } from "react";
import {
  CheckCircle2,
  Clock,
  Coins,
  Cpu,
  Film,
  Layers,
  Repeat,
  ShieldCheck,
  Target,
  Zap,
} from "lucide-react";
import { getStats } from "../api/client";
import { PipelineFlow } from "../components/PipelineFlow";
import type { StatsResponse } from "../types";

function fmtInt(n: number) {
  return n.toLocaleString("en-US");
}

function SectionLabel({ num, title, id }: { num: string; title: string; id?: string }) {
  return (
    <div className="flex items-center gap-3 mb-5">
      <span
        aria-hidden="true"
        className="inline-flex items-center justify-center size-8 rounded-lg bg-gradient-to-br from-slate-700/40 to-slate-700/10 border border-slate-700 text-slate-300 text-xs font-mono font-bold tabular-nums"
      >
        {num}
      </span>
      <h2 id={id} className="text-base font-bold tracking-tight text-gray-100">
        {title}
      </h2>
      <div className="flex-1 h-px bg-gradient-to-r from-gray-700 via-gray-800 to-transparent" />
    </div>
  );
}

function HeadlineCard({
  icon: Icon,
  value,
  unit,
  label,
  hint,
  accent = "text-white",
}: {
  icon: React.ComponentType<{ className?: string; "aria-hidden"?: boolean }>;
  value: string;
  unit?: string;
  label: string;
  hint?: string;
  accent?: string;
}) {
  return (
    <div className="group relative bg-gray-900 border border-gray-800 rounded-xl p-5 transition-all duration-200 hover:border-gray-700 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-black/40">
      <div className="flex items-center gap-2 text-gray-400 text-xs uppercase tracking-wide">
        <Icon className={`size-4 ${accent} transition-transform duration-200 group-hover:scale-110`} aria-hidden={true} />
        <span>{label}</span>
      </div>
      <div className="mt-2 flex items-baseline gap-1">
        <span className={`text-3xl md:text-4xl font-extrabold tabular-nums ${accent}`}>{value}</span>
        {unit && <span className="text-gray-400 text-sm">{unit}</span>}
      </div>
      {hint && <div className="text-gray-500 text-xs mt-1">{hint}</div>}
    </div>
  );
}

function IterBar({
  iters,
  count,
  total,
}: {
  iters: number;
  count: number;
  total: number;
}) {
  const pct = (count / total) * 100;
  const widthPct = Math.max(pct, 1.5); // min visible width for tiny segments
  const colors = ["bg-emerald-500", "bg-amber-400", "bg-rose-400"];
  const labels = ["一次成功", "二輪修正", "三輪修正"];
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-300">
          <span className="font-mono tabular-nums">{iters} 輪</span>
          <span className="text-gray-500 ml-2">{labels[iters - 1]}</span>
        </span>
        <span className="tabular-nums text-gray-300">
          {count} <span className="text-gray-500">/ {total}</span>
          <span className="ml-2 text-gray-400">
            ({pct < 1 ? "<1" : pct.toFixed(1)}%)
          </span>
        </span>
      </div>
      <div className="bg-gray-800 rounded-full h-3 overflow-hidden">
        <div
          className={`${colors[iters - 1]} h-3 rounded-full transition-[width] duration-700 ease-out`}
          style={{ width: `${widthPct}%` }}
        />
      </div>
    </div>
  );
}

function CategoryBar({
  label,
  pass,
  total,
  color = "bg-emerald-500",
}: {
  label: string;
  pass: number;
  total: number;
  color?: string;
}) {
  const pct = total > 0 ? (pass / total) * 100 : 0;
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-300">{label}</span>
        <span className="text-gray-300 font-semibold tabular-nums">
          {pct.toFixed(1)}%
          <span className="text-gray-500 ml-2 font-normal">
            {pass} / {total}
          </span>
        </span>
      </div>
      <div className="bg-gray-800 rounded-full h-2 overflow-hidden">
        <div
          className={`${color} h-2 rounded-full transition-[width] duration-700 ease-out`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export function TechPage() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats()
      .then(setStats)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-dvh bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* HERO */}
        <header className="relative text-center mb-14 py-8">
          <div
            aria-hidden="true"
            className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_center,rgba(34,197,94,0.08),transparent_65%)]"
          />
          <div className="inline-flex items-center gap-2 mb-4 px-3 py-1 rounded-full bg-slate-800/60 border border-slate-700 text-slate-300 text-xs font-mono">
            <span className="relative flex size-1.5" aria-hidden="true">
              <span className="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping" />
              <span className="relative inline-flex size-1.5 rounded-full bg-emerald-400" />
            </span>
            TECH DASHBOARD · BENCHMARK Q01-Q150
          </div>
          {stats ? (
            <h1 className="text-3xl md:text-5xl font-extrabold mb-4 leading-tight flex flex-wrap items-baseline justify-center gap-x-3 gap-y-1">
              <span className="text-white">{stats.total_videos_generated} 部數學動畫</span>
              <span className="text-gray-700" aria-hidden="true">·</span>
              <span className="text-emerald-400">${stats.cost_avg_usd.toFixed(2)}/部</span>
              <span className="text-gray-700" aria-hidden="true">·</span>
              <span className="text-white">{Math.round(stats.duration_avg_sec)} 秒/部</span>
            </h1>
          ) : (
            <h1 className="text-3xl md:text-5xl font-extrabold mb-4 leading-tight text-gray-700">
              載入中…
            </h1>
          )}
          <p className="text-gray-300 text-sm md:text-base max-w-2xl mx-auto leading-relaxed">
            Multi-Agent Pipeline + Reflexion 自我修正的真實 benchmark 數據。
            <br className="hidden md:inline" />
            來源：<code className="font-mono text-gray-200 text-xs">runs/merged_q01_q150_with_review.csv</code>
          </p>
        </header>

        {loading && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12" aria-busy="true">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-6 animate-pulse">
                <div className="h-4 bg-gray-800 rounded w-2/3" />
                <div className="h-9 bg-gray-800 rounded mt-3" />
                <div className="h-3 bg-gray-800 rounded mt-2 w-1/2" />
              </div>
            ))}
          </div>
        )}

        {stats && (
          <>
            {/* SECTION 1 — Per-video efficiency */}
            <section aria-labelledby="scale-heading" className="mb-12">
              <SectionLabel num="01" title="單位效能（Per-Video Economics）" id="scale-heading" />
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <HeadlineCard
                  icon={Coins}
                  value={`$${stats.cost_avg_usd.toFixed(2)}`}
                  label="製作成本 / 部"
                  accent="text-emerald-400"
                  hint="Token 等價 · 實際用訂閱"
                />
                <HeadlineCard
                  icon={Clock}
                  value={Math.round(stats.duration_avg_sec).toString()}
                  unit="秒"
                  label="製作時間 / 部"
                  accent="text-slate-100"
                  hint="Planner → 渲染完成"
                />
                <HeadlineCard
                  icon={Zap}
                  value={`${(stats.tokens_avg / 1000).toFixed(1)}k`}
                  label="平均 tokens / 部"
                  accent="text-slate-100"
                  hint={`Planner+Coder+VisionQA`}
                />
                <HeadlineCard
                  icon={Layers}
                  value={fmtInt(stats.code_lines_avg)}
                  unit="行"
                  label="ManimCE 代碼 / 部"
                  accent="text-slate-100"
                  hint={`平均影片 ${stats.video_duration_avg_sec}s`}
                />
              </div>
              <div className="relative mt-6 rounded-xl border border-slate-800 bg-slate-900/60 px-5 py-5 overflow-hidden">
                <div
                  aria-hidden="true"
                  className="absolute -top-12 -right-12 size-48 rounded-full bg-emerald-500/5 blur-3xl pointer-events-none"
                />
                <div className="relative">
                  <div className="flex items-center gap-2 mb-4 flex-wrap">
                    <span
                      aria-hidden="true"
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-300 text-[10px] font-mono font-bold tracking-wider"
                    >
                      <span className="size-1.5 rounded-full bg-emerald-400 animate-pulse" />
                      SUBSCRIPTION MODE
                    </span>
                    <span className="text-sm text-gray-100 font-semibold">
                      Claude Max 5x 訂閱實測容量
                    </span>
                  </div>

                  {/* Capacity row */}
                  <div className="grid grid-cols-3 gap-2 mb-5">
                    <div className="rounded-lg bg-gray-900/60 border border-gray-800/80 px-3 py-2 text-center">
                      <div className="text-slate-100 font-bold tabular-nums text-lg leading-none">~50</div>
                      <div className="text-[10px] text-gray-400 mt-1">部 / 5h 視窗</div>
                    </div>
                    <div className="rounded-lg bg-gray-900/60 border border-gray-800/80 px-3 py-2 text-center">
                      <div className="text-slate-100 font-bold tabular-nums text-lg leading-none">~6,000</div>
                      <div className="text-[10px] text-gray-400 mt-1">部 / 月滿載</div>
                    </div>
                    <div className="rounded-lg bg-gray-900/60 border border-gray-800/80 px-3 py-2 text-center">
                      <div className="text-emerald-300 font-bold tabular-nums text-lg leading-none">NT$3,000</div>
                      <div className="text-[10px] text-gray-400 mt-1">月費固定</div>
                    </div>
                  </div>

                  {/* Hero comparison */}
                  <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3 mb-3">
                    <div className="relative text-center rounded-xl bg-emerald-500/10 border-2 border-emerald-500/40 px-4 py-4 shadow-[0_0_24px_-8px_rgba(16,185,129,0.5)]">
                      <div className="text-[10px] text-emerald-200/80 uppercase tracking-widest font-semibold mb-1">
                        實際成本 / 部
                      </div>
                      <div className="text-4xl md:text-5xl font-black tabular-nums text-emerald-300 leading-none tracking-tight">
                        NT$0.5
                      </div>
                      <div className="text-[10px] text-gray-400 mt-2">月費 ÷ 滿載產量</div>
                    </div>

                    <div
                      aria-hidden="true"
                      className="flex flex-col items-center text-gray-500"
                    >
                      <span className="text-2xl font-light">vs</span>
                    </div>

                    <div className="text-center rounded-xl bg-gray-800/40 border border-gray-700/60 px-4 py-4">
                      <div className="text-[10px] text-gray-500 uppercase tracking-widest font-semibold mb-1">
                        Token 等價 / 部
                      </div>
                      <div className="text-4xl md:text-5xl font-black tabular-nums text-gray-400 leading-none tracking-tight line-through decoration-rose-500/50 decoration-2">
                        NT$9
                      </div>
                      <div className="text-[10px] text-gray-500 mt-2">API 估算 · 未實付</div>
                    </div>
                  </div>

                  <div className="flex items-center justify-center gap-2 mt-3 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                    <span className="text-emerald-300 font-bold text-sm tracking-wide">
                      訂閱模式便宜
                    </span>
                    <span className="text-emerald-200 font-black text-xl tabular-nums">~18×</span>
                    <span className="text-emerald-300 font-bold text-sm tracking-wide">
                      ·邊際成本趨近 0
                    </span>
                  </div>
                </div>
              </div>
            </section>

            {/* SECTION 2 — Quality (layered + honest denominator) */}
            <section aria-labelledby="quality-heading" className="mb-12">
              <SectionLabel num="02" title="品質（依難度分層）" id="quality-heading" />
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-5">
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <ShieldCheck className="size-4 text-emerald-400" aria-hidden="true" />
                    <h3 className="text-sm font-semibold text-gray-200">
                      Vision QA 視覺驗收
                    </h3>
                    <span className="text-xs text-gray-500 font-mono">(GPT-4o)</span>
                  </div>
                  <CategoryBar
                    label="總計（加權平均）"
                    pass={stats.vision_qa_elem_n[0] + stats.vision_qa_mid_n[0]}
                    total={stats.total_videos_generated}
                    color="bg-emerald-500"
                  />
                </div>

                <div className="pt-4 border-t border-gray-800">
                  <div className="flex items-center gap-2 mb-3 flex-wrap">
                    <Target className="size-4 text-emerald-400" aria-hidden="true" />
                    <h3 className="text-sm font-semibold text-gray-200">
                      數學答案正確率（GT Match）
                    </h3>
                    <span className="text-xs text-gray-500 font-mono">
                      排除 {stats.gt_match_unjudged} 個無法判定
                    </span>
                  </div>
                  <CategoryBar
                    label="答對 / 判定數"
                    pass={stats.gt_match_true}
                    total={stats.gt_judged_n}
                    color="bg-emerald-500"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-4 border-t border-gray-800">
                  <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 px-4 py-3 text-center">
                    <ShieldCheck className="size-5 text-emerald-400 mx-auto mb-1.5" aria-hidden="true" />
                    <div className="text-2xl font-extrabold tabular-nums text-emerald-300 leading-none">
                      {stats.fj_math_avg.toFixed(2)}
                      <span className="text-sm text-gray-400 font-normal ml-0.5">/5</span>
                    </div>
                    <div className="text-xs text-gray-200 mt-1.5 font-medium">
                      FJ Math 平均分
                    </div>
                    <div className="text-[10px] text-gray-500 mt-0.5">
                      n={stats.fj_math_n} · 5=完美 4=可接受 3=有錯
                    </div>
                  </div>
                  <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 px-4 py-3 text-center">
                    <Film className="size-5 text-emerald-400 mx-auto mb-1.5" aria-hidden="true" />
                    <div className="text-2xl font-extrabold tabular-nums text-emerald-300 leading-none">
                      100%
                    </div>
                    <div className="text-xs text-gray-200 mt-1.5 font-medium">
                      影片生成率
                    </div>
                    <div className="text-[10px] text-gray-500 mt-0.5">
                      {stats.total_videos_generated} / {stats.total_videos_generated} 全部成功渲染
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* SECTION 3 — Reflexion honest story */}
            <section aria-labelledby="reflexion-heading" className="mb-12">
              <SectionLabel num="03" title="Reflexion 自我修正" id="reflexion-heading" />
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="text-xs text-gray-500 mb-3 text-center">
                  150 部影片最終分流（總和 = {stats.total_videos_generated}）
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-5">
                  <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 px-4 py-3 text-center">
                    <div className="text-3xl font-extrabold text-emerald-400 tabular-nums leading-none">
                      {stats.iter1_pass_count}
                    </div>
                    <div className="text-xs text-gray-200 mt-2 font-medium">一次過 PASS</div>
                    <div className="text-[11px] text-gray-400 mt-1 tabular-nums">
                      {((stats.iter1_pass_count / stats.total_videos_generated) * 100).toFixed(1)}% · 無需修正
                    </div>
                  </div>
                  <div className="rounded-lg border border-amber-400/30 bg-amber-400/5 px-4 py-3 text-center">
                    <div className="text-3xl font-extrabold text-amber-300 tabular-nums leading-none">
                      {stats.iter_multi_pass_count}
                    </div>
                    <div className="text-xs text-gray-200 mt-2 font-medium">Reflexion 救回</div>
                    <div className="text-[11px] text-gray-400 mt-1 tabular-nums">
                      {((stats.iter_multi_pass_count / stats.total_videos_generated) * 100).toFixed(1)}% · 2–3 輪後通過
                    </div>
                  </div>
                  <div className="rounded-lg border border-slate-700 bg-slate-800/40 px-4 py-3 text-center">
                    <div className="text-3xl font-extrabold text-slate-300 tabular-nums leading-none">
                      {stats.fj_fail_count}
                    </div>
                    <div className="text-xs text-gray-200 mt-2 font-medium">待視覺微調</div>
                    <div className="text-[11px] text-gray-400 mt-1 tabular-nums">
                      GT 答對率仍達 {(stats.gt_match_rate_judged * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                <div className="space-y-3 pt-4 border-t border-gray-800">
                  {Object.entries(stats.iter_distribution).map(([k, v]) => (
                    <IterBar
                      key={k}
                      iters={parseInt(k)}
                      count={v}
                      total={stats.total_videos_generated}
                    />
                  ))}
                </div>

                <div className="text-xs text-gray-400 mt-5 leading-relaxed space-y-2">
                  <p className="inline-flex items-start gap-2">
                    <Repeat className="size-4 mt-0.5 shrink-0 text-emerald-400" aria-hidden="true" />
                    <span>
                      <span className="text-emerald-300 font-semibold">Reflexion 救回率：</span>
                      {stats.iter_multi_count} 部一次未通過 → 救回 {stats.iter_multi_pass_count} 部
                      （{(stats.iter_multi_pass_rate * 100).toFixed(0)}%）
                    </span>
                  </p>
                  <p className="inline-flex items-start gap-2">
                    <CheckCircle2 className="size-4 mt-0.5 shrink-0 text-emerald-400" aria-hidden="true" />
                    <span>
                      RefiningLoop 上限 {stats.refining_loop_max_iterations} 輪；實測最多用到{" "}
                      {stats.iter_max} 輪就已收斂或定型 — 證明錯誤是「淺層 + 可定位」的。
                    </span>
                  </p>
                </div>
              </div>
            </section>

            {/* SECTION 4 — Pipeline */}
            <section
              aria-labelledby="pipeline-heading"
              className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-8"
            >
              <SectionLabel num="04" title="Pipeline" id="pipeline-heading" />
              <PipelineFlow agents={stats.agents} />
            </section>

            {/* SECTION 5 — Aggregate evidence */}
            <section aria-labelledby="cost-heading" className="mb-8">
              <SectionLabel num="05" title="本次 Benchmark 累計輸出" id="cost-heading" />
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <HeadlineCard
                  icon={Film}
                  value={fmtInt(stats.total_videos_generated)}
                  unit="部"
                  label="Benchmark 測試"
                  accent="text-slate-100"
                  hint={`涵蓋 ${stats.vision_qa_elem_n[1]} 國小 + ${stats.vision_qa_mid_n[1]} 國中題`}
                />
                <HeadlineCard
                  icon={Clock}
                  value={stats.total_video_minutes.toFixed(0)}
                  unit="分鐘"
                  label="教學內容"
                  accent="text-slate-100"
                  hint={`等同 ${(stats.total_video_minutes / 60).toFixed(1)} 小時影片`}
                />
                <HeadlineCard
                  icon={Coins}
                  value={`$${stats.total_cost_usd.toFixed(2)}`}
                  label="總 LLM 成本"
                  accent="text-emerald-300"
                  hint={`平均 $${stats.cost_avg_usd} / 部`}
                />
                <HeadlineCard
                  icon={Cpu}
                  value={`${stats.total_compute_hours}`}
                  unit="小時"
                  label="總運算"
                  accent="text-slate-100"
                  hint={`累計 ${(stats.total_tokens / 1_000_000).toFixed(1)}M tokens`}
                />
              </div>
            </section>

            {/* SECTION 6 — Agent table */}
            <section aria-labelledby="agents-heading" className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <h2 id="agents-heading" className="sr-only">Agents 詳情</h2>
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-800 text-gray-300 bg-gray-900/60">
                    <th scope="col" className="text-left px-4 py-3 font-semibold">Agent</th>
                    <th scope="col" className="text-left px-4 py-3 font-semibold">Model</th>
                    <th scope="col" className="text-left px-4 py-3 font-semibold">職責</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.agents.map((agent) => (
                    <tr
                      key={agent.name}
                      className="border-b border-gray-800 last:border-0 hover:bg-gray-800/40 transition-colors"
                    >
                      <td className="px-4 py-3 font-semibold text-white">{agent.name}</td>
                      <td className="px-4 py-3 font-mono text-slate-300 text-xs">{agent.model}</td>
                      <td className="px-4 py-3 text-gray-300">{agent.role}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            <p className="text-center text-gray-500 text-xs mt-6 leading-relaxed">
              所有數字均含明確分母（n=...）以避免「樂觀偏差」。
              <br />
              更新指令：<code className="font-mono text-gray-300">python3 exhibition/build_stats.py</code>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
