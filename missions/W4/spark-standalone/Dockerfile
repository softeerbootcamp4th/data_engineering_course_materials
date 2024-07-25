FROM --platform=linux/amd64 ubuntu:22.04

ENV PDSH_RCMD_TYPE=ssh
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/usr/local/spark
ENV SPARK_CONFG_DIR=$SPARK_HOME/conf
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV MASTER=spark://spark-master:7077

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk python3-pip ssh pdsh wget sudo && \
    apt-get clean

# 사용자 및 그룹 생성 및 권한 설정
RUN groupadd -g 1000 hadoop && \
    useradd -m -u 1001 -g 1000 spark && \
    echo "spark ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Download and extract Hadoop to /opt
RUN wget http://apache.mirror.cdnetworks.com/spark/spark-3.5.1/spark-$SPARK_VERSION-bin-hadoop3.tgz -P /opt && \
    tar -xzvf /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop3 $SPARK_HOME && \
    rm /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz

RUN pip3 install pyspark

RUN chown -R spark:hadoop $SPARK_HOME && \
    chmod -R 775 $SPARK_HOME

USER spark
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa && \
    mkdir -p ~/.ssh && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

WORKDIR $SPARK_CONFG_DIR
RUN cp spark-env.sh.template spark-env.sh && \
    cp spark-defaults.conf.template spark-defaults.conf

#RUN echo "export SPARK_MASTER_IP=‘192.168.80.128'" >> spark-env.sh && \
#    echo "export SPARK_MASTER_HOST=spark-master" >> spark-env.sh && \
#    echo "export SPARK_MASTER_WEBUI_PORT=7777" >> spark-env.sh && \
#    echo "export SPARK_WORKER_INSTANCES=2" >> spark-env.sh && \
#    echo "export SPARK_EXECUTOR_CORES=1" >> spark-env.sh && \
#    echo "export SPARK_EXECUTOR_MEMORY=1g" >> spark-env.sh

RUN echo "spark-master spark://spark-master:7707" >> spark-defaults.conf && \
    echo "spark.serializer org.apache.spark.serializer.KryoSerializer" >> spark-defaults.conf

#RUN echo "192.168.80.128 spark-master" >> /etc/hosts

ENV SPARK_NO_DAEMONIZE=true
WORKDIR $SPARK_HOME

CMD ["./start-master.sh"]