FROM --platform=linux/amd64 python:3.10-slim as build

# 安装所需软件
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# 设置时区（按需修改）
ENV TZ=Asia/Shanghai
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime

# 创建日志目录
RUN mkdir -p /var/log/cron /app/logs \
 && chmod 777 /app/logs  # 确保容器内进程有写权限

# 复制文件
COPY copy_dirs.py /app/
COPY crontab /etc/cron.d/copy-job

# 设置权限
RUN chmod 0644 /etc/cron.d/copy-job \
 && touch /var/log/cron/cron.log \
 && chmod 777 /app/copy_dirs.py

# 安装Python依赖（如有）
# RUN pip install some-package

# 启动命令
CMD ["bash", "-c", "cron && tail -f /var/log/cron/cron.log"]