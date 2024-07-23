#!/bin/bash

# 인자를 2개만 받는다. 이때 첫 번째 인자는 HADOOP_HOME, 두 번째 인자는 CONTAINER_NAME이다. 세번재 인자는 없다
if [ $# -ne 2 ]; then
  echo "Usage: $0 <HADOOP_HOME> <CONTAINER_NAME>"
  exit 1
fi

# 여기 디렉토리에 있는 파일을 <CONTAINER_NAME> 컨테이너의 <HADOOP_HOME>/verification 폴더로 복사한다. 폴더가 없으면 생성한다.
# 이때 <HADOOP_HOME>은 컨테이너 내부의 하둡 설치 디렉토리를 가리킨다.
HADOOP_HOME=$1
CONTAINER_NAME=$2


# 함수 정의: 디렉토리 생성
create_directory() {
  local dir=$1
  echo "Creating directory $dir..."
  docker exec -it --user hadoop $CONTAINER_NAME bash -c "
    if [ ! -d $dir ]; then
      mkdir -p $dir
    fi"
  if [ $? -ne 0 ]; then
    echo "Failed to create directory $dir inside the container."
    exit 1
  fi
}

create_directory $HADOOP_HOME/verification

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

# src_file은 현재 디렉토리에 있는 verify...conf.sh 파일을 가리킨다.
copy_file verify_core-site_conf.sh $HADOOP_HOME/verification
copy_file verify_hdfs-site_conf.sh $HADOOP_HOME/verification
copy_file verify_mapred-site_conf.sh $HADOOP_HOME/verification
copy_file verify_yarn-site_conf.sh $HADOOP_HOME/verification


# 복사한 .sh 파일들을 도커 컨테이너 내부에서 실행할 수 있도록 권한을 변경한다.
docker exec -it --user hadoop $CONTAINER_NAME bash -c "
  sudo chown hadoop:hadoop $HADOOP_HOME/verification/* &&
  chmod +x $HADOOP_HOME/verification/verify_core-site_conf.sh &&
  chmod +x $HADOOP_HOME/verification/verify_hdfs-site_conf.sh &&
  chmod +x $HADOOP_HOME/verification/verify_mapred-site_conf.sh &&
  chmod +x $HADOOP_HOME/verification/verify_yarn-site_conf.sh
  "

if [ $? -ne 0 ]; then
    echo "Failed to change permission of verification scripts inside the container."
    exit 1
fi


# 복사한 .sh 파일들을 도커 컨테이너 내부에서 실행한다.
docker exec -it $CONTAINER_NAME bash -c "
  $HADOOP_HOME/verification/verify_core-site_conf.sh &&
  $HADOOP_HOME/verification/verify_hdfs-site_conf.sh &&
  $HADOOP_HOME/verification/verify_mapred-site_conf.sh &&
  $HADOOP_HOME/verification/verify_yarn-site_conf.sh
  "


    


