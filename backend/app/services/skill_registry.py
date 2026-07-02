from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
from app.core.settings import settings


@dataclass
class FeatureDefinition:
    feature_id: str
    label: str
    description: str
    skill: str
    required_files: bool
    output_type: str
    allow_tools: list[str]
    allow_shell: bool
    permission_profile: str
    confirm_before_execute: bool = False
    visible_to_customer: bool = True
    trigger_keywords: list[str] | None = None


@dataclass
class SkillDefinition:
    name: str
    path: Path
    skill_md: str


class SkillRegistry:
    def __init__(self, features: dict[str, FeatureDefinition], skills_dir: Path):
        self.features = features
        self.skills_dir = skills_dir

    @classmethod
    def load_default(cls) -> "SkillRegistry":
        features_path = settings.config_dir / "features.yaml"
        with features_path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        features: dict[str, FeatureDefinition] = {}
        for fid, item in (raw.get("features") or {}).items():
            features[fid] = FeatureDefinition(
                feature_id=fid,
                label=item["label"],
                description=item.get("description", ""),
                skill=item["skill"],
                required_files=bool(item.get("required_files", False)),
                output_type=item.get("output_type", "markdown"),
                allow_tools=list(item.get("allow_tools", [])),
                allow_shell=bool(item.get("allow_shell", False)),
                permission_profile=item.get("permission_profile", "readonly_document"),
                confirm_before_execute=bool(item.get("confirm_before_execute", False)),
                visible_to_customer=bool(item.get("visible_to_customer", True)),
                trigger_keywords=list(item.get("trigger_keywords", [])),
            )
        return cls(features=features, skills_dir=settings.skills_dir)

    def public_features(self) -> list[dict[str, Any]]:
        return [
            {
                "feature_id": f.feature_id,
                "label": f.label,
                "description": f.description,
                "required_files": f.required_files,
                "output_type": f.output_type,
                "visible_to_customer": f.visible_to_customer,
                "confirm_before_execute": f.confirm_before_execute,
            }
            for f in self.features.values()
            if f.visible_to_customer
        ]

    def get_feature(self, feature_id: str) -> FeatureDefinition:
        if feature_id not in self.features:
            raise ValueError(f"Unknown feature_id: {feature_id}")
        return self.features[feature_id]

    def get_skill(self, skill_name: str) -> SkillDefinition:
        skill_path = self.skills_dir / skill_name
        skill_md_path = skill_path / "SKILL.md"
        if not skill_md_path.exists():
            raise ValueError(f"Skill not found: {skill_name}")
        return SkillDefinition(
            name=skill_name,
            path=skill_path,
            skill_md=skill_md_path.read_text(encoding="utf-8"),
        )

    def detect_feature_by_keywords(self, message: str) -> str | None:
        text = message.lower()
        for fid, feature in self.features.items():
            for kw in feature.trigger_keywords or []:
                if kw.lower() in text:
                    return fid
        return None
