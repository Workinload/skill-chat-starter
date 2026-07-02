from __future__ import annotations

import shutil
import uuid
from pathlib import Path
from app.core.settings import settings
from app.routers.files import resolve_uploaded_file


class WorkspaceManager:
    def __init__(self):
        self.root = Path(settings.workspace_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def create_workspace(self, file_ids: list[str]) -> Path:
        workspace = self.root / str(uuid.uuid4())
        (workspace / "inputs").mkdir(parents=True, exist_ok=True)
        (workspace / "outputs").mkdir(parents=True, exist_ok=True)
        (workspace / "drafts").mkdir(parents=True, exist_ok=True)

        for fid in file_ids:
            src = resolve_uploaded_file(fid)
            if src:
                # Remove uuid prefix when copied to workspace.
                parts = src.name.split("__", 1)
                filename = parts[1] if len(parts) == 2 else src.name
                shutil.copy2(src, workspace / "inputs" / filename)
        return workspace
