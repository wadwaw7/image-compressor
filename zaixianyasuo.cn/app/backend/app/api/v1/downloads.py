"""Download counter API — persist counts to JSON file."""

import json
import threading
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/downloads", tags=["downloads"])

# Store counts next to other backend storage
COUNTS_FILE = Path(__file__).resolve().parents[4] / "storage" / "download_counts.json"
_lock = threading.Lock()


def _read_counts() -> dict:
    """Return {windows: int, android: int, total: int, updated_at: str}."""
    try:
        if COUNTS_FILE.exists():
            data = json.loads(COUNTS_FILE.read_text(encoding="utf-8"))
            return data
    except Exception:
        pass
    return {"windows": 0, "android": 0, "total": 0, "updated_at": ""}


def _write_counts(counts: dict) -> None:
    """Persist counts dict to JSON file (thread-safe)."""
    COUNTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        tmp = COUNTS_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(COUNTS_FILE)


@router.get("/stats")
def get_download_stats():
    """Return current download counts."""
    return _read_counts()


@router.post("/record")
def record_download(payload: dict):
    """
    Record a download event.
    Expected body: {"platform": "windows"} or {"platform": "android"}
    """
    platform = str(payload.get("platform", "")).lower()
    if platform not in ("windows", "android"):
        return {"ok": False, "error": "invalid platform, must be 'windows' or 'android'"}

    counts = _read_counts()
    counts[platform] = counts.get(platform, 0) + 1
    counts["total"] = counts.get("total", 0) + 1
    counts["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write_counts(counts)

    return {"ok": True, **counts}
