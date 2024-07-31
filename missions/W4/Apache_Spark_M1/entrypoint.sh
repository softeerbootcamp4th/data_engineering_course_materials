#!/bin/bash

# Start the master node
if [[ "$1" == "master" ]]; then
    $SPARK_HOME/sbin/start-master.sh
    tail -f $SPARK_HOME/logs/*

# Start the worker node
elif [[ "$1" == "worker" ]]; then
    $SPARK_HOME/sbin/start-slave.sh spark://spark-master:7077
    tail -f $SPARK_HOME/logs/*
fi

exec "$@"
