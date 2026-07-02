from __future__ import annotations

from .conftest import register_and_login, auth_header


def test_upload_unauthorized_fails(client):
    res = client.post("/api/files", files={"file": ("a.txt", b"aaa", "text/plain")})
    assert res.status_code == 403


def test_upload_text_file(client):
    token = register_and_login(client, "file_user")
    res = client.post(
        "/api/files",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
        headers=auth_header(token),
    )
    assert res.status_code == 200
    data = res.json()
    assert data["file_id"]
    assert data["filename"] == "hello.txt"
    assert data["size_bytes"] == 11


def test_upload_multiple_files(client):
    token = register_and_login(client, "file_user2")
    res1 = client.post(
        "/api/files",
        files={"file": ("a.txt", b"aaa", "text/plain")},
        headers=auth_header(token),
    )
    res2 = client.post(
        "/api/files",
        files={"file": ("b.txt", b"bbb", "text/plain")},
        headers=auth_header(token),
    )
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["file_id"] != res2.json()["file_id"]
