from __future__ import annotations

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models import User
from app.services.skill_registry import SkillRegistry

router = APIRouter()


@router.get("")
def list_features(user: User = Depends(get_current_user)):
    registry = SkillRegistry.load_default()
    return registry.public_features()
