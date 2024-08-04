FROM ubuntu:22.04

ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN apt update && apt install -y \
    python3 python3-pip \
    openjdk-8-jdk \
    wget sudo

COPY spark-3.5.1-bin-hadoop3.tgz /temp/
RUN tar -xvf /temp/spark-3.5.1-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark && \
    rm -rf /temp/spark-3.5.1-bin-hadoop3.tgz

RUN pip install --upgrade pip
RUN pip install jupyter pandas numpy matplotlib seaborn pyspark

EXPOSE 8080 7077 8888

CMD [ "bash" ]
