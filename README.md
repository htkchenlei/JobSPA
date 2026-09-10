# JobSPA - 项目管理平台

一个现代化的全栈项目管理平台，采用马卡龙撞色风格设计，帮助团队高效管理项目和工作日志。

## ✨ 功能特性

### 📊 仪表盘
- 项目统计概览（项目总数、进行中、已完成、本月日志），统计卡片可点击跳转到对应页面
- **本月日志** = 本月手动录入的项目进展条数（`project_progress`），不是 AI 生成的 `work_log`
- 项目阶段分布图表
- 最近项目更新动态

### 📋 项目管理
- 项目全生命周期管理，项目阶段统一为 5 档：**立项中 / 已立项 / 招投标 / 已中标 / 已完成**（历史 1-13 档数据已在升级时一次性归一化）
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
- 阶段分布分析（按 5 档）
- 月度趋势图
- 周日志数量（近 12 周）与月日志数量（近 12 个月）统计图（统计手动录入的项目进展条数）

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
- 在线 API 文档页面 (`/apis`，与后端 `/api/*` 接口前缀分离)

## 🛠 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 快速构建工具
- **Vue Router** - 路由管理
- **Naive UI** - 组件库（马卡龙主题定制）
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

## 📦 部署步骤（NAS / 服务器）

### 前置要求

- NAS / 服务器已安装 Docker 与 Docker Compose（SSH 执行 `docker compose version` 能正常输出）
- 本地电脑已安装 Node.js ≥ 18 与 npm（用于构建前端产物，NAS 上不需要 Node）
- 镜像采用「两层」设计：
  - `jobspa-base:latest`：基础镜像（Python 3.11 + 全部依赖），**只需构建一次，日常更新复用**
  - `jobspa:latest`：应用镜像（COPY 后端源码 + 前端 dist），业务更新只重建这一层，秒级完成

### 首次部署

#### 第 1 步：本地构建前端（你的电脑上）

```bash
cd frontend
npm install    # 首次或依赖变更后执行
npm run build  # 产物输出到 frontend/dist/
```

> NAS 不装 npm 依赖，页面全靠这份 `dist` 产物；构建报错请先解决再继续。

#### 第 2 步：上传项目到 NAS

用 File Station / SFTP 把**整个项目目录**上传到 NAS，例如 `/volume1/docker/JobSPA`（下文以此路径为例，以实际为准）。
`.gitignore` 已排除的内容（`node_modules`、`.env`、`data/*.db`、`frontend/dist` 以外的构建产物等）无需上传。

#### 第 3 步：准备环境变量与数据目录（SSH 到 NAS）

```bash
cd /volume1/docker/JobSPA
cp .env.example .env      # 编辑 .env，务必修改 SECRET_KEY；需要 AI 日志则填 DEEPSEEK_API_KEY
mkdir -p data uploads     # 数据库与上传目录（compose 挂载点，数据库将持久化于此）
```

#### 第 4 步：构建基础镜像（仅首次）

```bash
docker build -f Dockerfile.base -t jobspa-base:latest .
```

#### 第 5 步：启动并验收

```bash
docker compose up -d --build
docker compose logs -f    # 看到 gunicorn 启动信息即成功，Ctrl+C 退出日志
```

浏览器访问 `http://NAS的IP:15667`，默认账户 `admin / 123456`，**登录后请立即修改密码**。

> **首次启动说明**
> - 容器启动时先自动执行 `init_db.py`（幂等）再拉起 gunicorn：即使 `./data` 是空目录也会自动建表并创建默认账号，避免 `no such table: users`
> - 后端会在数据目录自动生成日历缓存 `progress_days_cache.json`，无需手工创建，也**不要**提交到 Git
> - 历史版本曾写入的「系统补齐」占位日志（`created_by_ai='系统补齐'`）如需清理（不影响手动 AI 日志与日历颜色），可执行一次性 SQL：
>   ```bash
>   docker compose exec jobspa python -c "import sqlite3; c=sqlite3.connect('/app/data/projectmanagement.db'); print('deleted', c.execute(\"DELETE FROM work_log WHERE created_by_ai='系统补齐'\").rowcount); c.commit()"
>   ```

### 日常更新（增量部署，推荐）

本地仓库有新提交时，**不要整包重新上传/重新 Clone**，只覆盖变化的部分：

1. 本地重新构建前端（本次有前端改动时）：

   ```bash
   cd frontend && npm run build
   ```

2. 覆盖上传到 NAS 项目目录（按对应相对路径）：
   - `frontend/dist/`（整个目录，Dockerfile 用 `COPY frontend/dist` 提供页面）
   - `backend/` 下本次变更的 `.py` 源码（**新增的 .py 文件必须一并上传**，否则容器启动报 `ModuleNotFoundError`）
   - `docker-compose.yml`（仅启动方式/环境变量变化时）

3. 重建应用镜像并启动：

   ```bash
   cd /volume1/docker/JobSPA
   docker compose up -d --build
   docker compose logs -f
   ```

   > 若报 `jobspa-base ... not found / 403`，说明这台机器没构建过基础镜像，回到[首次部署第 4 步](#第-4-步构建基础镜像仅首次)补一次即可。

**数据安全**：`./data`、`./uploads` 是宿主机挂载卷，不在镜像内，重建容器**不影响数据**。更新前可给旧镜像打备份 tag，出问题秒回滚：

```bash
docker tag jobspa:latest jobspa:backup-$(date +%m%d)
# 回滚：docker tag jobspa:backup-0910 jobspa:latest && docker compose up -d
```

**数据库说明**：新装库 `projects.stage` 直接使用 5 档，无需迁移；仅当从「1-13 档」旧版本升级时才需要一次性归一化（1-2→1、3-5→2、6-8→3、9-11→4、12-13→5，迁移脚本可从 Git 历史取回 `backend/migrate_stage_5.py`），操作前先 `cp data/projectmanagement.db data/projectmanagement.db.bak`。

### 常用运维命令

```bash
docker compose logs -f           # 实时日志
docker compose restart           # 重启容器
docker compose down              # 停止并移除容器（数据保留在宿主机 data/uploads 目录）
docker compose up -d --build     # 代码更新后重建并启动
```

数据库为 SQLite 单文件（`data/projectmanagement.db`），直接拷贝即备份：

```bash
cp data/projectmanagement.db data/projectmanagement.db.bak.$(date +%m%d)
```

### 端口修改

默认端口 `15667`，在 `docker-compose.yml` 中修改冒号左侧：

```yaml
ports:
  - "你的端口:5000"
```

## 💻 本地开发

#### 前端
```bash
cd frontend
npm install
npm run dev     # 开发模式（接口代理到本地后端 5000 端口）
npm run build   # 构建产物到 dist/
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

完整部署步骤（含 Synology NAS）见上文 [📦 部署步骤（NAS / 服务器）](#-部署步骤nas服务器)。

## 👤 默认账户

系统默认管理员账户：

- **用户名**: `admin`
- **密码**: `123456`

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

详细文档请访问：`http://your-domain/apis`

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

### 2026-09-10

- **前端 UI 马卡龙风格全面改造，接入 Naive UI**：全站页面迁移至 `n-card / n-modal / n-form / n-select / n-tag / n-timeline / n-popconfirm` 等组件；替换 23 处原生 `alert/confirm` 为统一风格弹窗；新增主题配置 `theme/naiveTheme.ts`、阶段色板 `constants/stageColors.ts`、统一反馈 `utils/feedback.ts` 与 `ProjectCard` 组件；保留品牌五色与移动端抽屉适配。
- **API 文档页路由 `/api` → `/apis`**：消除与后端 `/api/*` 接口前缀的撞名（此前开发模式被 Vite 代理截胡、生产环境命中后端路由，文档页无法直接打开）；Vite 代理规则同步收紧为 `/api/` 前缀。

### 2026-09-09

- **项目阶段归一化为 5 档**：`立项中 / 已立项 / 招投标 / 已中标 / 已完成`。后端 `STAGE_MAP`、前端项目/仪表盘/高级查询/统计均改为 5 档映射；数据库迁移脚本 `backend/migrate_stage_5.py`（1-2→1、3-5→2、6-8→3、9-11→4、12-13→5）。
- **统计分析**：新增「周日志数量（近 12 周）」与「月日志数量（近 12 个月）」柱状图，统计手动录入的 `project_progress` 条数，接口 `GET /api/projects/log-statistics?interval=week|month&size=12`。
- **工作日志**：改为按日期跨用户加载真实 AI 日志（`selectDate`/`onMounted` 统一走 `/api/work-log/date/<date>`），修复“从仪表盘跳转可见、切换日期后不显示”的问题；不再把项目进展自动补齐成工作日志；新增 `backend/cleanup_sync_worklog.py` 清理早期“系统补齐”占位记录。
- **仪表盘**：三栏等高布局（项目阶段分布 / 工作日志日历 / 最近更新），中间嵌入可复用日历组件 `MonthCalendar.vue`，点击日期直达工作日志对应日。

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
