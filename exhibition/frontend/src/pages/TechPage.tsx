import { useEffect, useState } from "react";
import { getStats } from "../api/client";
import { PipelineFlow } from "../components/PipelineFlow";
import type { StatsResponse } from "../types";

function StatCard({
  value,
  label,
  color = "text-white",
}: {
  value: string | number;
  label: string;
  color?: string;
}) {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 text-center">
      <div className={`text-4xl font-extrabold ${color}`}>{value}</div>
      <div className="text-gray-400 text-sm mt-1">{label}</div>
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
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-extrabold text-center mb-2">Tech Dashboard</h1>
        <p className="text-gray-400 text-center mb-10">系統架構 & 評測數據</p>

        {loading && (
          <div className="flex justify-center py-10">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-400" />
          </div>
        )}

        {stats && (
          <>
            {/* Hero metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
              <StatCard
                value={stats.benchmark_pass_rate}
                label="Benchmark 通過率"
                color="text-green-400"
              />
              <StatCard
                value={`${(stats.gt_match_rate * 100).toFixed(1)}%`}
                label="GT Match Rate"
                color="text-green-400"
              />
              <StatCard
                value={stats.bj_average_score.toFixed(1)}
                label="BJ 平均分數"
                color="text-indigo-400"
              />
              <StatCard
                value={stats.total_videos_generated}
                label="總生成影片數"
                color="text-blue-400"
              />
            </div>

            {/* Pipeline */}
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 mb-8">
              <h2 className="text-lg font-bold mb-6 text-center text-gray-200">
                Multi-Agent Pipeline
              </h2>
              <PipelineFlow agents={stats.agents} />
            </div>

            {/* Agent table */}
            <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-700 text-gray-400">
                    <th className="text-left px-4 py-3">Agent</th>
                    <th className="text-left px-4 py-3">Model</th>
                    <th className="text-left px-4 py-3">職責</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.agents.map((agent) => (
                    <tr key={agent.name} className="border-b border-gray-800 last:border-0">
                      <td className="px-4 py-3 font-semibold text-white">{agent.name}</td>
                      <td className="px-4 py-3 font-mono text-indigo-300 text-xs">{agent.model}</td>
                      <td className="px-4 py-3 text-gray-400">{agent.role}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <p className="text-center text-gray-600 text-xs mt-6">
              RefiningLoop 最多 {stats.refining_loop_max_iterations} 輪；
              Linter 有獨立 budget，不佔主迭代次數
            </p>
          </>
        )}
      </div>
    </div>
  );
}
