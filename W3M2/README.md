# Hadoop Multi-node Cluster with Docker

## Image Build + Container Execution

### Directory

```
+ hadoop_multi_node_cluster
    - docker-compose.yml
    + masternode
        - Dockerfile
        - start-hadoop.sh
        + master_config
            - core-site.xml
            - hdfs-site.xml
            - yarn-site.xml
            - mapred-site.xml
    + workernode
        - Dockerfile
        - start-hadoop.sh
        + worker_config
            - core-site.xml
            - hdfs-site.xml
            - yarn-site.xml
            - mapred-site.xml
```

- masternode와 workernode의 Dockerfile 구성은 기본적으로 동일
- config도 동일해도 됨.
- start-hadoop.sh에서 차이가 있음

#### Dockerfile

```dockerfile
# Hadoop Multi-node Cluster
# Master Node, Workernode

########## 기본 설정
##### ubuntu:20.04 + 기본 패키지 + openjdk 11 까지 설치된 베이스 이미지
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    wget curl net-tools vim openssh-server openssh-client sudo rsync && \
    mkdir /var/run/sshd

# JAVA 설치 및 환경변수 설정
RUN apt-get install -y openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${PATH}:${JAVA_HOME}/bin


# 하둡 설치 파일 압축 해제
# usr/local/hadoop
COPY hadoop-3.3.6.tar.gz /temp/
RUN tar -xzvf /temp/hadoop-3.3.6.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-3.3.6 /usr/local/hadoop && \
    rm /temp/hadoop-3.3.6.tar.gz

# 하둡 설정 파일 COPY
# usr/local/hadoop/etc/hadoop
COPY masternode_config/* /usr/local/hadoop/etc/hadoop/

# 하둡 환경 변수 설정
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_INSTALL=/usr/local/hadoop
ENV HADOOP_MAPRED_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_HOME=/usr/local/hadoop
ENV HADOOP_HDFS_HOME=/usr/local/hadoop
ENV YARN_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=/usr/local/hadoop/lib/native
ENV PATH=$PATH:/usr/local/hadoop/sbin:/usr/local/hadoop/bin
# 자바 환경 변수도 넣어줌
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh


########## 사용자 설정

# root 계정 설정, hadoopuser 추가 및 sudo 권한 부여
RUN echo 'root:root' | chpasswd
RUN useradd -m -s /bin/bash hadoopuser && \
    echo "hadoopuser:hadoopuser" | chpasswd && \
    adduser hadoopuser sudo

# hadoopuser -> 비밀번호 없이 sudo 명령을 실행할 수 있도록
RUN echo 'hadoopuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# SSH 설정
RUN mkdir /home/hadoopuser/.ssh && \
    chmod 700 /home/hadoopuser/.ssh && \
    ssh-keygen -t rsa -P '' -f /home/hadoopuser/.ssh/id_rsa && \
    cat /home/hadoopuser/.ssh/id_rsa.pub >> /home/hadoopuser/.ssh/authorized_keys && \
    chmod 600 /home/hadoopuser/.ssh/authorized_keys && \
    chown -R hadoopuser:hadoopuser /home/hadoopuser/.ssh

# SSH 구성 변경: 루트 로그인 허용 및 패스워드 인증 활성화
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo "AllowUsers hadoopuser" >> /etc/ssh/sshd_config

# 포트 노출
EXPOSE 22 9870 8088
# 하둡 디렉토리 및 파일의 소유권을 hadoopuser로 변경
RUN chown -R hadoopuser:hadoopuser /usr/local/hadoop

# 시작 스크립트
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh

USER hadoopuser

CMD ["/usr/local/bin/start-hadoop.sh"]
```

#### core-site.xml

```xml
<!--core-site.xml-->
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-master:9000/</value>
    </property>
</configuration>
```

#### hdfs-site.xml

```xml
<!--hdfs-site.xml-->

<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///usr/local/hadoop/data/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///usr/local/hadoop/data/datanode</value>
    </property>
</configuration>
```

#### mapred-site.xml

```xml
<!--mapred-site.xml-->

<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
  </property>
</configuration>
```

#### yarn-site.xml

```xml
<!--yarn-site.xml-->
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop-master</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>2</value>
    </property>
</configuration>
```

#### start-hadoop.sh

- 마스터노드와 워커노드는 서로 다른 역할을 수행

##### masternode

- namenode
- secondarynamenode
- resourcemanager

```sh
#!/bin/bash

# Start SSH service as root
sudo service ssh start

# Check if Namenode directory is empty
if [ ! "$(ls -A /usr/local/hadoop/data/namenode)" ]; then
  echo "Namenode directory is empty, formatting..."
  hdfs namenode -format
fi

# Start Hadoop services as hadoopuser
hdfs --daemon start namenode
hdfs --daemon start secondarynamenode
yarn --daemon start resourcemanager


# Keep the container running
tail -f /dev/null
```

##### workernode

- datanode
- nodemanager

```sh
#!/bin/bash

# Start SSH service as root
sudo service ssh start


# Start Hadoop services as hadoopuser
hdfs --daemon start datanode
yarn --daemon start nodemanager

# Keep the container running
tail -f /dev/null
```
#### docker-compose.yml

- docker volume, docker network 포함
- docker network create hadoop_net 선행 필요

```yml
version: '3'
services:
  master:
    image: masternode_image
    container_name: hadoop-master
    networks:
      - hadoop_net
    ports:
      - "2222:22"
      - "9870:9870"
      - "8088:8088"
    volumes:
      - master-data:/usr/local/hadoop/dlawork9888
    environment:
      - HADOOP_MASTER=true

  worker1:
    image: workernode_image
    container_name: hadoop-worker1
    networks:
      - hadoop_net
    volumes:
      - worker1-data:/usr/local/hadoop/dlawork9888
    environment:
      - HADOOP_MASTER=false

  worker2:
    image: workernode_image
    container_name: hadoop-worker2
    networks:
      - hadoop_net
    volumes:
      - worker2-data:/usr/local/hadoop/dlawork9888
    environment:
      - HADOOP_MASTER=false

  worker3:
    image: workernode_image
    container_name: hadoop-worker3
    networks:
      - hadoop_net
    volumes:
      - worker3-data:/usr/local/hadoop/dlawork9888
    environment:
      - HADOOP_MASTER=false

networks:
  hadoop_net:
    driver: bridge

volumes:
  master-data:
  worker1-data:
  worker2-data:
  worker3-data:

```


### Docker Commands

#### Image Build

```sh
# masternode
docker build -t masternode_image .

# workernode
docker build -t workernode_image .
```

#### Docker Compose

```sh
docker compose up -d
```

## Examples

```sh
# 마스터노드 접속
docker exec -it hadoop-master bash

# 하둡 프로세스 확인
jps

# HDFS 디렉토리 생성
hdfs dfs -mkdir -p tempdir

# HDFS 디렉토리 확인
hdfs dfs -ls    

# 로컬 디렉토리에 temp/sample.txt 생성
echo -e "Hello Hadoop\nHello Docker\nHello MapReduce" | sudo tee /temp/sample.txt

# 생성한 파일을 tempdir에 hdfs dfs -put
hdfs dfs -put temp/sample.txt tempdir

# 파일 확인
hdfs dfs -ls tempdir/

# MapReduce 결과 반환 디렉토리 생성 -> 반환할 폴더가 이미 있으면 안됨.
# hdfs dfs -mkdir tempdir_output

# MapReduce(example 사용)
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount tempdir tempdir_output

# 결과 확인
hdfs dfs -cat tempdir_output/part-r-00000

# 결과
#Docker	1
#Hadoop	1
#Hello	3
#MapReduce	1
```


