FROM ubuntu:22.04

RUN sed -i 's/ports.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list
RUN apt-get update\
    && apt-get install -y openjdk-8-jdk\
    && apt-get install -y ssh\
    && apt-get install -y nano\
    && apt-get install net-tools

ENV HADOOP_FILE_NAME=hadoop-3.3.6
# you can download hadoop in https://dlcdn.apache.org/hadoop/common/
COPY ./$HADOOP_FILE_NAME /opt/hadoop
ENV HADOOP_HOME=/opt/hadoop
RUN ln -s $HADOOP_HOME/etc/hadoop /etc/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop
RUN mkdir $HADOOP_HOME/dfs
# RUN rm -rf $HADOOP_HOME/share/doc
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN echo export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java)))) >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
ENV HDFS_NAMENODE_USER="root"
ENV HDFS_DATANODE_USER="root"
ENV HDFS_SECONDARYNAMENODE_USER="root"
ENV YARN_RESOURCEMANAGER_USER="root"
ENV YARN_NODEMANAGER_USER="root"

COPY ./config/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY ./config/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY ./config/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys
