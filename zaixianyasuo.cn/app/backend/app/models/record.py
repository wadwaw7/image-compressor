from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class CompressTask(Base):
    __tablename__ = "compress_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SmallInteger, nullable=False, default=0)
    format = Column(String(16), nullable=False)
    quality = Column(SmallInteger, nullable=False)
    max_width = Column(Integer, default=0)
    max_height = Column(Integer, default=0)
    output_path = Column(String(256))
    output_size = Column(Integer, default=0)
    error_message = Column(String(256))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
