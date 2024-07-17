#!/bin/sh

mkdir -p /run/sshd

/usr/sbin/sshd

hdfs --daemon start --config $HADOOP_CONF_DIR datanode

yarn --daemon start --config $HADOOP_CONF_DIR nodemanager

while true; do

  sleep 1

done
