# Set Hadoop-specific environment variables here.

# The java implementation to use.
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_LOG_DIR=$HADOOP_HOME/logs
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Define HDFS and YARN user
export HDFS_NAMENODE_USER=hdfs
export HDFS_DATANODE_USER=hdfs
export HDFS_SECONDARYNAMENODE_USER=hdfs
export YARN_RESOURCEMANAGER_USER=yarn
export YARN_NODEMANAGER_USER=yarn

# YARN logs
export HADOOP_LOG_DIR=/usr/local/hadoop/logs
export YARN_LOG_DIR=/usr/local/hadoop/logs
