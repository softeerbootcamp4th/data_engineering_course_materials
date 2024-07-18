# Ubuntu 24.04 with Hadoop 3.3.6
FROM ubuntu:24.04

# Set environment variables
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
# Set Hadoop users
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget ssh pdsh vim sudo && \
    apt-get clean

# Create Hadoop users and give them sudo privileges
RUN useradd -ms /bin/bash hdfs && \
    useradd -ms /bin/bash yarn  && \
    echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download and extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /tmp && \
    tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

# Copy Hadoop configuration files
COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml

# Make Hadoop directories and give permissions for each users
RUN mkdir -p $HADOOP_HOME/logs && \
    mkdir -p /hadoop/dfs/namenode && \
    mkdir -p /hadoop/dfs/datanode && \
    mkdir -p /home/hdfs/.ssh && \
    chown -R hdfs:hdfs /opt/hadoop/logs /home/hdfs/.ssh /hadoop/dfs && \
    chmod -R 777 $HADOOP_HOME/logs /hadoop/dfs && \
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

# Set the JAVA_HOME environment variable in Hadoop configuration files
USER root
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Copy the start-hadoop.sh script and a sample file
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
COPY samplefile.txt /root/samplefile.txt
RUN chmod +x /usr/local/bin/start-hadoop.sh

# Expose Hadoop ports
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Create a volume for Hadoop data
VOLUME ["/hadoop/dfs"]

# Start Hadoop
CMD ["/usr/local/bin/start-hadoop.sh"]