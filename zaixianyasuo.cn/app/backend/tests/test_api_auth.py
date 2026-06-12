"""Auth API 集成测试"""
import pytest
from fastapi.testclient import TestClient


class TestRegister:
    def test_register_success(self, client: TestClient):
        r = client.post("/api/v1/auth/register", json={
            "username": "newuser", "password": "Abc12345", "email": "new@qq.com"
        })
        assert r.status_code == 200
        assert r.json()["username"] == "newuser"

    def test_register_duplicate_username(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "dup", "password": "Abc12345"
        })
        r = client.post("/api/v1/auth/register", json={
            "username": "dup", "password": "Xyz98765"
        })
        assert r.status_code == 409

    def test_register_weak_password(self, client: TestClient):
        r = client.post("/api/v1/auth/register", json={
            "username": "weakpw", "password": "12345678"
        })
        assert r.status_code == 422

    def test_register_short_username(self, client: TestClient):
        r = client.post("/api/v1/auth/register", json={
            "username": "ab", "password": "Abc12345"
        })
        assert r.status_code == 422

    def test_register_xss_username(self, client: TestClient):
        r = client.post("/api/v1/auth/register", json={
            "username": "<script>alert(1)</script>", "password": "Abc12345"
        })
        assert r.status_code == 422

    def test_register_with_nickname(self, client: TestClient):
        r = client.post("/api/v1/auth/register", json={
            "username": "nickuser", "password": "NickP@ss1", "nickname": "小明"
        })
        assert r.status_code == 200
        assert r.json()["nickname"] == "小明"


class TestLogin:
    def test_login_success(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "loginuser", "password": "TestP@ss1"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "loginuser", "password": "TestP@ss1"
        })
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "wrongpw", "password": "RightP@ss1"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "wrongpw", "password": "WrongPass1"
        })
        assert r.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "nonexistent", "password": "Abc12345"
        })
        assert r.status_code == 401

    def test_login_empty_fields(self, client: TestClient):
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "", "password": ""
        })
        # 空字符串导致查无用户，返回 401 或 400
        assert r.status_code in (401, 400, 422)

    def test_login_by_email(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "emailuser", "password": "EmailP@ss1",
            "email": "emailuser@qq.com"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "emailuser@qq.com", "password": "EmailP@ss1"
        })
        assert r.status_code == 200


class TestTokenAuth:
    def test_me_with_valid_token(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "meuser", "password": "MePass123"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "meuser", "password": "MePass123"
        })
        token = r.json()["access_token"]
        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["username"] == "meuser"

    def test_me_without_token(self, client: TestClient):
        r = client.get("/api/v1/auth/me")
        assert r.status_code == 401

    def test_me_with_invalid_token(self, client: TestClient):
        r = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"})
        assert r.status_code == 401

    def test_delete_account(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "deluser", "password": "DelPass123"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "deluser", "password": "DelPass123"
        })
        token = r.json()["access_token"]
        r = client.delete("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        # 用户已删除，Token 不可用
        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 404


class TestPasswordReset:
    def test_forgot_password_exists(self, client: TestClient):
        """有真实邮箱的用户找回密码"""
        client.post("/api/v1/auth/register", json={
            "username": "fpuser", "password": "FpP@ss123",
            "email": "fpuser@qq.com"
        })
        r = client.post("/api/v1/auth/forgot-password", json={
            "email": "fpuser@qq.com"
        })
        assert r.status_code == 200
        assert r.json()["ok"] is True

    def test_forgot_password_nonexistent(self, client: TestClient):
        r = client.post("/api/v1/auth/forgot-password", json={
            "email": "noone@example.com"
        })
        assert r.status_code == 200  # 安全：不暴露用户是否存在
        assert r.json()["ok"] is True

    def test_reset_password_invalid_token(self, client: TestClient):
        r = client.post("/api/v1/auth/reset-password", json={
            "token": "invalid-token-here", "new_password": "NewP@ss123"
        })
        assert r.status_code == 400

    def test_reset_password_weak_new(self, client: TestClient):
        r = client.post("/api/v1/auth/reset-password", json={
            "token": "some-token", "new_password": "short"
        })
        assert r.status_code == 422
