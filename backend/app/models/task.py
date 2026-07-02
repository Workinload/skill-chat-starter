from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    task_id = Column(String, unique=True, nullable=False, index=True)
    feature_id = Column(String, nullable=False)
    skill = Column(String, nullable=False)
    status = Column(String, nullable=False, default="queued")
    output_text = Column(Text, nullable=True)
    output_files = Column(Text, nullable=True)  # JSON list stored as text
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
