#!/usr/bin/env bash

hdfs dfs -mkdir -p /user/root/data
for file in /home/hdfs/examples/*; do
  sudo -u hdfs $HADOOP_HOME/bin/hdfs dfs -put $file /user/root/data/
done
