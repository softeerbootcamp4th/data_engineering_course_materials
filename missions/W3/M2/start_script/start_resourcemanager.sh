#!/bin/bash

# SSH 서비스 시작
sudo service ssh start

# Hadoop resourcemanager 실행
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

# Keep the shell open
tail -f /dev/null
