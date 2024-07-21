FROM ubuntu:22.04

RUN sed -i 's/ports.ubuntu.com/ftp.kaist.ac.kr/g' /etc/apt/sources.list
RUN apt-get update\
    && apt-get install -y openjdk-8-jdk\
    && apt-get install -y ssh\
    && apt-get install -y nano\
    && apt-get install -y net-tools\
    && apt-get install -y curl\
    && apt-get install -y sudo

ENV HADOOP_FILE_NAME=hadoop-3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV HADOOP_LOG_DIR=/var/log/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys

RUN groupadd --gid 1000 hadoop
RUN useradd --uid 1000 hadoop --gid 100 --home /opt/hadoop
RUN echo "hadoop ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN chown hadoop /opt
RUN mkdir -p /var/log/hadoop && chmod 1777 /var/log/hadoop

USER hadoop
ARG HADOOP_URL=https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
WORKDIR /opt
RUN sudo rm -rf /opt/hadoop && curl -LSs -o hadoop.tar.gz $HADOOP_URL && tar zxf hadoop.tar.gz && rm hadoop.tar.gz && mv hadoop* hadoop && rm -rf /opt/hadoop/share/doc
RUN echo export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java)))) >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
WORKDIR /opt/hadoop
COPY ./config/core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY ./config/mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
COPY ./config/yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml
COPY ./config/hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
RUN sudo chown -R hadoop:users /opt/hadoop/etc/hadoop/*

