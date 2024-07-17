#!/bin/bash

# ssh 서비스 시작
service ssh start

# HDFS 포맷 및 서비스 시작 (hdfs 사용자로 실행)
su - hdfs -c '
  export HADOOP_HOME=/opt/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  if [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
    echo "Formatting HDFS namenode..."
    $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
  fi
  
  echo "Starting HDFS namenode..."
  $HADOOP_HOME/bin/hadoop --daemon start namenode

  echo "Starting HDFS datanode..."
  $HADOOP_HOME/bin/hadoop --daemon start datanode

  echo "Starting HDFS secondary namenode..."
  $HADOOP_HOME/bin/hadoop --daemon start secondarynamenode
'

# YARN 서비스 시작 (yarn 사용자로 실행)
su - yarn -c '
  export HADOOP_HOME=/opt/hadoop
  export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

  echo "Starting YARN ResourceManager..."
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager

  echo "Starting YARN NodeManager..."
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
'

# 컨테이너 실행을 유지하기 위해 로그 파일 출력
tail -f $HADOOP_HOME/logs/*.log
