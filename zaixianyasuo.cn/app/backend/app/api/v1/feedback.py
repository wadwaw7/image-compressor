import json, os, threading
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from ...utils.email_sender import send_email, EmailSendError
from ...utils.security import get_current_token
from ...database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/feedback", tags=["feedback"])

FEEDBACK_FILE = Path(__file__).resolve().parents[4] / "storage" / "feedback.json"
FEEDBACK_LOCK = threading.Lock()

class FeedbackSubmit(BaseModel):
    subject: str = Field(default="", max_length=200)
    message: str = Field(min_length=5, max_length=2000)
    contact: str = Field(default="", max_length=100)

def _load():
    try:
        if FEEDBACK_FILE.exists():
            return json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []

def _save(items):
    with FEEDBACK_LOCK:
        FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        FEEDBACK_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


@router.post("")
def submit_feedback(request: Request, payload: FeedbackSubmit):
    now = datetime.utcnow()
    fb = {
        "id": now.strftime("%Y%m%d%H%M%S") + "_" + str(int(now.timestamp() * 1000))[-6:],
        "subject": (payload.subject or "无主题").strip(),
        "message": payload.message.strip(),
        "contact": (payload.contact or "未留").strip(),
        "ip": request.client.host if request.client else "",
        "ua": (request.headers.get("User-Agent", "") or "")[:200],
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
    }
    items = _load()
    items.append(fb)
    _save(items)

    # Email to admin
    try:
        html = (
            '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.7">'
            '<h3>ImageCompress 用户反馈</h3>'
            '<p><b>主题：</b>' + fb["subject"] + '</p>'
            '<p><b>内容：</b>' + fb["message"].replace("\n", "<br>") + '</p>'
            '<p><b>联系方式：</b>' + fb["contact"] + '</p>'
            '<p><b>时间：</b>' + fb["time"] + '</p>'
            '<p><b>IP：</b>' + fb["ip"] + '</p>'
            '</div>'
        )
        admin_email = os.getenv("ADMIN_EMAIL", "")
        if admin_email:
            send_email(admin_email, "【ImageCompress】用户反馈 - " + fb["subject"], html)
    except EmailSendError:
        pass

    return {"ok": True, "id": fb["id"]}


@router.get("")
def list_feedback(token=Depends(get_current_token), db: Session = Depends(get_db)):
    from ...models.user import User
    from fastapi import HTTPException, status

    uid = int(token.get("sub"))
    user = db.query(User).get(uid)
    if not user or not getattr(user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅管理员可查看")

    items = _load()
    changed = False
    for item in items:
        if not item.get("read"):
            item["read"] = True
            changed = True
    if changed:
        _save(items)

    sorted_items = sorted(items, key=lambda x: x.get("time", ""), reverse=True)
    return {"items": sorted_items, "total": len(sorted_items)}
