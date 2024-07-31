#!/bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"
password="supergroup"

if [ "$SPARK_WORKLOAD" == "master" ];
then
  start-master.sh -p 7077
  echo "$password" | su -c "/home/hduser/start-hadoop.sh" hduser
  tail -f /dev/null
elif [ "$SPARK_WORKLOAD" == "worker" ];
then
  start-worker.sh spark://spark-master:7077
  echo "$password" | su -c "/home/hduser/start-hadoop.sh" hduser
  tail -f /dev/null
elif [ "$SPARK_WORKLOAD" == "history" ]
then
  start-history-server.sh
  echo "$password" | su -c "/home/hduser/start-hadoop.sh" hduser
  tail -f /dev/null
fi