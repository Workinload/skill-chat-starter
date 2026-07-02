# 01 非常详细的开发步骤

## 阶段 0：明确产品边界

先写在白板上：

```text
普通聊天不调用 Skill。
功能按钮才调用 Skill。
Skill 由系统内置，客户不能乱选。
```

不要一开始做：

- 多 Agent 协作
- 复杂 RAG
- 知识库管理后台
- 企业级权限
- 在线代码运行市场

## 阶段 1：跑通工程

### 1.1 启动基础设施

```bash
docker compose up -d postgres redis minio
```

### 1.2 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

检查：

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/features
```

### 1.3 启动前端

```bash
cd frontend
pnpm install
pnpm dev
```

检查：

```text
http://localhost:3000
```

## 阶段 2：跑通普通聊天

目标：不选功能，直接发消息。

预期：后端走 `ChatService`，返回普通聊天结果。

涉及文件：

```text
frontend/components/chat-panel.tsx
backend/app/routers/chat.py
backend/app/services/chat_service.py
```

开发任务：

1. 把 mock 回复换成真实普通 LLM。
2. 存储 conversation_id。
3. 存储 messages。
4. 加入上下文截断策略。

注意：不要在普通聊天里调用 Skill。

## 阶段 3：跑通 Skill 执行

目标：点击“生成报告”，发送需求，返回 mock Skill 结果。

涉及文件：

```text
config/features.yaml
skills/report-generator/SKILL.md
backend/app/services/task_service.py
backend/app/services/skill_runner.py
```

检查点：

- `feature_id=report_generate`
- 映射到 `skill=report-generator`
- 创建 workspace
- 复制上传文件到 inputs
- 生成 outputs/result.md
- 返回 TaskResult

## 阶段 4：接入 Claude Agent SDK

### 4.1 安装

```bash
pip install claude-agent-sdk
```

### 4.2 设置环境变量

```env
CLAUDE_AGENT_SDK_ENABLED=true
ANTHROPIC_API_KEY=你的key
```

### 4.3 修改 Runner

重点文件：

```text
backend/app/services/skill_runner.py
```

当前已预留：

```python
from claude_agent_sdk import query, ClaudeAgentOptions
```

你需要继续完善：

- 消息类型解析
- 错误处理
- 流式输出
- 超时控制
- cost usage 记录
- hooks
- structured output

## 阶段 5：任务异步化

当前任务是同步执行，不适合长任务。

建议改成：

```text
POST /api/tasks -> 创建任务 queued -> 返回 task_id
Worker -> 执行任务 -> 更新状态
GET /api/tasks/{id} -> 查询状态
SSE /api/tasks/{id}/events -> 实时进度
```

可选方案：

- 简单：FastAPI BackgroundTasks
- 中等：RQ + Redis
- 稳定：Celery + Redis
- 高级：Temporal

## 阶段 6：数据库落地

最少表：

```text
users
conversations
messages
files
tasks
task_events
skill_runs
```

优先实现：

1. conversations
2. messages
3. files
4. tasks
5. audit events

## 阶段 7：文件存储落地

当前上传文件存在 `/tmp/skill-chat-uploads`。

生产改成：

```text
MinIO/S3 保存原始文件
workspace 临时复制输入文件
任务结束后 outputs 上传到 MinIO/S3
数据库保存 file_id/object_key
```

## 阶段 8：完善权限控制

第一版权限：

- 文档类 Skill 禁止 Bash
- 代码类 Skill 需要确认
- 禁止读取 .env 和 secrets

后续增加：

- Docker sandbox
- 网络隔离
- CPU/内存限制
- 命令白名单
- 输出文件大小限制
- 审计日志后台

## 阶段 9：Skill 版本管理

建议目录：

```text
skills/report-generator/
  SKILL.md
  VERSION
  templates/
  examples/
  tests/
```

每次修改 Skill 都走 Git。

数据库记录：

```text
skill_name
skill_version
git_commit
execution_time
```

## 阶段 10：客户可用产品化

必须补：

- 登录
- 客户空间/租户
- 会话历史
- 文件历史
- 任务历史
- 下载结果
- 管理后台
- 错误重试
- 计费/额度
- 审计日志

