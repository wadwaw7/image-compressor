from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator, Field

try:  # Pydantic v2
    from pydantic import ConfigDict  # type: ignore
    _HAS_V2 = True
except Exception:  # pragma: no cover
    ConfigDict = dict  # type: ignore
    _HAS_V2 = False

# === 参数校验常量 ===
VALID_FORMATS = frozenset({"jpeg", "jpg", "png", "webp"})
VALID_CODECS = frozenset({"h264", "h265", "vp9"})
MAX_BATCH_IMAGES = 20       # 单次批量压缩最大图片数
MAX_BATCH_VIDEOS = 5        # 单次视频压缩最大数
MAX_IMAGE_WIDTH = 7680      # 8K 宽度
MAX_IMAGE_HEIGHT = 4320     # 8K 高度
MAX_FPS = 120               # 最大帧率


class CompressTaskOut(BaseModel):
    id: int
    image_id: int
    user_id: int
    compressed_path: str
    compressed_size: int
    format: str
    quality: int
    media_type: Optional[str] = "image"
    status: int
    created_at: Optional[datetime]
    finished_at: Optional[datetime]
    error_message: Optional[str]

    if _HAS_V2:
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:  # type: ignore
            orm_mode = True


class TaskCreate(BaseModel):
    format: str = Field(default="webp", description="输出格式: jpeg, png, webp")
    quality: int = Field(default=80, ge=1, le=100, description="压缩质量 1-100")

    @field_validator("format")
    @classmethod
    def check_format(cls, v: str) -> str:
        v = (v or "webp").lower()
        if v == "jpg":
            v = "jpeg"
        if v not in VALID_FORMATS:
            raise ValueError(f"不支持的格式: {v}，可选: jpeg, png, webp")
        return v


class BatchTaskCreate(BaseModel):
    image_ids: List[int] = Field(..., min_length=1, max_length=MAX_BATCH_IMAGES,
                                  description=f"图片ID列表，最多{MAX_BATCH_IMAGES}张")
    format: str = Field(default="webp", description="输出格式: jpeg, png, webp")
    quality: int = Field(default=80, ge=1, le=100, description="压缩质量 1-100")

    @field_validator("format")
    @classmethod
    def check_format(cls, v: str) -> str:
        v = (v or "webp").lower()
        if v == "jpg":
            v = "jpeg"
        if v not in VALID_FORMATS:
            raise ValueError(f"不支持的格式: {v}，可选: jpeg, png, webp")
        return v

    @field_validator("image_ids")
    @classmethod
    def check_no_duplicates(cls, v: List[int]) -> List[int]:
        """去除重复 ID 并检查有效性"""
        seen = set()
        result = []
        for iid in v:
            if not isinstance(iid, int) or iid <= 0:
                continue
            if iid not in seen:
                seen.add(iid)
                result.append(iid)
        if not result:
            raise ValueError("image_ids 不能为空")
        return result


class VideoCompressRequest(BaseModel):
    image_ids: List[int] = Field(..., min_length=1, max_length=MAX_BATCH_VIDEOS,
                                  description=f"视频ID列表，最多{MAX_BATCH_VIDEOS}个")
    codec: str = Field(default="h264", description="编码器: h264, h265, vp9")
    quality: int = Field(default=60, ge=1, le=100, description="压缩质量 1-100")
    max_width: int = Field(default=0, ge=0, le=MAX_IMAGE_WIDTH,
                           description=f"最大宽度(px)，0=不限制，上限{MAX_IMAGE_WIDTH}")
    max_height: int = Field(default=0, ge=0, le=MAX_IMAGE_HEIGHT,
                            description=f"最大高度(px)，0=不限制，上限{MAX_IMAGE_HEIGHT}")
    fps: int = Field(default=0, ge=0, le=MAX_FPS,
                     description=f"帧率限制，0=不限制，上限{MAX_FPS}")

    @field_validator("codec")
    @classmethod
    def check_codec(cls, v: str) -> str:
        v = (v or "h264").lower()
        if v not in VALID_CODECS:
            raise ValueError(f"不支持的编码器: {v}，可选: h264, h265, vp9")
        return v

    @field_validator("image_ids")
    @classmethod
    def check_no_duplicates(cls, v: List[int]) -> List[int]:
        seen = set()
        result = []
        for iid in v:
            if not isinstance(iid, int) or iid <= 0:
                continue
            if iid not in seen:
                seen.add(iid)
                result.append(iid)
        if not result:
            raise ValueError("image_ids 不能为空")
        return result


class TaskList(BaseModel):
    items: List[CompressTaskOut]
    total: int
