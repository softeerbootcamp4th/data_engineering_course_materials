#!/bin/bash

sudo mkdir -p /run/sshd
sudo /usr/sbin/sshd


$SPARK_HOME/sbin/start-master.sh -h spark

./sbin/start-workers.sh spark://spark:7077

spark-submit --master spark://spark:7077 /opt/spark/examples/src/main/python/pi.py

tail -f /dev/null