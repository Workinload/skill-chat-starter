from __future__ import annotations


def test_create_report_generate_task_succeeds(client):
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "report_generate",
            "conversation_id": None,
            "message": "生成一份测试报告",
            "file_ids": [],
            "user_confirmed": False,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["task_id"]
    assert data["feature_id"] == "report_generate"
    assert data["status"] == "succeeded"

    # Fetch detail.
    detail = client.get(f"/api/tasks/{data['task_id']}")
    assert detail.status_code == 200
    detail_data = detail.json()
    assert detail_data["status"] == "succeeded"
    assert detail_data["output_text"]
    assert "Mock Skill" in detail_data["output_text"]


def test_required_files_without_files_fails(client):
    """document_review requires files. Calling without file_ids must fail."""
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "document_review",
            "conversation_id": None,
            "message": "审查一下这个材料",
            "file_ids": [],
            "user_confirmed": False,
        },
    )
    assert res.status_code == 400
    data = res.json()
    assert "requires at least one uploaded file" in data["detail"]


def test_code_task_not_visible_to_customer(client):
    """code_task has visible_to_customer=false. Regular customer must be blocked."""
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "code_task",
            "conversation_id": None,
            "message": "修复这个 bug",
            "file_ids": [],
            "user_confirmed": True,
        },
    )
    assert res.status_code == 400
    data = res.json()
    assert "not available to customers" in data["detail"]


def test_code_task_unconfirmed_fails(client):
    """code_task blocked by visibility check before confirm check."""
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "code_task",
            "conversation_id": None,
            "message": "修复这个 bug",
            "file_ids": [],
            "user_confirmed": False,
        },
    )
    assert res.status_code == 400
    data = res.json()
    assert "not available to customers" in data["detail"]


def test_task_404(client):
    res = client.get("/api/tasks/nonexistent-id")
    assert res.status_code == 404


def test_extract_info_with_files_mock_succeeds(client):
    """extract_info is visible, requires files. Confirm via mock."""
    # First upload a file.
    files_res = client.post(
        "/api/files",
        files={"file": ("test.txt", b"hello world", "text/plain")},
    )
    assert files_res.status_code == 200
    file_data = files_res.json()

    # Now create task with file.
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "extract_info",
            "conversation_id": None,
            "message": "提取关键信息",
            "file_ids": [file_data["file_id"]],
            "user_confirmed": False,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "succeeded"


def test_task_result_has_required_fields(client):
    """Verify task result shape is correct."""
    res = client.post(
        "/api/tasks",
        json={
            "feature_id": "report_generate",
            "message": "test",
            "file_ids": [],
            "user_confirmed": False,
        },
    )
    task_id = res.json()["task_id"]
    detail = client.get(f"/api/tasks/{task_id}")
    data = detail.json()
    for key in ("task_id", "status", "feature_id", "skill", "created_at", "updated_at", "output_files", "audit"):
        assert key in data, f"Missing key: {key}"
