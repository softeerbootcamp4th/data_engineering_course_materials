# 베이스 이미지로 Ubuntu 20.04 사용
FROM ubuntu:20.04

# 환경 변수 설정
ENV SPARK_VERSION=3.1.2
ENV HADOOP_VERSION=3.2
ENV SPARK_HOME=/opt/spark
ENV SPARK_TGZ_URL=https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# 필수 패키지 설치 및 Spark 다운로드/설치
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk curl python3 sudo && \
    curl -L "$SPARK_TGZ_URL" -o spark.tgz && \
    mkdir -p /opt/spark && \
    tar -xzf spark.tgz -C /opt/spark --strip-components=1 && \
    rm spark.tgz && \
    apt-get clean && \
    useradd -m -d /home/spark -s /bin/bash spark && \
    echo "spark:spark" | chpasswd && adduser spark sudo && \
    mkdir -p /opt/spark/work && \
    chown -R spark:spark /opt/spark

# 환경 변수 PATH 업데이트
ENV PATH=$SPARK_HOME/bin:$PATH

# 작업 디렉토리 설정
WORKDIR /opt/spark/work

# 진입점 스크립트 복사 및 실행 권한 부여
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

# Spark 제출 스크립트 복사 및 실행 권한 부여
COPY submit.sh /opt/spark/submit.sh
RUN chmod +x /opt/spark/submit.sh

# 필요한 포트 개방
EXPOSE 8080 7077 8081 8082 4040

# spark 사용자로 변경
USER spark

# 컨테이너 시작 시 실행할 명령어
ENTRYPOINT ["/opt/entrypoint.sh"]
