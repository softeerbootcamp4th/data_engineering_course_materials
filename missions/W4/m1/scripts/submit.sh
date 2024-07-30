#!/bin/bash

$SPARK_HOME/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/data/pi_to_csv.py 20
