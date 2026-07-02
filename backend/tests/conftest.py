from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import database as db_module
from app.core.database import Base
from app.main import app

# Patch database BEFORE any imports use it.
TEST_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "test_skillchat.db"
TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override module-level engine/session.
db_module.engine = test_engine
db_module.SessionLocal = TestSessionLocal


@pytest.fixture(autouse=True)
def clean_db():
    """Recreate tables before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def register_and_login(client, username: str, password: str = "1234") -> str:
    resp = client.post("/api/auth/register", json={"username": username, "password": password})
    resp = client.post("/api/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    return resp.json()["token"]


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
