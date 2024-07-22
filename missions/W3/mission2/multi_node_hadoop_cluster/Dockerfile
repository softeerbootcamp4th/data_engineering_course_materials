FROM ubuntu:22.04

WORKDIR /root

RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends \
        sudo \
        wget \
        openjdk-8-jdk \
        vim \
        curl \
        ssh \
        openssh-server \
        wget \
    && apt-get clean

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN export DEBIAN_FRONTEND=noninteractive && apt install python3.9 -y

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop-$HADOOP_VERSION

# install hadoop 3.3.6
RUN curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | gunzip \
  | tar -x -C /usr/local/ \
 && rm -rf ${HADOOP_HOME}/share/doc


# set environment variable
# ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 
ENV HDFS_NAMENODE_USER root
ENV HDFS_DATANODE_USER root
ENV HDFS_SECONDARYNAMENODE_USER root
ENV YARN_RESOURCEMANAGER_USER root
ENV YARN_NODEMANAGER_USER root

RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
ENV PATH=$PATH:$HADOOP_HOME/bin:/$HADOOP_HOME/sbin 

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# RUN mkdir -p ~/hdfs/namenode && \ 
#     mkdir -p ~/hdfs/datanode && \
#     mkdir $HADOOP_HOME/logs

RUN mkdir $HADOOP_HOME/logs

COPY config/* /tmp/
COPY missions /tmp/missions

RUN mv /tmp/ssh_config ~/.ssh/config && \
    # mv /tmp/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \ 
    mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    mv /tmp/slaves $HADOOP_HOME/etc/hadoop/slaves && \
    mv /tmp/start-hadoop.sh ~/start-hadoop.sh 

# RUN mv /tmp/script_config_modify.sh ~/script_config_modify.sh && \
#     mv /tmp/script_verify.sh ~/script_verify.sh && \
#     mv /tmp/modify_config.py ~/modify_config.py

RUN mv /tmp/missions ~/missions

RUN chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    chmod +x $HADOOP_HOME/sbin/start-yarn.sh && \
    chmod +x ~/start-hadoop.sh && \
    chmod +x ~/missions/mission2-b/run_wordcount.sh && \
    chmod +x ~/missions/mission2-b/script_config_modify.sh && \
    chmod +x ~/missions/mission2-b/script_verify.sh && \
    chmod +x ~/missions/mission3/mission3.sh && \
    chmod +x ~/missions/mission4/mission4.sh && \
    chmod +x ~/missions/mission5/mission5.sh && \
    chmod +x ~/missions/mission6/mission6.sh && \
    chmod +x ~/missions/mission6/download_csv.sh 
    
CMD service ssh start && ~/start-hadoop.sh
# ENTRYPOINT ["~/start-hadoop.sh"]