import { Info } from "lucide-react";

export function FairnessDisclaimer() {
  return (
    <p
      role="note"
      className="text-xs text-gray-400 border border-gray-800 rounded px-3 py-2 mt-3 text-left flex items-start gap-2"
    >
      <Info className="size-4 mt-0.5 text-gray-500 shrink-0" aria-hidden="true" />
      <span>
        Opus 直接生成 = 直接給 Opus 用戶原始 topic + 「請寫一個 ManimCE 場景」最小指令。
        不給 Planner JSON、不給 RAG 範例、不給規則表、不修正。
        這代表 Opus 在「無系統工程」下的真實能力。
      </span>
    </p>
  );
}
