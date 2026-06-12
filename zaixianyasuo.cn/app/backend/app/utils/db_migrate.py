"""Database migration utilities."""

from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def ensure_media_type_column(engine: Engine) -> None:
    """Ensure media_type column exists on images table."""
    try:
        inspector = inspect(engine)
        if "images" not in inspector.get_table_names():
            return
        cols = {c["name"] for c in inspector.get_columns("images")}
        if "media_type" not in cols:
            with engine.begin() as conn:
                conn.exec_driver_sql(
                    "ALTER TABLE images ADD COLUMN media_type VARCHAR(8) NOT NULL DEFAULT 'image'"
                )
    except Exception:
        pass
