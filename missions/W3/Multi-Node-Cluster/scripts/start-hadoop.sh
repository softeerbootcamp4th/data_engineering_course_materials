#!/bin/bash

# Start SSH service
service ssh start

export HADOOP_HOME=/opt/hadoop

# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  if [ ! -d "/usr/local/hadoop/hdfs/namenode/current" ]; then
    echo "Formatting namenode..."
    hdfs namenode -format -force -nonInteractive
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  $HADOOP_HOME/bin/hdfs --daemon start namenode
  $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  $HADOOP_HOME/bin/yarn --daemon start nodemanager

  $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/
  $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/
else
  $HADOOP_HOME/bin/hdfs --daemon start datanode
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi

# Keep the container running
tail -f /dev/null
