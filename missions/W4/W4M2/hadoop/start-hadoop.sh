#!/bin/bash

# ssh 서비스 시작
sudo service ssh start

# HDFS 포맷 및 서비스 시작 (hdfs 사용자로 실행)
export HADOOP_HOME=/opt/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64


if [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
fi

$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

tail -f /dev/null