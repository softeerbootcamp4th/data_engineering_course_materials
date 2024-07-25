# 기본 이미지로 Ubuntu 사용 (특정 플랫폼 지정)
ARG PLATFORM=linux/amd64
FROM --platform=${PLATFORM} ubuntu:latest

# 환경 변수 설정
ENV SPARK_VERSION=3.4.3
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$SPARK_HOME/bin:$PATH
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# 필요한 패키지 설치 및 Spark 다운로드, 압축 해제
RUN apt-get update && \
    apt-get install -y wget openjdk-8-jdk-headless vim net-tools python3 python3-pip python3-venv curl && \
    mkdir -p /local && \
    wget https://archive.apache.org/dist/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz -O /local/spark.tgz && \
    tar -xzvf /local/spark.tgz -C /usr/local/ && \
    mv /usr/local/spark-$SPARK_VERSION-bin-hadoop3 $SPARK_HOME && \
    rm /local/spark.tgz && \
    mkdir -p /usr/local/spark/logs && \
    mkdir -p /usr/local/spark/history && \
    mkdir -p /data/spark-events && \
    rm -rf /var/lib/apt/lists/*

# 가상 환경 생성 및 pyspark 설치
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pyspark --timeout=120

# 가상 환경 활성화 스크립트
ENV PATH="/opt/venv/bin:$PATH"

# 작업 디렉토리 및 스크립트 복사
RUN mkdir -p $SPARK_HOME/examples/test
RUN mkdir -p /usr/local/spark/work-dir

# Start scripts 및 스크립트 복사 및 실행 권한 부여
COPY pi.py /usr/local/spark/work-dir/pi.py
COPY entrypoint.sh $SPARK_HOME/entrypoint.sh
COPY start-spark.sh /usr/local/spark/sbin/start-spark.sh
COPY submit-pi-job.sh /usr/local/spark/sbin/submit-pi-job.sh

RUN chmod +x $SPARK_HOME/entrypoint.sh
RUN chmod +x /usr/local/spark/sbin/start-spark.sh
RUN chmod +x /usr/local/spark/sbin/submit-pi-job.sh
RUN chmod 755 /data/spark-events

# 포트 노출
EXPOSE 8080 7077 8081 18080

# 포맷 작업을 컨테이너 시작 시 수행하도록 CMD 수정
CMD ["bash", "-c", "/usr/local/spark/sbin/start-spark.sh && $SPARK_HOME/entrypoint.sh"]
