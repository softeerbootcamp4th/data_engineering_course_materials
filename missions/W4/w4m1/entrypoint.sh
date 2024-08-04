#!/bin/bash

if [ "$ROLE" = "master" ]; then
  echo "Starting Spark master..."
  /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
elif [ "$ROLE" = "worker" ]; then
  echo "Starting Spark worker..."
  /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
fi
