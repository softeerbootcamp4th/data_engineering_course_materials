# Ubuntu 24.04 Base Image
FROM ubuntu:24.04

# Setting Environment Variables
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Set Hadoop Users
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SEONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# Install Necessary Packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk wget ssh pdsh vim rsync sudo
RUN apt-get clean

# Create Hadoop Users
RUN useradd -ms /bin/bash hdfs
RUN useradd -ms /bin/bash yarn 
RUN echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download and Extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
RUN tar -xzvf hadoop-$HADOOP_VERSION.tar.gz
RUN mv hadoop-$HADOOP_VERSION $HADOOP_HOME
RUN rm hadoop-$HADOOP_VERSION.tar.gz

# Make Hadoop Directories
RUN mkdir -p $HADOOP_HOME/logs
RUN mkdir -p $HADOOP_HOME/hdfs/namenode
RUN mkdir -p $HADOOP_HOME/hdfs/datanode
RUN mkdir -p /home/hdfs/.ssh
RUN chown -R hdfs:hdfs $HADOOP_HOME/logs /home/hdfs/.ssh $HADOOP_HOME/hdfs
RUN chmod -R 777 $HADOOP_HOME/logs
RUN mkdir -p /home/yarn/.ssh
RUN chown -R yarn:yarn /home/yarn/.ssh

# Generate SSH Keys
RUN mkdir -p /root/.ssh
RUN ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
RUN chmod 0600 /root/.ssh/authorized_keys

USER hdfs
RUN ssh-keygen -t rsa -P '' -f /home/hdfs/.ssh/id_rsa
RUN cat /home/hdfs/.ssh/id_rsa.pub >> /home/hdfs/.ssh/authorized_keys
RUN chmod 0600 /home/hdfs/.ssh/authorized_keys

USER yarn
RUN ssh-keygen -t rsa -P '' -f /home/yarn/.ssh/id_rsa
RUN cat /home/yarn/.ssh/id_rsa.pub >> /home/yarn/.ssh/authorized_keys
RUN chmod 0600 /home/yarn/.ssh/authorized_keys

USER root
# Set JAVA_HOME in Hadoop configuration
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Set environment variables for hdfs and root users
RUN echo "export HADOOP_HOME=/usr/local/hadoop" >> /home/hdfs/.bashrc
RUN echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> /home/hdfs/.bashrc

RUN echo "export HADOOP_HOME=/usr/local/hadoop" >> /root/.bashrc
RUN echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> /root/.bashrc

# Copy Files
COPY configs/* $HADOOP_HOME/etc/hadoop/
COPY new_configs/* $HADOOP_HOME/etc/hadoop/
COPY scripts/* /usr/local/bin/
COPY mapreduce_example.txt /home/hdfs/mapreduce_example.txt
RUN chmod +x /usr/local/bin/*.sh

# Expose necessary ports
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Set entrypoint script
ENTRYPOINT ["/usr/local/bin/start-hadoop.sh"]
