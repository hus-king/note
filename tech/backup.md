# Overleaf 数据定时自动备份到 GitHub 完整流程

前提：已完成本地 Overleaf 数据推送到 GitHub 仓库，当前目标实现 **定时自动备份**，方案：git + cron + 日志记录，保障实验报告安全不丢失。

# 一、编写自动备份脚本

## 1.1 编写备份脚本内容

```bash

#!/bin/bash

#  Husking 的 Overleaf 自动备份脚本
# 放在 ~/bin/，记得 chmod +x

REPO_DIR="/home/husking/overleaf-toolkit/data/overleaf/data"
LOG_FILE="/home/husking/logs/overleaf-backup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] 🐾 开始备份..." >> "$LOG_FILE"

cd "$REPO_DIR" || { echo "❌ 目录不存在！" >> "$LOG_FILE"; exit 1; }

# 1. 拉取最新（防冲突）
git pull origin main 2>> "$LOG_FILE"

# 2. 添加所有变动（.gitignore 已生效，不怕加错）
git add . 2>> "$LOG_FILE"

# 3. 若有变更，才提交推送
if git diff --cached --quiet; then
    echo "[$DATE] 🌤 无变更，跳过备份" >> "$LOG_FILE"
else
    # 生成带时间的提交信息
    COMMIT_MSG="[auto] backup at $DATE"
    git commit -m "$COMMIT_MSG" 2>> "$LOG_FILE"
    
    # 推送！（加重试更稳）
    if git push origin main; then
        echo "[$DATE]  备份成功！提交: $(git rev-parse --short HEAD)" >> "$LOG_FILE"
    else
        echo "[$DATE]  推送失败！请检查网络或权限" >> "$LOG_FILE"
    fi
fi
```

## 1.2 赋予脚本执行权限

执行以下命令创建必要目录并授权：

```bash

mkdir -p ~/bin ~/logs
chmod +x ~/bin/overleaf-backup.sh
```

# 二、配置定时任务（每5分钟执行备份）

## 2.1 编辑 crontab 任务

执行命令进入定时任务编辑界面：

```bash

crontab -e
```

## 2.2 选择编辑器并配置任务

1. 界面会提示选择编辑器，输入 `1` 并回车（选择 nano 编辑器，操作更简单）；

2. 按 `Ctrl + K` 多次删除默认空行，清空编辑器内容；

3. 粘贴以下内容（设置每5分钟执行一次备份）：
            `*/5 * * * * /home/husking/bin/overleaf-backup.sh`
    说明：`*/5 * * * *` 表示每5分钟执行一次后续脚本，需确保脚本路径与实际一致。

## 2.3 保存并退出编辑器

nano 编辑器快捷键操作：

- 按 `Ctrl + O` → 回车（Write Out，完成保存）；

- 按 `Ctrl + X` → 退出编辑器。

# 三、日志查看方法

执行以下命令实时查看备份日志，确认备份状态：

```bash

tail -f ~/logs/overleaf-backup.log
```

# 四、最终效果说明

|时间/触发条件|系统行为|
|---|---|
|每5分钟|自动执行备份脚本，检查 Overleaf 数据有无新改动|
|有变动时|执行 git add → commit（带时间戳）→ push，GitHub 新增一条自动备份记录|
|无变动时|不执行备份操作，仅在日志中记录“无变更”|