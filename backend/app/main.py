from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers import chat, tasks, files, features

app = FastAPI(
    title="Skill Chat Starter API",
    version="0.1.0",
    description="Lightweight chat + fixed feature Skill execution gateway.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(features.router, prefix="/api/features", tags=["features"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(files.router, prefix="/api/files", tags=["files"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "skill-chat-starter"}
