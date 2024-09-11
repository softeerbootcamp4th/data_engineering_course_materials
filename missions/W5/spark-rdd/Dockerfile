FROM ubuntu:22.04

ENV HADOOP_VERSION=3.4.0
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
# Set Hadoop User
ENV HDFS_NAMENODE_USER=hdfs
ENV HDFS_DATANODE_USER=hdfs
ENV HDFS_SECONDARYNAMENODE_USER=hdfs
ENV YARN_RESOURCEMANAGER_USER=yarn
ENV YARN_NODEMANAGER_USER=yarn
# Set Spark env.
ENV SPARK_VERSION=3.5.2
ENV SPARK_HOME=/opt/spark
ENV SPARK_CONFG_DIR=$SPARK_HOME/conf
ENV MASTER=spark://hadoop-master:7077

ENV PDSH_RCMD_TYPE=ssh
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin


RUN apt-get update && \
    apt-get install -y openjdk-11-jdk python3 python3-pip ssh pdsh wget sudo && \
    apt-get clean

# Download and extract Hadoop to /opt
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz -P /opt && \
    tar -xzvf /opt/hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm /opt/hadoop-$HADOOP_VERSION.tar.gz

# Download and extract Spark to /opt
RUN wget http://apache.mirror.cdnetworks.com/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz -P /opt && \
    tar -xzvf /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop3 $SPARK_HOME && \
    rm /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz

RUN pip3 install pyspark

# 사용자 및 그룹 생성 및 권한 설정
RUN groupadd -g 1000 hadoop && \
    useradd -m -u 1001 -g 1000 hdfs && \
    useradd -m -u 1002 -g 1000 yarn && \
    useradd -m -u 1003 -g 1000 spark && \
    echo "hdfs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "yarn ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "spark ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

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

USER spark
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
    mkdir -p ~/.ssh && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

USER root
RUN mkdir -p $HADOOP_HOME/logs && mkdir -p $HADOOP_HOME/data && \
    chown -R :hadoop $HADOOP_HOME/ && \
    chown -R hdfs:hadoop $HADOOP_HOME/data && \
    chmod -R 775 $HADOOP_HOME/

RUN chown -R spark:hadoop $SPARK_HOME

RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_CONF_DIR/hadoop-env.sh
RUN echo "export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"" >> ~/.bashrc

ENTRYPOINT ["/usr/local/bin/start.sh"]