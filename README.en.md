<h1 align="center">
  <img src="https://github.com/wadwaw7/image-compressor/actions/workflows/test.yml/badge.svg" alt="CI">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs">
</h1>

# 🚀 ImageCompressor — Online Image & Video Tool

<p align="center">
  <b>Compression | Background Change | Watermark Removal</b><br>
  Browser-side processing · Privacy safe · Cross-platform
</p>

<p align="center">
  <a href="https://zaixianyasuo.cn"><b>🌐 Live Demo: zaixianyasuo.cn</b></a> ·
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-contributing">Contributing</a>
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Image Compression** | JPG / PNG / WebP, batch processing |
| **Video Compression** | H.264 / H.265 / VP9, CRF control |
| **Background Change** | One-click blue/red/white background |
| **Watermark Removal** | AI-powered inpainting, local processing |

> 💡 **Core engine is open-source**. Advanced features (user accounts, cloud acceleration, PWA, desktop/mobile apps) available at [zaixianyasuo.cn](https://zaixianyasuo.cn).

## 📋 Requirements

- **Docker** 20.10+ or **Python** 3.10+
- 2GB+ RAM
- Chrome / Edge / Firefox (latest)

## 🚀 Quick Start

```bash
git clone https://github.com/wadwaw7/image-compressor.git
cd image-compressor/zaixianyasuo.cn
docker compose up -d
# http://localhost:8001
```

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + SQLAlchemy + Pillow + OpenCV |
| Frontend | Vanilla JS + CSS Custom Properties |
| Deploy | Docker + docker-compose |

## 📁 Project Structure

```
├── zaixianyasuo.cn/
│   ├── app/backend/          # FastAPI backend
│   ├── public/               # Frontend pages
│   ├── Dockerfile
│   └── docker-compose.yml
├── API.md                    # API docs
├── DEVELOPMENT.md            # Dev guide
├── LICENSE                   # MIT
└── CONTRIBUTING.md
```

## 🤝 Contributing

Issues and PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License © 2025 ImageCompressor

---

<p align="center">
  ⭐ Star if you find this useful!<br>
  <a href="https://zaixianyasuo.cn">🔗 Try the full version at zaixianyasuo.cn</a>
</p>
