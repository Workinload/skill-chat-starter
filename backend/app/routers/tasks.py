from fastapi import APIRouter, HTTPException
from app.schemas import TaskCreateRequest, TaskCreateResponse, TaskResult
from app.services.task_service import TaskService

router = APIRouter()
service = TaskService()


@router.post("", response_model=TaskCreateResponse)
async def create_task(req: TaskCreateRequest):
    try:
        return await service.create_and_run(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{task_id}", response_model=TaskResult)
async def get_task(task_id: str):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
