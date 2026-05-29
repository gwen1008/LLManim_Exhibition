import { ChevronRight, RotateCcw } from "lucide-react";
import type { Agent } from "../types";

interface Props {
  agents: Agent[];
}

const AGENT_COLORS: Record<string, string> = {
  Planner: "border-slate-600 bg-slate-900/60",
  Coder: "border-emerald-500 bg-emerald-950/40",
  VisionQA: "border-amber-500 bg-amber-950/30",
  RefiningLoop: "border-rose-500 bg-rose-950/30",
};

const AGENT_TEXT: Record<string, string> = {
  Planner: "text-slate-200",
  Coder: "text-emerald-300",
  VisionQA: "text-amber-300",
  RefiningLoop: "text-rose-300",
};

export function PipelineFlow({ agents }: Props) {
  const mainAgents = agents.filter((a) => a.name !== "RefiningLoop");
  const refining = agents.find((a) => a.name === "RefiningLoop");

  return (
    <div className="space-y-4">
      <ol className="flex items-center justify-center gap-2 flex-wrap list-none p-0">
        {mainAgents.map((agent, i) => (
          <li key={agent.name} className="flex items-center gap-2">
            <div
              className={`border-2 rounded-lg px-4 py-3 min-w-[140px] text-center ${
                AGENT_COLORS[agent.name] ?? "border-gray-600 bg-gray-900"
              }`}
            >
              <div className={`font-bold text-sm ${AGENT_TEXT[agent.name] ?? "text-gray-200"}`}>
                {agent.name}
              </div>
              <div className="text-gray-400 text-xs mt-0.5 font-mono">{agent.model}</div>
              <div className="text-gray-300 text-xs mt-1">{agent.role}</div>
            </div>
            {i < mainAgents.length - 1 && (
              <ChevronRight className="size-5 text-gray-500 shrink-0" aria-hidden="true" />
            )}
          </li>
        ))}
      </ol>

      {refining && (
        <div className="flex justify-center">
          <div
            className={`border-2 rounded-lg px-6 py-3 text-center max-w-sm w-full ${AGENT_COLORS.RefiningLoop}`}
          >
            <div className="text-rose-300 font-bold text-sm inline-flex items-center justify-center gap-1.5">
              <RotateCcw className="size-4" aria-hidden="true" />
              {refining.name}
            </div>
            <div className="text-gray-300 text-xs mt-0.5">{refining.role}</div>
            <div className="flex justify-center gap-1 mt-2" aria-label="最多 5 輪迭代">
              {Array.from({ length: 5 }).map((_, i) => (
                <div
                  key={i}
                  className="w-4 h-4 rounded-full bg-rose-900/60 border border-rose-700 text-rose-300 text-[10px] flex items-center justify-center tabular-nums"
                  aria-hidden="true"
                >
                  {i + 1}
                </div>
              ))}
            </div>
            <div className="text-gray-500 text-[10px] mt-1">最多 5 輪</div>
          </div>
        </div>
      )}
    </div>
  );
}
