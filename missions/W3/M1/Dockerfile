FROM ubuntu:22.04
ENV HADOOP_FILE_NAME=hadoop-3.3.6
RUN apt-get update
RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y ssh
RUN apt-get install -y nano
RUN mkdir $HADOOP_FILE_NAME
# you can download hadoop in https://dlcdn.apache.org/hadoop/common/
COPY ./$HADOOP_FILE_NAME ./$HADOOP_FILE_NAME

RUN echo export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64 >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_NAMENODE_USER="root" >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_DATANODE_USER="root" >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh
RUN echo export export HDFS_SECONDARYNAMENODE_USER="root" >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh
RUN echo export export YARN_RESOURCEMANAGER_USER="root" >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh
RUN echo export export YARN_NODEMANAGER_USER="root" >> ./$HADOOP_FILE_NAME/etc/hadoop/hadoop-env.sh

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys

ENV PATH=$PATH:/$HADOOP_FILE_NAME/bin:/$HADOOP_FILE_NAME/sbin

EXPOSE 8088 9870

COPY ./config/core-site.xml ./$HADOOP_FILE_NAME/etc/hadoop/core-site.xml
COPY ./config/hdfs-site.xml ./$HADOOP_FILE_NAME/etc/hadoop/hdfs-site.xml
COPY ./config/mapred-site.xml ./$HADOOP_FILE_NAME/etc/hadoop/mapred-site.xml
COPY ./config/yarn-site.xml ./$HADOOP_FILE_NAME/etc/hadoop/yarn-site.xml
COPY ./start.sh ./start.sh
CMD ["/bin/sh","./start.sh"]

