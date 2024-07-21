#!/bin/bash

# 변수 설정
CONTAINER_NAME=hadoop-master
LOCAL_DIR_PATH=./modify_config
CONTAINER_DIR_PATH=/usr/local/hadoop/etc/hadoop

# 파일별 속성 목록 설정
CORE_SITE_PROPERTIES=("fs.defaultFS" "hadoop.tmp.dir" "io.file.buffer.size")
HDFS_SITE_PROPERTIES=("dfs.replication" "dfs.blocksize" "dfs.namenode.name.dir")
YARN_SITE_PROPERTIES=("yarn.resourcemanager.hostname" "yarn.nodemanager.resource.memory-mb" "yarn.scheduler.minimum-allocation-mb")
MAPRED_SITE_PROPERTIES=("mapreduce.framework.name" "mapreduce.jobhistory.address" "mapreduce.task.io.sort.mb")

# 비교할 XML 파일 및 속성 목록 배열
FILES=("core-site.xml" "hdfs-site.xml" "mapred-site.xml" "yarn-site.xml")

for FILE in "${FILES[@]}"; do
    
    LOCAL_FILE_PATH="$LOCAL_DIR_PATH/$FILE"
    CONTAINER_FILE_PATH="$CONTAINER_DIR_PATH/$FILE"
    
    case $FILE in
        "core-site.xml")
            PROPERTIES=("${CORE_SITE_PROPERTIES[@]}")
        ;;
        "hdfs-site.xml")
            PROPERTIES=("${HDFS_SITE_PROPERTIES[@]}")
        ;;
        "yarn-site.xml")
            PROPERTIES=("${YARN_SITE_PROPERTIES[@]}")
        ;;
        "mapred-site.xml")
            PROPERTIES=("${MAPRED_SITE_PROPERTIES[@]}")
        ;;
        *)
            echo "Unknown file: $FILE"
            continue
        ;;
    esac
    
    for PROPERTY_NAME in "${PROPERTIES[@]}"; do
        # 로컬 파일에서 value 추출
        LOCAL_VALUE=$(xmllint --xpath "string(//property[name='$PROPERTY_NAME']/value)" $LOCAL_FILE_PATH 2>/dev/null)
        
        # 컨테이너 파일에서 value 추출
        CONTAINER_FILE_CONTENT=$(docker exec $CONTAINER_NAME cat $CONTAINER_FILE_PATH)
        CONTAINER_VALUE=$(echo "$CONTAINER_FILE_CONTENT" | xmllint --xpath "string(//property[name='$PROPERTY_NAME']/value)" - 2>/dev/null)
        
        # 값 비교
        if [ "$LOCAL_VALUE" == "$CONTAINER_VALUE" ]; then
            echo "PASS: [$FILE] ['hdfs', 'getconf', '-confKey', '$PROPERTY_NAME'] -> $CONTAINER_VALUE"
        else
            echo "FAIL: [$FILE] ['hdfs', 'getconf', '-confKey', '$PROPERTY_NAME'] -> $CONTAINER_VALUE (expected $LOCAL_VALUE)"
        fi
    done
done
