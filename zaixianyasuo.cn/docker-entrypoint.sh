#!/bin/bash
# Docker 启动脚本：等待 MySQL 就绪 → 创建表 → 启动应用
set -e

echo "ImageCompressor Backend starting..."

# 等待 MySQL 就绪（最多 30 秒）
if [ -n "$DATABASE_URL" ] && echo "$DATABASE_URL" | grep -q "mysql"; then
    echo "Waiting for MySQL..."
    HOST=$(echo "$DATABASE_URL" | sed -n 's/.*@\([^:]*\).*/\1/p')
    for i in $(seq 1 30); do
        if python -c "
import pymysql, os
url = os.environ['DATABASE_URL']
# mysql://user:pass@host:port/db
host = url.split('@')[1].split(':')[0]
user = url.split('://')[1].split(':')[0]
passwd = url.split(':')[2].split('@')[0]
db = url.split('/')[-1]
try:
    conn = pymysql.connect(host=host, user=user, password=passwd, database=db)
    conn.close()
    print('MySQL ready')
except:
    exit(1)
" 2>/dev/null; then
            echo "MySQL is ready"
            break
        fi
        echo "  Attempt $i/30..."
        sleep 1
    done
fi

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
