# Ubuntu 24.04 with Hadoop 3.3.6
FROM ubuntu:24.04

# Set environment variables
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
# Set Hadoop users
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SEONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget ssh pdsh vim rsync sudo && \
    apt-get clean

# Create Hadoop users and give them sudo privileges
RUN useradd -ms /bin/bash hdfs && \
    useradd -ms /bin/bash yarn  && \
    echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download and extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm hadoop-$HADOOP_VERSION.tar.gz

# Make Hadoop directories and give permissions for each users
RUN mkdir -p $HADOOP_HOME/logs && \
    mkdir -p $HADOOP_HOME/hdfs/namenode && \
    mkdir -p $HADOOP_HOME/hdfs/datanode && \
    mkdir -p /home/hdfs/.ssh && \
    chown -R hdfs:hdfs $HADOOP_HOME/logs /home/hdfs/.ssh $HADOOP_HOME/hdfs && \
    chmod -R 777 $HADOOP_HOME/logs && \
    mkdir -p /home/yarn/.ssh && \
    chown -R yarn:yarn /home/yarn/.ssh

# Generate SSH keys for root, hdfs, and yarn users
RUN mkdir -p /home/root/.ssh && \
    ssh-keygen -t rsa -P '' -f /home/root/.ssh/id_rsa && \
    cat /home/root/.ssh/id_rsa.pub >> /home/root/.ssh/authorized_keys && \
    chmod 0600 /home/root/.ssh/authorized_keys

USER hdfs
RUN ssh-keygen -t rsa -P '' -f /home/hdfs/.ssh/id_rsa && \
    cat /home/hdfs/.ssh/id_rsa.pub >> /home/hdfs/.ssh/authorized_keys && \
    chmod 0600 /home/hdfs/.ssh/authorized_keys

USER yarn
RUN ssh-keygen -t rsa -P '' -f /home/yarn/.ssh/id_rsa && \
    cat /home/yarn/.ssh/id_rsa.pub >> /home/yarn/.ssh/authorized_keys && \
    chmod 0600 /home/yarn/.ssh/authorized_keys

USER root
# Set JAVA_HOME in Hadoop configuration
RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Copy Hadoop configuration files
COPY configs/* $HADOOP_HOME/etc/hadoop/
# Copy scripts
COPY scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

# Expose necessary ports
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Set entrypoint script
ENTRYPOINT ["/usr/local/bin/start-hadoop.sh"]
