#!/bin/bash

# Hadoop 환경 설정
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# SSH 데몬 시작
sudo service ssh start

# HDFS 및 YARN 시작
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# 명령 프롬프트를 유지
exec "$@"
