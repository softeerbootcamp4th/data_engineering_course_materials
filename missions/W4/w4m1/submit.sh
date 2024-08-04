#!/bin/bash

# 샘플 1000개로 제한해서 pi.py 실행하고 출력
spark-submit --master spark://spark-master:7077 \
             --class org.apache.spark.examples.SparkPi \
             /opt/spark/examples/src/main/python/pi.py \
             1000
