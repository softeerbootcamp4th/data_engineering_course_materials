#!/bin/bash

# Docker Compose를 사용하여 실행 중인 모든 컨테이너의 이름을 얻고, 각 컨테이너에 대해 명령을 실행
for container in $(docker-compose ps -q); do

    hostname=$(docker exec $container hostname | tr -d '\r\n')

    echo "#########################"
    echo "#####    $hostname"
    echo "#########################"
    
    # 파이썬 스크립트를 각 컨테이너에 복사
    docker cp verify_config.py $container:/usr/local/hadoop/etc/hadoop/verify_config.py

    # 복사된 스크립트의 실행 권한 변경
    docker exec -it $container sudo chmod +x /usr/local/hadoop/etc/hadoop/verify_config.py

    # 스크립트 실행
    docker exec -it $container sudo python3 /usr/local/hadoop/etc/hadoop/verify_config.py

    # 마스터노드 테스트 파일 생성
    i# 마스터노드에서 추가 작업 수행
    if [ "$hostname" == "hadoop-master" ]; then
        # 테스트 파일 생성 및 HDFS 업로드
        docker exec $container bash -c "echo 'This is sample for verification.' > /tmp/verification_sample.txt"
        docker exec $container hdfs dfs -mkdir -p /temp_dir
        docker exec $container hdfs dfs -put /tmp/verification_sample.txt /temp_dir
        
        # 해당 파일의 replication info 확인
        replication_info=$(docker exec $container hdfs fsck /temp_dir/verification_sample.txt -files -blocks -locations)
        echo "Replication Info: $replication_info"

        # MapReduce 작업 실행
        docker exec $container hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples*.jar wordcount /temp_dir /output_dir
        
        # 결과 확인
        echo "MapReduce job output:"
        docker exec $container hdfs dfs -cat /output_dir/*

        # YARN ResourceManager, YARN의 총 사용 가능한 메모리를 확인
        yarn_status=$(docker exec $container yarn node -list -showDetails)
        echo "YARN Node Status: $yarn_status"
    fi
done