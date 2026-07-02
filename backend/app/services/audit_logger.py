from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class AuditLogger:
    def event(self, event_type: str, **kwargs: Any) -> dict[str, Any]:
        return {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **kwargs,
        }
