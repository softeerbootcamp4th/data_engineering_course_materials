#!/bin/bash
set -e
sudo service ssh start

if [ ! -d "/home/hduser/hdfs-data/namenode" ]; then
        $HADOOP_HOME/bin/hdfs namenode -format && echo "OK : HDFS namenode format operation finished successfully !"
fi

echo "running start-dfs.sh"
$HADOOP_HOME/sbin/start-dfs.sh
echo "running start-yarn.sh"
$HADOOP_HOME/sbin/start-yarn.sh
echo "YARNSTART = $YARNSTART"

$HADOOP_HOME/bin/hdfs dfsadmin -safemode leave

# keep the container running indefinitely
tail -f $HADOOP_HOME/logs/hadoop-*-namenode-*.log
