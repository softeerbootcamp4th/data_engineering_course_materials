#!/bin/bash

export PATH=$JAVA_HOME/bin:$PATH

if [ "$1" == "namenode" ]; then
    if [ ! -d /home/hduser/hadoop-3.3.3/data/namenode/current ]; then
        hdfs namenode -format
    fi

    sudo service ssh start
    hdfs namenode &
elif [ "$1" == "datanode" ]; then
    sudo service ssh start
    hdfs datanode &
else
    echo "Unknown command: $1"
    exit 1
fi

echo "Starting YARN services..."
$HADOOP_HOME/sbin/start-yarn.sh

sleep 10

echo "Listing log files..."
ls -l $HADOOP_HOME/logs

jps

tail -f $HADOOP_HOME/logs/hadoop-hduser-resourcemanager-*.log $HADOOP_HOME/logs/hadoop-hduser-nodemanager-*.log
