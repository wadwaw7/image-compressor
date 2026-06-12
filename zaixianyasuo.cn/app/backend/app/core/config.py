import os
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv

BACKEND_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
APP_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

for env_path in (APP_ENV_PATH, BACKEND_ENV_PATH):
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_UPLOAD_DIR = REPO_ROOT / "storage" / "uploads"
DEFAULT_COMPRESS_DIR = REPO_ROOT / "storage" / "compressed"

@lru_cache()
def get_settings():
    class Settings:
        DATABASE_URL: str = os.getenv("DATABASE_URL", "")
        CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
        UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(DEFAULT_UPLOAD_DIR))
        COMPRESS_DIR: str = os.getenv("COMPRESS_DIR", str(DEFAULT_COMPRESS_DIR))
        MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
        MAX_VIDEO_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_VIDEO_UPLOAD_SIZE_MB", "200"))
        MAX_VIDEO_DURATION_SEC: int = int(os.getenv("MAX_VIDEO_DURATION_SEC", "600"))
        CONCURRENCY: int = int(os.getenv("CONCURRENCY", "4"))
        FRONTEND_DIR: str = os.getenv("FRONTEND_DIR", str(REPO_ROOT / "frontend"))

        @property
        def sql_alchemy_url(self) -> str:
            dburl = (self.DATABASE_URL or "").strip()
            if dburl:
                return dburl
            sqlite_path = REPO_ROOT / "storage" / "db.sqlite3"
            sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{sqlite_path.as_posix()}"

    settings = Settings()
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.COMPRESS_DIR).mkdir(parents=True, exist_ok=True)
    return settings
