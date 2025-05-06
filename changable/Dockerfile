FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    gettext \
 && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Shanghai
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime

RUN mkdir -p /var/log/cron /app/logs \
 && chmod 777 /app/logs

# 复制模板文件（不再是原来的crontab）
COPY crontab.template /app/
COPY copy_dirs.py /app/
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh \
 && chmod 777 /app/copy_dirs.py

CMD ["/app/entrypoint.sh"]