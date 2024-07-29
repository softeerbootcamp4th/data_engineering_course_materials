#!/usr/bin/env bash

# Start SSH service
service ssh start

#export HADOOP_HOME=/opt/hadoop

#echo "Attempting initial SSH session"
#sudo -u hdfs ssh -o StrictHostKeyChecking=no localhost 'exit'
#sudo -u yarn ssh -o StrictHostKeyChecking=no localhost 'exit'

# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  if [ ! -d $HADOOP_HOME/name ]; then
    echo "Formatting namenode..."
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format -force
    chown -R hdfs:hadoop $HADOOP_HOME/data
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start namenode
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager

  echo "create directory /user/root & change owner"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -chown root:root /user/root
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -chown root:root /
else
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start datanode
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi

# Keep the container running
echo "Keep foreground process to maintain running"
tail -f /dev/null