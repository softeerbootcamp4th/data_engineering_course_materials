# 기본 이미지 설정
FROM ubuntu:20.04

# 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y sudo wget nano openjdk-11-jdk python3

# 사용자 생성 및 권한 설정
RUN adduser --disabled-password --gecos '' sparkuser && \
    usermod -aG sudo sparkuser

# Spark 다운로드 및 설치
RUN mkdir -p /tmp && \
    cd /tmp && \
    wget https://dlcdn.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz && \
    tar -xvzf spark-3.4.3-bin-hadoop3.tgz -C /opt && \
    mkdir -p /opt/spark && \
    mv /opt/spark-3.4.3-bin-hadoop3/* /opt/spark && \
    chown -R sparkuser:sparkuser /opt/spark

# 환경 변수 설정
RUN echo 'export SPARK_HOME=/opt/spark' >> /home/sparkuser/.bashrc && \
    echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> /home/sparkuser/.bashrc

COPY pi.py /opt/spark/scripts/pi.py

# start-worker-custom.sh 스크립트 복사 및 권한 설정
COPY start-spark.sh /opt/spark/sbin/start-spark.sh
RUN chmod +x /opt/spark/sbin/start-spark.sh && \
    chown sparkuser:sparkuser /opt/spark/sbin/start-spark.sh

# 기본 사용자를 sparkuser로 설정
USER sparkuser

CMD ["/opt/spark/sbin/start-spark.sh"]