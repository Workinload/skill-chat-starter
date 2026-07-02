from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskResult,
    TaskListItem,
    TaskStatus,
)
from app.services.task_service import TaskService

router = APIRouter()
service = TaskService()


@router.post("", response_model=TaskCreateResponse)
def create_task(
    req: TaskCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return service.create_and_run(req, user_id=user.id, db=db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[TaskListItem])
def list_tasks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    results = service.list_user_tasks(user.id, db)
    return [
        TaskListItem(
            task_id=r.task_id,
            feature_id=r.feature_id,
            skill=r.skill,
            status=r.status.value,
            created_at=r.created_at,
            error=r.error,
        )
        for r in results
    ]


@router.get("/{task_id}", response_model=TaskResult)
def get_task(
    task_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = service.get_task(task_id, user.id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
