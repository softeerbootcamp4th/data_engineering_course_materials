#!/bin/bash

# ssh 서비스 시작
service ssh start

# HDFS 포맷 및 서비스 시작 (hdfs 사용자로 실행)
su - hdfs -c '
  export HADOOP_HOME=/usr/local/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  if [ ! -d "/usr/local/hadoop/hdfs/namenode/current" ]; then
    echo "Formatting HDFS namenode..."
    $HADOOP_HOME/bin/hdfs namenode -format
  fi

  echo "Starting HDFS namenode..."
  $HADOOP_HOME/bin/hdfs --daemon start namenode

  echo "Starting HDFS secondarynamenode..."
  $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
'

# YARN 서비스 시작 (yarn 사용자로 실행)
su - yarn -c '
  export HADOOP_HOME=/usr/local/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  echo "Starting YARN resource manager..."
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
'

tail -f /dev/null
