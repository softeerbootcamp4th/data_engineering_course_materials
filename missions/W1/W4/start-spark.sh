#!/bin/bash

if [ "$SPARK_MODE" == "master" ]; then
    $SPARK_HOME/sbin/start-master.sh
    tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.master.Master-*.out
elif [ "$SPARK_MODE" == "worker" ]; then
    $SPARK_HOME/sbin/start-worker.sh $SPARK_MASTER_URL
    tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.worker.Worker-*.out
elif [ "$SPARK_MODE" == "history" ]; then
    $SPARK_HOME/sbin/start-history-server.sh
    tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.history.HistoryServer-*.out
else
    echo "Unknown mode: $SPARK_MODE"
    exit 1
fi
