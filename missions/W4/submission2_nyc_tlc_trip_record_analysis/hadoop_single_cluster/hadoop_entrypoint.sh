#!/bin/bash

# ssh 서비스 시작
service ssh start

# HDFS 포맷 및 서비스 시작 (hdfs 사용자로 실행)
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

if [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
  echo "Formatting HDFS namenode..."
  $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
fi

echo "start HDFS"
$HADOOP_HOME/sbin/start-dfs.sh

echo "start YARN"
$HADOOP_HOME/sbin/start-yarn.sh

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /data
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /spark-logs

# 컨테이너 실행을 유지하기 위해 로그 파일 출력
tail -f /dev/null