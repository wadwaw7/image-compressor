# 开发指南

## 环境设置

```bash
# 克隆仓库
git clone https://github.com/wadwaw7/image-compressor.git
cd image-compressor

# 后端
cd zaixianyasuo.cn/app/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# 运行
uvicorn app.main:app --reload --port 8001
```

## 运行测试

```bash
cd zaixianyasuo.cn/app/backend
python -m pytest tests/ -v
```

## Docker 开发

```bash
cd zaixianyasuo.cn
docker compose up -d --build
docker compose logs -f
```

## 代码风格

- Python: PEP 8
- 前端: 保持项目已有风格
- 提交: 约定式提交 (feat/fix/docs/chore)

## 在线体验

[zaixianyasuo.cn](https://zaixianyasuo.cn)
