#!/bin/bash

sudo service ssh start

echo "HOSTNAME: $HOSTNAME"
# Format the Hadoop namenode if not formatted (run as hdfs user)
if [[ $HOSTNAME == "hadoop-master" ]]; then
  if [ ! -d "/usr/local/hadoop/data/namenode/current" ]; then
    hdfs namenode -format -force -nonInteractive
    sudo chmod 777 /usr/local/hadoop/data/namenode/
  fi
  hdfs --daemon start namenode
  hdfs --daemon start secondarynamenode
  yarn --daemon start resourcemanager
else
  hdfs --daemon start datanode
  yarn --daemon start nodemanager
fi

# Keep the container running
tail -f /dev/null