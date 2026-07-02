import type {
  AuthResponse,
  ChatResponse,
  ConversationInfo,
  FeatureInfo,
  MessageInfo,
  TaskCreateResponse,
  TaskListItem,
  TaskResult,
  UploadedFile,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

async function jsonFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
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
  // Auth
  register(username: string, password: string): Promise<AuthResponse> {
    return jsonFetch<AuthResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
  },

  login(username: string, password: string): Promise<AuthResponse> {
    return jsonFetch<AuthResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
  },

  // Features
  getFeatures(): Promise<FeatureInfo[]> {
    return jsonFetch<FeatureInfo[]>("/api/features");
  },

  // Chat
  chat(body: {
    conversation_id: string | null;
    message: string;
    context: unknown[];
  }): Promise<ChatResponse> {
    return jsonFetch<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  // Conversations
  getConversations(): Promise<ConversationInfo[]> {
    return jsonFetch<ConversationInfo[]>("/api/conversations");
  },

  getMessages(conversationId: number): Promise<MessageInfo[]> {
    return jsonFetch<MessageInfo[]>(`/api/conversations/${conversationId}/messages`);
  },

  // Tasks
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

  listTasks(): Promise<TaskListItem[]> {
    return jsonFetch<TaskListItem[]>("/api/tasks");
  },

  // Files
  async uploadFile(file: File): Promise<UploadedFile> {
    const data = new FormData();
    data.append("file", file);
    const res = await fetch(`${API_BASE}/api/files`, {
      method: "POST",
      body: data,
      headers: authHeaders(),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
