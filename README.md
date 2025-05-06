# 代码说明
- changable文件夹下面是新建docker容器时可配置时间的定时脚本
- 外面的是build时写死的定时脚本

# 命令备忘
- 构建镜像：docker build -t image_name .
- 保存镜像：docker save -o my_image.tar my-python-app:1.0
- 执行:
  docker run -d \
    --name daily-copy-photos-dynamically \
    -e CRON_SCHEDULE="0 3 * * *" \
    -e SOURCE_DIR="/source" \
    -e DEST_DIR="/dest" \
    -v /home/NickelFox/Photos:/source \
    -v /volume2/Photos:/dest \
    -v /volume1/docker/daily_copy_photos:/app/logs \
    dynamic-copy
- 查看cron任务: cat /etc/cron.d/copy-job