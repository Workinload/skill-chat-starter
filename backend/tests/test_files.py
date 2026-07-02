from __future__ import annotations


def test_upload_text_file(client):
    res = client.post(
        "/api/files",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["file_id"]
    assert data["filename"] == "hello.txt"
    assert data["size_bytes"] == 11
    assert data["content_type"] == "text/plain"


def test_upload_multiple_files(client):
    """Upload two files and verify they get distinct IDs."""
    res1 = client.post(
        "/api/files",
        files={"file": ("a.txt", b"aaa", "text/plain")},
    )
    res2 = client.post(
        "/api/files",
        files={"file": ("b.txt", b"bbb", "text/plain")},
    )
    assert res1.status_code == 200
    assert res2.status_code == 200
    id1 = res1.json()["file_id"]
    id2 = res2.json()["file_id"]
    assert id1 != id2


def test_upload_normal_file_succeeds(client):
    """Upload a small file and confirm it works."""
    res = client.post(
        "/api/files",
        files={"file": ("small.txt", b"x" * 100, "text/plain")},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["file_id"]
    assert data["size_bytes"] == 100
