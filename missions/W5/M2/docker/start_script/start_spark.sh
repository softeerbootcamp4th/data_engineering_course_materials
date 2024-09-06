#!/bin/bash


# $NODE_TYPE에 따라 다른 명령을 수행할꺼야
case $NODE_TYPE in
    "master")
        # SSH 서비스 시작
        sudo service ssh start

        # spark master 실행
        $SPARK_HOME/sbin/start-master.sh

        # Hadoop Datanode 실행
        $HADOOP_HOME/bin/hdfs --daemon start namenode
        
        # Hadoop resourcemanager 실행
        $HADOOP_HOME/bin/yarn --daemon start resourcemanager
        
        # Keep the shell open
        tail -f /dev/null
        ;;
    "worker")
        # SSH 서비스 시작
        sudo service ssh start

        # spark worker 실행
        $SPARK_HOME/sbin/start-worker.sh spark-master:7077

        # Hadoop Datanode 실행
        $HADOOP_HOME/bin/hdfs --daemon start datanode

        # Hadoop nodemanager 실행
        $HADOOP_HOME/bin/yarn --daemon start nodemanager

        # Keep the shell open
        tail -f /dev/null
        ;;
    *)
        echo "Invalid NODE_TYPE: $NODE_TYPE"
        exit 1
        ;;
esac


