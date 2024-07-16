#!/bin/bash

service ssh start

if [ ! -d "/hadoop/dfs/namenode/current" ]; then
  hdfs namenode -format -force
fi

start-dfs.sh
start-yarn.sh

hdfs dfs -mkdir -p /user/
hdfs dfs -mkdir -p /user/root/

tail -f /dev/null
