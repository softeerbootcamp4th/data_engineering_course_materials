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
