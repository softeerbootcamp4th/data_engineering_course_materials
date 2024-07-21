# 기본 이미지로 Ubuntu 사용
FROM ubuntu:20.04

# 필수 패키지 설치
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        openjdk-8-jdk \
        wget \
        curl \
        ssh \
        sudo \
        rsync \
    && apt-get clean

# JAVA_HOME 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_HOME=/home/hduser/hadoop-3.3.3
ENV PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# 사용자 생성 및 설정
RUN useradd -m hduser \
    && echo "hduser:supergroup" | chpasswd \
    && adduser hduser sudo \
    && echo "hduser     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 작업 디렉토리 설정
WORKDIR /home/hduser

# .ssh 디렉토리 생성 및 SSH 키 생성
RUN mkdir -p /home/hduser/.ssh \
    && ssh-keygen -t rsa -P '' -f /home/hduser/.ssh/id_rsa \
    && cat /home/hduser/.ssh/id_rsa.pub >> /home/hduser/.ssh/authorized_keys \
    && chmod 0600 /home/hduser/.ssh/authorized_keys \
    && chown -R hduser:hduser /home/hduser/.ssh

# Hadoop 설치
ENV HADOOP_VERSION=3.3.3

# wget을 사용하여 Hadoop 다운로드 및 설치
RUN wget "https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
    && tar -xzvf hadoop-$HADOOP_VERSION.tar.gz -C /home/hduser/ \
    && rm -rf /home/hduser/hadoop-$HADOOP_VERSION.tar.gz

# 로그 디렉토리 생성 및 권한 설정
RUN mkdir -p $HADOOP_HOME/logs \
    && chown -R hduser:hduser $HADOOP_HOME

# 환경 변수 설정
ENV HDFS_NAMENODE_USER=hduser
ENV HDFS_DATANODE_USER=hduser
ENV HDFS_SECONDARYNAMENODE_USER=hduser
ENV YARN_RESOURCEMANAGER_USER=hduser
ENV YARN_NODEMANAGER_USER=hduser

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Hadoop 설정 파일 복사
COPY core-site.xml $HADOOP_HOME/etc/hadoop/
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/

# docker-entrypoint.sh 복사 및 실행 권한 부여
COPY docker-entrypoint.sh $HADOOP_HOME/etc/hadoop/
RUN chmod +x $HADOOP_HOME/etc/hadoop/docker-entrypoint.sh

# 데이터 디렉토리를 볼륨으로 설정
VOLUME /home/hduser/hadoop-3.3.3/data

# 데이터 디렉토리 생성 및 권한 설정
RUN mkdir -p /home/hduser/hadoop-3.3.3/data/namenode /home/hduser/hadoop-3.3.3/data/datanode \
    && chown -R hduser:hduser /home/hduser/hadoop-3.3.3/data

# SSHD 실행 디렉토리 생성
USER root
RUN mkdir -p /run/sshd

# 포트 노출
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# 작업 디렉토리 설정 및 심볼릭 링크 생성
WORKDIR /usr/local/bin
RUN ln -s ${HADOOP_HOME}/etc/hadoop/docker-entrypoint.sh .

WORKDIR /home/hduser
# 사용자 변경
USER hduser

# YARNSTART=0 환경 변수 설정
ENV YARNSTART=0

# 엔트리포인트 설정
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# 네임노드와 데이터노드 프로세스 우선순위 설정 제거
RUN sed -i 's/sudo -u ${HDFS_NAMENODE_USER} nice -n 0 //g' $HADOOP_HOME/sbin/hadoop-daemon.sh
RUN sed -i 's/sudo -u ${HDFS_DATANODE_USER} nice -n 0 //g' $HADOOP_HOME/sbin/hadoop-daemon.sh
