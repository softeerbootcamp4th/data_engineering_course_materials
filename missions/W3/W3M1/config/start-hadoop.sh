#!/bin/bash

# Start SSH service
service ssh start

# Export Hadoop-related environment variables
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Format the Hadoop namenode if not formatted (run as hdfs user)
if [ ! -d "/hadoop/dfs/namenode/current" ]; then
    su - hdfs -c "$HADOOP_HOME/bin/hdfs namenode -format -force"
fi

# Start HDFS services as hdfs user
su - hdfs -c "$HADOOP_HOME/sbin/start-dfs.sh"

# Start YARN services as yarn user
su - yarn -c "$HADOOP_HOME/sbin/start-yarn.sh"

# Create directories in HDFS as hdfs user
su - hdfs -c "$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/"
su - hdfs -c "$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/"
su - hdfs -c "$HADOOP_HOME/bin/hdfs dfs -chown root:root /user/root"
su - hdfs -c "$HADOOP_HOME/bin/hdfs dfs -chown root:root /"

# Keep the container running
tail -f /dev/null