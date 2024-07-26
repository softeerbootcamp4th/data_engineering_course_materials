# Spark Standalone Cluster on Docker

## Directory

```
+ spark_standalone_cluster
    + spark_image
        - Dockerfile
        - spark-3.5.1-bin-hadoop3.tgz
        - start-spark.sh
    - docker-compose.yml
    - pi.py
    - submit.sh
```

## spark_image/Dockerfile

- 기본 설정
    - Base Image >>> ubuntu:22.04
    - Base Package
        - python3
        - jdk17 (arm64, PATH 설정 필수 !)
        - wget, vim, rsync
    - Spark >>> 3.5.1
        - 다운로드 시간을 줄이기 위해 spark-3.5.1-bin-hadoop3.tgz 를 미리 다운로드
        - opt에
        - PATH 설정 필수 !

- User 설정
    - sparkuser 생성, 비밀번호 설정, sudo 권환 설정
    - spark 디렉토리 소유 변경

- 

```Dockerfile
###
# spark_image/Dockerfile

FROM ubuntu:22.04

##### 기본 세팅
# vim, wget, openjdk17
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y vim wget openjdk-17-jdk

# rsync도 있어야한대용
RUN apt-get install -y rsync

# Python3
RUN apt-get install -y python3 python3-pip

# JAVA HOME(amd아니고 arm!)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$PATH:$JAVA_HOME/bin

# 나만의 작은 temp 디렉토리
RUN mkdir /temp

##### Spark 
# Spark -> 다운로드 시간은 사치
COPY spark-3.5.1-bin-hadoop3.tgz /temp/

# Spark 압축풀기
RUN tar -xvf /temp/spark-3.5.1-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark && \
    rm -rf /temp  # 파일 삭제 후 디렉토리 제거

# Spark Home
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

##### 사용자 설정
# sparkuser 생성 및 환경 변수 적용
RUN adduser --disabled-password --gecos '' sparkuser && \
    usermod -aG sudo sparkuser && \
    echo 'export SPARK_HOME=/opt/spark' >> /home/sparkuser/.bashrc && \
    echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> /home/sparkuser/.bashrc && \
    mkdir -p /home/sparkuser && \
    chown -R sparkuser:sparkuser /home/sparkuser /opt/spark

##### 시작
# 시작 스크립트 복사
COPY --chown=sparkuser:sparkuser start-spark.sh /opt/spark/sbin/start-spark.sh
# 실행가능파일로 변경
RUN chmod +x /opt/spark/sbin/start-spark.sh

# 유저 설정
USER sparkuser

##### RUN
CMD ["/opt/spark/sbin/start-spark.sh"]
```

## docker-compose.yml

- spark_iamge/Dockerfile 빌드한 이미지 이용
- SPARK_MASTER 환경 변수로 마스터-워커 관리
- Docker Network: spark_net

```yml
# docker-compose.yml


version: '3.7'
services:
  spark-master:
    image: spark_image 
    container_name: spark-master
    environment:
      - SPARK_MASTER=true
    ports:
      - "8080:8080"
      - "7077:7077"
    networks:
      - spark_net

  spark-worker-1:
    image: spark_image 
    container_name: spark-worker-1
    depends_on:
      - spark-master
    networks:
      - spark_net

  spark-worker-2:
    image: spark_image 
    container_name: spark-worker-2
    depends_on:
      - spark-master
    networks:
      - spark_net

networks:
  spark_net:
    driver: bridge
```

## submit.sh

```sh
#!/bin/bash

# pi.py 복사
docker cp pi.py spark-master:/opt/spark/bin/pi.py
# 소유/실행가능
docker exec -it spark-master sudo chown sparkuser:sparkuser /opt/spark/bin/pi.py
docker exec -it spark-master sudo chmod +x /opt/spark/bin/pi.py
# submit
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/bin/pi.py
```

## pi.py

```python
#!usr/bin/env/ python3
  
from pyspark.sql import SparkSession
import random

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

if __name__ == "__main__":
    spark = SparkSession.builder.appName("PythonPi").getOrCreate()
    slices = 2
    n = 100000 * slices
    count = spark.sparkContext.parallelize(range(1, n + 1), slices).filter(inside).count()
    print(f"""
          \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n           
          estimated pi => {4.0 * count / n}
          \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
          """)
    spark.stop()
```