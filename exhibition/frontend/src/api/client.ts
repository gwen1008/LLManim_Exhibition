import type { GalleryResponse, StatsResponse, TaskResponse } from "../types";

const BASE = "";

async function fetchWithFallback<T>(apiPath: string, fallbackPath: string): Promise<T> {
  try {
    const res = await fetch(BASE + apiPath);
    if (!res.ok) throw new Error(`${res.status}`);
    return res.json();
  } catch {
    const res = await fetch(BASE + fallbackPath);
    if (!res.ok) throw new Error(`Fallback also failed: ${fallbackPath}`);
    return res.json();
  }
}

export const getGallery = (): Promise<GalleryResponse> =>
  fetchWithFallback("/api/gallery", "/static/data/gallery.json");

export const getStats = (): Promise<StatsResponse> =>
  fetchWithFallback("/api/stats", "/static/data/stats.json");

export async function postGenerate(
  topic: string,
  mode: "opus_only" | "full_system"
): Promise<{ task_id: string } | null> {
  const res = await fetch(`${BASE}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic, mode }),
  });
  if (res.status === 501) return null;
  if (!res.ok) throw new Error(`Generate failed: ${res.status}`);
  return res.json();
}

export async function getTask(taskId: string): Promise<TaskResponse> {
  const res = await fetch(`${BASE}/api/task/${taskId}`);
  if (!res.ok) throw new Error(`Task fetch failed: ${res.status}`);
  return res.json();
}
