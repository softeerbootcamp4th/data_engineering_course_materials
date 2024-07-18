#!/bin/bash

# Start SSH service as root
sudo service ssh start

# Set Hadoop environment variables for users
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"

# Start HDFS services
if [ -x "$HADOOP_HOME/sbin/start-dfs.sh" ]; then
  echo "Starting HDFS services..."
  $HADOOP_HOME/sbin/start-dfs.sh
else
  echo "start-dfs.sh not found or not executable."
fi

# Start YARN services
if [ -x "$HADOOP_HOME/sbin/start-yarn.sh" ]; then
  echo "Starting YARN services..."
  $HADOOP_HOME/sbin/start-yarn.sh
else
  echo "start-yarn.sh not found or not executable."
fi

# Keep container running
echo "Container is running. Press Ctrl+C to stop."
tail -f /dev/null
