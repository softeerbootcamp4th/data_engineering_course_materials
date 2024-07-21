#!/bin/bash

sudo service ssh start

# Format the Hadoop namenode if not formatted (run as hdfs user)
if [ ! -d "/usr/local/hadoop/data/namenode/current" ]; then
  hdfs namenode -format
fi

# Start Hadoop services
/usr/local/hadoop/sbin/start-dfs.sh
/usr/local/hadoop/sbin/start-yarn.sh

# Keep the container running
tail -f /dev/null
