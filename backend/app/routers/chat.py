from __future__ import annotations

from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """普通上下文聊天入口。

    这里必须保持纯聊天：不调用 Skill、不读写文件、不执行命令。
    """
    service = ChatService()
    return await service.respond(req)
