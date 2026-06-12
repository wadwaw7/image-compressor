from typing import List
import logging
import os
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from ...database import get_db
from ...core.config import get_settings
from ...models.image import Image as ImageModel
from ...models.record import CompressTask as CompressTaskModel
from ...schemas.image import UploadResult
from ...utils.files import save_upload_file, get_ext_from_filename, FileTooLargeError, is_video, IMAGE_MIMES, VIDEO_MIMES, IMAGE_EXTS, VIDEO_EXTS
from ...core.compression import compress_image

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/images", tags=["images"])
ALLOWED_EXTS = IMAGE_EXTS | VIDEO_EXTS


@router.post("/upload", response_model=List[UploadResult])
async def upload_images(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    allowed_mime = IMAGE_MIMES | VIDEO_MIMES
    results: List[UploadResult] = []
    max_image_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    max_video_bytes = settings.MAX_VIDEO_UPLOAD_SIZE_MB * 1024 * 1024

    for f in files:
        if f.content_type not in allowed_mime:
            raise HTTPException(status_code=400, detail=f"Unsupported: {f.content_type}")

        ext = get_ext_from_filename(f.filename or "")
        max_bytes = max_video_bytes if is_video(f.filename or "") else max_image_bytes

        try:
            saved = save_upload_file(f, settings.UPLOAD_DIR, max_bytes)
        except FileTooLargeError:
            raise HTTPException(status_code=413, detail=f"File too large: {f.filename}")

        img = ImageModel(
            filename=saved["original_name"],
            filepath=saved["path"],
            size=saved["size"],
            width=saved.get("width"),
            height=saved.get("height"),
            duration=saved.get("duration"),
            mime_type=f.content_type,
        )
        db.add(img)
        db.commit()
        db.refresh(img)
        results.append(UploadResult(id=img.id, filename=img.filename, size=img.size,
                                     width=img.width, height=img.height, duration=img.duration))

    return results


@router.post("/batch-compress")
async def batch_compress(
    background_tasks: BackgroundTasks,
    image_ids: List[int],
    fmt: str = "jpeg",
    quality: int = 80,
    max_w: int = 0,
    max_h: int = 0,
    db: Session = Depends(get_db),
):
    results = []
    for img_id in image_ids:
        img = db.query(ImageModel).filter(ImageModel.id == img_id).first()
        if not img:
            continue

        task = CompressTaskModel(
            image_id=img.id,
            status=0,
            format=fmt,
            quality=quality,
            max_width=max_w,
            max_height=max_h,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        results.append({"task_id": task.id, "image_id": img.id})

    for t in results:
        background_tasks.add_task(run_compress, t["task_id"])

    return {"ok": True, "tasks": results}


def run_compress(task_id: int):
    from ...database import SessionLocal
    db = SessionLocal()
    try:
        task = db.query(CompressTaskModel).filter(CompressTaskModel.id == task_id).first()
        if not task:
            return
        task.status = 1
        db.commit()

        img = db.query(ImageModel).filter(ImageModel.id == task.image_id).first()
        if not img:
            task.status = 3
            task.error_message = "Image not found"
            db.commit()
            return

        output_path = os.path.join(settings.COMPRESS_DIR, f"{uuid.uuid4().hex}.{task.format}")
        compress_image(img.filepath, output_path, task.format, task.quality, task.max_width, task.max_height)

        task.output_path = output_path
        task.output_size = os.path.getsize(output_path)
        task.status = 2
        db.commit()
    except Exception as e:
        try:
            task.status = 3
            task.error_message = str(e)
            db.commit()
        except Exception:
            pass
    finally:
        db.close()


@router.get("/download/{task_id}")
def download_result(task_id: int, db: Session = Depends(get_db)):
    task = db.query(CompressTaskModel).filter(CompressTaskModel.id == task_id).first()
    if not task or not task.output_path:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(task.output_path, filename=os.path.basename(task.output_path))
