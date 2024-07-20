# Hadoop Multi Node Cluster

## Run multi-node cluster
```bash
docker compose up -d
```

## Retrieve the file
```bash
# list directories and files
docker exec <namenode container name or id> bin/hdfs dfs -ls <directory>

# show content of a file
docker exec <namenode container name or id> bin/hdfs dfs -cat <filename>
```

## Create a new directory in HDFS
```bash
# create a directory in /
docker exec <namenode container name or id> bin/hdfs dfs -mkdir -p <diretory>

# create a directory in /user/hdoop
docker exec <namenode container name or id> bin/hdfs dfs -mkdir <directory>
```

## Upload a file in HDFS
```bash
docker exec <namenode container name or id> \
       bin/hdfs dfs -copyFromLocal <container file path> <hdfs directory path>
```

## Modify hadoop configuration
컨테이너 안의 `config.toml`에서 설정값을 저장한 후 다음을 실행
```bash
docker exec <container name or id> ./modify_config.sh config.toml <node name>
```
- node name 목록
  - nodename
    - master 컨테이너
      - namenode
      - job history server
      - resource manager
  - worker1
    - 첫번째 worker 컨테이너 ('worker1')
      - secondary namenode
      - datanode
      - node manager
  - worker
    - 첫번째 이후 worker 컨테이너 ('worker2', 'worker3', ...)
      - datanode
      - node manager

## Verify hadoop configuration
```bash
docker exec <container name or id> python3 verify.py
```