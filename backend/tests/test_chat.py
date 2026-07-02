from __future__ import annotations


def test_chat_does_not_trigger_skill(client):
    res = client.post(
        "/api/chat",
        json={
            "conversation_id": None,
            "message": "你好，请帮我分析一下",
            "context": [],
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "context_chat"
    assert "conversation_id" in data
    # Chat response must not mention Skill execution.
    assert "task_id" not in data
    assert "feature_id" not in data


def test_chat_returns_conversation_id(client):
    res = client.post(
        "/api/chat",
        json={
            "conversation_id": None,
            "message": "hello",
            "context": [],
        },
    )
    data = res.json()
    assert data["conversation_id"]
    assert len(data["conversation_id"]) > 0


def test_chat_empty_message(client):
    res = client.post(
        "/api/chat",
        json={
            "conversation_id": None,
            "message": "",
            "context": [],
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert "Skill" not in data["message"]
