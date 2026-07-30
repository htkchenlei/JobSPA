# JobSPA 应用镜像
# 基于 jobspa-base:latest（需先构建基础镜像，构建一次即可复用）
#
# 首次部署：
#   docker build -f Dockerfile.base -t jobspa-base:latest .
#   docker-compose up -d --build
#
# 后续更新（业务代码改动，秒级完成）：
#   docker-compose up -d --build

# ==================== 基于预构建的基础镜像 ====================
FROM jobspa-base:latest

WORKDIR /app

# 复制后端源码
COPY backend/ ./

# 复制前端构建产物
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
