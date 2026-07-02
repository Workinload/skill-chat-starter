# 06 数据库设计

MVP 暂时用内存，生产建议 PostgreSQL。

## users

```sql
id uuid primary key
email text unique
name text
role text
created_at timestamptz
```

## conversations

```sql
id uuid primary key
user_id uuid
title text
created_at timestamptz
updated_at timestamptz
```

## messages

```sql
id uuid primary key
conversation_id uuid
role text
content text
mode text -- context_chat / skill_execution
created_at timestamptz
```

## uploaded_files

```sql
id uuid primary key
user_id uuid
conversation_id uuid
filename text
content_type text
size_bytes bigint
storage_provider text -- local / s3
object_key text
created_at timestamptz
```

## tasks

```sql
id uuid primary key
user_id uuid
conversation_id uuid
feature_id text
skill_name text
skill_version text
status text
input_message text
output_text text
error text
created_at timestamptz
updated_at timestamptz
```

## task_files

```sql
task_id uuid
file_id uuid
role text -- input / output
```

## task_events

```sql
id uuid primary key
task_id uuid
event_type text
payload jsonb
created_at timestamptz
```

## skill_runs

```sql
id uuid primary key
task_id uuid
skill_name text
skill_version text
model text
allowed_tools jsonb
permission_profile text
workspace_path text
started_at timestamptz
finished_at timestamptz
cost_usd numeric
usage jsonb
```

