#!/bin/bash

echo "$HOSTNAME Start"

if [[ "$HOSTNAME" == "spark-master" ]]; then
  if [ ! -d "/home/hduser/data/namenode/" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format && echo "OK : HDFS namenode format operation finished successfully !"
  fi
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  $HADOOP_HOME/bin/hdfs --daemon start namenode
  $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
else
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
  $HADOOP_HOME/sbin/hadoop-daemon.sh start datanode
fi/