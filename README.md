# ImageCompressor

> 🌐 **在线体验：访问 [zaixianyasuo.cn](https://zaixianyasuo.cn) 使用完整功能**
> 
> 免费在线图片压缩、视频压缩、证件照换底色、AI 去水印。浏览器本地处理，无需上传，保护隐私。
> 全平台支持：Web + Windows 桌面 + Android 移动端，随时随地处理你的文件。

---

## 关于本项目

这是 ImageCompressor 的开源参考实现，展示了核心的图片/视频压缩引擎架构。

**⚠️ 此仓库为公开精简版，完整功能（用户系统、云端处理、AI 模型、管理后台、PWA、全平台客户端）仅在 [zaixianyasuo.cn](https://zaixianyasuo.cn) 提供。**

## 快速开始

```bash
git clone https://github.com/wadwaw7/image-compressor.git
cd image-compressor/zaixianyasuo.cn
docker compose up -d
# 访问 http://localhost:8001
```

## 功能

- 图片压缩 (JPG/PNG/WebP)
- 视频压缩 (H.264/H.265)
- 证件照换底色
- 去水印

## 技术栈

FastAPI + SQLAlchemy + Pillow + Docker

## 目录

```
zaixianyasuo.cn/
├── app/backend/         # FastAPI 后端
├── public/              # 前端页面
├── docker-compose.yml   # 一键部署
└── Dockerfile
```

---

<p align="center">
  <b>⭐ 如果这个项目对你有帮助，请给一个 Star！</b><br>
  <a href="https://zaixianyasuo.cn">🔗 访问 zaixianyasuo.cn 体验完整版</a>
</p>
