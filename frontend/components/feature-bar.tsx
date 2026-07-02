"use client";

import type { FeatureInfo } from "@/lib/types";

export function FeatureBar({
  features,
  selectedFeature,
  onSelect,
}: {
  features: FeatureInfo[];
  selectedFeature: string | null;
  onSelect: (featureId: string | null) => void;
}) {
  return (
    <section className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-semibold">固定功能</h2>
        <button
          onClick={() => onSelect(null)}
          className="rounded-lg border px-3 py-1 text-sm hover:bg-slate-50"
        >
          普通聊天
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {features.map((f) => (
          <button
            key={f.feature_id}
            onClick={() => onSelect(f.feature_id)}
            className={
              "rounded-xl border px-4 py-2 text-sm transition " +
              (selectedFeature === f.feature_id
                ? "border-slate-900 bg-slate-900 text-white"
                : "bg-white hover:bg-slate-50")
            }
            title={f.description}
          >
            {f.label}
            {f.required_files ? " · 需文件" : ""}
          </button>
        ))}
      </div>
      <p className="mt-3 text-xs text-slate-500">
        当前模式：{selectedFeature ? `功能执行：${selectedFeature}` : "普通上下文聊天"}
      </p>
    </section>
  );
}
