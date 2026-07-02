# 04 安全设计

## 1. 最大风险

你的系统不是普通聊天机器人。只要后台 Agent 能读文件、写文件、运行命令，就必须按执行系统设计安全边界。

风险包括：

- Prompt Injection
- 恶意上传文件
- 越权读取 `.env`
- 运行危险命令
- 外网下载恶意脚本
- 泄露客户文件
- 跨任务 workspace 污染

## 2. 默认权限

```text
普通聊天：无工具
文档审查：Read only
报告生成：Read + Write outputs
代码任务：Sandbox + limited Bash
```

## 3. 路径限制

禁止：

```text
.env
.env.*
secrets/
*.pem
*.key
/etc/
/var/
/root/
/home/
.git/
```

## 4. Bash 限制

禁止：

```text
sudo
ssh
scp
curl
wget
rm -rf /
chmod 777
docker run --privileged
```

## 5. 文件隔离

每个任务：

```text
workspace/{task_uuid}/
  inputs/
  outputs/
  drafts/
```

不要复用 workspace。

## 6. 客户侧隐藏

客户不应看到：

- Skill 名称
- 系统提示词
- 内部路径
- Shell 输出的敏感内容
- 审计日志原文

客户只看：

- 最终结果
- 缺失材料
- 失败原因的安全摘要

## 7. 生产上线前必做

- Docker sandbox 不挂宿主机敏感目录
- 禁止容器特权模式
- 限制 CPU/内存/磁盘
- 任务超时
- 上传文件扫描
- 租户级隔离
- 全量审计日志
- 人工确认高风险任务

