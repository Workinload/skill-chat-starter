"use client";

import { useEffect, useState } from "react";
import { AuthForm } from "@/components/auth-form";
import { FeatureBar } from "@/components/feature-bar";
import { ChatPanel } from "@/components/chat-panel";
import { FileUploader } from "@/components/file-uploader";
import { api } from "@/lib/api";
import type { FeatureInfo, UploadedFile, ConversationInfo, TaskListItem } from "@/lib/types";

export default function HomePage() {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [features, setFeatures] = useState<FeatureInfo[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<FeatureInfo | null>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // Init: check localStorage for existing token.
  useEffect(() => {
    const saved = localStorage.getItem("token");
    const savedUser = localStorage.getItem("username");
    if (saved) {
      setToken(saved);
      setUsername(savedUser || "");
    }
  }, []);

  // Load features when logged in.
  useEffect(() => {
    if (token) {
      api.getFeatures().then(setFeatures).catch(console.error);
    }
  }, [token]);

  function handleAuth(newToken: string, newUsername: string) {
    setToken(newToken);
    setUsername(newUsername);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
    setUsername(null);
    setSelectedFeature(null);
    setFiles([]);
  }

  // --- Unauthenticated ---
  if (!token) {
    return <AuthForm onAuth={handleAuth} />;
  }

  // --- Authenticated ---
  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 p-4 md:p-8">
        <header className="rounded-2xl border bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Skill Chat Starter</h1>
              <p className="mt-2 text-sm text-slate-600">
                当前用户：{username} · 普通聊天不会调用 Skill
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="rounded-lg border px-3 py-2 text-sm hover:bg-slate-50"
              >
                {showHistory ? "关闭记录" : "历史记录"}
              </button>
              <button
                onClick={handleLogout}
                className="rounded-lg border px-3 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                退出登录
              </button>
            </div>
          </div>
        </header>

        {showHistory && (
          <HistoryPanel onClose={() => setShowHistory(false)} />
        )}

        {!showHistory && (
          <>
            <FeatureBar
              features={features}
              selectedFeature={selectedFeature}
              onSelect={setSelectedFeature}
            />

            <FileUploader files={files} onFilesChange={setFiles} />

            <ChatPanel
              selectedFeature={selectedFeature}
              features={features}
              files={files}
            />
          </>
        )}
      </div>
    </main>
  );
}

function HistoryPanel({ onClose }: { onClose: () => void }) {
  const [conversations, setConversations] = useState<ConversationInfo[]>([]);
  const [tasks, setTasks] = useState<TaskListItem[]>([]);
  const [tab, setTab] = useState<"chats" | "tasks">("chats");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [selectedConv, setSelectedConv] = useState<number | null>(null);

  useEffect(() => {
    api.getConversations().then(setConversations).catch(console.error);
    api.listTasks().then(setTasks).catch(console.error);
  }, []);

  async function loadMessages(convId: number) {
    setSelectedConv(convId);
    const msgs = await api.getMessages(convId);
    setMessages(msgs.map((m) => ({ role: m.role, content: m.content })));
  }

  return (
    <section className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="mb-3 flex gap-2">
        <button
          onClick={() => { setTab("chats"); setSelectedConv(null); setMessages([]); }}
          className={"rounded-lg px-3 py-1 text-sm " + (tab === "chats" ? "bg-slate-900 text-white" : "bg-slate-100")}
        >
          对话记录
        </button>
        <button
          onClick={() => { setTab("tasks"); setSelectedConv(null); setMessages([]); }}
          className={"rounded-lg px-3 py-1 text-sm " + (tab === "tasks" ? "bg-slate-900 text-white" : "bg-slate-100")}
        >
          任务记录
        </button>
      </div>

      {tab === "chats" && (
        <div className="flex gap-4">
          <div className="w-1/3 space-y-1">
            {conversations.length === 0 && <p className="text-sm text-slate-500">暂无对话</p>}
            {conversations.map((c) => (
              <button
                key={c.id}
                onClick={() => loadMessages(c.id)}
                className={"block w-full rounded-lg px-3 py-2 text-left text-sm " + (selectedConv === c.id ? "bg-slate-100" : "hover:bg-slate-50")}
              >
                <p className="truncate font-medium">{c.title}</p>
                <p className="text-xs text-slate-400">{new Date(c.created_at).toLocaleString()}</p>
              </button>
            ))}
          </div>
          <div className="w-2/3 space-y-2">
            {messages.length === 0 && <p className="text-sm text-slate-500">选择对话查看消息</p>}
            {messages.map((m, i) => (
              <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
                <pre className={"inline-block max-w-[80%] rounded-xl px-3 py-2 text-sm whitespace-pre-wrap " + (m.role === "user" ? "bg-slate-900 text-white" : "bg-slate-100")}>
                  {m.content}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "tasks" && (
        <div className="space-y-2">
          {tasks.length === 0 && <p className="text-sm text-slate-500">暂无任务</p>}
          {tasks.map((t) => (
            <div key={t.task_id} className="rounded-lg border p-3">
              <div className="flex items-center justify-between">
                <span className="font-medium text-sm">{t.feature_id}</span>
                <span className={"rounded px-2 py-0.5 text-xs " + (t.status === "succeeded" ? "bg-green-100 text-green-700" : t.status === "failed" ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700")}>
                  {t.status}
                </span>
              </div>
              {t.error && <p className="mt-1 text-xs text-red-500">{t.error}</p>}
              <p className="mt-1 text-xs text-slate-400">{new Date(t.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
