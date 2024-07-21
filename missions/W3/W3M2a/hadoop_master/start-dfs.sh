#!/bin/bash

# Start HDFS namenode
$HADOOP_HOME/bin/hdfs --daemon start namenode

# Start HDFS datanode
# $HADOOP_HOME/bin/hdfs --daemon start datanode

# Keep the container running
tail -f /dev/null