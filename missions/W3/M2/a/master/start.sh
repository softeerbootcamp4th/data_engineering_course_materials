#!/bin/bash

mkdir -p /run/sshd
/usr/sbin/sshd

# 네임스페이스 디렉토리를 입력받아서 
NAME_DIR=$1
echo $NAME_DIR

# current라는 폴더가 있다면 포맷해야대
if [ -d "$NAME_DIR/current" ]; then
  echo "NameNode is already formatted."
# 비어있다면 포맷을 진행
else
  echo "Format NameNode."
  hdfs --config $HADOOP_CONF_DIR namenode -format
fi

# NameNode, Resource manager 시작
hdfs --daemon start --config $HADOOP_CONF_DIR namenode
yarn --daemon start --config $HADOOP_CONF_DIR resourcemanager
while true; do
  sleep 1
done
