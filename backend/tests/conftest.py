from __future__ import annotations

import sys
from pathlib import Path

# Ensure the backend app is importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
