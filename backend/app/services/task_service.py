from __future__ import annotations

from datetime import datetime, timezone
import uuid
from app.schemas import TaskCreateRequest, TaskCreateResponse, TaskResult, TaskStatus
from app.services.skill_registry import SkillRegistry
from app.services.permission_guard import PermissionGuard
from app.services.workspace_manager import WorkspaceManager
from app.services.skill_runner import SkillRunner
from app.services.output_validator import OutputValidator
from app.services.audit_logger import AuditLogger


class TaskService:
    """MVP 使用内存存储任务。

    生产中把这里替换为 PostgreSQL task 表 + Redis/RQ/Celery 异步队列。
    """

    def __init__(self):
        self.tasks: dict[str, TaskResult] = {}
        self.registry = SkillRegistry.load_default()
        self.guard = PermissionGuard()
        self.workspace_manager = WorkspaceManager()
        self.runner = SkillRunner()
        self.validator = OutputValidator()
        self.audit = AuditLogger()

    async def create_and_run(self, req: TaskCreateRequest) -> TaskCreateResponse:
        feature = self.registry.get_feature(req.feature_id)
        self.guard.validate_feature(feature, req.user_confirmed)

        if feature.required_files and not req.file_ids:
            raise ValueError("This feature requires at least one uploaded file")

        skill = self.registry.get_skill(feature.skill)
        task_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        task = TaskResult(
            task_id=task_id,
            status=TaskStatus.running,
            feature_id=feature.feature_id,
            skill=skill.name,
            created_at=now,
            updated_at=now,
            audit=[self.audit.event("task_created", feature_id=feature.feature_id, skill=skill.name)],
        )
        self.tasks[task_id] = task

        try:
            workspace = self.workspace_manager.create_workspace(req.file_ids)
            task.audit.append(self.audit.event("workspace_created", workspace=str(workspace)))
            output = await self.runner.run(
                feature=feature,
                skill=skill,
                message=req.message,
                workspace=workspace,
            )
            ok, error = self.validator.validate(feature, output)
            if not ok:
                raise ValueError(error or "Output validation failed")

            task.status = TaskStatus.succeeded
            task.output_text = output
            task.output_files = [str(p) for p in (workspace / "outputs").glob("*")]
            task.audit.append(self.audit.event("task_succeeded"))
        except Exception as exc:
            task.status = TaskStatus.failed
            task.error = str(exc)
            task.audit.append(self.audit.event("task_failed", error=str(exc)))
        finally:
            task.updated_at = datetime.now(timezone.utc)

        return TaskCreateResponse(
            task_id=task_id,
            status=task.status,
            feature_id=feature.feature_id,
            skill=skill.name,
            message="Task created and executed. Query task detail for result.",
        )

    def get_task(self, task_id: str) -> TaskResult | None:
        return self.tasks.get(task_id)
