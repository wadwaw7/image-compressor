"""验证码数据库模型 — 解决多 worker 进程间内存不共享问题"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from ..database import Base


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    purpose = Column(String(64), nullable=False, index=True)
    subject = Column(String(256), nullable=False, index=True)
    value = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("purpose", "subject", name="uq_verification_purpose_subject"),
    )
