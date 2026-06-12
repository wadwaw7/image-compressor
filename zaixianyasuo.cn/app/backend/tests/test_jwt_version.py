"""JWT token_version 失效机制测试"""
import pytest
import base64
import json
from fastapi.testclient import TestClient


class TestJwtTokenVersion:
    def test_token_contains_version(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "jwtuser", "password": "JwtP@ss123"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "jwtuser", "password": "JwtP@ss123"
        })
        assert r.status_code == 200
        token = r.json()["access_token"]
        parts = token.split(".")
        payload = parts[1] + "=" * (4 - len(parts[1]) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        assert data.get("ver") == 0

    def test_old_token_rejected(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "veruser", "password": "VerP@ss123"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "veruser", "password": "VerP@ss123"
        })
        old_token = r.json()["access_token"]
        # 旧 Token 可用
        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {old_token}"})
        assert r.status_code == 200

        # 递增 token_version
        from app.database import SessionLocal
        from app.models.user import User
        db = SessionLocal()
        user = db.query(User).filter(User.username == "veruser").first()
        user.token_version = 1
        db.commit()
        db.close()

        # 旧 Token 被拒
        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {old_token}"})
        assert r.status_code == 401
        assert "失效" in r.json()["detail"]

    def test_relogin_after_bump(self, client: TestClient):
        """版本递增后重新登录，新 Token 可用"""
        client.post("/api/v1/auth/register", json={
            "username": "reuser", "password": "ReP@ss123"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "reuser", "password": "ReP@ss123"
        })
        old_token = r.json()["access_token"]

        from app.database import SessionLocal
        from app.models.user import User
        db = SessionLocal()
        user = db.query(User).filter(User.username == "reuser").first()
        user.token_version = 1
        db.commit()
        db.close()

        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {old_token}"})
        assert r.status_code == 401

        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "reuser", "password": "ReP@ss123"
        })
        new_token = r.json()["access_token"]
        r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {new_token}"})
        assert r.status_code == 200
        assert r.json()["username"] == "reuser"

    def test_multiple_password_resets(self, client: TestClient):
        client.post("/api/v1/auth/register", json={
            "username": "multiuser", "password": "MultiP@ss1"
        })
        r = client.post("/api/v1/auth/login", json={
            "username_or_email": "multiuser", "password": "MultiP@ss1"
        })
        token_v0 = r.json()["access_token"]

        from app.database import SessionLocal
        from app.models.user import User
        db = SessionLocal()
        user = db.query(User).filter(User.username == "multiuser").first()

        for ver in range(1, 4):
            user.token_version = ver
            db.commit()
            r = client.get("/api/v1/auth/me",
                           headers={"Authorization": f"Bearer {token_v0}"})
            assert r.status_code == 401, f"ver={ver}: old token rejected"

            r = client.post("/api/v1/auth/login", json={
                "username_or_email": "multiuser", "password": "MultiP@ss1"
            })
            r = client.get("/api/v1/auth/me",
                           headers={"Authorization": f"Bearer {r.json()['access_token']}"})
            assert r.status_code == 200, f"ver={ver}: new token works"

        db.close()
