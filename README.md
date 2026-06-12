# ImageCompressor 🚀

**在线图片/视频压缩工具** — 浏览器端处理，无需上传，保护隐私。

> 🌐 在线体验：[zaixianyasuo.cn](https://zaixianyasuo.cn)

## ✨ 功能亮点

- **图片压缩** — 支持 JPG/PNG/WebP/AVIF，智能质量调节，批量处理
- **视频压缩** — H.264/H.265 编码，CRF 控制，保留最佳画质
- **背景更换** — 一键抠图换背景，预设证件照尺寸
- **去水印** — AI 修复算法，智能去除图片水印
- **全平台覆盖** — Web + Windows 桌面 + Android 移动端
- **PWA 离线支持** — 添加到桌面，离线也能用
- **中英双语** — 完整国际化

## 🚀 快速开始

### Docker（推荐）

```bash
cd zaixianyasuo.cn
cp .env.example .env
# 编辑 .env 设置密码
docker compose up -d
# 访问 http://localhost:8001
```

### 手动运行

```bash
cd zaixianyasuo.cn/app/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

> 📖 详细文档见 [zaixianyasuo.cn](https://zaixianyasuo.cn)

## 🛠 技术栈

| 层 | 技术 |
|---|------|
| 后端 | FastAPI + SQLAlchemy + Pillow + FFmpeg |
| 前端 | Vanilla JS (ES Modules) + CSS Custom Properties |
| 桌面 | Tauri v2 + Rust |
| 移动 | Capacitor + Android |
| 数据库 | MySQL 8.0 / SQLite |
| 部署 | Docker + Nginx + systemd |

## 📁 目录结构

```
├── zaixianyasuo.cn/          # 主应用
│   ├── app/backend/          # FastAPI 后端
│   ├── app/frontend/         # 现代前端 (SPA)
│   ├── public/               # 静态页面
│   ├── deploy/               # 部署脚本
│   ├── docker-compose.yml    # Docker 编排
│   └── Dockerfile
├── image-compress-online/    # 桌面 + 移动端
│   └── app/                  # Vite + Tauri + Capacitor
└── README.md
```

## ⚙️ 配置

复制 `.env.example` 为 `.env`，按需修改：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接（空=SQLite） | 空 |
| `SECRET_KEY` | JWT 签名密钥 | 自动生成 |
| `AUTH_DISABLED` | 跳过认证（本地调试） | 0 |
| `CONCURRENCY` | 压缩并发数 | 4 |

## 📄 许可

本项目仅供学习和参考。在线服务请访问 [zaixianyasuo.cn](https://zaixianyasuo.cn)。

---

⭐ 如果这个项目对你有帮助，欢迎 Star & 分享！
