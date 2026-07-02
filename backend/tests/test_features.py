from __future__ import annotations

from .conftest import register_and_login, auth_header


def test_features_unauthorized_fails(client):
    res = client.get("/api/features")
    assert res.status_code == 403


def test_features_only_returns_visible_to_customer(client):
    token = register_and_login(client, "feat_test_user")
    res = client.get("/api/features", headers=auth_header(token))
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

    for f in data:
        assert f["visible_to_customer"] is True

    feature_ids = [f["feature_id"] for f in data]
    assert "code_task" not in feature_ids
    assert "report_generate" in feature_ids
    assert "document_review" in feature_ids
    assert "extract_info" in feature_ids


def test_features_no_internal_terms(client):
    token = register_and_login(client, "internal_test")
    res = client.get("/api/features", headers=auth_header(token))
    data = res.json()
    for f in data:
        assert "Skill" not in f["label"]
        assert "Claude" not in f["label"]
        assert "Agent" not in f["label"]
        assert "Runner" not in f["label"]
