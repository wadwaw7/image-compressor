<h1 align="center">
  <img src="https://github.com/wadwaw7/image-compressor/actions/workflows/test.yml/badge.svg" alt="CI">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="PRs">
</h1>

# 🚀 ImageCompressor — 在线图片/视频压缩工具

<p align="center">
  <b>图片/视频压缩 | 证件照换底色 | AI 去水印</b><br>
  浏览器本地处理 · 隐私安全 · 全平台
</p>

<p align="center">
  <a href="https://zaixianyasuo.cn"><b>🌐 zaixianyasuo.cn 在线体验</b></a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-功能">功能</a> ·
  <a href="#-技术栈">技术栈</a> ·
  <a href="#-贡献">贡献</a>
</p>

---

## 📸 功能演示

### 🎯 简单强大的压缩工具

支持多种格式、批量处理、隐私保护：

![功能介绍](https://zaixianyasuo.cn/images/features.png)

### 💪 实际压缩效果

一张 60.7 KB 的图片压缩到 26.7 KB，质量 80%：

![压缩效果](https://zaixianyasuo.cn/images/compress-demo.png)

### 📱 Web vs 应用对比

网页版无限制，应用版功能更强：

![功能对比](https://zaixianyasuo.cn/images/comparison.png)

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| **图片压缩** | JPG / PNG / WebP，智能质量调节，批量处理 |
| **视频压缩** | H.264 / H.265 / VP9 编码，CRF 控制 |
| **证件照换底色** | 一键换蓝底/红底/白底，预设尺寸 |
| **AI 去水印** | 智能框选修复，本地处理 |

> 💡 **本项目开源核心压缩引擎**。用户系统、云端加速、PWA、桌面/移动客户端等进阶功能请访问 [zaixianyasuo.cn](https://zaixianyasuo.cn)。

## 📋 系统要求

- **Docker** 20.10+ 或 **Python** 3.10+
- 2GB+ 可用内存
- 推荐 Chrome / Edge / Firefox 最新版

## 🚀 快速开始

```bash
git clone https://github.com/wadwaw7/image-compressor.git
cd image-compressor/zaixianyasuo.cn
docker compose up -d
# http://localhost:8001
```

## 🛠 技术栈

| 层 | 技术 |
|---|------|
| 后端 | FastAPI + SQLAlchemy + Pillow + OpenCV |
| 前端 | Vanilla JS + CSS Custom Properties |
| 部署 | Docker + docker-compose |

## 📁 项目结构

```
├── zaixianyasuo.cn/
│   ├── app/backend/          # FastAPI 后端
│   │   ├── api/v1/           # API 路由
│   │   ├── core/             # 压缩引擎
│   │   ├── models/           # 数据模型
│   │   └── tests/            # 测试
│   ├── public/               # 前端页面
│   ├── Dockerfile
│   └── docker-compose.yml
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # 贡献指南
└── CHANGELOG.md              # 更新日志
```

## 🤝 贡献

欢迎 Issue / PR！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可

MIT License © 2025 ImageCompressor

---

<p align="center">
  ⭐ 有帮助的话，给个 Star！<br>
  <a href="https://zaixianyasuo.cn">🔗 zaixianyasuo.cn 体验完整版</a>
</p>
