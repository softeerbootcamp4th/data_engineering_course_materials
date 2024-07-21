#!/bin/bash

# 인수 확인
if [ $# -ne 1 ]; then
    echo "Usage: $0 <hadoop-config-dir>"
    exit 1
fi

# 하둡 설정 디렉토리 경로
HADOOP_CONFIG_DIR=$1

# Docker 컨테이너 이름
CONTAINER_NAME=(
    "hadoop-master"
    "hadoop-slave1"
    "hadoop-slave2"
    "hadoop-slave3"
)

# 하둡 설정 파일들
HADOOP_CONFIG_FILES=(
    "core-site.xml"
    "hdfs-site.xml"
    "mapred-site.xml"
    "yarn-site.xml"
)

# 로컬 백업 디렉토리
BACKUP_DIR="./backup"

# 백업 디렉토리가 없으면 생성
mkdir -p $BACKUP_DIR

# 각 컨테이너에 로그 파일 경로 설정
LOG_DIR="/usr/local/hadoop/logs"
LOG_FILE="$LOG_DIR/hadoop.log"

# 각 컨테이너에 로그 디렉토리 및 파일 생성
for CONTAINER in "${CONTAINER_NAME[@]}"; do
    docker exec $CONTAINER /bin/bash -c "mkdir -p $LOG_DIR && touch $LOG_FILE && chmod 777 $LOG_FILE"
done

# 백업 및 복사 수행
for FILE_NAME in "${HADOOP_CONFIG_FILES[@]}"; do
    # 하둡 설정 파일 전체 경로
    CONFIG_PATH="$HADOOP_CONFIG_DIR/$FILE_NAME"
    
    # 로컬 백업 파일 경로
    BACKUP_FILE="$BACKUP_DIR/$FILE_NAME.backup"
    
    # 백업
    docker cp "hadoop-master":$CONFIG_PATH $BACKUP_FILE
    
    # 백업 완료 메시지 및 성공 여부 확인
    if [ $? -eq 0 ]; then
        echo "Backing up $FILE_NAME..."
    else
        echo "Backup of $FILE_NAME failed."
        exit 1
    fi
done

for CONTAINER in "${CONTAINER_NAME[@]}"; do
    
    for FILE_NAME in "${HADOOP_CONFIG_FILES[@]}"; do
        # 하둡 설정 파일 전체 경로
        CONFIG_PATH="$HADOOP_CONFIG_DIR/$FILE_NAME"
        # 복사
        LOCAL_CONFIG_FILE="./modify_config/$FILE_NAME"
        
        # 로컬에서 컨테이너로 파일 복사
        docker cp $LOCAL_CONFIG_FILE $CONTAINER:$CONFIG_PATH
        
        # 복사 완료 메시지 및 성공 여부 확인
        if [ $? -eq 0 ]; then
            echo "Modifying $FILE_NAME..."
        else
            echo "Failed to copy $FILE_NAME from local to container."
            exit 1
        fi
    done
done

echo "Stopping Hadoop DFS..."
echo "Stopping YARN..."
# HDFS YARN 종료
for CONTAINER in "${CONTAINER_NAME[@]}"; do
    
    if [[ $CONTAINER == "hadoop-master" ]]; then
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon stop secondarynamenode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon stop namenode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "yarn --daemon stop resourcemanager >> $LOG_FILE 2>&1"
    else
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon stop datanode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "yarn --daemon stop nodemanager >> $LOG_FILE 2>&1"
    fi
done

echo "Starting Hadoop DFS..."
echo "Starting YARN..."
for CONTAINER in "${CONTAINER_NAME[@]}"; do
    # namenod, datanode가 저장될 디렉토리 경로
    NAMENODE_DIR="/usr/local/hadoop"
    
    # HDFS YARN 시작
    if [[ $CONTAINER == "hadoop-master" ]]; then
        if ! docker exec $CONTAINER /bin/bash -c "[ -d \"$NAMENODE_DIR/dfs/name/current\" ]"; then
            docker exec $CONTAINER /bin/bash -c "hdfs namenode -format -force -nonInteractive >> $LOG_FILE 2>&1"
            docker exec $CONTAINER /bin/bash -c "chmod -R 777 \"$NAMENODE_DIR/dfs/name\" >> $LOG_FILE 2>&1"
        fi
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon start namenode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "mkdir -p \"$NAMENODE_DIR/tmp/dfs/namesecondary\" >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon start secondarynamenode >> $LOG_FILE 2>&1"
    else
        docker exec $CONTAINER /bin/bash -c "rm -rf $NAMENODE_DIR/data/datanode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "mkdir $NAMENODE_DIR/data/datanode >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "chmod -R 777 \"$NAMENODE_DIR/data/datanode\" >> $LOG_FILE 2>&1"
        docker exec $CONTAINER /bin/bash -c "hdfs --daemon start datanode >> $LOG_FILE 2>&1"
    fi
    
    if [[ $CONTAINER == "hadoop-master" ]]; then
        docker exec $CONTAINER /bin/bash -c "yarn --daemon start resourcemanager >> $LOG_FILE 2>&1"
    else
        docker exec $CONTAINER /bin/bash -c "yarn --daemon start nodemanager >> $LOG_FILE 2>&1"
    fi
done

# 모든 작업 완료 메시지
echo "Configuration changes applied and services restarted."
