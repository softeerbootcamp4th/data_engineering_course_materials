#!/bin/bash

# Start SSH service as root
sudo service ssh start

# Check if Namenode directory is empty
if [ ! "$(ls -A /usr/local/hadoop/data/namenode)" ]; then
  echo "Namenode directory is empty, formatting..."
  hdfs namenode -format
fi

# Start Hadoop services as hadoopuser
start-dfs.sh
start-yarn.sh

# Keep the container running
tail -f /dev/null
