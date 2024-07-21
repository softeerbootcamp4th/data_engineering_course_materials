
## **1. Docker 이미지 빌드 및 컨테이너 실행**

### 1.1. Dockerfile 작성

먼저 `Dockerfile`을 작성합니다. 

### 1.2. Docker 이미지 빌드

```python
# 마스터 노드 이미지 빌드
cd /users/admin/hadoop_m2a
docker build --platform=linux/amd64 -t namenode .

# 워커 노드 이미지 빌드
cd /users/admin/hadoop_worker
docker build --no-cache --platform=linux/amd64 -t hadoop-worker .

```

## **2. Docker Compose를 사용하여 클러스터 실행**

### 2.1. Docker Compose로 클러스터 실행

```python
# 네트워크 생성
#
docker exec -it namenode bash 
docker network create hadoop-net

# Docker Compose로 클러스터 실행
export HADOOP_HOME=/usr/local/hadoop
docker-compose up -d

#docker-compose down
```

### 2.2 클러스터 상태 확인

```python
docker exec -it namenode bash -c "/usr/local/hadoop/bin/yarn node -list"

```

```python
ResourceManager 수동 시작
docker exec -it namenode bash -c "/usr/local/hadoop/sbin/start-yarn.sh"
docker-compose down
docker-compose up -d

```

## 3. 기본적인 HDFS 작업 수행

### 3.1. **로컬 파일 시스템에서 HDFS로 파일 업로드**:

```python
docker exec -it namenode hdfs dfs -mkdir -p /user/hadoop/input

docker cp localfile.txt namenode:/tmp/localfile.txt
docker exec -it namenode hdfs dfs -put /tmp/localfile.txt /user/hadoop/input/

```

### 3.2.**HDFS 에서 파일 다운로드**:

 

```python
docker exec -it namenode hdfs dfs -ls /user/hadoop/input/
docker exec -itnamenode hdfs dfs -get /user/hadoop/input/localfile.txt /tmp/
docker cp namenode:/tmp/localfile.txt .

```

### 3.3 HDFS 작업

```python
docker exec -it namenode bash -c "/usr/local/hadoop/bin/hdfs dfs -mkdir /user"
	/usr/local/hadoop/bin/hdfs dfs -mkdir /user

docker exec -it namenode bash -c "/usr/local/hadoop/bin/hdfs dfs -mkdir /user/root"
	/usr/local/hadoop/bin/hdfs dfs -mkdir /user/root

docker exec -it namenode bash -c "echo 'Deer Bear RiverCar Car River Deer Car Bear' > /root/sample.txt"
	echo 'Deer Bear RiverCar Car River Deer Car Bear' > /root/sample_mr.txt

docker exec -it namenode bash -c "/usr/local/hadoop/bin/hdfs dfs -put /root/sample.txt /user/root/"
	/usr/local/hadoop/bin/hdfs dfs -put /root/sample_mr.txt /user/hadoop/

docker exec -it namenode bash -c "/usr/local/hadoop/bin/hdfs dfs -ls /user/root/"
	/usr/local/hadoop/bin/hdfs dfs -ls /user/hadoop/

```

### 3.4. MapReduce 작업 실행

```python

#/usr/local/hadoop/bin/hdfs dfs -mkdir /user/hadoop/output
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/hadoop/sample_mr.txt /user/hadoop/output
#hdfs dfs -rm -r /user/hadoop/output
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/hadoop/sample_mr.txt /user/hadoop/output

```

```python
hadoop fs -ls user/hadoop/output
/user/hadoop/output
hadoop fs -ls /user/hadoop/output
hadoop fs -cat /user/hadoop/output/part-r-00000
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6ec20228-be51-4a9f-a5f2-85b8c55a6714/3af2e229-9e5c-4146-b018-673758748e31/Untitled.png)

## 4. 클러스터 상태 확인

```python
docker exec -it namenode bash -c "/usr/local/hadoop/bin/hdfs dfsadmin -report"
docker exec -it namenode bash -c "/usr/local/hadoop/bin/yarn node -list"

```

## 5.  웹 인터페이스 접근

- HDFS 웹 UI: [`http://<호스트 머신 IP>:9870`](http://localhost:9870/dfshealth.html#tab-overview)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6ec20228-be51-4a9f-a5f2-85b8c55a6714/542e39a0-9c80-4247-bacb-747475e2ff54/Untitled.png)

- YARN 웹 UI: `http://<호스트 머신 IP>:8088`

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6ec20228-be51-4a9f-a5f2-85b8c55a6714/b4a0a0c3-8f05-40b3-8140-d3a5b3d9bf21/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6ec20228-be51-4a9f-a5f2-85b8c55a6714/59d1b2b1-2800-4cda-8670-ded4196c0d0e/Untitled.png)

## **6. 컨테이너 내에서 Hadoop 구성 및 서비스 시작**

### 6.1. DataNode 수동으로 시작 (필요한 경우)

DataNode가 실행되지 않으면 수동으로 시작합니다.

```
docker exec -it namenode bash -c "hdfs --daemon start datanode"

```

### 6.2. 프로세스 상태 확인

`jps` 명령어로 NameNode, DataNode, ResourceManager, NodeManager가 모두 실행 중인지 확인합니다.

```
docker exec -it namenode bash -c "jps"

```


## 8. 클러스터 구성 파일

구성파일

- `core-site.xml`: Hadoop의 기본 설정을 포함합니다. 파일 시스템 URI와 같은 공통 설정이 있습니다.
    
    ```python
    <configuration>
        <property>
            <name>fs.defaultFS</name>
            <value>hdfs://namenode:9000</value>
        </property>
    </configuration>
    
    ```
    
- `hdfs-site.xml`: HDFS 설정을 포함합니다. 복제 인수와 네임노드/데이터노드 경로 등이 있습니다.
    
    master
    
    ```python
    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>3</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:///usr/local/hadoop/hdfs/namenode</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:///usr/local/hadoop/hdfs/datanode</value>
        </property>
        <property>
            <name>dfs.namenode.datanode.registration.ip-hostname-check</name>
            <value>false</value>
        </property>
    </configuration>
    
    ```
    
    worker
    
    ```python
    <configuration>
        <property>
            <name>dfs.replication</name>
            <value>3</value>
        </property>
        <property>
            <name>dfs.namenode.http-address</name>
            <value>namenode:9870</value>
        </property>
        <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:///usr/local/hadoop/hdfs/namenode</value>
        </property>
        <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:///usr/local/hadoop/hdfs/datanode</value>
        </property>
        <property>
            <name>dfs.namenode.datanode.registration.ip-hostname-check</name>
            <value>false</value>
        </property>
    </configuration>
    
    ```
    
- `mapred-site.xml`: MapReduce 설정을 포함합니다. 작업 추적기와 맵/리듀스 환경 변수를 설정합니다.
    
    ```python
    <configuration>
        <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
        </property>
        <property>
            <name>yarn.app.mapreduce.am.env</name>
            <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
        </property>
        <property>
            <name>mapreduce.map.env</name>
            <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
        </property>
        <property>
            <name>mapreduce.reduce.env</name>
            <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
        </property>
    </configuration>
    
    ```
    
- `yarn-site.xml`: YARN 설정을 포함합니다. 리소스 매니저와 노드 매니저 설정이 있습니다.
    
    ```python
    <configuration>
        <property>
            <name>yarn.resourcemanager.hostname</name>
            <value>namenode</value>
        </property>
        <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
        </property>
        <property>
            <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
            <value>org.apache.hadoop.mapred.ShuffleHandler</value>
        </property>
    </configuration>
    
    ```