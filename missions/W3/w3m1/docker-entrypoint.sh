#!/bin/bash

# SSH 서비스 시작
sudo service ssh start

# 데이터 디렉토리가 비어 있으면 네임노드 포맷 수행
if [ ! -d "$HADOOP_HOME/data/namenode/current" ]; then
    echo "Formatting namenode..."
    $HADOOP_HOME/bin/hdfs namenode -format
else
    echo "Namenode already formatted."
fi

# Hadoop 서비스 시작
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# Bash 쉘 실행
/bin/bash
