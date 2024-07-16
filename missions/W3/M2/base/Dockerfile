FROM ubuntu:22.04

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
ENV YARN_CONF_DIR=$HADOOP_CONF_DIR
## TODO:  cpu 아키텍처에 따라 arm64, amd64
RUN echo export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64 >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_NAMENODE_USER="root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_DATANODE_USER="root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_SECONDARYNAMENODE_USER="root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo export export YARN_RESOURCEMANAGER_USER="root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo export export YARN_NODEMANAGER_USER="root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

COPY ./config/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY ./config/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY ./config/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys
