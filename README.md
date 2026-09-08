# JobSPA - 项目管理平台

一个现代化的全栈项目管理平台，采用马卡龙撞色风格设计，帮助团队高效管理项目和工作日志。

## ✨ 功能特性

### 📊 仪表盘
- 项目统计概览（项目总数、进行中、已完成、本月日志），统计卡片可点击跳转到对应页面
- **本月日志** = 本月手动录入的项目进展条数（`project_progress`），不是 AI 生成的 `work_log`
- 项目阶段分布图表
- 最近项目更新动态

### 📋 项目管理
- 项目全生命周期管理（立项 → 招投标 → 已中标 → 已完成）
- 项目进度历史记录
- 项目自动分组展示：
  - **进行中项目**：近 1 个月内有更新
  - **近期项目**：1 ~ 3 个月未更新
  - **超期项目**：超过 3 个月未更新（默认收起，点击「显示更多」展开）
- 查看已完成项目：一键切换「已完成视图」，从仪表盘点击「已完成」卡片可直达
- 删除项目（**仅管理员**，软删除）
- 已全面适配移动端（≤768px 侧栏抽屉化、卡片/表单单列、弹窗底部抽屉）

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
- AI 自动生成工作日志（在日历上点「生成今日日志」，可保存到数据库）
- 手动录入的项目进展（在项目详情点「更新」）也会按日期体现在日历上
- 日历标记由**缓存文件**驱动（`progress_days_cache.json`）：打开页面秒级渲染颜色，避免逐日查询数据库；写进展时同步更新缓存
- 日历图例区分：今天 / 已生成 AI 日志 / 仅有项目进展；日期格悬停可查看详情
- 历史日志查看

### 🌐 对外公开 API
- 无需认证的公共接口
- 支持按周/月/自定义范围查询项目更新
- 在线 API 文档页面 (`/api`)

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

#### 6. 数据库与运行时缓存说明

- 容器**启动时会先自动执行 `init_db.py`（幂等）再拉起 gunicorn**：即使挂载的 `./data` 目录是空库，也会自动建表并创建默认账号 `admin/123456`，避免出现 `no such table: users`。
- 后端会在数据目录自动生成 `progress_days_cache.json`（工作日志日历缓存），**无需手工创建/上传**；该文件请勿提交到 Git。
- 如果历史 `work_log` 表中缺少某些日期的日志，可在容器内执行数据补齐（幂等，可重复运行）：
  ```bash
  docker compose exec jobspa python sync_worklog.py
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

详细文档请访问：`http://your-domain/api`

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

## 🆕 更新记录

### 2026-09-08

- **项目管理**：按最新更新日期自动分组为「进行中项目（近1个月）/ 近期项目（1~3个月）/ 超期项目（超3个月）」，「超期项目」默认收起，点「显示更多」展开。
- **移动端适配**：整体平台（Layout、项目管理、仪表盘、高级查询、工作日志、统计分析、个人设置、登录）支持移动端查看；≤768px 侧栏变为抽屉式。
- **仪表盘**：统计卡片可点击跳转（项目总数/进行中 → 项目管理，已完成 → 已完成视图，本月日志 → 工作日志）；「本月日志」统计口径改为手动录入的 `project_progress` 条数，并提供 `/api/projects/monthly-progress-count`。
- **工作日志**：
  - 新增 `/api/projects/month-days`（读 `progress_days_cache.json` 缓存返回当月有进展的日期）与 `/api/projects/date-progress/<日期>` 等价接口；
  - 日历颜色渲染改为依赖缓存接口，并处理接口缺失/非 JSON 的降级与容错；
  - 日历新增图例与悬停提示；在项目里写进展成功后同步更新日期缓存。
- **运维**：`docker-compose.yml` 启动命令改为「先 `init_db.py` 再 gunicorn」，避免空数据卷导致 `no such table: users`；新增 `backend/sync_worklog.py` 一次性/可重复数据补齐脚本。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Vue.js](https://vuejs.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)

---

**JobSPA** - 让项目管理更简单 💼
