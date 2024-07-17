FROM openjdk:8-jdk

# HADOOP 환경 변수 추가
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

# 의존성 파일 설치
RUN apt-get update -y && \
    apt-get install -y wget sudo curl ssh openssh-server sshpass && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# HADOOP 다운로드 및 설치
RUN curl -o /tmp/hadoop-$HADOOP_VERSION.tar.gz https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt/ && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

# Config 파일 복사
COPY core-site.xml $HADOOP_HOME/etc/hadoop/
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/
COPY workers $HADOOP_HOME/etc/hadoop/

# HADOOP 디렉토리 생성
RUN mkdir -p $HADOOP_HOME/hdfs/namenode && \
    mkdir -p $HADOOP_HOME/hdfs/datanode && \
    mkdir -p $HADOOP_HOME/logs && \
    chmod -R 777 $HADOOP_HOME/hdfs && \
    chmod -R 777 $HADOOP_HOME/logs

# SSH 설정
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# 쉘 파일 복사
COPY format-hdfs.sh /usr/local/bin/format-hdfs.sh
RUN chmod +x /usr/local/bin/format-hdfs.sh

# JAVA_HOME 설정
RUN echo "export JAVA_HOME=$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# 포트 설정
EXPOSE 9864 9870 9000 8042 8088 22

# 실행
CMD service ssh start && /usr/local/bin/format-hdfs.sh