FROM ubuntu:22.04

ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN apt update
RUN apt install -y wget openjdk-8-jdk sudo \
    && apt clean

RUN wget https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz
RUN tar xvf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt/ \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop3/ /opt/spark/ \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# COPY submit.sh /root/submit.sh
# COPY pi_to_csv.py /root/pi_to_csv.py
# RUN chmod +x submit.sh