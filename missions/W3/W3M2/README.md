# Hadoop Multi Node Cluster on Docker.

# 1. 컨테이너 생성
## 1.1. Docker-compose image를 build
```bash
docker-compose build
```
* Dockerfile, Docker-compose.yml이 있는 디렉토리에서 터미널이 입력

## 1.2. Docker container를 실행한다.
```bash
docker-compose up -d
```
* docke-compose file을 보고 포트 뚫고 컨테이너 실행한다.

## 1.3. 실행 중인 Docker를 확인한다.
```
docker ps
```

# 2. Mapreduce 확인
## 2.1. container 접속
```bash
docker exec -it hadoop-master /bin/bash
```
* hadoop-master : master container 이름

## 2.2. HDFS state 확인
```bash
hdfs dfsadmin -report
```

```bash
jps
```

## 2.3. hdfs로 접속
```bash
su - hdfs
```

```bash
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

## 2.4. slave1에 접속
```bash
ssh hadoop-slave1
``` 
* slave로 접속이 가능함을 확인

# 3. Map Reduce
## 3.1. 텍스트 파일을 컨테이너로 복사
```bash
docker cp /Users/admin/Desktop/Data_Engineering/W3/W3M2a/Multi_Node_Hadoop_M2_test/mapreduce_example.txt hadoop-master:/root/mapreduce_example.txt
```

## 3.2. hadoop-master 컨테이너에 접속하여 HDFS에 업로드
```bash
docker exec -it hadoop-master /bin/bash
```
## 3.3. HDFS 확인
```bash
hdfs dfs -ls /user/hdfs/input
```

## 3.4. Word Count 작업
```bash
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hdfs/input/mapreduce_example.txt /user/hdfs/output
```

## 3.5. Output Result 확인
```bash
hdfs dfs -cat /user/hdfs/output/part-r-00000
```


# 4. Modification and Verification
## 4.1. modify 스크립트로 config 수정
```bash
docker exec -it hadoop-master /bin/bash -c "/usr/local/bin/modify_hadoop_config.sh /usr/local/hadoop/etc/hadoop"
```

## 4.2. verify 스크립트로 config 검증
```bash
docker exec -it hadoop-master /bin/bash -c "/usr/local/bin/verify_hadoop_config.sh"
```