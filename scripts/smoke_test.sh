#!/usr/bin/env bash
set -euo pipefail

BASE=${BASE:-http://localhost:8000}

echo "Health"
curl -s "$BASE/health" | jq .

echo "Features"
curl -s "$BASE/api/features" | jq .

echo "Chat"
curl -s -X POST "$BASE/api/chat" \
  -H 'Content-Type: application/json' \
  -d '{"conversation_id":null,"message":"你好","context":[]}' | jq .

echo "Task"
curl -s -X POST "$BASE/api/tasks" \
  -H 'Content-Type: application/json' \
  -d '{"feature_id":"report_generate","conversation_id":null,"message":"生成一个测试报告","file_ids":[],"user_confirmed":true}' | jq .
