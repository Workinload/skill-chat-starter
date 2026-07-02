# Skill Chat Starter

一个面向客户的轻量对话系统工程骨架：

- 客户侧只看到：普通聊天、文件上传、几个固定功能按钮。
- 后台做：Feature Router → Skill Registry → Skill Runner → 输出校验。
- 普通聊天不会自动调用 Skill；只有命中固定功能时才调用指定 Skill。
- Skill 作为可版本管理的业务能力包，放在 `skills/*/SKILL.md`。

## 技术栈

- Frontend: Next.js + React + Tailwind CSS v4
- Backend: FastAPI + Pydantic
- Agent: Claude Agent SDK Python（本阶段暂不启用）
- 当前阶段：Mock Runner 内存执行，不依赖 PostgreSQL / Redis / MinIO

## 快速启动

### 1. 准备环境

```bash
cp .env.example .env
```

`.env` 中关键配置（Mock MVP 阶段无需修改）：

```env
CLAUDE_AGENT_SDK_ENABLED=false    # Mock MVP 阶段必须为 false
ANTHROPIC_API_KEY=                # 本阶段可为空
```

### 2. 启动后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd frontend
pnpm install
pnpm dev
```

浏览器打开：`http://localhost:3000`

## Mock MVP 验收

本阶段不依赖 Docker、PostgreSQL、Redis、MinIO。后端使用内存存储和 Mock Runner。

### 验收命令

```bash
# 1. 后端编译检查
cd backend && python -m compileall app

# 2. 运行测试
cd backend && pytest -q

# 3. 启动后端
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

# 4. 手动接口测试
curl http://localhost:8000/health
curl http://localhost:8000/api/features
curl -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{"message":"你好"}'
curl -X POST http://localhost:8000/api/tasks -H 'Content-Type: application/json' -d '{"feature_id":"report_generate","message":"生成报告"}'
```

### 前端验收点

- 功能按钮从 `/api/features` 动态加载
- 只显示 "生成报告、审查材料、提取信息" 等业务名称，不显示内部术语
- 普通聊天调用 `/api/chat`，不触发 Skill
- 选择功能后调用 `/api/tasks`，触发 Mock Runner
- 代码任务（code_task）不在前端功能列表中
- 需要确认的功能会显示确认按钮

## 关键接口

| 接口 | 作用 |
|---|---|
| `GET /health` | 健康检查 |
| `GET /api/features` | 获取客户可见功能列表 |
| `POST /api/chat` | 普通上下文聊天，不调用 Skill |
| `POST /api/tasks` | 功能触发，固定调用 Skill |
| `GET /api/tasks/{task_id}` | 查询任务状态 |
| `POST /api/files` | 上传文件 |

## 核心理念

```text
普通聊天：只对话，不执行工具，不读写文件，不调用 Skill
功能触发：按钮/显式 feature_id → 固定 Skill → Runner → 校验 → 返回
```

不要让模型"自己决定要不要调用 Skill"。

## 目录说明

```text
skill-chat-starter/
  frontend/                 Next.js 前端
  backend/                  FastAPI 后端
    app/
      routers/              API 路由
      services/             Skill Registry, Runner, Task Service 等
      core/                 配置
    tests/                  pytest 测试
  skills/                   内置 Skill 包（SKILL.md）
  config/                   功能注册表 (features.yaml) 和权限配置 (permissions.yaml)
  docs/                     架构、开发步骤、安全规范
  scripts/                  辅助脚本
  .github/workflows/        CI
  docker-compose.yml        可选：PostgreSQL / Redis / MinIO（Mock MVP 阶段不需要）
  CLAUDE.md                 Claude Code 项目说明
```

## 当前阶段：Mock MVP

- **不启用** Claude Agent SDK（`CLAUDE_AGENT_SDK_ENABLED=false`）
- **不依赖** PostgreSQL、Redis、MinIO
- **不依赖** Docker（后端和前端直接本机运行）
- TaskService 使用内存存储
- SkillRunner 使用 Mock Runner，结果写入 `workspace/outputs/result.md`

## 下一阶段

1. 接入真实 Claude Agent SDK
2. 接入 PostgreSQL 持久化任务
3. 接入 Redis 异步任务队列
4. 接入 MinIO 文件存储
5. Docker sandbox 安全执行
6. 用户认证与多租户
