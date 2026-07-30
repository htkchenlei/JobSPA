# JobSPA - 全栈项目管理平台 Dockerfile
# 优化版：跳过前端构建阶段，直接使用本地构建好的 dist 目录
#
# 使用前请确保已在前端目录执行过：pnpm run build (或 npm run build)
# 这样 frontend/dist 目录会存在构建产物，Docker 直接复制即可

# ==================== 单阶段构建: 后端运行 ====================
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件（利用 Docker 缓存层，依赖不变时不会重新安装）
COPY backend/requirements.txt ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 复制后端源码
COPY backend/ ./

# 直接复制本地构建好的前端产物（跳过前端构建阶段）
# 请确保在构建镜像前已执行：cd frontend && pnpm run build
COPY frontend/dist ./frontend/dist

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
