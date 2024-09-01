#!/usr/bin/env bash

# SSH 키 복사 함수
copy_ssh_key() {
  local user=$1
  local host=$2
  echo "${user} to ${user}@${host}"
  su -c "ssh-copy-id -i /home/${user}/.ssh/id_rsa.pub ${user}@${host}" ${user}
}

echo "Starting SSH service"
service ssh start

# docker volume 부착 시, root:root (user:group)으로 부착되어서 dfs 디렉토리 내에 name, data 등 디렉토리를 생성하지 못하는 문제 해결
chown -R hdfs:hadoop $HADOOP_HOME/data
chmod -R 770 $HADOOP_HOME/data

echo "Attempting initial SSH session"
su -c "ssh -o StrictHostKeyChecking=no localhost 'exit'" hdfs
su -c "ssh -o StrictHostKeyChecking=no localhost 'exit'" yarn
su -c "ssh -o StrictHostKeyChecking=no localhost 'exit'" spark

echo "Performing Hadoop initialization tasks"
# Format namenode if not formatted
if [ "$HOSTNAME" = "hadoop-master" ]; then
  if [ ! -d $HADOOP_HOME/data/name ]; then
    echo "Formatting namenode..."
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format -force
  fi
fi

# Start Hadoop services
if [ "$HOSTNAME" = "hadoop-master" ]; then
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start namenode
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start resourcemanager
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager

  echo "Create direcotry /user/root"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root/
  echo "Change owner /user/root root->hdfs"
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs dfs -chown root:root /user/root
  sudo -E -u spark $SPARK_HOME/sbin/start-master.sh
  jupyter notebook --notebook-dir='/' --allow-root --ip=0.0.0.0 --no-browser --port=8888 --NotebookApp.token=''
else
  sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start datanode
  sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager
  sudo -E -u spark $SPARK_HOME/sbin/start-worker.sh spark://hadoop-master:7077
fi

# 포그라운드 프로세스를 유지하기 위한 임시 명령 (예시)
echo "Keeping a foreground process to maintain the script running"
tail -f /dev/null
