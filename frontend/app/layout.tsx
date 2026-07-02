import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Skill Chat Starter",
  description: "Lightweight chat with fixed Skill execution.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
