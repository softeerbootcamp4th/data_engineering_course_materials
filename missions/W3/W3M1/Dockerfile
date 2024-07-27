# Using Ubuntu 24.04 Base Image
FROM ubuntu:24.04

# Setting Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Setting Users
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

# Install Packages
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk wget ssh pdsh vim sudo curl
RUN apt-get clean


# Create Hadoop Users
RUN useradd -ms /bin/bash hdfs
RUN useradd -ms /bin/bash yarn
RUN echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download and Extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /tmp
RUN tar -xzvf /tmp/hadoop-$HADOOP_VERSION.tar.gz -C /opt
RUN mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME
RUN rm /tmp/hadoop-$HADOOP_VERSION.tar.gz

# Copy Hadoop configuration files
COPY config/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY config/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
COPY config/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
COPY config/start-hadoop.sh /usr/local/bin/start-hadoop.sh
COPY config/hello-hadoop.txt /root/hello-hadoop.txt

RUN chmod +x /usr/local/bin/start-hadoop.sh

# Make Hadoop directories and give permissions for each users
RUN mkdir -p $HADOOP_HOME/logs
RUN mkdir -p /hadoop/dfs/namenode
RUN mkdir -p /hadoop/dfs/datanode
RUN mkdir -p /home/hdfs/.ssh
RUN mkdir -p /home/yarn/.ssh
RUN chown -R hdfs:hdfs /opt/hadoop/logs /home/hdfs/.ssh /hadoop/dfs
RUN chmod -R 777 $HADOOP_HOME/logs /hadoop/dfs
RUN chown -R yarn:yarn /home/yarn/.ssh

# Generate SSH keys
RUN mkdir -p /home/root/.ssh
RUN ssh-keygen -t rsa -P '' -f /home/root/.ssh/id_rsa
RUN cat /home/root/.ssh/id_rsa.pub >> /home/root/.ssh/authorized_keys
RUN chmod 0600 /home/root/.ssh/authorized_keys

USER hdfs
RUN ssh-keygen -t rsa -P '' -f /home/hdfs/.ssh/id_rsa
RUN cat /home/hdfs/.ssh/id_rsa.pub >> /home/hdfs/.ssh/authorized_keys
RUN chmod 0600 /home/hdfs/.ssh/authorized_keys

USER yarn
RUN ssh-keygen -t rsa -P '' -f /home/yarn/.ssh/id_rsa
RUN cat /home/yarn/.ssh/id_rsa.pub >> /home/yarn/.ssh/authorized_keys
RUN chmod 0600 /home/yarn/.ssh/authorized_keys

# Setting JAVA_HOME environment variable in Hadoop configuration files
USER root
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Expose Hadoop ports
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Create a volume for Hadoop data
VOLUME ["/hadoop/dfs"]

# Start Hadoop
CMD ["/usr/local/bin/start-hadoop.sh"]