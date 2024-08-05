FROM ubuntu:22.04

ENV PDSH_RCMD_TYPE=ssh
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
# Set Hadoop ENV
ENV HADOOP_VERSION=3.4.0
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin
# Set Hadoop User
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk ssh pdsh wget sudo && \
    apt-get clean

# Download and extract Hadoop to /opt
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /opt && \
    tar -xzvf /opt/hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /opt/hadoop-$HADOOP_VERSION.tar.gz

RUN apt-get install -y sshpass vim && \
    sudo apt-get install -y jq && \
    wget https://github.com/mikefarah/yq/releases/download/v4.16.1/yq_linux_amd64 -O /usr/bin/yq && \
    chmod +x /usr/bin/yq

# 사용자 및 그룹 생성 및 권한 설정
RUN groupadd -g 1000 hadoop && \
    useradd -m -u 1001 -g 1000 hdfs && \
    useradd -m -u 1002 -g 1000 yarn && \
    echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER hdfs
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
    mkdir -p ~/.ssh && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

USER yarn
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
    mkdir -p ~/.ssh && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

USER root
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
    mkdir -p ~/.ssh && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

RUN mkdir -p $HADOOP_HOME/logs && mkdir -p $HADOOP_HOME/dfs && \
    chown -R :hadoop $HADOOP_HOME/ && \
    chmod -R 775 $HADOOP_HOME/

RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_CONF_DIR/hadoop-env.sh

COPY configs/* $HADOOP_CONF_DIR/
COPY scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

WORKDIR $HADOOP_HOME

ENTRYPOINT ["/usr/local/bin/start.sh"]