# 先看这里

你要 vibecoding，建议按这个顺序：

1. 打开 `CLAUDE.md`，让 Claude Code 先理解项目边界。
2. 打开 `docs/01_DEVELOPMENT_STEPS.md`，按阶段做。
3. 先不要接真 SDK，保持 `CLAUDE_AGENT_SDK_ENABLED=false` 跑通 mock。
4. 跑通后，再用 `docs/05_VIBECODING_PROMPTS.md` 里的 Prompt 逐步让 Agent 完善。

第一条提示词建议直接用：

```text
请阅读 CLAUDE.md、README.md 和 docs/01_DEVELOPMENT_STEPS.md，先检查这个项目能否本地跑通。不要改变产品定位：普通聊天不调用 Skill，只有固定功能按钮才调用对应 Skill。请修复必要的路径、依赖和类型问题。
```

