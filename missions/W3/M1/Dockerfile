# Base image
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget ssh rsync sudo && \
    apt-get clean

# Create Hadoop user
RUN useradd -ms /bin/bash hadoop
RUN echo "hadoop ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# # Set environment variables
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR $HADOOP_HOME/lib/native
ENV PATH $PATH:$HADOOP_HOME/bin

# Download and install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm hadoop-$HADOOP_VERSION.tar.gz && \
    chown -R hadoop:hadoop $HADOOP_HOME

# Configure SSH
USER hadoop

RUN ssh-keygen -t rsa -P '' -f /home/hadoop/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys

# Set environment variables in .bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64" >> ~/.bashrc && \
    echo "export HADOOP_VERSION=3.3.6" >> ~/.bashrc && \
    echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.bashrc && \
    echo "export HADOOP_INSTALL=\$HADOOP_HOME" >> ~/.bashrc && \
    echo "export HADOOP_MAPRED_HOME=\$HADOOP_HOME" ~/.bashrc && \
    echo "export HADOOP_COMMON_HOME=\$HADOOP_HOME" ~/.bashrc && \
    echo "export HADOOP_HDFS_HOME=\$HADOOP_HOME" ~/.bashrc && \
    echo "export HADOOP_YARN_HOME=\$HADOOP_HOME" ~/.bashrc && \
    echo "export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native" >> ~/.bashrc && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/bin" >> ~/.bashrc

# Add Hadoop configuration files
COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml

# Configure JAVA_HOME in Hadoop environment
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Format HDFS namenode
RUN sudo mkdir -p /usr/local/hadoop/data/namenode && \
    sudo mkdir -p /usr/local/hadoop/data/datanode && \
    sudo chown -R hadoop:hadoop /usr/local/hadoop/data && \
    $HADOOP_HOME/bin/hdfs namenode -format

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh

# Expose ports
EXPOSE 22 9870 8088 9864

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
