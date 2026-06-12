from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy.sql import func
from ..database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    filename = Column(String(128), nullable=False)
    filepath = Column(String(256), nullable=False)
    size = Column(Integer, nullable=False)
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)
    mime_type = Column(String(64))
    upload_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(SmallInteger, server_default="1")
    media_type = Column(String(8), nullable=False, default="image")
