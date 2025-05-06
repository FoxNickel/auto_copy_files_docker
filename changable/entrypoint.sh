#!/bin/bash

# 设置默认值（可选）
export CRON_SCHEDULE=${CRON_SCHEDULE:-"0 2 * * *"}
export SOURCE_DIR=${SOURCE_DIR:-"/source"}
export DEST_DIR=${DEST_DIR:-"/dest"}

# 生成crontab文件
envsubst < /app/crontab.template > /etc/cron.d/copy-job

# 必须的权限设置
chmod 0644 /etc/cron.d/copy-job \
 && touch /var/log/cron/cron.log \
 && chmod 777 /app/copy_dirs.py

# 时区配置（从环境变量读取）
ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime

# 启动服务
echo "✅ 生效的Cron任务配置："
cat /etc/cron.d/copy-job
cron && tail -f /var/log/cron/cron.log