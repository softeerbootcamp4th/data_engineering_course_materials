#!/bin/bash

# SSH 서비스 시작
sudo service ssh start

# Hadoop nodemanager 실행
$HADOOP_HOME/bin/yarn --daemon start nodemanager

# Keep the shell open
tail -f /dev/null
