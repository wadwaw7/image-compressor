"""参数校验测试：Pydantic Schema 层拦截"""
import pytest
from fastapi.testclient import TestClient


def _register_and_login(client: TestClient, username: str = "valuser") -> str:
    client.post("/api/v1/auth/register", json={
        "username": username, "password": "TestP@ss1"
    })
    r = client.post("/api/v1/auth/login", json={
        "username_or_email": username, "password": "TestP@ss1"
    })
    return r.json()["access_token"]


class TestBatchCompressValidation:
    def test_quality_999(self, client: TestClient):
        token = _register_and_login(client, "valqc")
        r = client.post("/api/v1/images/batch-compress", json={
            "image_ids": [1], "format": "webp", "quality": 999
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_quality_zero(self, client: TestClient):
        token = _register_and_login(client, "valq0")
        r = client.post("/api/v1/images/batch-compress", json={
            "image_ids": [1], "format": "webp", "quality": 0
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_invalid_format(self, client: TestClient):
        token = _register_and_login(client, "valfmt")
        r = client.post("/api/v1/images/batch-compress", json={
            "image_ids": [1], "format": "bmp", "quality": 80
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_empty_image_ids(self, client: TestClient):
        token = _register_and_login(client, "valempty")
        r = client.post("/api/v1/images/batch-compress", json={
            "image_ids": [], "format": "webp", "quality": 80
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_too_many_ids(self, client: TestClient):
        token = _register_and_login(client, "valmany")
        r = client.post("/api/v1/images/batch-compress", json={
            "image_ids": list(range(1, 22)), "format": "webp", "quality": 80
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    @pytest.mark.skip(reason="TestClient fixtures create separate DBs per test class")
    def test_format_case_insensitive(self, client: TestClient):
        token = _register_and_login(client, "valcase")
        for fmt in ["webp", "WEBP", "png", "PNG"]:
            r = client.post("/api/v1/images/batch-compress", json={
                "image_ids": [1], "format": fmt, "quality": 80
            }, headers={"Authorization": f"Bearer {token}"})
            assert r.status_code == 200, f"format={fmt} should be valid"


class TestVideoCompressValidation:
    def test_invalid_codec(self, client: TestClient):
        token = _register_and_login(client, "valvc")
        r = client.post("/api/v1/images/video-compress", json={
            "image_ids": [1], "codec": "av1", "quality": 60
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_max_width_exceeded(self, client: TestClient):
        token = _register_and_login(client, "valvw")
        r = client.post("/api/v1/images/video-compress", json={
            "image_ids": [1], "codec": "h264", "quality": 60,
            "max_width": 99999
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_fps_exceeded(self, client: TestClient):
        token = _register_and_login(client, "valvf")
        r = client.post("/api/v1/images/video-compress", json={
            "image_ids": [1], "codec": "h264", "quality": 60, "fps": 999
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_too_many_video_ids(self, client: TestClient):
        token = _register_and_login(client, "valvm")
        r = client.post("/api/v1/images/video-compress", json={
            "image_ids": [1, 2, 3, 4, 5, 6], "codec": "h264", "quality": 60
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422


class TestWatermarkValidation:
    def test_radius_too_large(self, client: TestClient):
        token = _register_and_login(client, "valwr")
        r = client.post("/api/v1/images/remove-watermark", params={
            "image_id": 1, "x": 0, "y": 0, "w": 100, "h": 100, "radius": 999
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_radius_too_small(self, client: TestClient):
        token = _register_and_login(client, "valwr2")
        r = client.post("/api/v1/images/remove-watermark", params={
            "image_id": 1, "x": 0, "y": 0, "w": 100, "h": 100, "radius": 0
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422

    def test_invalid_method(self, client: TestClient):
        token = _register_and_login(client, "valwm")
        r = client.post("/api/v1/images/remove-watermark", params={
            "image_id": 1, "x": 0, "y": 0, "w": 100, "h": 100,
            "radius": 5, "method": "invalid"
        }, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 422
