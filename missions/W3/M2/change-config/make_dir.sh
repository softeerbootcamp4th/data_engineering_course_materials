#!/bin/bash

# 인자를 1개만 받는다. 이때 첫 번째 인자는 컨테이너 이름이다.
if [ $# -ne 1 ]; then
  echo "Usage: $0 <CONTAINER_NAME>"
  exit 1
fi

CONTAINER_NAME=$1

# 함수 정의: 디렉토리 생성
create_directory() {
  local dir=$1
  echo "Creating directory $dir..."
  docker exec -it $CONTAINER_NAME bin/bash -c "
    if [ ! -d $dir ]; then
      sudo mkdir -p $dir && \
      sudo chown -R hadoop:hadoop $dir
    fi"
  if [ $? -ne 0 ]; then
    echo "Failed to create directory $dir inside the container."
    exit 1
  fi
}

# add hadoop directories for change configure
create_directory /hadoop/dfs/name
create_directory /hadoop/dfs/data
create_directory /hadoop/tmp