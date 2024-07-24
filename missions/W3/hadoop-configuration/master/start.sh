#!/usr/bin/env bash

service ssh start

export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_VERSION=3.4.0

## docker volume 부착 시, root:root (user:group)으로 부착되어서 dfs 디렉토리 내에 name, data 등 디렉토리를 생성하지 못하는 문제 해결
#chown -R hdfs:hadoop $HADOOP_HOME/data
#chmod -R 770 $HADOOP_HOME/data
#echo "Starting SSH service"

if [ "$HOSTNAME" = "hadoop-master" ]; then
  if [ ! -d $HADOOP_HOME/data/name ]; then
    # hdfs 유저로 전환하여 namenode 포맷
    echo "Formatting namenode as hdfs user"
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format --force
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  su - hdfs -c "$HADOOP_HOME/bin/hdfs --daemon start namenode"
  su - hdfs -c "$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode"
  su - yarn -c "$HADOOP_HOME/bin/yarn --daemon start resourcemanager"

  echo "Create direcotry /user"
  sudo -E -u hdfs $HADOOP_HOME/bin/hadoop fs -mkdir /user
  echo "Create direcotry /user/root"
  sudo -E -u hdfs $HADOOP_HOME/bin/hadoop fs -mkdir /user/root
  echo "Change owner /user/root root->hdfs"
  sudo -E -u hdfs $HADOOP_HOME/bin/hadoop fs -chown root:root /user/root
  sudo -E -u hdfs $HADOOP_HOME/bin/hadoop fs -chown root:root /
else
  su - hdfs -c "$HADOOP_HOME/bin/hdfs --daemon start datanode"
  su - yarn -c "$HADOOP_HOME/bin/yarn --daemon start nodemanager"
fi

# 포그라운드 프로세스를 유지하기 위한 임시 명령
echo "Keeping a foreground process to maintain the script running"
tail -f /dev/null