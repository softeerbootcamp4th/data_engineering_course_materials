#!/bin/bash

# 실행할 스크립트를 입력받는다.


if [ $# -ne 1 ]; then
  echo "Usage: $0 <script-name> "
  exit 1
fi

SCRIPT_NAME=$1
CONTAINER_NAME="spark-master"
SPARK_HOME=/usr/local/spark


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

create_directory $SPARK_HOME/rdd

# 함수 정의: 파일 복사
copy_file() {
  local src_file=$1
  local dest_dir=$2
  echo "Copying $src_file..."
  docker cp ./rdd/$src_file $CONTAINER_NAME:$dest_dir/
  if [ $? -ne 0 ]; then
    echo "Failed to copy $src_file."
    exit 1
  fi
}

# src_file은 현재 디렉토리에 있는 verify...conf.sh 파일을 가리킨다.
copy_file $1 $SPARK_HOME/rdd



# 복사한 .sh 파일들을 도커 컨테이너 내부에서 실행할 수 있도록 권한을 변경한다.
docker exec -it --user hadoop $CONTAINER_NAME bash -c "
  sudo chown hadoop:hadoop $SPARK_HOME/rdd/* &&
  chmod +x $SPARK_HOME/rdd/$1
  "

if [ $? -ne 0 ]; then
    echo "Failed to change permission of verification scripts inside the container."
    exit 1
fi

# 주피터 켜기
docker exec -it --user hadoop $CONTAINER_NAME bash -c "
  jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
  "
    



