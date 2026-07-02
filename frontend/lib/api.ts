import type { ChatResponse, FeatureInfo, TaskCreateResponse, TaskResult, UploadedFile } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

export const api = {
  getFeatures(): Promise<FeatureInfo[]> {
    return jsonFetch<FeatureInfo[]>("/api/features");
  },

  chat(body: { conversation_id: string | null; message: string; context: any[] }): Promise<ChatResponse> {
    return jsonFetch<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  createTask(body: {
    feature_id: string;
    conversation_id: string | null;
    message: string;
    file_ids: string[];
    user_confirmed: boolean;
  }): Promise<TaskCreateResponse> {
    return jsonFetch<TaskCreateResponse>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  getTask(taskId: string): Promise<TaskResult> {
    return jsonFetch<TaskResult>(`/api/tasks/${taskId}`);
  },

  async uploadFile(file: File): Promise<UploadedFile> {
    const data = new FormData();
    data.append("file", file);
    const res = await fetch(`${API_BASE}/api/files`, {
      method: "POST",
      body: data,
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
