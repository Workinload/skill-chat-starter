"use client";

import type { UploadedFile } from "@/lib/types";
import { api } from "@/lib/api";

export function FileUploader({
  files,
  onFilesChange,
}: {
  files: UploadedFile[];
  onFilesChange: (files: UploadedFile[]) => void;
}) {
  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const list = e.target.files;
    if (!list || list.length === 0) return;
    const uploaded: UploadedFile[] = [];
    for (const file of Array.from(list)) {
      uploaded.push(await api.uploadFile(file));
    }
    onFilesChange([...files, ...uploaded]);
    e.target.value = "";
  }

  return (
    <section className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="font-semibold">上传材料</h2>
          <p className="text-xs text-slate-500">文件会传给功能型 Skill，普通聊天默认不读取文件。</p>
        </div>
        <label className="cursor-pointer rounded-xl border px-4 py-2 text-sm hover:bg-slate-50">
          上传文件
          <input type="file" multiple className="hidden" onChange={handleUpload} />
        </label>
      </div>

      {files.length > 0 && (
        <ul className="mt-3 space-y-1 text-sm text-slate-700">
          {files.map((f) => (
            <li key={f.file_id} className="rounded-lg bg-slate-50 px-3 py-2">
              {f.filename} · {(f.size_bytes / 1024).toFixed(1)} KB
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
