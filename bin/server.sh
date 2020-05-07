#!/usr/bin/env bash

PORT=8080
MODE=single

echo "环境变量："
echo "-------------------"
echo "PROT:$PORT"
echo "MODE:$MODE"
echo "-------------------"


echo "服务器Single模式启动..."
# 参考：https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
# worker=3是根据GPU的显存数调整出来的，ration=0.2，大概一个进程占满为2.5G,4x2.5=10G显存
_CMD="MODE=$MODE gunicorn \
    --name=table_web_server \
    --workers=1 \
    --bind 0.0.0.0:$PORT \
    --timeout=300 \
    server.start_up:app"
#         >../logs/console.log 2>&1"
echo "启动服务："
echo "$_CMD"
eval $_CMD
exit 0

