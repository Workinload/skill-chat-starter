from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    frontend_origin: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"

    database_url: str = "postgresql+psycopg://skillchat:skillchat@localhost:5432/skillchat"
    redis_url: str = "redis://localhost:6379/0"

    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "skill-chat-files"
    s3_region: str = "us-east-1"
    s3_use_ssl: bool = False

    anthropic_api_key: str | None = None
    claude_agent_sdk_enabled: bool = False
    claude_model: str = "claude-sonnet-4-5"
    claude_permission_mode: str = "acceptEdits"

    workspace_root: str = "/tmp/skill-chat-workspaces"
    max_upload_mb: int = 50
    max_task_seconds: int = 600
    allow_shell_for_code_skills: bool = False

    config_dir: Path = Path(__file__).resolve().parents[3] / "config"
    skills_dir: Path = Path(__file__).resolve().parents[3] / "skills"


settings = Settings()
