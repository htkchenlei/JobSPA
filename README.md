# JobSPA 项目说明

## 项目简介
JobSPA 是一个基于 Vue 3 和 Flask 开发的全栈单页应用，旨在提供一个综合性的项目管理和文件管理平台。该系统集成了仪表盘、项目管理、高级查询、统计分析、待办事项、文件管理和工作日志等功能，为用户提供一站式的工作管理解决方案。

## 主要功能

- **仪表盘**：系统概览和关键指标展示，支持项目阶段统计图表
- **项目管理**：管理项目信息和进度，支持项目更新和历史记录查看
- **高级查询**：执行复杂的项目和数据查询
- **统计分析**：提供数据可视化和统计报表
- **待办事项**：个人任务管理和跟踪
- **文件管理**：树形结构的文件和文件夹管理，支持创建文件夹、上传文件等操作
- **工作日志**：自动记录日常活动，支持AI生成工作日志
- **地名查询**：文档关键词检查工具，支持行政区划管理
- **API文档**：系统API接口的详细文档
- **用户管理**：支持用户登录、修改密码等功能

## 技术栈

### 前端
- **框架**：Vue 3 + Composition API
- **语言**：TypeScript
- **路由**：Vue Router 4
- **构建工具**：Vite
- **图表库**：Chart.js

### 后端
- **框架**：Flask 2.0.1
- **数据库**：SQLite (内置，无需额外安装)
- **ORM**：SQLAlchemy 1.4.32
- **CORS**：Flask-CORS 3.0.10
- **环境管理**：python-dotenv 0.19.2
- **AI集成**：支持调用大模型API生成内容（如DeepSeek、Qwen、Doubao）

## 快速开始

### 1. 环境准备

- **前端**：Node.js 16+，npm 7+
- **后端**：Python 3.8+，pip 20+
- **数据库**：SQLite（内置，无需额外安装）

### 2. 安装依赖

#### 前端依赖
```bash
cd frontend
npm install
```

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件，添加以下内容（根据需要修改）：

```
# 数据库配置
DATABASE_URL=sqlite:///projectmanagement.db

# JWT密钥
SECRET_KEY=your_secret_key_here

# AI API密钥（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key
QWEN_API_KEY=your_qwen_api_key
DOUBAO_API_KEY=your_doubao_api_key
```

### 4. 启动服务

#### 启动后端服务
```bash
cd backend
python app.py
```
后端服务将运行在 `http://localhost:15667`

#### 启动前端服务
```bash
cd frontend
npm run dev
```
前端服务将运行在 `http://localhost:15668`

### 5. 访问系统

打开浏览器，访问 `http://localhost:15668`，即可进入 JobSPA 系统。

## 目录结构

### 前端结构
```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/          # 图片、样式等资源
│   ├── components/      # 通用组件
│   ├── router/          # 路由配置
│   ├── views/           # 页面组件
│   ├── App.vue          # 根组件
│   ├── main.ts           # 入口文件
│   └── style.css         # 全局样式
├── package.json         # 项目配置和依赖
├── tsconfig.json        # TypeScript 配置
└── vite.config.ts       # Vite 配置
```

### 后端结构
```
backend/
├── app/
│   ├── models/          # 数据模型
│   ├── routes/          # API 路由
│   │   ├── ai_routes.py           # AI相关API路由
│   │   ├── auth_routes.py         # 认证相关API路由
│   │   ├── file_routes.py         # 文件管理API路由
│   │   ├── file_parse_routes.py    # 文件解析API路由
│   │   ├── place_routes.py         # 地名查询API路由
│   │   ├── project_routes.py      # 项目管理API路由
│   │   ├── todo_routes.py         # 待办事项API路由
│   │   ├── user_routes.py         # 用户相关API路由
│   │   └── work_log_routes.py     # 工作日志API路由
│   └── __init__.py      # 应用初始化
├── app.py               # 应用入口
├── china_regions.json   # 行政区划数据
├── requirements.txt     # Python 依赖
└── projectmanagement.db # SQLite 数据库文件
```

## Docker部署

### 1. 构建Docker镜像

在项目根目录执行：

```bash
docker-compose build
```

### 2. 启动Docker容器

```bash
docker-compose up -d
```

### 3. 访问系统

容器启动后，可通过以下地址访问：
- 前端应用：`http://localhost:15668`
- 后端API：`http://localhost:15667/api/`

### 4. 数据持久化

- SQLite数据库文件存储在 `/volume1/docker/JobSPA/data` 目录
- 确保该目录存在且权限正确

## 使用示例

### 行政区划管理

1. **访问地名查询**：点击侧边栏中的「地名查询」链接
2. **行政区划管理**：在地名查询页面中切换到「行政区划管理」标签页
3. **查看行政区划**：页面会显示省级、市级和区级行政区的列表
4. **新增行政区**：点击「新增」按钮，在弹出的对话框中输入行政区名称
5. **删除行政区**：鼠标悬停在行政区标签上，点击显示的删除按钮

### 工作日志

1. **查看工作日志**：点击侧边栏中的「工作日志」链接，进入工作日志页面
2. **选择日期**：在日历中点击日期，查看或生成该日期的工作日志
3. **生成今日活动**：系统会自动获取今日的活动记录
4. **生成工作日志**：点击「生成今日日志」按钮，系统会调用AI生成工作日志
5. **查看历史日志**：在日历中选择历史日期，查看已保存的工作日志

### 修改密码

1. 点击页面右上角的用户名，在下拉菜单中选择「修改密码」
2. 输入当前密码和新密码，点击保存按钮

## 常见问题

### 1. 无法登录系统
- 检查后端服务是否正常运行
- 确认用户名和密码是否正确
- 检查浏览器控制台是否有网络错误

### 2. 行政区划管理没有数据
- 检查 `china_regions.json` 文件是否存在
- 确认后端服务是否正常启动
- 检查浏览器控制台是否有错误信息

### 3. AI生成工作日志失败
- 检查 `.env` 文件中是否配置了AI API密钥
- 确认网络连接是否正常
- 检查浏览器控制台是否有错误信息

## 注意事项

- 系统默认使用 JWT 进行用户认证，token 存储在 localStorage 中
- 文件管理功能会为每个用户创建独立的文件存储目录
- SQLite数据库文件已添加到 `.gitignore`，不会被上传到版本控制系统
- 生产环境部署时，建议修改 `SECRET_KEY` 为强随机值

## 许可证

MIT License