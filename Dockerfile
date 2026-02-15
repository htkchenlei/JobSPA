# 后端服务Dockerfile
FROM python:3.9-slim

# 设置参数
ARG WERKZEUG_VERSION=2.0.1

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir Werkzeug==${WERKZEUG_VERSION}

# 复制后端代码
COPY backend/ .

# 复制前端构建文件
COPY frontend/dist/ ./frontend/dist/

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["python", "app.py"]