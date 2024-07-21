# 기본 이미지로 Ubuntu 사용 (특정 플랫폼 지정)
FROM --platform=linux/amd64 ubuntu:latest

# 환경 변수 설정
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR $HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_LOG_DIR /usr/local/hadoop/logs
ENV YARN_LOG_DIR /usr/local/hadoop/logs

# 필요한 패키지 설치 및 하둡 다운로드, 압축 해제
RUN apt-get update && \
    apt-get install -y ssh rsync openjdk-8-jdk wget vim net-tools && \
    wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION /usr/local/hadoop && \
    rm hadoop-$HADOOP_VERSION.tar.gz && \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    mkdir -p /usr/local/hadoop/logs && \
    mkdir -p /usr/local/hadoop/hdfs/namenode && \
    mkdir -p /usr/local/hadoop/hdfs/datanode && \
    rm -rf /var/lib/apt/lists/*

# 설정 파일 복사
COPY core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml
COPY hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Start scripts 복사
COPY start-dfs.sh $HADOOP_HOME/sbin/start-dfs.sh
COPY start-yarn.sh $HADOOP_HOME/sbin/start-yarn.sh

# 스크립트 실행 권한 부여
RUN chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh

# DataNode, NodeManager를 위한 포트 노출
EXPOSE 9870 9864 8088 8042 22

# CMD 수정
CMD ["/bin/bash", "-c", "service ssh start && $HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh && bash"]