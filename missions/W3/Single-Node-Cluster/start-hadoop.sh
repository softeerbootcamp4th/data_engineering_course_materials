#!/bin/bash

# Start SSH service
service ssh start

# Format the Hadoop namenode if not formatted
if [ ! -d "/hadoop/dfs/namenode/current" ]; then
  hdfs namenode -format -force
fi

# Start Hadoop services
start-dfs.sh
start-yarn.sh

# Create a directory in HDFS
hdfs dfs -mkdir -p /user/
hdfs dfs -mkdir -p /user/root/

# Keep the container running
tail -f /dev/null
