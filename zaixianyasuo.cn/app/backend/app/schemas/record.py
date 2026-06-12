from typing import Optional
from pydantic import BaseModel


class CompressTaskOut(BaseModel):
    id: int
    image_id: int
    status: int
    format: str
    quality: int
    output_path: Optional[str] = None
    output_size: Optional[int] = None

    class Config:
        orm_mode = True
