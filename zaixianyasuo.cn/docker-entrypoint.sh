#!/bin/bash
set -e
echo "ImageCompressor starting..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
