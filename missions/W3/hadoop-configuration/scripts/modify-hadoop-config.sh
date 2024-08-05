#!/usr/bin/env bash

YAML_FILE="sample-configuration.yaml"
HADOOP_HOME="${1:-/opt/hadoop}"
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

if [ ! -d $HADOOP_CONF_DIR ]; then
  echo "default configuration directory not exists. create directory"
  mkdir $HADOOP_CONF_DIR
fi

# 필요한 프로그램 설치 확인
if ! command -v yq &> /dev/null
then
    echo "yq could not be found, installing..."
    sudo apt-get update
    sudo apt-get install -y jq
    wget https://github.com/mikefarah/yq/releases/download/v4.16.1/yq_linux_amd64 -O /usr/bin/yq
    chmod +x /usr/bin/yq
fi

# 구성 파일 경로
CORE_SITE="core-site.xml"
HDFS_SITE="hdfs-site.xml"
MAPRED_SITE="mapred-site.xml"
YARN_SITE="yarn-site.xml"

servers=("hadoop-master" "hadoop-slave1" "hadoop-slave2")
configs=($CORE_SITE $HDFS_SITE $MAPRED_SITE $YARN_SITE)

# hosts 파일 변경
#./update-hosts.sh

for server in "${servers[@]}"; do
  if [ $server != "hadoop-master" ]; then
    sshpass -p "root" ssh -o StrictHostKeyChecking=no root@$server "echo 'sucess'"
  fi
done

# create backup directory
if [ ! -d $HADOOP_CONF_DIR/snapshot/ ]; then
  mkdir $HADOOP_CONF_DIR/snapshot
fi

for file in "${configs[@]}"; do
  if [ -f $HADOOP_CONF_DIR/$file ]; then
    echo "Backing up ${file}..."
    mv $HADOOP_CONF_DIR/$file $HADOOP_CONF_DIR/snapshot/$file
  fi

  echo "Modifying ${file}..."
  section="${file%.xml}" # Remove the .xml extension to get the section name
  new_file_content="${HADOOP_CONF_DIR}/${file}"
  # 새 XML 파일 생성
  echo "<configuration>" > $new_file_content
  # YAML 파일의 내용을 새로운 XML 파일에 추가
  yq eval -o=json ".${section}" $YAML_FILE | jq -r 'to_entries[] | "<property><name>\(.key)</name><value>\(.value)</value></property>"' >> $new_file_content
  echo "</configuration>" >> $new_file_content

  for server in "${servers[@]}"; do
    if [ $server != "hadoop-master" ]; then
      sshpass -p "root" scp $new_file_content root@$server:$new_file_content
    fi
  done
done

for server in "${servers[@]}"; do
  if [ $server = "hadoop-master" ]; then
    echo "Stop $server node daemon"
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop namenode
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop secondarynamenode
    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop resourcemanager
    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop nodemanager
  else
    echo "Stop $server node daemon"
    ssh root@$server "sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop datanode"
    ssh root@$server "sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop nodemanager"
  fi
done

echo "Formatting namenode..."
sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format --force

for server in "${servers[@]}"; do
  if [ $server = "hadoop-master" ]; then
    echo "Restart $server node daemon"
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start namenode
    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start resourcemanager
    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager
  else
    ssh root@$server "rm -rf $HADOOP_HOME/dfs/*"
    echo "ReStart $server node daemon"
    ssh root@$server "sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start datanode"
    ssh root@$server "sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager"
  fi
done

#for server in "${servers[@]}"; do
#  if [ $server = "hadoop-master" ]; then
#    echo "Stop $server node daemon"
#    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop namenode
#    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop secondarynamenode
#    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop resourcemanager
#    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop nodemanager
#
#    echo "Formatting namenode..."
#    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format
#
#    echo "Restart $server node daemon"
#    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start namenode
#    sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start secondarynamenode
#    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start resourcemanager
#    sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager
#  else
#
#    echo "Stop $server node daemon"
#    ssh root@$server "sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon stop datanode"
#    ssh root@$server "sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon stop nodemanager"
#
#    ssh root@$server "rm -rf $HADOOP_HOME/dfs/*"
#
#    echo "ReStart $server node daemon"
#    ssh root@$server "sudo -E -u hdfs $HADOOP_HOME/bin/hdfs --daemon start datanode"
#    ssh root@$server "sudo -E -u yarn $HADOOP_HOME/bin/yarn --daemon start nodemanager"
#  fi
#done

echo "Configuration changes applied and services restarted."



