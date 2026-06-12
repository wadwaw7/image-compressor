"""数据库支持的验证码存储 — 解决多 worker 进程间内存不共享问题"""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import delete as sql_delete

from ..models.verification_code import VerificationCode


def gen_code(length: int = 6) -> str:
    length = max(4, min(8, int(length)))
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def _key(purpose: str, subject: str) -> tuple[str, str]:
    return (purpose, (subject or "").strip().lower())


def set_code(db: Session, purpose: str, subject: str, value: Any, ttl_seconds: int) -> None:
    """存储验证码/数据到数据库。同 (purpose, subject) 会覆盖旧记录。"""
    p, s = _key(purpose, subject)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)

    # Upsert: 删除旧记录再插入新记录
    db.execute(
        sql_delete(VerificationCode).where(
            VerificationCode.purpose == p,
            VerificationCode.subject == s,
        )
    )
    record = VerificationCode(
        purpose=p,
        subject=s,
        value=json.dumps(value, ensure_ascii=False),
        expires_at=expires_at,
    )
    db.add(record)
    db.commit()


def get_code(db: Session, purpose: str, subject: str) -> Any | None:
    """获取存储的验证码/数据。过期返回 None。"""
    p, s = _key(purpose, subject)
    now = datetime.now(timezone.utc)

    record = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.purpose == p,
            VerificationCode.subject == s,
        )
        .first()
    )
    if not record:
        return None
    if record.expires_at.replace(tzinfo=timezone.utc) < now:
        db.delete(record)
        db.commit()
        return None
    try:
        return json.loads(record.value)
    except (json.JSONDecodeError, TypeError):
        return record.value


def delete_code(db: Session, purpose: str, subject: str) -> None:
    """删除验证码记录。"""
    p, s = _key(purpose, subject)
    db.execute(
        sql_delete(VerificationCode).where(
            VerificationCode.purpose == p,
            VerificationCode.subject == s,
        )
    )
    db.commit()


def verify_code(db: Session, purpose: str, subject: str, code: str) -> bool:
    """验证验证码。成功则删除记录，失败返回 False。"""
    p, s = _key(purpose, subject)
    now = datetime.now(timezone.utc)

    record = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.purpose == p,
            VerificationCode.subject == s,
        )
        .first()
    )
    if not record:
        return False
    if record.expires_at.replace(tzinfo=timezone.utc) < now:
        db.delete(record)
        db.commit()
        return False

    stored_value = None
    try:
        stored_value = json.loads(record.value)
    except (json.JSONDecodeError, TypeError):
        stored_value = record.value

    if str(code or "").strip() != str(stored_value):
        return False

    db.delete(record)
    db.commit()
    return True


# 清理过期记录（可在定时任务或请求时调用）
def clean_expired(db: Session) -> int:
    """清理所有过期验证码，返回删除条数。"""
    now = datetime.now(timezone.utc)
    result = db.execute(
        sql_delete(VerificationCode).where(VerificationCode.expires_at < now)
    )
    db.commit()
    return result.rowcount


# 保留旧版单例引用以兼容任何仍引用 STORE 的代码（但不应再使用）
class _DeprecatedStore:
    """已废弃的内存存储 — 仅用于提示迁移到数据库版本。"""

    def __getattr__(self, name):
        raise RuntimeError(
            "EmailCodeStore (STORE) 已迁移到数据库。请使用 email_codes.set_code/get_code/verify_code/delete_code 并传入 db session。"
        )


STORE = _DeprecatedStore()
