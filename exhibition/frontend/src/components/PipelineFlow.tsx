import type { Agent } from "../types";

interface Props {
  agents: Agent[];
}

const AGENT_COLORS: Record<string, string> = {
  Planner: "border-blue-500 bg-blue-950/30",
  Coder: "border-indigo-500 bg-indigo-950/30",
  VisionQA: "border-purple-500 bg-purple-950/30",
  RefiningLoop: "border-amber-500 bg-amber-950/30",
};

const AGENT_TEXT: Record<string, string> = {
  Planner: "text-blue-400",
  Coder: "text-indigo-400",
  VisionQA: "text-purple-400",
  RefiningLoop: "text-amber-400",
};

export function PipelineFlow({ agents }: Props) {
  const mainAgents = agents.filter((a) => a.name !== "RefiningLoop");
  const refining = agents.find((a) => a.name === "RefiningLoop");

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-center gap-2 flex-wrap">
        {mainAgents.map((agent, i) => (
          <div key={agent.name} className="flex items-center gap-2">
            <div
              className={`border-2 rounded-lg px-4 py-3 min-w-[140px] text-center ${
                AGENT_COLORS[agent.name] ?? "border-gray-500 bg-gray-900"
              }`}
            >
              <div
                className={`font-bold text-sm ${
                  AGENT_TEXT[agent.name] ?? "text-gray-300"
                }`}
              >
                {agent.name}
              </div>
              <div className="text-gray-400 text-xs mt-0.5">{agent.model}</div>
              <div className="text-gray-300 text-xs mt-1">{agent.role}</div>
            </div>
            {i < mainAgents.length - 1 && (
              <span className="text-gray-500 text-xl">→</span>
            )}
          </div>
        ))}
      </div>

      {refining && (
        <div className="flex justify-center">
          <div
            className={`border-2 rounded-lg px-6 py-3 text-center max-w-sm w-full ${
              AGENT_COLORS.RefiningLoop
            }`}
          >
            <div className="text-amber-400 font-bold text-sm">↩ {refining.name}</div>
            <div className="text-gray-400 text-xs mt-0.5">
              {refining.role}
            </div>
            <div className="flex justify-center gap-1 mt-2">
              {Array.from({ length: 5 }).map((_, i) => (
                <div
                  key={i}
                  className="w-4 h-4 rounded-full bg-amber-800/60 border border-amber-600 text-amber-400 text-[10px] flex items-center justify-center"
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
