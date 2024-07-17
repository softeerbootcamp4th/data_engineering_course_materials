FROM openjdk:8-jdk

# 환경 변수 설정
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_DIR /opt/hadoop/hdfs/namenode
ENV HDFS_DATANODE_DIR /opt/hadoop/hdfs/datanode
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# 필요한 패키지 설치
RUN apt-get update -y && \
    apt-get install -y wget sudo curl ssh openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# hdfs와 yarn 사용자 생성
RUN useradd -ms /bin/bash hdfs && \
    useradd -ms /bin/bash yarn

# Hadoop 다운로드 및 설치
RUN curl -o /tmp/hadoop-$HADOOP_VERSION.tar.gz https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

# 설정 파일 복사
COPY core-site.xml $HADOOP_HOME/etc/hadoop/
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/

# ssh 설정
USER hdfs
RUN mkdir -p $HADOOP_HOME/hdfs/namenode && \
    mkdir -p $HADOOP_HOME/hdfs/datanode && \
    mkdir -p $HADOOP_HOME/logs && \
    chmod -R 777 $HADOOP_HOME/hdfs && \
    chmod -R 777 $HADOOP_HOME/logs

RUN mkdir -p /home/hdfs/.ssh && \
    ssh-keygen -t rsa -N '' -f /home/hdfs/.ssh/id_rsa && \
    cat /home/hdfs/.ssh/id_rsa.pub >> /home/hdfs/.ssh/authorized_keys && \
    chmod 0600 /home/hdfs/.ssh/authorized_keys && \
    chmod 700 /home/hdfs/.ssh

USER yarn
RUN mkdir -p /home/yarn/.ssh && \
    ssh-keygen -t rsa -N '' -f /home/yarn/.ssh/id_rsa && \
    cat /home/yarn/.ssh/id_rsa.pub >> /home/yarn/.ssh/authorized_keys && \
    chmod 0600 /home/yarn/.ssh/authorized_keys && \
    chmod 700 /home/yarn/.ssh

USER root
RUN mkdir -p /home/root/.ssh && \
    ssh-keygen -t rsa -N '' -f /home/root/.ssh/id_rsa && \
    cat /home/root/.ssh/id_rsa.pub >> /home/root/.ssh/authorized_keys && \
    chmod 0600 /home/root/.ssh/authorized_keys && \
    chmod 700 /home/root/.ssh && \
    ssh-keygen -A && \
    echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# HDFS 포맷 스크립트 & JAVA_HOME 설정
COPY format-hdfs.sh /usr/local/bin/format-hdfs.sh
RUN chmod +x /usr/local/bin/format-hdfs.sh
RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Port 설정
EXPOSE 9864 9870 8042 8088 22
EXPOSE 9866 9867 9871 10020 8020

# HDFS 포맷 및 SSH 서비스 시작
CMD service ssh start && /usr/local/bin/format-hdfs.sh
