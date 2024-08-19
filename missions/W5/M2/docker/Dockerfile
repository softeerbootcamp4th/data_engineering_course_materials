# Base image
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y vim wget unzip ssh openjdk-8-jdk python3-pip rsync sudo net-tools && \
    apt-get clean

# Create Hadoop user
RUN useradd -ms /bin/bash hadoop
RUN echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set environment variables
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-arm64
ENV SPARK_HOME /usr/local/spark
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_COMMON_LIB_NATIVE_DIR $HADOOP_HOME/lib/native
ENV PATH $PATH:$HADOOP_HOME/bin
ENV PATH $PATH:$SPARK_HOME/bin

# Download and install Hadoop
COPY /untracked/spark-3.5.1-bin-hadoop3.tgz $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz
RUN tar -zxvf $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz -C $SPARK_HOME/
RUN mv $SPARK_HOME/spark-3.5.1-bin-hadoop3/* $SPARK_HOME/
RUN rm -rf $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz
RUN mkdir -p $SPARK_HOME/data
RUN chown -R hadoop:hadoop $SPARK_HOME

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm hadoop-$HADOOP_VERSION.tar.gz && \
    chown -R hadoop:hadoop $HADOOP_HOME

# Change user
USER hadoop

# Configure SSH
RUN ssh-keygen -t rsa -P '' -f /home/hadoop/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys

# Start SSH service as root
RUN sudo service ssh start

# Set environment variables in .bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> ~/.bashrc && \
    echo "export PATH=\$PATH:\$SPARK_HOME" >> ~/.bashrc && \
    echo "export SPARK_HOME=/usr/local/spark" >> ~/.bashrc \
    echo "export HADOOP_VERSION=3.3.6" >> ~/.bashrc && \
    echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.bashrc && \
    echo "export HADOOP_INSTALL=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_MAPRED_HOME=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_COMMON_HOME=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_HDFS_HOME=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_YARN_HOME=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native" >> ~/.bashrc && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/bin" >> ~/.bashrc

# Add Hadoop configuration files
COPY ./config/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY ./config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY ./config/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY ./config/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml

# chown Hadoop configuration files
RUN sudo chown -R hadoop:hadoop $HADOOP_HOME

# Configure JAVA_HOME in Hadoop environment
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Format HDFS namenode
RUN sudo mkdir -p $HADOOP_HOME/data/namenode && \
    sudo mkdir -p $HADOOP_HOME/data/datanode && \
    sudo chown -R hadoop:hadoop $HADOOP_HOME/data && \
    $HADOOP_HOME/bin/hdfs namenode -format

COPY /start_script/start_spark.sh $SPARK_HOME/start_spark.sh
COPY /start_script/start_pi.sh $SPARK_HOME/start_pi.sh
RUN sudo chmod +x $SPARK_HOME/start_spark.sh
RUN sudo chmod +x $SPARK_HOME/start_pi.sh

# Expose ports
EXPOSE 22 9870

# 시작 명령어 설정
CMD ["/usr/local/spark/start_spark.sh"]
