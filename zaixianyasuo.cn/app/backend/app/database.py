import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.config import get_settings
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.sql_alchemy_url

_engine_kwargs = {"pool_pre_ping": True}
_parsed = urlparse(SQLALCHEMY_DATABASE_URL)
_is_mysql = "mysql" in _parsed.scheme or "mysql" in SQLALCHEMY_DATABASE_URL.lower()
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
elif _is_mysql:
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["pool_recycle"] = 3600

engine = create_engine(SQLALCHEMY_DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================
# 安全检查：禁止在生产 MySQL 上执行 drop_all
# SQLAlchemy 的 Base.metadata.drop_all(engine) 会删除全部表 —
# 测试框架的 conftest.py 误触此操作即为本次事故根因。
# 这个 monkey-patch 确保 drop_all 在 MySQL 上直接报错。
# ============================================================
_original_drop_all = Base.metadata.drop_all

def _safe_drop_all(bind=None, **kwargs):
    url = str(getattr(bind, 'url', '') if bind else '')
    if 'mysql' in url.lower():
        raise RuntimeError(
            "DROP_ALL 被拒绝：当前连接的是 MySQL 生产数据库！"
            "测试必须使用 SQLite（conftest.py 模块级已覆盖 DATABASE_URL）。"
        )
    _original_drop_all(bind=bind, **kwargs)

Base.metadata.drop_all = _safe_drop_all

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

