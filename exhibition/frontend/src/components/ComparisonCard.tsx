import type { GalleryItem } from "../types";
import { FairnessDisclaimer } from "./FairnessDisclaimer";

interface Props {
  item: GalleryItem;
}

function MetricRow({
  label,
  opusVal,
  sysVal,
  lowerIsBetter = true,
}: {
  label: string;
  opusVal: number | string;
  sysVal: number | string;
  lowerIsBetter?: boolean;
}) {
  const opusNum = typeof opusVal === "number" ? opusVal : null;
  const sysNum = typeof sysVal === "number" ? sysVal : null;

  const opusBetter =
    opusNum !== null && sysNum !== null
      ? lowerIsBetter
        ? opusNum < sysNum
        : opusNum > sysNum
      : false;

  return (
    <div className="flex justify-between text-xs py-0.5">
      <span className="text-gray-400">{label}</span>
      <div className="flex gap-4">
        <span className={opusBetter ? "text-green-400" : "text-red-400"}>{opusVal}</span>
        <span className={opusBetter ? "text-red-400" : "text-green-400"}>{sysVal}</span>
      </div>
    </div>
  );
}

export function ComparisonCard({ item }: Props) {
  const { opus_metrics: om, system_metrics: sm } = item;

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-700">
        <h3 className="text-white font-semibold text-lg">{item.topic_en}</h3>
        {item.topic !== item.topic_en && (
          <p className="text-gray-400 text-sm">{item.topic}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-0">
        {/* Opus side */}
        <div className="border-r border-gray-700">
          <div className="bg-red-950/40 px-3 py-1.5 text-center">
            <span className="text-red-400 text-xs font-bold uppercase tracking-wider">
              Opus 一發直出
            </span>
          </div>
          <div className="relative bg-black aspect-video">
            {om.render_success ? (
              <video
                src={item.opus_video_url}
                controls
                className="w-full h-full object-contain"
                preload="metadata"
              />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
                <span className="text-4xl">❌</span>
                <span className="text-red-400 text-sm font-medium">Render Failed</span>
                {om.notes && (
                  <span className="text-gray-500 text-xs px-4 text-center">{om.notes}</span>
                )}
              </div>
            )}
          </div>
        </div>

        {/* System side */}
        <div>
          <div className="bg-green-950/40 px-3 py-1.5 text-center">
            <span className="text-green-400 text-xs font-bold uppercase tracking-wider">
              本系統（5-Agent Pipeline）
            </span>
          </div>
          <div className="relative bg-black aspect-video">
            {sm.render_success ? (
              <video
                src={item.system_video_url}
                controls
                className="w-full h-full object-contain"
                preload="metadata"
              />
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
                <span className="text-4xl">❌</span>
                <span className="text-red-400 text-sm font-medium">Render Failed</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Metrics comparison */}
      <div className="px-4 py-3">
        <div className="grid grid-cols-2 gap-4 text-xs mb-2">
          <span className="text-red-400 font-medium text-center">Opus</span>
          <span className="text-green-400 font-medium text-center">本系統</span>
        </div>

        <MetricRow
          label="渲染時間"
          opusVal={`${om.render_duration_sec}s`}
          sysVal={`${sm.render_duration_sec}s`}
          lowerIsBetter={true}
        />
        <MetricRow
          label="程式碼行數"
          opusVal={om.code_lines}
          sysVal={sm.code_lines}
          lowerIsBetter={true}
        />
        <MetricRow
          label="棄用 API 數"
          opusVal={om.deprecated_api_count}
          sysVal={sm.deprecated_api_count}
          lowerIsBetter={true}
        />

        <div className="flex justify-between text-xs py-0.5 mt-1 border-t border-gray-700 pt-1.5">
          <span className="text-gray-400">BJ 品質分數</span>
          <div className="flex gap-4">
            <span className="text-gray-600">—</span>
            <span className="text-green-400 font-bold">{sm.bj_score}/100</span>
          </div>
        </div>

        {sm.refining_iterations > 0 && (
          <div className="flex justify-between text-xs py-0.5">
            <span className="text-gray-400">Reflexion 修正輪數</span>
            <span className="text-indigo-400">{sm.refining_iterations} 輪</span>
          </div>
        )}

        {om.deprecated_api_count > 0 && (
          <div className="mt-2">
            <span className="bg-red-900/50 text-red-400 border border-red-800 text-xs px-2 py-0.5 rounded">
              使用 {om.deprecated_api_count} 個已棄用 API
            </span>
          </div>
        )}

        <FairnessDisclaimer />
      </div>
    </div>
  );
}
