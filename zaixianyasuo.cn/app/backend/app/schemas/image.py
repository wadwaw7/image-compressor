from typing import Optional
from pydantic import BaseModel


class UploadResult(BaseModel):
    id: int
    filename: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

    class Config:
        orm_mode = True
