#!/bin/bash

# Start SSH service
service ssh start

export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  if [ ! -d "/usr/local/hadoop/hdfs/namenode/current" ]; then
    echo "Formatting namenode..."
    su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive"
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs --daemon start namenode"
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode"
  su - yarn -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/yarn --daemon start resourcemanager"
  su - yarn -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/yarn --daemon start nodemanager"

  # Move the file to HDFS user's home directory and upload to HDFS
  chown hdfs:hdfs /home/hdfs/mapreduce_example.txt
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hdfs/input"
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -put /home/hdfs/mapreduce_example.txt /user/hdfs/input/"

  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/"
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/"
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -chown root:root /user/root"
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs dfs -chown root:root /"
else
  su - hdfs -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/hdfs --daemon start datanode"
  su - yarn -c "export HADOOP_HOME=/usr/local/hadoop; export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin; $HADOOP_HOME/bin/yarn --daemon start nodemanager"
fi

# Keep the container running
tail -f /dev/null
