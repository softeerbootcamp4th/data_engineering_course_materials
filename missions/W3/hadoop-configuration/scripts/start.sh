#!/usr/bin/env bash

# Start SSH service
service ssh start


# 마스터 노드 IP 가져오기
MASTER_IP=$(getent hosts hadoop-master | awk '{ print $1 }')
# 슬레이브 노드 IP 가져오기
SLAVE1_IP=$(getent hosts hadoop-slave1 | awk '{ print $1 }')
SLAVE2_IP=$(getent hosts hadoop-slave2 | awk '{ print $1 }')

# /etc/hosts에 추가
echo "$MASTER_IP hadoop-master" >> /etc/hosts
echo "$SLAVE1_IP hadoop-slave1" >> /etc/hosts
echo "$SLAVE2_IP hadoop-slave2" >> /etc/hosts


# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  echo "Checking if namenode format is needed..."
  if [ ! -d "$HADOOP_HOME/dfs/namenode/current" ]; then
    echo "Formatting namenode..."
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format
  fi
fi

#chown -R hdfs:hadoop $HADOOP_HOME/dfs

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