#!/usr/bin/env bash
Date=$(date +%Y%m%d%H%M)

PORT=8086
MODE=single


echo "选择您的操作"
select var in "start" "stop"; do
  break;
done
echo "You have selected $var "

if [ "$var" = "stop" ]; then
    echo "停止web服务"
    ps aux|grep table_web_server|grep -v grep|awk '{print $2}'|xargs kill -9
    exit
fi


#echo "输入训练要用的GPU"
read -p "输入启用的端口号:" PORT ;

echo "您选择了端口号 $port 进行启动"

echo "环境变量："
echo "-------------------"
echo "PROT:$PORT"
echo "MODE:$MODE"
echo "-------------------"

mkdir -p logs

echo "服务器Single模式启动..."
# 参考：https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
# worker=3是根据GPU的显存数调整出来的，ration=0.2，大概一个进程占满为2.5G,4x2.5=10G显存
_CMD="MODE=$MODE gunicorn \
    --name=table_web_server \
    --workers=1 \
    --bind 0.0.0.0:$PORT \
    --timeout=300 \
    server.start_up:app \
   > ./logs/console.log 2>&1"
echo "启动服务："
echo "$_CMD"
eval $_CMD
exit 0

