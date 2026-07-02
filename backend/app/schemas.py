from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str
    context: list[dict[str, Any]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    mode: str = "context_chat"


class TaskStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class TaskCreateRequest(BaseModel):
    feature_id: str
    conversation_id: str | None = None
    message: str
    file_ids: list[str] = Field(default_factory=list)
    user_confirmed: bool = False


class TaskCreateResponse(BaseModel):
    task_id: str
    status: TaskStatus
    feature_id: str
    skill: str
    message: str


class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    feature_id: str
    skill: str
    created_at: datetime
    updated_at: datetime
    output_text: str | None = None
    output_files: list[str] = Field(default_factory=list)
    error: str | None = None
    audit: list[dict[str, Any]] = Field(default_factory=list)


class FeatureInfo(BaseModel):
    feature_id: str
    label: str
    description: str
    required_files: bool
    output_type: str
    visible_to_customer: bool = True
    confirm_before_execute: bool = False


class FileInfo(BaseModel):
    file_id: str
    filename: str
    content_type: str | None = None
    size_bytes: int
