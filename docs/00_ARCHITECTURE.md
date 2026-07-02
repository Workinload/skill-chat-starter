# 00 架构说明

## 1. 产品目标

构建一个面向客户的轻量 Web 对话系统。客户只看到简单的聊天窗口和固定功能按钮，后台通过内置 Skill 执行业务任务。

核心不是“开放式 Agent”，而是“可控的 Skill Gateway”。

## 2. 系统边界

### 普通聊天

```text
用户输入 -> Chat Service -> 普通 LLM 或 mock -> 回复
```

限制：

- 不调用 Skill
- 不读取上传文件
- 不执行 Bash
- 不修改文件
- 不访问工作区

### 功能执行

```text
用户点击功能 -> Feature ID -> Skill Registry -> Permission Guard -> Workspace -> Claude Agent SDK -> Output Validator -> 回复
```

限制：

- 必须有功能 ID
- 必须映射到固定 Skill
- 必须过权限配置
- 必须写审计日志

## 3. 为什么不用 Dify 当核心

Dify 适合低代码工作流和知识库问答，但本项目需要：

- Skill 文件化
- 业务能力版本化
- 固定功能触发
- 代码/文档级执行
- hooks/权限/沙箱更细粒度控制

因此使用自研 Skill Gateway。

## 4. 关键模块

| 模块 | 作用 |
|---|---|
| Feature Router | 判断当前是普通聊天还是固定功能 |
| Skill Registry | 注册功能和 Skill 的绑定关系 |
| Permission Guard | 控制工具、路径、命令权限 |
| Workspace Manager | 为每个任务创建独立工作区 |
| Skill Runner | 调用 Claude Agent SDK 或 mock runner |
| Output Validator | 检查输出格式、空结果、文件产物 |
| Audit Logger | 记录任务生命周期和风险事件 |

## 5. 数据流

```text
Frontend
  |  POST /api/chat       普通聊天
  |  POST /api/tasks      功能执行
  v
FastAPI
  |  Skill Registry
  |  Permission Guard
  |  Workspace Manager
  v
Claude Agent SDK / Mock Runner
  v
outputs/result.md
  v
API Response
```

## 6. MVP 只做同步执行

当前 TaskService 使用内存存储和同步执行，方便 vibecoding。生产化时替换为：

- PostgreSQL `tasks` 表
- Redis 队列
- Worker 进程
- SSE/WebSocket 任务进度

