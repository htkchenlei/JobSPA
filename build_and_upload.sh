#!/bin/bash

# 项目根目录
PROJECT_ROOT="$(pwd)"
# NAS地址
NAS_ADDRESS="192.168.2.2"
# NAS上的项目目录
NAS_PROJECT_DIR="/volume1/docker/JobSPA"

# 停止并移除现有的容器
echo "停止并移除现有的容器..."
docker-compose down

# 构建Docker镜像
echo "构建Docker镜像..."
docker-compose build

# 验证构建结果
if [ $? -ne 0 ]; then
    echo "构建失败，请检查错误信息"
    exit 1
fi

echo "构建成功！"

# 保存镜像为tar文件
echo "保存镜像为tar文件..."
docker save jobspa-backend jobspa-frontend > jobspa_images.tar

if [ $? -ne 0 ]; then
    echo "保存镜像失败，请检查错误信息"
    exit 1
fi

echo "镜像保存成功！"

# 上传到NAS
echo "上传镜像到NAS..."
scp jobspa_images.tar admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/

if [ $? -ne 0 ]; then
    echo "上传失败，请检查错误信息"
    exit 1
fi

echo "上传成功！"

# 上传docker-compose.yml文件
echo "上传docker-compose.yml文件到NAS..."
scp docker-compose.yml admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/

if [ $? -ne 0 ]; then
    echo "上传docker-compose.yml失败，请检查错误信息"
    exit 1
fi

echo "docker-compose.yml上传成功！"

# 上传SQLite数据库文件
echo "上传SQLite数据库文件到NAS..."
mkdir -p $PROJECT_ROOT/data
cp $PROJECT_ROOT/backend/projectmanagement.db $PROJECT_ROOT/data/
scp $PROJECT_ROOT/data/projectmanagement.db admin@$NAS_ADDRESS:$NAS_PROJECT_DIR/data/

if [ $? -ne 0 ]; then
    echo "上传数据库文件失败，请检查错误信息"
    exit 1
fi

echo "数据库文件上传成功！"

# 清理本地文件
echo "清理本地文件..."
rm -f jobspa_images.tar
rm -rf $PROJECT_ROOT/data

echo "清理完成！"
echo "项目打包并上传到NAS成功！"
echo "请在NAS上执行以下命令启动容器："
echo "cd $NAS_PROJECT_DIR && docker-compose up -d"
