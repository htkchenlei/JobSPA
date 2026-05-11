# JobSPA - 全栈项目管理平台 Dockerfile
# 多阶段构建：前端构建 + 后端运行

# ==================== 阶段1: 前端构建 ====================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package.json frontend/pnpm-lock.yaml* ./

# 安装 pnpm 并安装依赖
RUN npm install -g pnpm && pnpm install --frozen-lockfile

# 复制前端源码
COPY frontend/ ./

# 构建前端
RUN pnpm run build

# ==================== 阶段2: 后端运行 ====================
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 复制后端源码
COPY backend/ ./

# 从前端构建阶段复制构建产物
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 创建数据目录和上传目录
RUN mkdir -p /app/data /app/uploads && chmod 777 /app/data /app/uploads

# 设置环境变量
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# 初始化数据库
RUN python init_db.py

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]
