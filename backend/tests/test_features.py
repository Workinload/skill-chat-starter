from __future__ import annotations


def test_features_only_returns_visible_to_customer(client):
    res = client.get("/api/features")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

    # All returned features must be visible_to_customer.
    for f in data:
        assert f["visible_to_customer"] is True

    # code_task has visible_to_customer=false, must not appear.
    feature_ids = [f["feature_id"] for f in data]
    assert "code_task" not in feature_ids

    # visible features should appear.
    assert "report_generate" in feature_ids
    assert "document_review" in feature_ids
    assert "extract_info" in feature_ids


def test_features_show_business_labels_not_internal_terms(client):
    res = client.get("/api/features")
    data = res.json()
    for f in data:
        # Labels should be business-facing Chinese, not internal IDs.
        assert "Skill" not in f["label"]
        assert "Claude" not in f["label"]
        assert "Agent" not in f["label"]
        assert "Runner" not in f["label"]
        # Every feature should have these keys.
        assert "feature_id" in f
        assert "label" in f
        assert "description" in f
        assert "required_files" in f
        assert "confirm_before_execute" in f
