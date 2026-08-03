# JobSPA - 项目管理平台

一个现代化的全栈项目管理平台，采用马卡龙撞色风格设计，帮助团队高效管理项目和工作日志。

## ✨ 功能特性

### 📊 仪表盘
- 项目统计概览（总数、进行中、已完成、本周日志）
- 项目阶段分布图表
- 最近项目更新动态

### 📋 项目管理
- 项目全生命周期管理（立项 → 招投标 → 已中标 → 已完成）
- 项目进度历史记录
- 项目分类展示
- 快速筛选和搜索
- 删除项目（**仅管理员**，软删除）

### 🔍 高级查询
- 多条件组合查询
- 按省份、阶段、规模筛选
- 关键词搜索

### 📈 统计分析
- 各省份项目分布
- 项目金额统计
- 阶段分布分析
- 月度趋势图

### 📝 工作日志
- 日历视图展示
- AI 自动生成工作日志
- 历史日志查看

### 🌐 对外公开 API
- 无需认证的公共接口
- 支持按周/月/自定义范围查询项目更新
- 在线 API 文档页面 (`/api-documentation`)

## 🛠 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 快速构建工具
- **Vue Router** - 路由管理
- **Chart.js** - 图表可视化
- **ECharts** - 高级图表

### 后端
- **Flask 2.0** - Python Web 框架
- **SQLAlchemy** - ORM 数据库工具
- **SQLite** - 轻量级数据库
- **PyJWT** - 身份认证

## 📁 项目结构

```
JobSPA/
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   ├── router/         # 路由配置
│   │   └── style.css       # 全局样式
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── routes/         # API 路由
│   │   ├── models/         # 数据模型
│   │   └── __init__.py     # Flask 应用
│   ├── uploads/            # 文件上传目录
│   ├── requirements.txt
│   └── app.py              # 入口文件
├── data/                    # 数据库目录 (Docker)
├── uploads/                 # 上传目录 (Docker)
├── Dockerfile              # Docker 构建文件
├── docker-compose.yml      # Docker Compose 配置
├── .env.example            # 环境变量示例
└── README.md
```

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/htkchenlei/JobSPA.git
cd JobSPA
```

#### 2. 创建环境变量文件
```bash
cp .env.example .env
# 编辑 .env 文件，修改 SECRET_KEY 等配置
```

#### 3. 启动服务
```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

#### 4. 访问应用
打开浏览器访问 `http://localhost:15667`

#### 5. 停止服务
```bash
docker-compose down
```

### 方式二：本地开发

#### 前端
```bash
cd frontend
pnpm install
pnpm dev
```

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥 | `dev_secret_key` |
| `DATABASE_URL` | 数据库连接 | SQLite |
| `UPLOAD_FOLDER` | 文件上传目录 | `./uploads` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |

### 数据库

默认使用 SQLite，数据文件存储在 `data/projectmanagement.db`。

如需使用其他数据库，修改 `DATABASE_URL`：

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/jobspa

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/jobspa
```

### NAS Docker 部署

#### Synology NAS

1. **通过 SSH 登录 NAS**
```bash
ssh admin@your-nas-ip
```

2. **创建项目目录**
```bash
mkdir -p /volume1/docker/JobSPA
cd /volume1/docker/JobSPA
```

3. **上传项目文件**（使用 Git 或 SFTP）

4. **修改 docker-compose.yml 中的卷挂载路径**
```yaml
volumes:
  - ./data:/app/data
  - ./uploads:/app/uploads
```

5. **启动服务**
```bash
docker-compose up -d
```

#### 端口说明

默认端口：`15667`，可在 `docker-compose.yml` 中修改：

```yaml
ports:
  - "你的端口:5000"
```

## 👤 默认账户

系统默认管理员账户：

- **用户名**: `admin`
- **密码**: `admin`

其他用户（如 `Marco`、`Chenlei`）为普通账户，无删除项目权限。

⚠️ **请登录后立即修改密码！**

## 🎨 设计风格

采用马卡龙撞色风格设计，主要配色：

| 颜色 | 用途 | 色值 |
|------|------|------|
| 🟢 薄荷绿 | 成功/完成 | `#A8E6CF` |
| 🔴 珊瑚粉 | 警告/重要 | `#FF9A8B` |
| 🔵 天蓝 | 信息/进行中 | `#7EC8E3` |
| 🟣 薰衣草紫 | 次要/已完成 | `#C3B1E1` |
| 🟡 奶油黄 | 提示/中等 | `#FFEAA7` |

## 📝 开发指南

### 🔗 对外公开 API（无需认证）

系统提供以下公开接口，方便外部系统获取项目更新数据：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/public/weekly-updates` | GET | 获取本周项目更新列表（上周六~当天） |
| `/api/public/weekly-updates/count` | GET | 获取本周更新数量 |
| `/api/public/monthly-updates` | GET | 获取当月项目更新列表（本月1号~当天） |
| `/api/public/range-updates` | GET | 获取指定日期范围的项目更新（需传 `start_date` 和 `end_date`） |

详细文档请访问：`http://your-domain/api-documentation`

### API 文档

主要 API 端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login` | POST | 用户登录 |
| `/api/projects/` | GET | 获取项目列表 |
| `/api/projects/<id>` | GET | 获取项目详情 |
| `/api/projects/<id>` | PUT | 更新项目 |
| `/api/projects/<id>` | DELETE | 删除项目（**仅管理员**，需携带 `Authorization` 头） |
| `/api/projects/<id>/progress` | GET | 获取项目进度 |
| `/api/work-log/` | GET/POST | 工作日志 |

> **权限说明**：删除项目接口 `/api/projects/<id>` (DELETE) 仅管理员可用，普通用户调用会返回 `403 无权限`，前端也会根据用户角色隐藏删除按钮。

### 数据库迁移

```bash
cd backend
python init_db.py  # 初始化数据库
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Vue.js](https://vuejs.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)

---

**JobSPA** - 让项目管理更简单 💼
