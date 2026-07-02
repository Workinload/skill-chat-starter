from __future__ import annotations

import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.settings import settings
from app.dependencies import get_current_user
from app.models import User, UploadedFileModel
from app.schemas import FileInfo

router = APIRouter()
UPLOAD_ROOT = Path(os.environ.get("UPLOAD_ROOT", str(Path(__file__).resolve().parents[3] / "uploads")))


@router.post("", response_model=FileInfo)
def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = file.file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.max_upload_mb}MB")

    file_id = str(uuid.uuid4())
    safe_name = Path(file.filename or "upload.bin").name

    # Save under user-specific directory.
    user_dir = UPLOAD_ROOT / str(user.id)
    user_dir.mkdir(parents=True, exist_ok=True)
    target = user_dir / f"{file_id}__{safe_name}"
    target.write_bytes(content)

    # Save to database.
    db_file = UploadedFileModel(
        user_id=user.id,
        file_id=file_id,
        filename=safe_name,
        content_type=file.content_type,
        size_bytes=len(content),
        path=str(target),
    )
    db.add(db_file)
    db.commit()

    return FileInfo(
        file_id=file_id,
        filename=safe_name,
        content_type=file.content_type,
        size_bytes=len(content),
    )


def resolve_uploaded_file(file_id: str, user_id: int, db: Session) -> Path | None:
    record = db.query(UploadedFileModel).filter(
        UploadedFileModel.file_id == file_id,
        UploadedFileModel.user_id == user_id,
    ).first()
    if record and Path(record.path).exists():
        return Path(record.path)
    return None
