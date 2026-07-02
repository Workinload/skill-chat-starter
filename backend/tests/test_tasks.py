from __future__ import annotations

from .conftest import register_and_login, auth_header


def test_tasks_unauthorized_fails(client):
    res = client.post("/api/tasks", json={
        "feature_id": "report_generate", "message": "test"
    })
    assert res.status_code == 403


def test_create_report_generate_task_succeeds(client):
    token = register_and_login(client, "task_user")
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "report_generate", "message": "生成报告",
            "file_ids": [], "user_confirmed": False,
        },
        headers=auth_header(token),
    )
    assert res.status_code == 200
    data = res.json()
    assert data["task_id"]
    assert data["status"] == "succeeded"

    detail = client.get(f"/api/tasks/{data['task_id']}", headers=auth_header(token))
    assert detail.status_code == 200
    detail_data = detail.json()
    assert detail_data["status"] == "succeeded"
    assert "Mock Skill" in detail_data["output_text"]


def test_required_files_without_files_fails(client):
    token = register_and_login(client, "req_file_user")
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "document_review", "message": "审查材料",
            "file_ids": [], "user_confirmed": False,
        },
        headers=auth_header(token),
    )
    assert res.status_code == 400
    assert "requires at least one uploaded file" in res.json()["detail"]


def test_code_task_not_visible_to_customer(client):
    token = register_and_login(client, "code_block_user")
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "code_task", "message": "fix bug",
            "file_ids": [], "user_confirmed": True,
        },
        headers=auth_header(token),
    )
    assert res.status_code == 400
    assert "not available to customers" in res.json()["detail"]


def test_task_list_user_isolation(client):
    """User A's tasks must not be visible to User B."""
    token_a = register_and_login(client, "iso_a")
    token_b = register_and_login(client, "iso_b")

    # User A creates a task.
    client.post(
        "/api/tasks",
        json={"feature_id": "report_generate", "message": "A's task", "file_ids": [], "user_confirmed": False},
        headers=auth_header(token_a),
    )

    # User A sees it.
    tasks_a = client.get("/api/tasks", headers=auth_header(token_a))
    assert len(tasks_a.json()) == 1

    # User B sees nothing.
    tasks_b = client.get("/api/tasks", headers=auth_header(token_b))
    assert len(tasks_b.json()) == 0


def test_conversation_user_isolation(client):
    """User A's conversations must not be visible to User B."""
    token_a = register_and_login(client, "conv_iso_a")
    token_b = register_and_login(client, "conv_iso_b")

    # User A chats.
    resp = client.post(
        "/api/chat",
        json={"conversation_id": None, "message": "A's chat", "context": []},
        headers=auth_header(token_a),
    )
    conv_id = resp.json()["conversation_id"]

    # User A sees conversation.
    convs_a = client.get("/api/conversations", headers=auth_header(token_a))
    assert len(convs_a.json()) == 1

    # User B sees nothing.
    convs_b = client.get("/api/conversations", headers=auth_header(token_b))
    assert len(convs_b.json()) == 0

    # User B cannot access A's messages.
    msgs = client.get(f"/api/conversations/{conv_id}/messages", headers=auth_header(token_b))
    assert msgs.json() == []
