import uuid
from app.schemas import ChatRequest, ChatResponse


class ChatService:
    async def respond(self, req: ChatRequest) -> ChatResponse:
        """普通聊天服务。

        MVP 先返回可替换的 mock。生产中可以在这里接普通模型 API。
        注意：这里绝不调用 Skill，不读取用户上传文件，不执行命令。
        """
        conversation_id = req.conversation_id or str(uuid.uuid4())
        msg = req.message.strip()
        if not msg:
            answer = "你可以直接输入问题，或者点击上方固定功能按钮开始处理材料。"
        else:
            answer = (
                "这是普通上下文聊天模式，未触发任何 Skill。\n\n"
                f"你刚才说：{msg}\n\n"
                "如果要执行固定业务功能，请点击“生成报告 / 审查材料 / 提取信息”等按钮。"
            )
        return ChatResponse(conversation_id=conversation_id, message=answer)
