# Docker를 사용하여 다중 노드 Hadoop 클러스터 설정하기

## 디렉터리 구조

```bash
.
├── hadoop_master
│   ├── Dockerfile
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   ├── yarn-site.xml
│   ├── hadoop-env.sh
│   └── start-yarn.sh
├── hadoop_worker
│   ├── Dockerfile
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   ├── yarn-site.xml
│   ├── hadoop-env.sh
│   └── start-yarn.sh
└── docker-compose.yml
```
- master 노드 폴더와 worker 노드 폴더에 dockerfile과 기타 구성 파일 생성

## Docker 네트워크 설정

```bash
docker network create hadoop-network 
```

## Docker 이미지 빌드

```bash
# docker-compose.yml 파일이 있는 루트 디렉터리로 이동
# 빌드하고 클러스터 시작
docker-compose up --build -d
```  

## HDFS 및 YARN 웹 인터페이스 확인

```
- HDFS: http://localhost:9870
- YARN: http://localhost:8088
```

## 마스터 노드에서 HDFS 명령어를 실행하여 HDFS와 상호작용

```bash
docker exec -it master bash
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/root
echo "Hello Hadoop" > hello.txt
hdfs dfs -put hello.txt /user/root/
hdfs dfs -cat /user/root/hello.txt
```

## MapReduce 작업 실행

```bash
docker exec -it master bash

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-$HADOOP_VERSION.jar wordcount /user/root/hello.txt /user/root/output

# 출력 확인
hdfs dfs -cat /user/root/output/part-r-00000
```

## MapReduce 작업 실행시 Error

- HDFS의 NameNode가 안전 모드(Safe Mode) 상태에 있기 때문에 발생
- NameNode가 안전 모드에 있는 동안에는 파일 삭제와 같은 변경 작업이 제한
- 안전 모드는 HDFS가 시작될 때 데이터 노드의 상태를 점검하고 충분한 블록이 보고될 때까지 유지

```bash
# NameNode의 안전 모드 상태를 확인
$HADOOP_HOME/bin/hdfs dfsadmin -safemode get

# 안전 모드 해제
$HADOOP_HOME/bin/hdfs dfsadmin -safemode leave
```
