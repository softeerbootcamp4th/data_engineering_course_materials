# 0. Directory Hierarchy
```
├── Dockerfile
├── Dockerfile.base
├── docker-compose.yml
├── config
│   ├── core-site.xml
│   ├── hadoop-env.sh
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   └── yarn-site.xml
└── start-node.sh
```

# 1. Build Hadoop Base Image
```bash
(local)% docker build -t hadoop-base -f Dockerfile.base hadoop-base .
```

# 2. Build Hadoop Cluster Image
```bash
(local)% docker build -t hadoop-cluster .
```

# 3. Run Containers
```bash
(local)% docker-compose up -d 
```

# 4. Verify Hadoop Cluster Functionality
### Hadoop Cluster
```bash
# master, worker1, worker2 세 개의 컨테이너 돌아가는지 확인
(local)% docker ps

# master container에서 bash 실행
(loacl)% docker exec -it master /bin/bash

# hdfs report 확인 (Live datanodes = 2)
(master)$ hdfs dfsadmin -report
```
### Web UI
```text
아래의 두 주소로 접속이 잘 되는지 확인
http://localhost:9870
http://localhost:8088
```
### Mapreduce
```bash
# 테스트 파일 생성 및 HDFS에 업로드
(master)$ echo "word count test file test test" >> input.txt
(master)$ hdfs dfs -mkdir -p /user/hadoop/user/input
(master)$ hdfs dfs -put input.txt /user/hadoop/user/input/

# MapReduce 작업 실행 (WordCount 예제)
(master)$ hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoopuser/input /user/hadoopuser/output

# MapReduce 작업 결과 확인
(master)$ hdfs dfs -ls /user/hadoopuser/output
(master)$ hdfs dfs -cat /user/hadoopuser/output/part-r-00000
```
