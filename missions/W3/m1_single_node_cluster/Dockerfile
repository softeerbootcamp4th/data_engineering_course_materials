# 베이스 이미지로 Ubuntu 22.04 사용
FROM ubuntu:22.04

# 필요 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    openjdk-8-jdk \
    ssh \
    sudo \
    && apt-get clean

# 사용자 생성 및 설정
RUN useradd -ms /bin/bash hadoopuser \
    && echo "hadoopuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Hadoop 다운로드 및 설치
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xzvf hadoop-${HADOOP_VERSION}.tar.gz -C /usr/local/ \
    && mv /usr/local/hadoop-${HADOOP_VERSION} /usr/local/hadoop \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && chown -R hadoopuser:hadoopuser /usr/local/hadoop

# SSH 설정 (Hadoop은 SSH를 사용하여 노드 간 통신)
USER hadoopuser
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 0600 ~/.ssh/authorized_keys

# Hadoop 환경 설정 파일 복사
COPY --chown=hadoopuser:hadoopuser config/* $HADOOP_HOME/etc/hadoop/

# 포트 노출
EXPOSE 9870 8088 9864 9866

# HDFS 포맷
RUN $HADOOP_HOME/bin/hdfs namenode -format

# Hadoop 시작 스크립트 복사 및 실행 권한 설정
COPY --chown=hadoopuser:hadoopuser start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh

# .bashrc에 시작 스크립트 추가
RUN echo "/usr/local/bin/start-hadoop.sh" >> /home/hadoopuser/.bashrc

# 기본 명령어 설정
CMD ["bash"]
