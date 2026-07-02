from pathlib import Path
import fnmatch
import yaml
from app.core.settings import settings
from app.services.skill_registry import FeatureDefinition


class PermissionGuard:
    def __init__(self):
        path = settings.config_dir / "permissions.yaml"
        self.raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    def profile(self, name: str) -> dict:
        profiles = self.raw.get("profiles") or {}
        if name not in profiles:
            raise ValueError(f"Permission profile not found: {name}")
        return profiles[name]

    def validate_feature(self, feature: FeatureDefinition, user_confirmed: bool):
        profile = self.profile(feature.permission_profile)
        if feature.allow_shell and not profile.get("allow_bash", False):
            raise ValueError("Feature allows shell but permission profile forbids bash")
        if feature.confirm_before_execute and not user_confirmed:
            raise ValueError("This feature requires explicit user confirmation before execution")
        if feature.allow_shell and not settings.allow_shell_for_code_skills:
            raise ValueError("Shell execution is disabled by environment setting")

    def is_denied_path(self, workspace: Path, path: Path, profile_name: str) -> bool:
        profile = self.profile(profile_name)
        rel = str(path.relative_to(workspace)) if path.is_relative_to(workspace) else str(path)
        for pattern in profile.get("deny_paths", []):
            if fnmatch.fnmatch(rel, pattern) or rel.startswith(pattern.rstrip("/") + "/"):
                return True
        return False

    def validate_command(self, command: str, profile_name: str):
        profile = self.profile(profile_name)
        if not profile.get("allow_bash", False):
            raise ValueError("Bash is not allowed for this permission profile")
        for pattern in profile.get("bash_deny_patterns", []):
            if pattern in command:
                raise ValueError(f"Denied bash command pattern: {pattern}")
