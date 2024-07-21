#!/bin/bash

# ssh 서비스 시작
service ssh start

# HDFS 포맷 및 서비스 시작 (hdfs 사용자로 실행)
su - hdfs -c '
  export HADOOP_HOME=/usr/local/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  echo "Starting HDFS namenode..."
  $HADOOP_HOME/bin/hdfs --daemon start datanode
'

# YARN 서비스 시작 (yarn 사용자로 실행)
su - yarn -c '
  export HADOOP_HOME=/usr/local/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  echo "Starting YARN node manager..."
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
'

tail -f /dev/null
