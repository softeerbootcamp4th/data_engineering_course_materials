#! /bin/bash

mkdir cfg_backup
echo Backing up core-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/core-site.xml ~/cfg_backup/core-site.xml
echo Modifying core-site.xml...
python3 ~/missions/mission2-b/modify_config.py $HADOOP_HOME/etc/hadoop/core-site.xml

echo Backing up hdfs-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/hdfs-site.xml ~/cfg_backup/hdfs-site.xml
echo Modifying hdfs-site.xml...
python3 ~/missions/mission2-b/modify_config.py $HADOOP_HOME/etc/hadoop/hdfs-site.xml

echo Backing up mapred-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/mapred-site.xml ~/cfg_backup/mapred-site.xml
echo Modifying mapred-site.xml...
python3 ~/missions/mission2-b/modify_config.py $HADOOP_HOME/etc/hadoop/mapred-site.xml

echo Backing up yarn-site.xml...
cp /usr/local/hadoop-3.3.6/etc/hadoop/yarn-site.xml ~/cfg_backup/yarn-site.xml
echo Modifying yarn-site.xml...
python3 ~/missions/mission2-b/modify_config.py $HADOOP_HOME/etc/hadoop/yarn-site.xml

if [[ "$HOSTNAME" == "namenode" ]]; then
  # IN NAMENODE
  echo Stopping Hadoop DFS...
  $HADOOP_HOME/bin/hdfs --daemon stop namenode
  $HADOOP_HOME/bin/hdfs --daemon stop secondarynamenode
  echo Stopping YARN...
  $HADOOP_HOME/bin/yarn --daemon stop resourcemanager

  # Init namenode dir
  name_dir=$(hdfs getconf -confKey dfs.namenode.name.dir)
  rm -r $name_dir
  mkdir -p $name_dir
  $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive && echo "OK : HDFS namenode format operation finished successfully !"
  
  # Restart HDFS
  echo Starting Hadoop DFS...
  $HADOOP_HOME/bin/hdfs --daemon start namenode
  $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

  # Restart YARN
  echo Starting YARN...
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
else
  # IN DATANODE
  echo Stopping Hadoop DFS...
  $HADOOP_HOME/sbin/hadoop-daemon.sh stop datanode
  echo Stopping YARN...
  $HADOOP_HOME/bin/yarn --daemon stop nodemanager

  # Init datanode dir
  data_dir=$(hdfs getconf -confKey dfs.datanode.data.dir)
  rm -r $data_dir
  mkdir -p $data_dir

  # Restart HDFS
  echo Starting YARN...
  $HADOOP_HOME/sbin/hadoop-daemon.sh start datanode

  # Restart YARN
  echo Starting Hadoop DFS...
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi

echo Configuration changes applied and services restarted.

# start-dfs.sh
# start-yarn.sh