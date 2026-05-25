import { useEffect, useState } from "react";
import { getGallery } from "../api/client";
import { ComparisonCard } from "../components/ComparisonCard";
import type { GalleryItem } from "../types";

export function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getGallery()
      .then((data) => setItems(data.items))
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Hero */}
      <div className="bg-gradient-to-b from-gray-900 to-gray-950 border-b border-gray-800 px-6 py-16 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            同樣的 Prompt，
            <span className="text-red-400"> 差距有多大？</span>
          </h1>
          <p className="text-xl text-gray-300 mb-2">
            <span className="text-red-400 font-semibold">Opus 一發直出</span>
            {" vs. "}
            <span className="text-green-400 font-semibold">本系統（5 階段 Multi-Agent Pipeline）</span>
          </p>
          <p className="text-gray-500 text-sm mt-4 max-w-2xl mx-auto">
            每組影片使用完全相同的數學主題。左邊是 Opus 無任何輔助系統直接生成的結果；
            右邊是經過 Planner → Coder → VisionQA → Reflexion 修正的完整 pipeline 輸出。
          </p>
        </div>
      </div>

      {/* Gallery */}
      <div className="max-w-7xl mx-auto px-4 py-10">
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-400" />
          </div>
        )}

        {error && (
          <div className="bg-red-950/50 border border-red-800 rounded-lg p-6 text-center text-red-400">
            資料載入失敗：{error}
          </div>
        )}

        {!loading && !error && items.length === 0 && (
          <div className="text-center text-gray-500 py-20">尚無資料</div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {items.map((item) => (
            <ComparisonCard key={item.id} item={item} />
          ))}
        </div>
      </div>
    </div>
  );
}
