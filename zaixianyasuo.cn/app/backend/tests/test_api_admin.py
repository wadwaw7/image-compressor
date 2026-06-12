"""管理员 API 测试"""
import pytest
from fastapi.testclient import TestClient


class TestAdminPermission:
    def test_normal_user_cannot_access(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "normal", "password": "NormalP@ss1"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "normal", "password": "NormalP@ss1"
        })
        token = r.json()["access_token"]
        r = client.get("/api/v1/admin/users",
                       headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 403

    def test_admin_can_list_users(self, client: TestClient, admin_token: str):
        r = client.get("/api/v1/admin/users",
                       headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200

    def test_admin_search(self, client: TestClient, admin_token: str):
        r = client.get("/api/v1/admin/users?q=admin",
                       headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 200

    def test_page_zero_rejected(self, client: TestClient, admin_token: str):
        r = client.get("/api/v1/admin/users?page=0",
                       headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 422

    def test_page_size_too_large(self, client: TestClient, admin_token: str):
        r = client.get("/api/v1/admin/users?page_size=9999",
                       headers={"Authorization": f"Bearer {admin_token}"})
        assert r.status_code == 422

    def test_unauthenticated(self, client: TestClient):
        r = client.get("/api/v1/admin/users")
        assert r.status_code == 401


class TestFeedback:
    def test_submit_feedback(self, client: TestClient):
        r = client.post("/api/v1/feedback", json={
            "subject": "测试", "message": "测试消息内容", "contact": "t@t.com"
        })
        assert r.status_code == 200
        assert r.json()["ok"] is True

    def test_submit_empty_message(self, client: TestClient):
        r = client.post("/api/v1/feedback", json={
            "subject": "test", "message": ""
        })
        assert r.status_code == 422

    def test_message_too_short(self, client: TestClient):
        r = client.post("/api/v1/feedback", json={
            "subject": "test", "message": "ab"
        })
        assert r.status_code == 422

    def test_list_requires_admin(self, client: TestClient):
        r = client.get("/api/v1/feedback")
        assert r.status_code == 401  # 未认证
