import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.settings import settings
from app.schemas import FileInfo

router = APIRouter()
UPLOAD_ROOT = Path("/tmp/skill-chat-uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=FileInfo)
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large. Max {settings.max_upload_mb}MB")

    file_id = str(uuid.uuid4())
    safe_name = Path(file.filename or "upload.bin").name
    target = UPLOAD_ROOT / f"{file_id}__{safe_name}"
    target.write_bytes(content)

    return FileInfo(
        file_id=file_id,
        filename=safe_name,
        content_type=file.content_type,
        size_bytes=len(content),
    )


def resolve_uploaded_file(file_id: str) -> Path | None:
    matches = list(UPLOAD_ROOT.glob(f"{file_id}__*"))
    return matches[0] if matches else None
