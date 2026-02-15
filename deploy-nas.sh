#!/bin/bash

# JobSPA项目NAS部署脚本

echo "=== JobSPA项目部署到NAS ==="

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装"
    exit 1
fi

echo "Docker和Docker Compose已安装"

# 进入项目目录
cd "$(dirname "$0")"

echo "当前目录: $(pwd)"

# 创建uploads目录
if [ ! -d "uploads" ]; then
    echo "创建uploads目录..."
    mkdir -p uploads
fi

# 构建Docker镜像
echo "构建Docker镜像..."
docker-compose -f docker-compose-nas.yml build

# 启动服务
echo "启动服务..."
docker-compose -f docker-compose-nas.yml up -d

# 检查服务状态
echo "检查服务状态..."
docker-compose -f docker-compose-nas.yml ps

echo "\n=== 部署完成 ==="
echo "项目已部署到: http://localhost:15667"
echo "\n后续操作:"
echo "1. 访问 http://localhost:15667 登录系统"
echo "2. 默认用户名: admin, 密码: tianyu.123"
echo "3. 如需停止服务: docker-compose -f docker-compose-nas.yml down"
echo "4. 如需查看日志: docker-compose -f docker-compose-nas.yml logs"
