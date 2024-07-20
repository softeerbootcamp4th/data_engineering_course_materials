#!/bin/bash

NODE=$1

if [ $NODE = "namenode" ] ; then
    bin/hdfs --daemon start namenode
    bin/mapred --daemon start historyserver
    bin/yarn --daemon start resourcemanager
elif [ $NODE = "worker1" ] ; then
    bin/hdfs --daemon start secondarynamenode
    bin/hdfs --daemon start datanode
    bin/yarn --daemon start nodemanager
elif [ $NODE = "worker" ] ; then
    bin/hdfs --daemon start datanode
    bin/yarn --daemon start nodemanager
fi

tail -f /dev/null