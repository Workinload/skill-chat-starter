"use client";

import { useEffect, useState } from "react";
import { FeatureBar } from "@/components/feature-bar";
import { ChatPanel } from "@/components/chat-panel";
import { FileUploader } from "@/components/file-uploader";
import { api } from "@/lib/api";
import type { FeatureInfo, UploadedFile } from "@/lib/types";

export default function HomePage() {
  const [features, setFeatures] = useState<FeatureInfo[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);

  useEffect(() => {
    api.getFeatures().then(setFeatures).catch(console.error);
  }, []);

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 p-4 md:p-8">
        <header className="rounded-2xl border bg-white p-5 shadow-sm">
          <h1 className="text-2xl font-bold">Skill Chat Starter</h1>
          <p className="mt-2 text-sm text-slate-600">
            普通聊天不会调用 Skill；点击固定功能后，后台才会调用对应内置 Skill。
          </p>
        </header>

        <FeatureBar
          features={features}
          selectedFeature={selectedFeature}
          onSelect={setSelectedFeature}
        />

        <FileUploader files={files} onFilesChange={setFiles} />

        <ChatPanel selectedFeature={selectedFeature} files={files} />
      </div>
    </main>
  );
}
