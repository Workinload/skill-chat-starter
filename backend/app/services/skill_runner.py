from __future__ import annotations

from pathlib import Path
from app.core.settings import settings
from app.services.skill_registry import FeatureDefinition, SkillDefinition


class SkillRunner:
    async def run(
        self,
        *,
        feature: FeatureDefinition,
        skill: SkillDefinition,
        message: str,
        workspace: Path,
    ) -> str:
        if settings.claude_agent_sdk_enabled:
            return await self._run_claude_agent_sdk(
                feature=feature,
                skill=skill,
                message=message,
                workspace=workspace,
            )
        return await self._run_mock(feature=feature, skill=skill, message=message, workspace=workspace)

    async def _run_mock(self, *, feature: FeatureDefinition, skill: SkillDefinition, message: str, workspace: Path) -> str:
        input_files = sorted([p.name for p in (workspace / "inputs").glob("*")])
        output = f"""
# Mock Skill 执行结果

当前是 mock runner，未真正调用 Claude Agent SDK。

## 功能

- feature_id: `{feature.feature_id}`
- label: `{feature.label}`
- skill: `{skill.name}`
- output_type: `{feature.output_type}`

## 用户需求

{message}

## 已上传文件

{chr(10).join([f'- {name}' for name in input_files]) if input_files else '- 暂无'}

## 下一步

将 `.env` 中设置：

```env
CLAUDE_AGENT_SDK_ENABLED=true
ANTHROPIC_API_KEY=你的key
```

然后在 `backend/app/services/skill_runner.py` 中继续完善真实 Runner。
""".strip()
        (workspace / "outputs" / "result.md").write_text(output, encoding="utf-8")
        return output

    async def _run_claude_agent_sdk(
        self,
        *,
        feature: FeatureDefinition,
        skill: SkillDefinition,
        message: str,
        workspace: Path,
    ) -> str:
        """Claude Agent SDK 执行层。

        这个函数是生产化重点。当前版本使用官方 Python SDK 的 query() 形态。
        你后续可以改成 ClaudeSDKClient 以支持长期会话、用户中断、结构化流式输出。
        """
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("claude-agent-sdk is not installed or not available") from exc

        system_prompt = f"""
You are executing a fixed product feature. The customer must not see internal Skill details.

Hard rules:
- Use only the requested Skill.
- Do not decide to use another skill.
- Do not expose internal chain-of-thought.
- Follow the Skill exactly.
- Work only inside the current workspace.
- Output final customer-facing result in Chinese unless the user asks otherwise.

Loaded Skill:

{skill.skill_md}
""".strip()

        prompt = f"""
Customer request:
{message}

Workspace:
{workspace}

Input files are under:
{workspace / 'inputs'}

Write generated artifacts under:
{workspace / 'outputs'}
""".strip()

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            cwd=str(workspace),
            allowed_tools=feature.allow_tools,
            permission_mode=settings.claude_permission_mode,
            model=settings.claude_model,
        )

        chunks: list[str] = []
        async for msg in query(prompt=prompt, options=options):
            text = self._extract_message_text(msg)
            if text:
                chunks.append(text)

        output = "\n".join(chunks).strip()
        if not output:
            output = "任务已执行，但未捕获到文本输出。请检查 workspace outputs 目录。"
        (workspace / "outputs" / "result.md").write_text(output, encoding="utf-8")
        return output

    def _extract_message_text(self, msg) -> str:
        """兼容 SDK 消息对象/字典的简易文本提取。

        SDK 消息结构可能随版本演进，生产中建议按官方类型细化处理。
        """
        if isinstance(msg, str):
            return msg
        if isinstance(msg, dict):
            if "text" in msg:
                return str(msg["text"])
            if "content" in msg:
                return str(msg["content"])
        text = getattr(msg, "text", None)
        if text:
            return str(text)
        content = getattr(msg, "content", None)
        if content:
            return str(content)
        return ""
