#!/usr/bin/env bash

# SSH 키 생성 및 설정 함수
setup_ssh() {
  local user=$1
  su - $user -c "
  ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
  mkdir -p ~/.ssh
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod 0600 ~/.ssh/authorized_keys
  "
}

# SSH 키 복사 함수
copy_ssh_key() {
  local user=$1
  local host=$2
  su -c "ssh-copy-id -i /home/${user}/.ssh/id_rsa.pub ${user}@${host}" ${user}
}

export HADOOP_HOME=/usr/local/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_VERSION=3.4.0

# docker volume 부착 시, root:root (user:group)으로 부착되어서 dfs 디렉토리 내에 name, data 등 디렉토리를 생성하지 못하는 문제 해결
chown -R hdfs:hadoop /usr/local/hadoop/data
chmod -R 770 /usr/local/hadoop/data
echo "Starting SSH service"
service ssh start

echo "Setting up SSH keys for hdfs user"
setup_ssh hdfs
echo "Setting up SSH keys for yarn user"
setup_ssh yarn

echo "Attempting initial SSH session"
su -c "ssh -o StrictHostKeyChecking=no localhost 'exit'" hdfs
su -c "ssh -o StrictHostKeyChecking=no localhost 'exit'" yarn

echo "Starting datanode as hdfs user"
su -c "export PDSH_RCMD_TYPE=ssh && export HADOOP_HOME=/usr/local/hadoop && export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop && export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin && export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && export HADOOP_VERSION=3.4.0 && hadoop-daemon.sh start datanode" hdfs

echo "Setting permissions for Hadoop logs"
chmod -R 770 $HADOOP_HOME/logs

echo "Starting nodemanager daemons as yarn user"
su -c "export PDSH_RCMD_TYPE=ssh && export HADOOP_HOME=/usr/local/hadoop && export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop && export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin && export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 && export HADOOP_VERSION=3.4.0 && yarn-daemon.sh start nodemanager" yarn

# 포그라운드 프로세스를 유지하기 위한 임시 명령 (예시)
echo "Keeping a foreground process to maintain the script running"
tail -f /dev/null