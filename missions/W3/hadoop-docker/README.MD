# Docker를 사용하여 단일 노드 Hadoop 클러스터 설정하기

## Dockerfile과 Hadoop 설정 파일 생성 후 Docker 이미지 빌드

```bash
docker build -t hadoop-single-node .  
```

## Docker 볼륨 생성

```bash
docker volume create hadoop-data 
```
- 데이터를 지속시키기 위해 Docker 볼륨을 사용하여 호스트 머신의 디렉토리와 컨테이너의 Hadoop 데이터 디렉토리를 연결
- 컨테이너가 중지되거나 다시 시작되더라도 데이터는 유지


## Docker 컨테이너 실행

```bash
docker run -it --platform linux/amd64 --name hadoop-container -p 9870:9870 -p 9864:9864 -p 8088:8088 -p 8042:8042 -v hadoop-data:/usr/local/hadoop/hdfs hadoop-single-node
```  
- 컨테이너를 실행할 때 Hadoop 데이터 디렉토리를 생성한 볼륨에 마운트
- 이를 통해 데이터가 지속적으로 저장

## 컨테이너 실행 상태 확인

```
http://localhost:9870 # NameNode
http://localhost:9864 # DataNode
http://localhost:8088 # ResourceManager
http://localhost:8042 # NodeManager 
```

## HDFS에 저장

```bash
# Docker 컨테이너 내부에 접속
docker exec -it hadoop-container bash

# HDFS에 디렉터리 생성 
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/root
```

## 파일을 HDFS에 업로드

```bash
# 컨테이너 내부에서 파일을 생성하고 HDFS에 업로드
echo "Hello Hadoop" > hello.txt
hdfs dfs -put hello.txt /user/root/
```

## HDFS에서 파일 가져오기

```bash
# 컨테이너 내부에서 HDFS에 업로드한 파일을 조회
hdfs dfs -cat /user/root/hello.txt # Hello Hadoop
```

## HDFS 웹 인터페이스 접근

```bash
웹 브라우저에서 http://localhost:9870으로 이동하여 HDFS 웹 인터페이스에 접근하여 파일 확인
```

- 기존 컨테이너 중지 및 제거

```bash
# 기존 컨테이너 중지
docker stop hadoop-container

# 기존 컨테이너 제거
docker rm hadoop-container

# 새 컨테이너 실행
docker run -it --platform linux/amd64 --name hadoop-container -p 9870:9870 -p 9864:9864 -p 8088:8088 -p 8042:8042 -v hadoop-data:/usr/local/hadoop/hdfs hadoop-single-node
```

- http://localhost:9870/에 접속이 안될  때

```bash
# 실행 중인 NameNode 및 DataNode 프로세스 중지
$HADOOP_HOME/sbin/stop-dfs.sh

# PID 파일 제거
rm /tmp/hadoop-root-namenode.pid
rm /tmp/hadoop-root-datanode.pid

# NameNode 및 DataNode 서비스 다시 시작
$HADOOP_HOME/sbin/start-dfs.s

# 포트 확인
netstat -tuln | grep 9870
```

- 컨테이너가 중지되었다가 다시 시작되더라도 HDFS에 저장된 데이터가 그대로 유지

```bash
docker exec -it hadoop-container bash

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/root

echo "Hello Hadoop" > hello.txt
hdfs dfs -put hello.txt /user/root/

hdfs dfs -cat /user/root/hello.txt # Hello Hadoop
```

