#!/bin/bash

# SSH 서비스 시작
sudo service ssh start

# 환경 변수 설정
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

if [ "$NODE_TYPE" == "master" ]; then
    # 최초 한번 포맷
    if [ ! -d "$HADOOP_HOME/data/namenode" ]; then
        mkdir -p $HADOOP_HOME/data/namenode
        mkdir -p $HADOOP_HOME/data/datanode
        chown -R hadoopuser:hadoopuser $HADOOP_HOME/data
        $HADOOP_HOME/bin/hdfs namenode -format -force
    fi

    hdfs namenode & yarn resourcemanager
    echo "Master started"
else
    # DataNode 및 NodeManager 데몬 시작
    $HADOOP_HOME/bin/hdfs --daemon start datanode
    $HADOOP_HOME/bin/yarn --daemon start nodemanager
    echo "Worker started"
fi

# 무한 루프를 통해 컨테이너 유지
tail -f /dev/null