from __future__ import annotations

from app.services.skill_registry import FeatureDefinition


class OutputValidator:
    def validate(self, feature: FeatureDefinition, output_text: str) -> tuple[bool, str | None]:
        if not output_text or not output_text.strip():
            return False, "Output is empty"

        if feature.output_type in {"markdown", "json_markdown"}:
            # MVP: very light validation. Expand this per skill later.
            return True, None

        return True, None
