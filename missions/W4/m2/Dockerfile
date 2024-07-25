FROM ubuntu:22.04

ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN apt update
RUN apt install -y python3 python3-pip
RUN apt install -y openjdk-8-jdk
RUN apt install -y wget sudo

RUN wget https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz
RUN tar xvf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt/
RUN mv /opt/spark-${SPARK_VERSION}-bin-hadoop3/ /opt/spark/
RUN rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

RUN pip install --upgrade pip
RUN pip install jupyter pandas numpy matplotlib seaborn
RUN pip install pyspark

EXPOSE 8888

CMD [ "bash", "-c", "/opt/spark/sbin/start-master.sh \
                    && jupyter notebook --notebook-dir='/root' --allow-root --ip=0.0.0.0 --no-browser --port=8888 --NotebookApp.token=''" ]