from __future__ import annotations

import json
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from app.schemas import TaskCreateRequest, TaskCreateResponse, TaskResult, TaskStatus
from app.services.skill_registry import SkillRegistry
from app.services.permission_guard import PermissionGuard
from app.services.workspace_manager import WorkspaceManager
from app.services.skill_runner import SkillRunner
from app.services.output_validator import OutputValidator
from app.services.audit_logger import AuditLogger


class TaskService:
    """MVP 使用 SQLite 存储任务。"""

    def __init__(self):
        self.registry = SkillRegistry.load_default()
        self.guard = PermissionGuard()
        self.runner = SkillRunner()
        self.validator = OutputValidator()
        self.audit = AuditLogger()

    def create_and_run(
        self, req: TaskCreateRequest, user_id: int, db: Session
    ) -> TaskCreateResponse:
        from app.models import TaskModel

        feature = self.registry.get_feature(req.feature_id)

        if not feature.visible_to_customer:
            raise ValueError("This feature is not available to customers")

        self.guard.validate_feature(feature, req.user_confirmed)

        if feature.required_files and not req.file_ids:
            raise ValueError("This feature requires at least one uploaded file")

        skill = self.registry.get_skill(feature.skill)
        task_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        # Create workspace with user isolation.
        wm = WorkspaceManager(user_id=user_id)
        workspace = wm.create_workspace(req.file_ids, db)

        status = TaskStatus.running
        output_text = None
        output_files = []
        error = None
        audit = [self.audit.event("task_created", feature_id=feature.feature_id, skill=skill.name)]

        try:
            audit.append(self.audit.event("workspace_created", workspace=str(workspace)))
            output_text = self.runner.run_sync(
                feature=feature,
                skill=skill,
                message=req.message,
                workspace=workspace,
            )
            ok, validation_error = self.validator.validate(feature, output_text)
            if not ok:
                raise ValueError(validation_error or "Output validation failed")

            status = TaskStatus.succeeded
            output_files = [str(p) for p in (workspace / "outputs").glob("*")]
            audit.append(self.audit.event("task_succeeded"))
        except Exception as exc:
            status = TaskStatus.failed
            error = str(exc)
            audit.append(self.audit.event("task_failed", error=str(exc)))

        # Persist to database.
        db_task = TaskModel(
            user_id=user_id,
            task_id=task_id,
            feature_id=feature.feature_id,
            skill=skill.name,
            status=status.value,
            output_text=output_text,
            output_files=json.dumps(output_files),
            error=error,
            created_at=now,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(db_task)
        db.commit()

        return TaskCreateResponse(
            task_id=task_id,
            status=status,
            feature_id=feature.feature_id,
            skill=skill.name,
            message="Task created and executed. Query task detail for result.",
        )

    def get_task(self, task_id: str, user_id: int, db: Session) -> TaskResult | None:
        from app.models import TaskModel

        record = db.query(TaskModel).filter(
            TaskModel.task_id == task_id,
            TaskModel.user_id == user_id,
        ).first()
        if not record:
            return None

        return TaskResult(
            task_id=record.task_id,
            status=TaskStatus(record.status),
            feature_id=record.feature_id,
            skill=record.skill,
            created_at=record.created_at,
            updated_at=record.updated_at,
            output_text=record.output_text,
            output_files=json.loads(record.output_files) if record.output_files else [],
            error=record.error,
            audit=[],
        )

    def list_user_tasks(self, user_id: int, db: Session) -> list[TaskResult]:
        from app.models import TaskModel

        records = (
            db.query(TaskModel)
            .filter(TaskModel.user_id == user_id)
            .order_by(TaskModel.created_at.desc())
            .all()
        )
        return [
            TaskResult(
                task_id=r.task_id,
                status=TaskStatus(r.status),
                feature_id=r.feature_id,
                skill=r.skill,
                created_at=r.created_at,
                updated_at=r.updated_at,
                output_text=r.output_text,
                output_files=json.loads(r.output_files) if r.output_files else [],
                error=r.error,
                audit=[],
            )
            for r in records
        ]
