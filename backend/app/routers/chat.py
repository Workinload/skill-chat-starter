from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import User, Conversation, Message
from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """普通上下文聊天入口。保存消息到数据库。"""
    service = ChatService()
    response = service.respond(req)

    # Find or create conversation.
    if req.conversation_id and req.conversation_id.isdigit():
        conv = db.query(Conversation).filter(
            Conversation.id == int(req.conversation_id),
            Conversation.user_id == user.id,
        ).first()
    else:
        conv = None

    if not conv:
        conv = Conversation(user_id=user.id, title=req.message[:40] or "新对话")
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Save user message.
    db.add(Message(conversation_id=conv.id, role="user", content=req.message))
    # Save assistant response.
    db.add(Message(conversation_id=conv.id, role="assistant", content=response.message))
    db.commit()

    response.conversation_id = str(conv.id)
    return response
