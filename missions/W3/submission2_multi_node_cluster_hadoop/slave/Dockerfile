FROM openjdk:8-jdk

# 환경 변수 설정
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin 

ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# 패키지 설치
RUN apt-get update -y && \
    apt-get install -y wget sudo curl ssh openssh-server vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# HADOOP 다운로드 및 설치
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzvf hadoop-${HADOOP_VERSION}.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# SSH 설정
RUN ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# 사용자 계정 설정
RUN adduser --disabled-password --gecos "" hadoop && \
    adduser --disabled-password --gecos "" hdfs && \
    adduser --disabled-password --gecos "" yarn && \
    usermod -aG hadoop hadoop && \
    usermod -aG sudo hdfs && \
    usermod -aG sudo yarn

# HADOOP 디렉토리 생성
RUN mkdir -p $HADOOP_HOME/hdfs/namenode && \
    mkdir -p $HADOOP_HOME/hdfs/datanode && \
    mkdir -p $HADOOP_HOME/logs && \
    mkdir -p $HADOOP_HOME/tmp && \
    chown -R hdfs:hadoop $HADOOP_HOME/hdfs && \
    chown -R hdfs:hadoop $HADOOP_HOME/logs && \
    chown -R hdfs:hadoop $HADOOP_HOME/tmp && \
    chmod -R 777 $HADOOP_HOME/logs && \
    chmod -R 777 $HADOOP_HOME/tmp

# Config 파일 복사
COPY config/* $HADOOP_HOME/etc/hadoop/
RUN chown -R hdfs:hadoop $HADOOP_HOME/etc/hadoop

# 쉘 파일 복사
COPY slave_entrypoint.sh /usr/local/bin/slave_entrypoint.sh
RUN chmod +x /usr/local/bin/slave_entrypoint.sh

# JAVA_HOME 설정
RUN echo "export JAVA_HOME=$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# 포트 설정
EXPOSE 9864 9870 9000 8042 8088 22

# 실행
CMD service ssh start && usr/local/bin/slave_entrypoint.sh