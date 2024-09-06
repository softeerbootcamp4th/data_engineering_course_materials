#!/bin/bash


# $NODE_TYPE에 따라 다른 명령을 수행할꺼야
case $NODE_TYPE in
    "master")
        $SPARK_HOME/sbin/start-master.sh

        # Keep the shell open
        tail -f /dev/null
        ;;
    "worker")
        $SPARK_HOME/sbin/start-worker.sh spark-master:7077

        # Keep the shell open
        tail -f /dev/null
        ;;
    *)
        echo "Invalid NODE_TYPE: $NODE_TYPE"
        exit 1
        ;;
esac


