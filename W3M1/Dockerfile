########## 베이스 이미지 및 기본 환경 설정

# 베이스 이미지 설정: Ubuntu 20.04
FROM ubuntu:20.04

# 패키지 업데이트 및 기본 도구 설치
# 맨 아래는 SSH 디렉터리 !
RUN apt-get update && apt-get install -y \
    wget curl net-tools vim openssh-server openssh-client sudo rsync && \
    mkdir /var/run/sshd

# JAVA 설치 및 환경변수 설정
RUN apt-get install -y openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${PATH}:${JAVA_HOME}/bin


########## 유저 관리 및 SSH 설정

# 루트 사용자 비밀번호 설정 및 유저 추가
RUN echo 'root:root' | chpasswd
RUN useradd -ms /bin/bash hadoopuser

# SSH 구성 변경: 루트 로그인 허용 및 패스워드 인증 활성화
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# hadoopuser 유저 sudo 권한 부여
RUN echo 'hadoopuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

##### SSH 키 설정 및 사용자 전환

# hadoopuser로 전환하여 SSH 키 설정
USER hadoopuser
RUN mkdir -p /home/hadoopuser/.ssh && \
    ssh-keygen -t rsa -P "" -f /home/hadoopuser/.ssh/id_rsa && \
    cat /home/hadoopuser/.ssh/id_rsa.pub >> /home/hadoopuser/.ssh/authorized_keys && \
    chmod 600 /home/hadoopuser/.ssh/authorized_keys

# 루트 사용자로 다시 전환
USER root


########## 네트워크 포트 및 시스템 리소스 제한 설정

# 필요한 포트들 노출
EXPOSE 22 9870 8088

# 시스템 리소스 제한 설정
RUN echo 'hadoopuser  -  nproc  65536' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  nofile  65536' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  memlock  unlimited' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  stack  8192' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  rtprio  0' >> /etc/security/limits.conf


########## Hadoop 설치 및 설정

# Hadoop 설치
COPY hadoop-3.4.0.tar.gz /temp/
RUN tar -xzvf /temp/hadoop-3.4.0.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-3.4.0 /usr/local/hadoop && \
    chown -R hadoopuser:hadoopuser /usr/local/hadoop && \
    rm /temp/hadoop-3.4.0.tar.gz

# Hadoop 구성 파일 복사 및 소유권 변경
COPY config/* /usr/local/hadoop/etc/hadoop/
RUN chown -R hadoopuser:hadoopuser /usr/local/hadoop/etc/hadoop/

# Hadoop 환경변수 설정
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_INSTALL=/usr/local/hadoop
ENV HADOOP_MAPRED_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_HOME=/usr/local/hadoop
ENV HADOOP_HDFS_HOME=/usr/local/hadoop
ENV YARN_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=/usr/local/hadoop/lib/native
ENV PATH=$PATH:/usr/local/hadoop/sbin:/usr/local/hadoop/bin

# 하둡 시작 스크립트, 엔트리포인트 스크립트 복사 및 실행 권한 부여
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh


# hadoopuser로 전환하여 JAVA_HOME 환경 설정 추가
USER hadoopuser
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh


########### RUN !!!
CMD ["/usr/local/bin/start-hadoop.sh"]


############ 이후 도커 명령

##### 0. docker volume 설정
## docker volume create <볼륨>
#### 이후 생성되는 컨테이너의 usr/local/hadoop/data에 마운트되어 영속성을 보장

##### 이미지 빌드
## docker run -v <볼륨>:/usr/local/hadoop/data -d --name <컨테이너> --ulimit nofile=65536:65536 --ulimit nproc=65536:65536 -p 9870:9870 -p 8088:8088 <이미지>
## -d : 데몬으로 실행
## --ulimit (없어도 무방)
#### nofile : 하나의 프로세스가 열 수 있는 최대 파일 디스크립터 수
#### nproc : 하나의 사용자 ID로 생성할 수 있는 최대 프로세스 수
## -p
#### 9870 : NameNode Web UI port
#### 8088 : YARN ResourceManage Web UI port

##### 컨테이너 접속
## docker exec -it <컨테이너> /bin/bash
#### bash 실행

