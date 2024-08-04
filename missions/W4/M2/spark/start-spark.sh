#!/bin/bash

if [ "$SPARK_ROLE" == "master" ]; then
  /spark/bin/spark-class org.apache.spark.deploy.master.Master
else
  /spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
fi
