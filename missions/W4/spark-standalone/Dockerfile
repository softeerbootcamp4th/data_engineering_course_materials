FROM ubuntu:22.04

ENV PDSH_RCMD_TYPE=ssh
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/opt/spark
ENV SPARK_CONFG_DIR=$SPARK_HOME/conf
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin:$JAVA_HOME/bin
ENV MASTER=spark://spark-master:7077

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk python3 python3-pip ssh pdsh wget sudo && \
    apt-get clean

# Download and extract Hadoop to /opt
RUN wget http://apache.mirror.cdnetworks.com/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz -P /opt && \
    tar -xzvf /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop3 $SPARK_HOME && \
    rm /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz

# RUN pip3 install pyspark

# 사용자 및 그룹 생성 및 권한 설정
RUN groupadd -g 1000 hadoop && \
    useradd -m -u 1001 -g 1000 spark && \
    echo "spark ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chown -R spark:hadoop $SPARK_HOME

#RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
#    mkdir -p ~/.ssh && \
#    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
#    chmod 0600 ~/.ssh/authorized_keys

ENV SPARK_NO_DAEMONIZE=true
USER spark

CMD ["you must override this"]