# 기본 이미지 설정
FROM ubuntu:20.04

# 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && \
    apt-get install -y sudo wget nano openjdk-11-jdk python3

# 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y python3-pip

# Python 패키지 설치
RUN pip3 install requests pandas jupyter
RUN pip3 install numpy matplotlib geopy pyarrow
RUN pip3 install pyspark==3.4.0

RUN apt-get update && \
    apt-get install -y openssh-server sudo rsync && \
    mkdir /var/run/sshd

# 사용자 생성 및 권한 설정
RUN adduser --disabled-password --gecos '' sparkuser && \
    usermod -aG sudo sparkuser

# sparkuser sudo 사용시 비밀번호 묻지 않음
RUN echo "sparkuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set root password
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Permit root login via SSH
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Allow password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Switch to sparkuser and set up SSH keys
USER sparkuser

RUN mkdir -p /home/sparkuser/.ssh && \
    ssh-keygen -t rsa -P "" -f /home/sparkuser/.ssh/id_rsa && \
    cat /home/sparkuser/.ssh/id_rsa.pub >> /home/sparkuser/.ssh/authorized_keys && \
    chmod 600 /home/sparkuser/.ssh/authorized_keys

# Switch back to root for further setup
USER root

# Hadoop 다운로드 및 설치
RUN mkdir -p /tmp && \
    cd /tmp && \
    wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz && \
    tar -xzvf hadoop-3.4.0.tar.gz -C /opt && \
    mkdir -p /opt/hadoop && \
    mv /opt/hadoop-3.4.0/* /opt/hadoop && \
    chown -R sparkuser:sparkuser /opt/hadoop

# Set Hadoop environment variables
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_INSTALL=/opt/hadoop
ENV HADOOP_MAPRED_HOME=/opt/hadoop
ENV HADOOP_COMMON_HOME=/opt/hadoop
ENV HADOOP_HDFS_HOME=/opt/hadoop
ENV YARN_HOME=/opt/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=/opt/hadoop/lib/native
ENV PATH=$PATH:/opt/hadoop/sbin:/opt/hadoop/bin
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${PATH}:${JAVA_HOME}/bin

# Config
COPY config/* /opt/hadoop/etc/hadoop/
RUN chown -R sparkuser:sparkuser /opt/hadoop/etc/hadoop/

# Spark 다운로드 및 설치
RUN mkdir -p /tmp && \
    cd /tmp && \
    wget https://dlcdn.apache.org/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz && \
    tar -xvzf spark-3.4.3-bin-hadoop3.tgz -C /opt && \
    mkdir -p /opt/spark && \
    mv /opt/spark-3.4.3-bin-hadoop3/* /opt/spark && \
    chown -R sparkuser:sparkuser /opt/spark

# 환경 변수 설정
RUN echo 'export SPARK_HOME=/opt/spark' >> /home/sparkuser/.bashrc && \
    echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> /home/sparkuser/.bashrc && \
    echo 'export PATH=$PATH:/home/sparkuser/.local/bin' >> /home/sparkuser/.bashrc

COPY start-spark-worker.sh /opt/spark/sbin/start-spark-worker.sh
RUN chmod +x /opt/spark/sbin/start-spark-worker.sh && \
    chown sparkuser:sparkuser /opt/spark/sbin/start-spark-worker.sh

RUN pip3 install hdfs

# 기본 사용자를 sparkuser로 설정
USER sparkuser

# 컨테이너 시작 시 download.py 실행 및 Spark 시작
CMD ["/opt/spark/sbin/start-spark-worker.sh"]