from __future__ import annotations

from .conftest import register_and_login, auth_header


def test_chat_unauthorized_fails(client):
    res = client.post("/api/chat", json={"message": "hello", "context": []})
    assert res.status_code == 403


def test_chat_does_not_trigger_skill(client):
    token = register_and_login(client, "chat_user")
    res = client.post(
        "/api/chat",
        json={"conversation_id": None, "message": "你好", "context": []},
        headers=auth_header(token),
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "context_chat"
    assert "conversation_id" in data
    assert "task_id" not in data
    assert "feature_id" not in data


def test_chat_returns_conversation_id(client):
    token = register_and_login(client, "chat_user2")
    res = client.post(
        "/api/chat",
        json={"conversation_id": None, "message": "hello", "context": []},
        headers=auth_header(token),
    )
    data = res.json()
    assert data["conversation_id"]
    assert len(data["conversation_id"]) > 0


def test_chat_empty_message(client):
    token = register_and_login(client, "chat_user3")
    res = client.post(
        "/api/chat",
        json={"conversation_id": None, "message": "", "context": []},
        headers=auth_header(token),
    )
    assert res.status_code == 200
    data = res.json()
    assert "Skill" not in data["message"]
