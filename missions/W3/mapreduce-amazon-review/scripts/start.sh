#!/usr/bin/env bash

# Start SSH service
service ssh start

# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  echo "Checking if namenode format is needed..."
  if [ ! -d "$HADOOP_HOME/dfs/namenode/current" ]; then
    echo "Formatting namenode..."
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  echo "Start hadoop-master node daemon"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start namenode
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager

  echo "create directory /user/root & change owner"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -chown root:root /user/root
else
  echo "Start hadoop-worker datanode daemon"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start datanode
  echo "Start hadoop-worker nodemanager daemon"
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi

# Keep the container running
echo "Keep foreground process to maintain running"
tail -f /dev/null