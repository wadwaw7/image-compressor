# ImageCompressor Backend Dockerfile
# 基于 Python 3.12 + OpenCV + FFmpeg
FROM python:3.12-slim

LABEL app="image-compressor" description="在线图片视频压缩工具后端"

# 系统依赖：OpenCV 需要 libGL，FFmpeg 用于视频压缩
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先装依赖（利用 Docker 层缓存）
COPY app/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/backend/app ./app
COPY app/backend/tests ./tests
COPY app/backend/storage ./storage

# 创建上传和压缩目录
RUN mkdir -p /app/storage/uploads /app/storage/compressed && \
    chmod 755 /app/storage

EXPOSE 8001

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')" || exit 1

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
