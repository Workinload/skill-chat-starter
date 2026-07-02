"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { UploadedFile } from "@/lib/types";

type Msg = {
  role: "user" | "assistant";
  text: string;
};

export function ChatPanel({
  selectedFeature,
  files,
}: {
  selectedFeature: string | null;
  files: UploadedFile[];
}) {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", text }]);
    setLoading(true);
    try {
      if (selectedFeature) {
        const created = await api.createTask({
          feature_id: selectedFeature,
          conversation_id: conversationId,
          message: text,
          file_ids: files.map((f) => f.file_id),
          user_confirmed: true,
        });
        const result = await api.getTask(created.task_id);
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            text:
              result.status === "succeeded"
                ? result.output_text || "任务完成，但没有文本结果。"
                : `任务失败：${result.error || "未知错误"}`,
          },
        ]);
      } else {
        const res = await api.chat({
          conversation_id: conversationId,
          message: text,
          context: messages,
        });
        setConversationId(res.conversation_id);
        setMessages((m) => [...m, { role: "assistant", text: res.message }]);
      }
    } catch (err: any) {
      setMessages((m) => [...m, { role: "assistant", text: `请求失败：${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="rounded-2xl border bg-white shadow-sm">
      <div className="border-b p-4">
        <h2 className="font-semibold">对话</h2>
        <p className="text-xs text-slate-500">
          {selectedFeature ? "发送后将触发固定 Skill" : "普通聊天，不触发 Skill"}
        </p>
      </div>

      <div className="min-h-[360px] space-y-4 p-4">
        {messages.length === 0 && (
          <div className="rounded-xl bg-slate-50 p-4 text-sm text-slate-600">
            你可以直接聊天，或者选择上方功能后输入具体要求。
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <pre
              className={
                "inline-block max-w-[85%] rounded-2xl px-4 py-3 text-left text-sm " +
                (m.role === "user" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-900")
              }
            >
              {m.text}
            </pre>
          </div>
        ))}
        {loading && <div className="text-sm text-slate-500">处理中...</div>}
      </div>

      <div className="flex gap-2 border-t p-4">
        <textarea
          className="min-h-[48px] flex-1 rounded-xl border p-3 text-sm outline-none focus:ring-2 focus:ring-slate-300"
          placeholder={selectedFeature ? "描述你要执行的任务..." : "输入普通聊天内容..."}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
        />
        <button
          onClick={send}
          disabled={loading}
          className="rounded-xl bg-slate-900 px-5 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          发送
        </button>
      </div>
    </section>
  );
}
