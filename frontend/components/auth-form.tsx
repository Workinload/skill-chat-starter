"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function AuthForm({ onAuth }: { onAuth: (token: string, username: string) => void }) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    setError("");
    if (!username.trim() || !password.trim()) {
      setError("请输入用户名和密码");
      return;
    }
    setLoading(true);
    try {
      const res =
        mode === "login"
          ? await api.login(username.trim(), password)
          : await api.register(username.trim(), password);
      localStorage.setItem("token", res.token);
      localStorage.setItem("username", res.username);
      onAuth(res.token, res.username);
    } catch (err: any) {
      setError(err.message || "操作失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="w-full max-w-sm rounded-2xl border bg-white p-8 shadow-sm">
        <h1 className="mb-6 text-center text-2xl font-bold">Skill Chat</h1>
        <div className="mb-4 flex gap-2">
          <button
            onClick={() => { setMode("login"); setError(""); }}
            className={
              "flex-1 rounded-lg py-2 text-sm font-medium " +
              (mode === "login" ? "bg-slate-900 text-white" : "bg-slate-100")
            }
          >
            登录
          </button>
          <button
            onClick={() => { setMode("register"); setError(""); }}
            className={
              "flex-1 rounded-lg py-2 text-sm font-medium " +
              (mode === "register" ? "bg-slate-900 text-white" : "bg-slate-100")
            }
          >
            注册
          </button>
        </div>

        <input
          className="mb-3 w-full rounded-xl border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-slate-300"
          placeholder="用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
        />
        <input
          className="mb-3 w-full rounded-xl border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-slate-300"
          type="password"
          placeholder="密码"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
        />

        {error && <p className="mb-3 text-sm text-red-500">{error}</p>}

        <button
          onClick={submit}
          disabled={loading}
          className="w-full rounded-xl bg-slate-900 py-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {loading ? "处理中..." : mode === "login" ? "登录" : "注册"}
        </button>
      </div>
    </div>
  );
}
