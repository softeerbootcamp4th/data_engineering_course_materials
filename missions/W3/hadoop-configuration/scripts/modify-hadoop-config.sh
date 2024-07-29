#!/usr/bin/env bash

YAML_FILE="sample-configuration.yaml"
HADOOP_HOME="${1:-/usr/local/hadoop}"
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_VERSION=3.4.0

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

configs=($CORE_SITE $HDFS_SITE $MAPRED_SITE $YARN_SITE)

if [ ! -d $HADOOP_CONF_DIR/snapshot/ ]; then
  mkdir $HADOOP_CONF_DIR/snapshot
fi

for file in "${configs[@]}"; do
  if [ -f $HADOOP_CONF_DIR/$file ]; then
    echo "Backing up ${file}..."
    mv $HADOOP_CONF_DIR/$file $HADOOP_CONF_DIR/snapshot/
  fi

  echo "Modifying ${file}..."
  section="${file%.xml}" # Remove the .xml extension to get the section name
  new_file_content="${HADOOP_CONF_DIR}/${file}"
  # 새 XML 파일 생성
  echo "<configuration>" >> $new_file_content
  # YAML 파일의 내용을 새로운 XML 파일에 추가
  yq eval -o=json ".${section}" $YAML_FILE | jq -r 'to_entries[] | "<property><name>\(.key)</name><value>\(.value)</value></property>"' >> $new_file_content
  echo "</configuration>" >> $new_file_content
done

# Hadoop 서비스 재시작
echo "Stopping Hadoop DFS..."
sudo -E -u hdfs $HADOOP_HOME/sbin/stop-dfs.sh
echo "Stopping YARN..."
sudo -E -u yarn $HADOOP_HOME/sbin/stop-yarn.sh
echo "Starting Hadoop DFS..."
sudo -E -u hdfs $HADOOP_HOME/bin/hdfs namenode -format
sudo -E -u hdfs $HADOOP_HOME/sbin/start-dfs.sh
echo "Starting YARN..."
sudo -E -u yarn $HADOOP_HOME/sbin/start-yarn.sh

echo "Configuration changes applied and services restarted."
