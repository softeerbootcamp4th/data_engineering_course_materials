#!/bin/bash

# SSH 서비스 시작
sudo service ssh start

# Hadoop Datanode 실행
$HADOOP_HOME/bin/hdfs --daemon start datanode

# Keep the shell open
tail -f /dev/null
