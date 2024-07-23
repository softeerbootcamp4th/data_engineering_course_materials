# Understanding of Hadoop Configuration Files

## Directory

```
+ hadoop_configure
    + node
        + config
            - core-site.xml
            - hdfs-site.xml
            - yarn-site.xml
            - mapred-site.xml
        - hadoop-3.3.6.tar.gz (이미지 빌드 속도를 위해 미리 다운로드)
        - start-hadoop.sh
        - Dockerfile
    + docker-compose.yml
    - update_config.py (각 노드의 컨테이너 안에서 실행됨)
    - update_config_all_nodes.sh (모든 컨테이너에 대해서 실행)
    - verify_config.py
    - verify_config_all_nodes.sh
```

## Config update

### update_config.py

```python
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import shutil
import subprocess

def delete_files(file_names, directory):
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"파일이 삭제되었습니다: {file_name}")
        else:
            print(f"파일이 존재하지 않습니다: {file_name}")

def backup_files(file_names, directory):
    for file_name in file_names:
        original_file = os.path.join(directory, file_name)
        backup_file = f"{original_file}.bak"
        if os.path.isfile(original_file):
            shutil.copy2(original_file, backup_file)
            print(f"백업 성공: {backup_file}")
        else:
            print(f"파일이 존재하지 않습니다: {original_file}")

def save_new_config(config_updates, directory):
    def dict_to_xml(tag, d):
        elem = Element(tag)
        for key, val in d.items():
            child = SubElement(elem, 'property')
            name = SubElement(child, 'name')
            name.text = str(key)
            value = SubElement(child, 'value')
            value.text = str(val)
        return elem

    def save_config_xml(config, filename):
        xml_element = dict_to_xml('configuration', config)
        xml_str = tostring(xml_element, 'utf-8')
        pretty_xml_str = parseString(xml_str).toprettyxml(indent="    ")
        with open(os.path.join(directory, filename), 'w') as f:
            f.write(pretty_xml_str)

    for filename, config in config_updates.items():
        save_config_xml(config, filename)

if __name__ == "__main__":

    hadoop_config_directory = "/usr/local/hadoop/etc/hadoop"
    config_files = ["core-site.xml", "hdfs-site.xml", "mapred-site.xml", "yarn-site.xml"]
    
    ##### -site.xml 백업
    backup_files(config_files, hadoop_config_directory)

    ##### -site.xml 삭제
    delete_files(config_files, hadoop_config_directory)

    ##### 설정으로 xml 파일 생성
    config_updates = {
        "core-site.xml": {
            "fs.defaultFS": "hdfs://hadoop-master:9000",
            "hadoop.tmp.dir": "file:///usr/local/hadoop/tmp",
            "io.file.buffer.size": "131072"
        },
        "hdfs-site.xml": {
            "dfs.replication": "2",
            "dfs.blocksize": "134217728",
            "dfs.namenode.name.dir": "file:///usr/local/hadoop/dfs/name"
        },
        "mapred-site.xml": {
            "mapreduce.framework.name": "yarn",
            "mapreduce.jobhistory.address": "hadoop-master:10020",
            "mapreduce.task.io.sort.mb": "256"
        },
        "yarn-site.xml": {
            "yarn.resourcemanager.address": "hadoop-master:8032",
            "yarn.nodemanager.resource.memory-mb": "8192",
            "yarn.scheduler.minimum-allocation-mb": "1024"
        }
    }

    save_new_config(config_updates, hadoop_config_directory)
```
- 각 컨테이너 안에서 *-site.xml을 백업, 수정

## update_config_all_nodes.sh

```sh
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
```
- masternode와 workernode에 대해 각각 namenode, resourcemanager / datanode, nodemanager를 종료
- 업데이트된 config를 적용 후 재실행

## Config Verification

### verify_config.py

```python
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.output.strip()}"
    

def main():

    ##### ##### verify configs    
    config_updates = {
        "core-site.xml": {
            "fs.defaultFS": "hdfs://hadoop-master:9000",
            "hadoop.tmp.dir": "file:///usr/local/hadoop/tmp",
            "io.file.buffer.size": "131072"
        },
        "hdfs-site.xml": {
            "dfs.replication": "2",
            "dfs.blocksize": "134217728",
            "dfs.namenode.name.dir": "file:///usr/local/hadoop/dfs/name"
        },
        "mapred-site.xml": {
            "mapreduce.framework.name": "yarn",
            "mapreduce.jobhistory.address": "hadoop-master:10020",
            "mapreduce.task.io.sort.mb": "256"
        },
        "yarn-site.xml": {
            "yarn.resourcemanager.address": "hadoop-master:8032",
            "yarn.nodemanager.resource.memory-mb": "8192",
            "yarn.scheduler.minimum-allocation-mb": "1024"
        }
    }
    expected_config = {
        "fs.defaultFS": "hdfs://hadoop-master:9000",
        "hadoop.tmp.dir": "file:///usr/local/hadoop/tmp",
        "io.file.buffer.size": "131072",
        "dfs.replication": "2",
        "dfs.blocksize": "134217728",  # 128 MB
        "dfs.namenode.name.dir": "file:///usr/local/hadoop/dfs/name",
        "mapreduce.framework.name": "yarn",
        "mapreduce.jobhistory.address": "hadoop-master:10020",
        "mapreduce.task.io.sort.mb": "256",
        "yarn.resourcemanager.address": "hadoop-master:8032",
        "yarn.nodemanager.resource.memory-mb": "8192",
        "yarn.scheduler.minimum-allocation-mb": "1024"
    }

    for config_key, expected_value in expected_config.items():
        command = ['/usr/local/hadoop/bin/hdfs', 'getconf', '-confKey', config_key]
        actual_value = run_command(command)
        if actual_value == expected_value:
            print('PASS:', end=' ')
            print(command, end=' ')
            print(f'-> {actual_value}')
        else:
            print('FAIL:', end=' ')
            print(command, end=' ')
            print(f'-> {actual_value} (expected {expected_value})')

    ##### ##### create testfile
    


if __name__ == "__main__":
    main()
```

- 각 노드 내에서 config를 확인

### verify_config_all_nodes

```sh
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
```

- 각 컨테이너에 대해 verify_config.py 스크립트를 실행 
- masternode에 한해 복제 계수 확인, example mapred job, yarn 질의 추가 실행
