from fastapi import APIRouter
from app.services.skill_registry import SkillRegistry

router = APIRouter()


@router.get("")
def list_features():
    registry = SkillRegistry.load_default()
    return registry.public_features()
