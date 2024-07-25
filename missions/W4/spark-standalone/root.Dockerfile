FROM --platform=linux/amd64 ubuntu:22.04

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/usr/local/spark
ENV SPARK_CONFG_DIR=$SPARK_HOME/conf
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV MASTER=spark://spark-master:7077

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk python3-pip wget sudo && \
    apt-get clean

# Download and extract Hadoop to /opt
RUN wget http://apache.mirror.cdnetworks.com/spark/spark-3.5.1/spark-$SPARK_VERSION-bin-hadoop3.tgz -P /opt && \
    tar -xzvf /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop3 $SPARK_HOME && \
    rm /opt/spark-$SPARK_VERSION-bin-hadoop3.tgz

RUN pip3 install pyspark

WORKDIR $SPARK_CONFG_DIR
#RUN cp spark-env.sh.template spark-env.sh && \
#    cp spark-defaults.conf.template spark-defaults.conf

RUN echo "spark-master spark://spark-master:7707" >> spark-defaults.conf && \
    echo "spark.serializer org.apache.spark.serializer.KryoSerializer" >> spark-defaults.conf

#RUN echo "192.168.80.128 spark-master" >> /etc/hosts

ENV SPARK_NO_DAEMONIZE=true
WORKDIR $SPARK_HOME

CMD ["./start-master.sh"]