FROM openjdk:8-jdk

# 환경 변수 설정
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_DIR /opt/hadoop/hdfs/namenode
ENV HDFS_DATANODE_DIR /opt/hadoop/hdfs/datanode

# 필요한 패키지 설치
RUN apt-get update -y && \
    apt-get install -y wget sudo curl ssh openssh-server openssh-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Hadoop 다운로드 및 설치
RUN curl -o /tmp/hadoop-$HADOOP_VERSION.tar.gz https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

RUN mkdir -p $HADOOP_HOME/logs && \
    mkdir -p $HDFS_NAMENODE_DIR && \
    mkdir -p $HDFS_DATANODE_DIR && \
    chmod -R 777 $HDFS_DATANODE_DIR && \
    chmod -R 777 $HDFS_NAMENODE_DIR

# 설정 파일 복사
COPY config/* $HADOOP_HOME/etc/hadoop/

# ssh 설정
RUN mkdir -p /root/.ssh && \
    ssh-keygen -t rsa -N '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys

COPY ssh_config /root/.ssh/config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Hadoop 환경 변수 설정
COPY hadoop-env.sh $HADOOP_HOME/etc/hadoop/

# HDFS 포맷 스크립트
COPY hadoop_entrypoint.sh /usr/local/bin/hadoop_entrypoint.sh
RUN chmod +x /usr/local/bin/hadoop_entrypoint.sh

# Port 설정
EXPOSE 9864 9870 8088 9000

# HDFS 포맷 및 SSH 서비스 시작
CMD /usr/local/bin/hadoop_entrypoint.sh