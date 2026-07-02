# 03 API 设计

## GET /health

健康检查。

## GET /api/features

返回客户可见功能。

响应：

```json
[
  {
    "feature_id": "report_generate",
    "label": "生成报告",
    "description": "根据用户材料生成结构化业务报告。",
    "required_files": false,
    "output_type": "markdown",
    "visible_to_customer": true,
    "confirm_before_execute": false
  }
]
```

## POST /api/chat

普通上下文聊天，不调用 Skill。

请求：

```json
{
  "conversation_id": null,
  "message": "这个系统能做什么？",
  "context": []
}
```

响应：

```json
{
  "conversation_id": "uuid",
  "message": "...",
  "mode": "context_chat"
}
```

## POST /api/files

上传文件。

`multipart/form-data`，字段名 `file`。

响应：

```json
{
  "file_id": "uuid",
  "filename": "材料.docx",
  "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "size_bytes": 12345
}
```

## POST /api/tasks

功能执行，固定调用 Skill。

请求：

```json
{
  "feature_id": "report_generate",
  "conversation_id": null,
  "message": "根据这些材料生成一份报告",
  "file_ids": ["uuid"],
  "user_confirmed": true
}
```

响应：

```json
{
  "task_id": "uuid",
  "status": "succeeded",
  "feature_id": "report_generate",
  "skill": "report-generator",
  "message": "Task created and executed. Query task detail for result."
}
```

## GET /api/tasks/{task_id}

查询任务结果。

响应：

```json
{
  "task_id": "uuid",
  "status": "succeeded",
  "feature_id": "report_generate",
  "skill": "report-generator",
  "output_text": "# 报告...",
  "output_files": ["/tmp/.../outputs/result.md"],
  "error": null,
  "audit": []
}
```

