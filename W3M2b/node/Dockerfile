# Hadoop Multi-node Cluster
# Master Node

########## 기본 설정
##### ubuntu:20.04 + 기본 패키지 + openjdk 11 까지 설치된 베이스 이미지
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    wget curl net-tools vim openssh-server openssh-client sudo rsync -y && \
    mkdir /var/run/sshd

# Python 설치
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip

# JAVA 설치 및 환경변수 설정
RUN apt-get install -y openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${PATH}:${JAVA_HOME}/bin


# 하둡 설치 파일 압축 해제
# usr/local/hadoop
COPY hadoop-3.3.6.tar.gz /temp/
RUN tar -xzvf /temp/hadoop-3.3.6.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-3.3.6 /usr/local/hadoop && \
    rm /temp/hadoop-3.3.6.tar.gz

# 하둡 설정 파일 COPY
# usr/local/hadoop/etc/hadoop
COPY config/* /usr/local/hadoop/etc/hadoop/

# 하둡 환경 변수 설정
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_INSTALL=/usr/local/hadoop
ENV HADOOP_MAPRED_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_HOME=/usr/local/hadoop
ENV HADOOP_HDFS_HOME=/usr/local/hadoop
ENV YARN_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=/usr/local/hadoop/lib/native
ENV PATH=$PATH:/usr/local/hadoop/sbin:/usr/local/hadoop/bin
# 자바 환경 변수도 넣어줌
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh


########## 사용자 설정

# root 계정 설정, hadoopuser 추가 및 sudo 권한 부여
RUN echo 'root:root' | chpasswd
RUN useradd -m -s /bin/bash hadoopuser && \
    echo "hadoopuser:hadoopuser" | chpasswd && \
    adduser hadoopuser sudo

# hadoopuser -> 비밀번호 없이 sudo 명령을 실행할 수 있도록
RUN echo 'hadoopuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# SSH 설정
RUN mkdir /home/hadoopuser/.ssh && \
    chmod 700 /home/hadoopuser/.ssh && \
    ssh-keygen -t rsa -P '' -f /home/hadoopuser/.ssh/id_rsa && \
    cat /home/hadoopuser/.ssh/id_rsa.pub >> /home/hadoopuser/.ssh/authorized_keys && \
    chmod 600 /home/hadoopuser/.ssh/authorized_keys && \
    chown -R hadoopuser:hadoopuser /home/hadoopuser/.ssh

# SSH 구성 변경: 루트 로그인 허용 및 패스워드 인증 활성화
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo "AllowUsers hadoopuser" >> /etc/ssh/sshd_config

# 포트 노출
EXPOSE 22 9870 8088
# 하둡 디렉토리 및 파일의 소유권을 hadoopuser로 변경
RUN chown -R hadoopuser:hadoopuser /usr/local/hadoop

# 시작 스크립트
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh

USER hadoopuser

CMD ["/usr/local/bin/start-hadoop.sh"]
