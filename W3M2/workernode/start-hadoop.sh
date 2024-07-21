#!/bin/bash

# Start SSH service as root
sudo service ssh start

# Start Hadoop services as hadoopuser
hdfs --daemon start datanode
yarn --daemon start nodemanager

# Keep the container running
tail -f /dev/null
