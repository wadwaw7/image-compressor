import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

_TEST_DB = "sqlite:///./pytest_shared.db"
os.environ["DATABASE_URL"] = _TEST_DB


@pytest.fixture(autouse=True)
def setup_test_env():
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    try:
        os.remove("./pytest_shared.db")
    except OSError:
        pass


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
