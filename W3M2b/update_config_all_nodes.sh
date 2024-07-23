#!/bin/bash

# Docker Compose를 사용하여 실행 중인 모든 컨테이너의 이름을 얻고, 각 컨테이너에 대해 명령을 실행
for container in $(docker-compose ps -q); do

    hostname=$(docker exec $container hostname | tr -d '\r\n')
    echo "#########################"
    echo "#####    $hostname"
    echo "#########################"
    
    # 파이썬 스크립트를 각 컨테이너에 복사
    docker cp update_config.py $container:/usr/local/hadoop/etc/hadoop/update_config.py
s
    # 복사된 스크립트의 실행 권한 변경
    docker exec -it $container sudo chmod +x /usr/local/hadoop/etc/hadoop/update_config.py

    # 스크립트 실행
    docker exec -it $container sudo python3 /usr/local/hadoop/etc/hadoop/update_config.py


    if [ "$hostname" == "hadoop-master" ]; then
        
        echo "---------------------------- hadoop-master ---------------------------- "

        echo "Stopping NameNode and SecondaryNameNode on hadoop-master..."
        docker exec $container hdfs --daemon stop namenode
        docker exec $container hdfs --daemon stop secondarynamenode
        docker exec $container yarn --daemon stop resourcemanager

        echo "Creating and setting permissions on HDFS directory..."
        docker exec $container sudo mkdir /usr/local/hadoop/dfs
        docker exec $container sudo chown hadoopuser:hadoopuser /usr/local/hadoop/dfs

        echo "Formatting NameNode..."
        docker exec $container hdfs namenode -format -force -nonInteractive

        echo "Starting NameNode, SecondaryNameNode, and ResourceManager..."
        docker exec $container hdfs --daemon start namenode
        docker exec $container hdfs --daemon start secondarynamenode
        docker exec $container yarn --daemon start resourcemanager
    else
        echo "---------------------------- hadoop-worker ---------------------------- "

        echo "Stopping DataNode and NodeManager on other nodes..."
        docker exec $container hdfs --daemon stop datanode
        docker exec $container yarn --daemon stop nodemanager

        echo "Setting Datanode ..."
        docker exec $container rm -rf usr/local/hadoop/data/datanode
        docker exec $container sudo mkdir usr/local/hadoop/data/datanode
        docker exec $container sudo chown hadoopuser:hadoopuser usr/local/hadoop/data/datanode

        echo "Starting DataNode and NodeManager..."
        docker exec $container hdfs --daemon start datanode
        docker exec $container yarn --daemon start nodemanager
    fi

done



