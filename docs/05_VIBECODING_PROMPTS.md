# 05 Vibecoding 提示词

下面这些提示词可以直接丢给 Claude Code / Cursor / Codex。

## Prompt 1：跑通项目

```text
请阅读 CLAUDE.md 和 README.md。先不要大改架构。帮我检查这个项目是否能在本地跑起来：
1. 后端 FastAPI 是否能启动
2. /health、/api/features、/api/chat、/api/tasks 是否可用
3. 前端 Next.js 是否能启动
4. 修复所有明显的类型错误和路径错误
要求：保持“普通聊天不调用 Skill，功能按钮才调用 Skill”的产品边界。
```

## Prompt 2：接入真实普通聊天模型

```text
请在 backend/app/services/chat_service.py 中把 mock 普通聊天替换为 OpenAI-compatible API 调用。
要求：
1. 普通聊天仍然不能调用 Skill
2. 支持 conversation context
3. 加入基础上下文截断
4. 配置从 .env 读取
5. 保留 mock fallback
```

## Prompt 3：完善 Claude Agent SDK Runner

```text
请完善 backend/app/services/skill_runner.py 的 _run_claude_agent_sdk：
1. 按 Claude Agent SDK Python 官方用法处理 query 消息流
2. 捕获工具调用、文本块、错误、usage
3. 将最终输出写入 outputs/result.md
4. 如果 feature.allow_shell=false，则不允许 Bash
5. 保持 allowed_tools 来自 features.yaml
6. 不要让模型自行选择其他 Skill
```

## Prompt 4：任务异步化

```text
请把当前同步 TaskService 改成 Redis Queue 模式：
1. POST /api/tasks 只创建任务并返回 queued
2. worker 执行 SkillRunner
3. GET /api/tasks/{id} 返回状态
4. 新增 task_events 记录阶段进度
5. 保持现有 API 兼容
```

## Prompt 5：数据库持久化

```text
请引入 SQLAlchemy，把当前内存 tasks 改成 PostgreSQL 持久化。
最少实现：
- conversations
- messages
- uploaded_files
- tasks
- task_events
要求提供 alembic 初始化和迁移文件。
```

## Prompt 6：MinIO 文件存储

```text
请把 backend/app/routers/files.py 的本地文件上传改成 MinIO 存储：
1. 上传后保存到 S3_BUCKET
2. 数据库记录 file_id、object_key、filename、size
3. workspace 创建时从 MinIO 下载到 inputs/
4. outputs 结束后上传回 MinIO
```

## Prompt 7：增加新的 Skill

```text
请新增一个 Skill：contract-risk-reviewer。
要求：
1. 在 skills/contract-risk-reviewer/SKILL.md 写完整规范
2. 在 config/features.yaml 注册 feature_id=contract_review
3. 权限使用 readonly_document
4. 前端自动展示这个新功能
5. 输出格式包含风险等级、条款位置、修改建议
```

## Prompt 8：安全加固

```text
请增强 Permission Guard：
1. 检查 workspace 路径逃逸
2. 拦截危险 Bash 命令
3. 拦截读取 .env、secrets、*.pem、*.key
4. 将拦截事件写入 audit log
5. 添加单元测试
```

