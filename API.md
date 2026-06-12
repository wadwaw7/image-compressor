# API 文档

基础 URL: `http://localhost:8001`

## 端点

### 健康检查

```bash
curl http://localhost:8001/health
# {"status":"ok"}
```

### 上传图片

```bash
curl -X POST http://localhost:8001/api/v1/images/upload \
  -F "files=@photo.jpg" \
  -F "files=@photo2.png"
# [{"id":1,"filename":"photo.jpg","size":204800,"width":1920,"height":1080}]
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `files` | File[] | 图片/视频文件，支持 JPG/PNG/WebP/MP4/MOV |

### 批量压缩

```bash
curl -X POST http://localhost:8001/api/v1/images/batch-compress \
  -H "Content-Type: application/json" \
  -d '{"image_ids":[1,2],"fmt":"webp","quality":80,"max_w":1920,"max_h":0}'
# {"ok":true,"tasks":[{"task_id":1,"image_id":1}]}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_ids` | int[] | 必填 | 图片 ID 列表 |
| `fmt` | string | `jpeg` | 输出格式: jpeg/png/webp |
| `quality` | int | `80` | 压缩质量 1-100 |
| `max_w` | int | `0` | 最大宽度，0=不限 |
| `max_h` | int | `0` | 最大高度，0=不限 |

### 下载结果

```bash
curl -O http://localhost:8001/api/v1/images/download/1
```

## 支持格式

| 类型 | 输入 | 输出 |
|------|------|------|
| 图片 | JPG, PNG, WebP | JPEG, PNG, WebP |
| 视频 | MP4, MOV, AVI, WebM, MKV, FLV, WMV | H.264/H.265/VP9 |

## 限制

| 项目 | 限制 |
|------|------|
| 图片大小 | 20 MB |
| 视频大小 | 200 MB |
| 视频时长 | 600 秒 |

> 完整功能（用户系统、云端加速、全平台客户端）请访问 [zaixianyasuo.cn](https://zaixianyasuo.cn)
