#!/bin/bash
# 환경 변수 설정
export HADOOP_HOME=/usr/local/hadoop
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HADOOP_HOME/lib/native
# ssh 서비스 시작
service ssh start
# HDFS 포맷 및 서비스 시작 (Master 노드에서만 실행)
if [[ $HOSTNAME == "namenode" ]] && [ ! -d "$HADOOP_HOME/hdfs/namenode/current" ]; then
  hdfs namenode -format -force -nonInteractive
  touch /hdfs-formatted
fi
$HADOOP_HOME/sbin/stop-dfs.sh
$HADOOP_HOME/sbin/stop-yarn.sh


# ResourceManager 중지 및 PID 파일 삭제
if [[ $HOSTNAME == "namenode" ]]; then
  echo "Stopping existing ResourceManager if running..."
  $HADOOP_HOME/bin/yarn --daemon stop resourcemanager
  echo "Removing ResourceManager PID file if exists..."
  rm -f /tmp/hadoop-root-resourcemanager.pid
fi
if [[ $HOSTNAME == "namenode" ]]; then
  $HADOOP_HOME/sbin/start-dfs.sh
  hdfs dfsadmin -safemode leave
  $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
else

  $HADOOP_HOME/bin/hadoop --daemon start datanode
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
fi
# 로그 파일을 출력하여 컨테이너 실행 유지
tail -f $HADOOP_HOME/logs/hadoop-*.log#
