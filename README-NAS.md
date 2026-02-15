# JobSPA项目NAS部署说明

本文档提供将JobSPA项目部署到Synology NAS或其他支持Docker的NAS设备的详细步骤。

## 前提条件

- NAS设备运行Docker服务
- NAS设备上已安装Docker Compose
- 网络连接正常
- 有足够的存储空间

## 部署步骤

### 步骤1: 准备项目文件

1. **从GitHub克隆项目**（推荐）：
   在NAS的终端中执行：
   ```bash
   cd /volume1/docker
   git clone https://github.com/htkchenlei/JobSPA.git
   cd JobSPA
   ```

2. **或通过其他方式复制项目文件**：
   - 将项目压缩包上传到NAS
   - 解压到 `/volume1/docker/JobSPA` 目录

### 步骤2: 构建前端项目（如果需要）

如果项目中没有 `frontend/dist` 目录，需要先构建前端项目：

```bash
# 进入frontend目录
cd /volume1/docker/JobSPA/frontend

# 安装依赖
npm install

# 构建前端项目
npm run build

# 返回项目根目录
cd ..
```

### 步骤3: 运行部署脚本

1. **给部署脚本添加执行权限**：
   ```bash
   chmod +x deploy-nas.sh
   ```

2. **运行部署脚本**：
   ```bash
   ./deploy-nas.sh
   ```

   脚本会自动：
   - 检查Docker和Docker Compose是否安装
   - 创建uploads目录
   - 构建Docker镜像
   - 启动服务
   - 检查服务状态

### 步骤4: 访问项目

部署完成后，可以通过以下地址访问JobSPA项目：

```
http://<NAS的IP地址>:15667
```

例如：
```
http://192.168.2.2:15667
```

### 步骤5: 登录系统

- **默认用户名**: admin
- **默认密码**: tianyu.123

## 配置说明

### 环境变量

主要配置项在 `docker-compose-nas.yml` 文件中：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT签名密钥
- `DEBUG`: 调试模式（生产环境应设为False）
- `FILE_ROOT_DIRECTORY`: 文件上传根目录

### 数据持久化

- **上传文件**: 存储在 `./uploads` 目录
- **数据库数据**: 存储在Docker卷 `mysql-data` 中

## 管理命令

### 启动服务
```bash
docker-compose -f docker-compose-nas.yml up -d
```

### 停止服务
```bash
docker-compose -f docker-compose-nas.yml down
```

### 查看服务状态
```bash
docker-compose -f docker-compose-nas.yml ps
```

### 查看日志
```bash
docker-compose -f docker-compose-nas.yml logs
```

### 重启服务
```bash
docker-compose -f docker-compose-nas.yml restart
```

## 常见问题

### 1. 服务启动失败

- 检查Docker服务是否运行
- 检查端口5000和3306是否被占用
- 查看日志获取详细错误信息：
  ```bash
  docker-compose -f docker-compose-nas.yml logs
  ```

### 2. 数据库连接错误

- 确保MySQL服务已启动
- 检查数据库连接字符串配置
- 检查数据库用户名和密码

### 3. 文件上传失败

- 确保uploads目录存在且有写权限
- 检查FILE_ROOT_DIRECTORY配置

### 4. 前端页面无法访问

- 确保frontend/dist目录存在
- 检查前端构建是否成功
- 检查Docker卷映射是否正确

## 技术支持

如果遇到部署问题，请参考以下资源：

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose官方文档](https://docs.docker.com/compose/)
- [Synology NAS Docker指南](https://www.synology.com/en-global/knowledgebase/DSM/tutorial/Virtualization/How_to_deploy_a_Node_js_project_with_Docker)

## 版本信息

- 项目版本: 1.0.0
- Docker版本: 推荐19.03+
- Docker Compose版本: 推荐1.25+
