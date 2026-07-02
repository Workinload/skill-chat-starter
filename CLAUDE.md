# Project Instructions for Claude Code / Vibecoding

你正在开发一个 Skill-driven Lightweight Chat System。

## 产品定位

这个系统不是通用 Agent 平台，不是 Dify，不是 Open WebUI。

它的产品形态是：

```text
客户只看到简单 Web 对话界面：
- 普通聊天
- 文件上传
- 少量固定功能按钮

后台：
- 普通聊天不调用 Skill
- 用户点击功能按钮后，后端固定调用对应 Skill
- Skill 由系统内置，客户不可自由创建/选择危险 Skill
```

## 绝对规则

1. 不要让模型自行决定是否调用 Skill。
2. 不要在普通聊天中读写文件、执行命令、调用 Claude Code 工具。
3. Skill 触发必须经过 `features.yaml`。
4. 每个任务必须创建独立 workspace。
5. 每次 Skill 执行必须经过 Permission Guard。
6. 报告/文档类 Skill 默认禁止 Bash。
7. 代码类 Skill 即使允许 Bash，也必须在 sandbox 中执行。
8. 不要读取 `.env`、`secrets/`、系统目录、用户无权访问的路径。
9. 所有生成结果必须经过 Output Validator。
10. 所有任务要写审计日志。

## 开发优先级

第一阶段只做：

- 功能按钮
- 文件上传
- 普通聊天
- Skill Registry
- Mock Runner
- Claude Agent SDK Runner
- 任务状态查询

不要一开始加复杂 RAG、多 Agent、企业权限、多租户。

## 代码风格

- 后端使用 FastAPI + Pydantic。
- 前端使用 Next.js + React。
- 配置优先 YAML。
- Skill 是文件夹，不是数据库记录。
- 业务规则写进 Skill 和配置，而不是散落在 Prompt 里。

## 当前重点文件

- `config/features.yaml`
- `config/permissions.yaml`
- `backend/app/services/skill_registry.py`
- `backend/app/services/skill_runner.py`
- `backend/app/services/permission_guard.py`
- `skills/*/SKILL.md`

