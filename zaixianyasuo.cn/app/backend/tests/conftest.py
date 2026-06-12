"""Pytest 配置：为所有测试提供统一的基础设施

安全设计：
- 模块级 os.environ["DATABASE_URL"] = SQLite 文件 → 确保 pytest 收集阶段
  test_security.py 等旧测试的模块级 import 链不会误触 database.py 连生产 MySQL
- 每个测试函数跑前 create_all、跑后 drop_all → 测试隔离
- slowapi 限流用 monkeypatch mock 掉 → 避免 429
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ============================================================
# 模块级安全网 —— 先于任何测试模块 import 生效
# ============================================================
_TEST_DB = "sqlite:///./pytest_shared.db"
os.environ["DATABASE_URL"] = _TEST_DB


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """每个测试函数前后：建表 / 删表（同一 SQLite 文件，串行安全）"""
    # mock 限流
    def fake_limit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    monkeypatch.setattr("app.utils.ratelimit.limiter.limit", fake_limit)
    monkeypatch.setattr("app.utils.ratelimit.limiter._check_request_limit", lambda *a, **kw: None)
    monkeypatch.setenv("MAX_LOGIN_ATTEMPTS", "999")
    monkeypatch.setenv("LOGIN_LOCK_MINUTES", "0")

    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """整个测试会话结束后删除共享 SQLite 文件"""
    yield
    try:
        os.remove("./pytest_shared.db")
    except OSError:
        pass


@pytest.fixture
def client():
    """FastAPI TestClient"""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    """创建一个管理员并返回 token（绕过 2FA）"""
    from app.database import SessionLocal
    from app.models.user import User
    from app.utils.security import create_access_token, get_password_hash

    db = SessionLocal()
    admin = db.query(User).filter(User.username == "testadmin").first()
    if not admin:
        admin = User(
            username="testadmin", email="testadmin@test.com",
            password_hash=get_password_hash("AdminP@ss1"),
            is_admin=True, is_active=True, status=1, token_version=0
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    token = create_access_token({"sub": str(admin.id)}, token_version=admin.token_version)
    db.close()
    return token
