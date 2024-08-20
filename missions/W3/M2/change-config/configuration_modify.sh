#!/bin/bash

# 인자를 3개 받는다. 이때 첫 번째 인자는 HADOOP_HOME, 두 번째 인자는 CONTAINER_NAME, 세번째 인자는 하둡 서비스 종류이다.
# SERVICE_TYPE = {namenode, datanode, resourcemanager, nodemanager}
if [ $# -ne 3 ]; then
  echo "Usage: $0 <HADOOP_HOME> <CONTAINER_NAME> <SERVICE_TYPE>"
  exit 1
fi

# make_dir.sh 실행 인자는 CONTAINER_NAME
./make_dir.sh $2

# 환경 변수 설정
HADOOP_HOME=$1
CONTAINER_NAME=$2
SERVICE_TYPE=$3

# 올바른 서비스 타입인지 확인
if [[ ! "namenode datanode resourcemanager nodemanager" =~ (^|[[:space:]])$SERVICE_TYPE($|[[:space:]]) ]]; then
  echo "Invalid service type. Please specify one of the following: namenode, datanode, resourcemanager, nodemanager."
  exit 1
fi

# 함수 정의: 디렉토리 생성
create_directory() {
  local dir=$1
  echo "Creating directory $dir..."
  docker exec -it $CONTAINER_NAME bash -c "
    if [ ! -d $dir ]; then
      mkdir -p $dir
    fi"
  if [ $? -ne 0 ]; then
    echo "Failed to create directory $dir inside the container."
    exit 1
  fi
}

# 함수 정의: 파일 복사
copy_file() {
  local src_file=$1
  local dest_dir=$2
  echo "Copying $src_file..."
  docker cp $src_file $CONTAINER_NAME:$dest_dir/
  if [ $? -ne 0 ]; then
    echo "Failed to copy $src_file."
    exit 1
  fi
}

# 함수 정의: 파일 백업
backup_file() {
  local file=$1
  local backup_dir=$2
  echo "Backing up $file..."
  docker exec -it $CONTAINER_NAME bash -c "
    timestamp=$timestamp
    mkdir -p $backup_dir &&
    cp $file $backup_dir &&
    echo 'Configuration file[$(basename $file)] have been backed up to $backup_dir.'
    "
  if [ $? -ne 0 ]; then
    echo "Failed to back up configuration file[$(basename $file)] inside the container."
    exit 1
  fi
}

# 함수 정의: 파일 업데이트
update_file() {
  local src_file=$1
  local dest_file=$2
  echo "Updating $dest_file..."
  docker exec -it $CONTAINER_NAME bash -c "
    cp $src_file $dest_file &&
    rm -rf $src_file &&
    chmod +x $dest_file &&
    echo 'Configuration file[$(basename $dest_file)] have been updated and temporary files removed.'"
  if [ $? -ne 0 ]; then
    echo "Failed to update configuration file[$(basename $dest_file)] inside the container."
    exit 1
  fi
}

# 함수 정의: namenode 서비스 재시작 (HDFS 서비스)
restart_namenode_service() {
  local service=$1
  local name_dir_origin=$2
  local name_dir_changed=$3
  echo "Restarting Hadoop $service service..."

  # Determine whether to format or not
  if [ "$name_dir_origin" != "$name_dir_changed" ]; then
    echo "Formatting NameNode directory..."
    docker exec -it $CONTAINER_NAME bash -c "
    $HADOOP_HOME/bin/hdfs --daemon stop $service &&
    $HADOOP_HOME/bin/hdfs namenode -format &&
    nohup $HADOOP_HOME/bin/hdfs --daemon start $service > /dev/null
    "
  else
    echo "NameNode directory has not changed. Restarting Hadoop $service service..."
    docker exec -it $CONTAINER_NAME bash -c "
    $HADOOP_HOME/bin/hdfs --daemon stop $service &&
    nohup $HADOOP_HOME/bin/hdfs --daemon start $service > /dev/null
    "
  fi

  if [ $? -ne 0 ]; then
    echo "Failed to restart Hadoop $service service."
    exit 1
  fi
  echo "Hadoop $service service has been restarted successfully."
}

# 함수 정의: datanode 서비스 재시작 (HDFS 서비스)
restart_datanode_service() {
  local service=$1
  echo "Restarting Hadoop $service service..."
  docker exec -it $CONTAINER_NAME bash -c "
  $HADOOP_HOME/bin/hdfs --daemon stop $service &&
  nohup $HADOOP_HOME/bin/hdfs --daemon start $service > /dev/null
  "
  if [ $? -ne 0 ]; then
    echo "Failed to restart Hadoop $service service."
    exit 1
  fi
  echo "Hadoop $service service has been restarted successfully."
}

# 함수 정의: YARN 서비스 재시작
restart_yarn_service() {
  local service=$1
  echo "Restarting Hadoop $service service..."
  docker exec -it $CONTAINER_NAME bash -c "
    $HADOOP_HOME/bin/yarn --daemon stop $service &&
    nohup $HADOOP_HOME/bin/yarn --daemon start $service > /dev/null
    "
  if [ $? -ne 0 ]; then
    echo "Failed to restart Hadoop $service service."
    exit 1
  fi
  echo "Hadoop $service service has been restarted successfully."
}

# 타임스탬프 생성
timestamp=$(date +%s)

# 디렉토리 생성 및 파일 복사
create_directory "$HADOOP_HOME/etc/hadoop/tmp"
copy_file "core-site.xml" "$HADOOP_HOME/etc/hadoop/tmp"
copy_file "hdfs-site.xml" "$HADOOP_HOME/etc/hadoop/tmp"
copy_file "mapred-site.xml" "$HADOOP_HOME/etc/hadoop/tmp"
copy_file "yarn-site.xml" "$HADOOP_HOME/etc/hadoop/tmp"

create_directory "$HADOOP_HOME/etc/hadoop/backup/$timestamp"

# 파일 백업
backup_file "$HADOOP_HOME/etc/hadoop/core-site.xml" "$HADOOP_HOME/etc/hadoop/backup/$timestamp"
backup_file "$HADOOP_HOME/etc/hadoop/hdfs-site.xml" "$HADOOP_HOME/etc/hadoop/backup/$timestamp"
backup_file "$HADOOP_HOME/etc/hadoop/mapred-site.xml" "$HADOOP_HOME/etc/hadoop/backup/$timestamp"
backup_file "$HADOOP_HOME/etc/hadoop/yarn-site.xml" "$HADOOP_HOME/etc/hadoop/backup/$timestamp"

# Get the NameNode directory
NAME_DIR_ORIGIN=$(docker exec -it $CONTAINER_NAME bash -c "$HADOOP_HOME/bin/hdfs getconf -confKey dfs.namenode.name.dir 2>&1" | awk '/file:\/\// {print $1}' | xargs)
DATA_DIR_ORIGIN=$(docker exec -it $CONTAINER_NAME bash -c "$HADOOP_HOME/bin/hdfs getconf -confKey dfs.datanode.data.dir 2>&1" | awk '/file:\/\// {print $1}' | xargs)
echo "NameNode directory: $NAME_DIR_ORIGIN"
echo "DataNode directory: $DATA_DIR_ORIGIN"

# 파일 업데이트
update_file "$HADOOP_HOME/etc/hadoop/tmp/core-site.xml" "$HADOOP_HOME/etc/hadoop/core-site.xml"
update_file "$HADOOP_HOME/etc/hadoop/tmp/hdfs-site.xml" "$HADOOP_HOME/etc/hadoop/hdfs-site.xml"
update_file "$HADOOP_HOME/etc/hadoop/tmp/mapred-site.xml" "$HADOOP_HOME/etc/hadoop/mapred-site.xml"
update_file "$HADOOP_HOME/etc/hadoop/tmp/yarn-site.xml" "$HADOOP_HOME/etc/hadoop/yarn-site.xml"

echo "Configuration files have been copied and updated successfully."

# Get the NameNode directory
NAME_DIR_CHANGED=$(docker exec -it $CONTAINER_NAME bash -c "$HADOOP_HOME/bin/hdfs getconf -confKey dfs.namenode.name.dir 2>&1" | awk '/file:\/\// {print $1}' | xargs)
DATA_DIR_CHANGED=$(docker exec -it $CONTAINER_NAME bash -c "$HADOOP_HOME/bin/hdfs getconf -confKey dfs.datanode.data.dir 2>&1" | awk '/file:\/\// {print $1}' | xargs)

# 서비스 재시작
case $SERVICE_TYPE in
  namenode)
    restart_namenode_service $SERVICE_TYPE $NAME_DIR_ORIGIN $NAME_DIR_CHANGED
    ;;
  datanode)
    restart_datanode_service $SERVICE_TYPE
    ;;
  resourcemanager|nodemanager)
    restart_yarn_service $SERVICE_TYPE
    ;;
esac

echo "Configuration changes applied and services restarted."
