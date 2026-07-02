# Skill Chat Starter

一个面向客户的轻量对话系统工程骨架：

- 客户侧只看到：普通聊天、文件上传、几个固定功能按钮。
- 后台做：Feature Router -> Skill Registry -> Claude Agent SDK Runner -> 输出校验。
- 普通聊天不会自动调用 Skill；只有命中固定功能时才调用指定 Skill。
- Skill 作为可版本管理的业务能力包，放在 `skills/*/SKILL.md`。

## 技术栈

- Frontend: Next.js + React + assistant-ui 可替换组件结构
- Backend: FastAPI
- Agent: Claude Agent SDK Python
- DB: PostgreSQL，开发期可换 SQLite
- Queue/Cache: Redis
- Object Storage: MinIO / S3
- Sandbox: Docker workspace / future isolated runner
- Core: 自研 Skill Registry、Permission Guard、Workspace Manager、Output Validator

## 快速启动

### 1. 准备环境

```bash
cp .env.example .env
```

把 `.env` 中的 Key 补上：

```env
ANTHROPIC_API_KEY=你的key
CLAUDE_AGENT_SDK_ENABLED=false
```

第一次建议先保持 `CLAUDE_AGENT_SDK_ENABLED=false`，用 mock runner 跑通前后端闭环。

### 2. 启动基础设施

```bash
docker compose up -d postgres redis minio
```

### 3. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Windows PowerShell：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动前端

```bash
cd frontend
pnpm install
pnpm dev
```

浏览器打开：

```text
http://localhost:3000
```

## 关键接口

| 接口 | 作用 |
|---|---|
| `GET /health` | 健康检查 |
| `GET /api/features` | 获取固定功能列表 |
| `POST /api/chat` | 普通上下文聊天，不调用 Skill |
| `POST /api/tasks` | 功能触发，固定调用 Skill |
| `GET /api/tasks/{task_id}` | 查询任务状态 |
| `POST /api/files` | 上传文件 |

## 核心理念

```text
普通聊天：只对话，不执行工具，不读写项目，不调用 Skill
功能触发：按钮/显式功能 ID -> 固定 Skill -> Agent Runner -> 校验 -> 返回
```

不要让模型“自己决定要不要调用 Skill”。

## 目录说明

```text
skill-chat-starter/
  frontend/                 Next.js 前端壳
  backend/                  FastAPI 后端
  skills/                   内置 Skill 包
  config/                   功能注册表和权限配置
  docs/                     架构、开发步骤、安全规范
  scripts/                  辅助脚本
  docker-compose.yml        本地依赖服务
  CLAUDE.md                 给 Claude Code / vibecoding 的项目说明
```

## 第一版目标

先跑通：

```text
客户点击“生成报告”
  -> 上传文件
  -> 后端读取 features.yaml
  -> 找到 report-generator Skill
  -> Claude Agent SDK 或 mock runner 执行
  -> 返回 Markdown 结果
```

然后再扩展成：

- 文档导出 docx
- 任务队列异步执行
- 用户系统
- 多租户
- 知识库/RAG
- Docker 强沙箱
- Skill 版本管理
- 审计后台

