#!/bin/bash

echo "HOSTNAME: $HOSTNAME"

if [[ $HOSTNAME == "spark-master" ]]; then
    /opt/spark/sbin/start-master.sh -h spark-master
else
    /opt/spark/sbin/start-worker.sh spark://spark-master:7077
fi

tail -f /dev/null