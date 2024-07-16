# Use the latest Ubuntu image as the base image
FROM ubuntu:latest

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Update the package repository and install necessary packages
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget ssh pdsh vim

# Download and extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /tmp && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION /opt/hadoop && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

# Configure SSH
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -P '' && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HADOOP_HOME=${HADOOP_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    echo "export HADOOP_OPTS=\"-Djava.library.path=${HADOOP_HOME}/lib/native\"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ~/.bashrc && \
    echo "export HADOOP_HOME=${HADOOP_HOME}" >> ~/.bashrc && \
    echo "export HADOOP_OPTS=\"-Djava.library.path=${HADOOP_HOME}/lib/native\"" >> ~/.bashrc && \
    echo "export PATH=${PATH}" >> ~/.bashrc

ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

# Configure Hadoop
COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
COPY samplefile.txt /root/samplefile.txt
RUN chmod +x /usr/local/bin/start-hadoop.sh

# Expose HDFS and YARN web interfaces
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Create a directory for HDFS data that persists outside the container
VOLUME ["/hadoop/dfs"]

# Start Hadoop services when the container runs
CMD ["/usr/local/bin/start-hadoop.sh"]