#!/bin/bash


if [ $1 = "master" ]; then
    LOG_FILE=$(./sbin/start-master.sh | sed "s/.\+logging to //")
elif [ $1 = "connect" ]; then
    LOG_FILE=$(./sbin/start-connect-server.sh --jars ./jars/spark-connect_2.12-3.5.1.jar --master spark://master:7077 | sed "s/.\+logging to //")
elif [ $1 = "worker" ]; then
    LOG_FILE=$(./sbin/start-worker.sh spark://master:7077 | sed "s/.\+logging to //")
else
    echo "Usage: $0 [master|connect|worker]"
    exit 1
fi 

tail -f $LOG_FILE