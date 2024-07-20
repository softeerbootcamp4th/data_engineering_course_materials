#!/bin/bash

if [ ! -z $1 ] && [ ! -z $2 ] ; then
    CONFIG_FILE=$1
    NODE_NAME=$2

    python3 toml2xml.py $CONFIG_FILE -o etc/hadoop &&

    if [ $NODE_NAME = "namenode" ] ; then
        echo "Stopping Hadoop DFS..."
        bin/hdfs --daemon stop namenode
        echo "Stopping Yarn..."
        bin/mapred --daemon stop historyserver
        bin/yarn --daemon stop resourcemanager

        echo "Starting Hadoop DFS..."
        bin/hdfs --daemon start namenode
        echo "Starting Yarn..."
        bin/mapred --daemon start historyserver
        bin/yarn --daemon start resourcemanager
    elif [ $NODE_NAME = "worker1" ] ; then
        echo "Stopping Hadoop DFS..."
        bin/hdfs --daemon stop secondarynamenode
        bin/hdfs --daemon stop datanode
        echo "Stopping Yarn..."
        bin/yarn --daemon stop nodemanager

        echo "Starting Hadoop DFS..."
        bin/hdfs --daemon start secondarynamenode
        bin/hdfs --daemon start datanode
        echo "Starting Yarn..."
        bin/yarn --daemon start nodemanager
    elif [ $NODE_NAME = "worker" ] ; then
        echo "Stopping Hadoop DFS..."
        bin/hdfs --daemon stop datanode
        echo "Stopping Yarn..."
        bin/yarn --daemon stop nodemanager

        echo "Starting Hadoop DFS..."
        bin/hdfs --daemon start datanode
        echo "Starting Yarn..."
        bin/yarn --daemon start nodemanager
    fi &&

    echo "Configuration changes applied and services restarted."
else
    echo "Usage: $0 config_file node_name"
fi
