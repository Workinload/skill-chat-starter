from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import User, Conversation, Message
from app.schemas import ConversationInfo, MessageInfo

router = APIRouter()


@router.get("", response_model=list[ConversationInfo])
def list_conversations(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    convs = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    return [
        ConversationInfo(
            id=c.id,
            title=c.title,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in convs
    ]


@router.get("/{conversation_id}/messages", response_model=list[MessageInfo])
def get_messages(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id,
    ).first()
    if not conv:
        return []

    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [
        MessageInfo(
            id=m.id,
            role=m.role,
            content=m.content,
            created_at=m.created_at,
        )
        for m in msgs
    ]
