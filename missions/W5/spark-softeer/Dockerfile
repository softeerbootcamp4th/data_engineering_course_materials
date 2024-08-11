FROM ubuntu:jammy

EXPOSE 8080

RUN apt update -y && apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install wget sudo openjdk-11-jdk -y

RUN useradd sparkuser -s /bin/bash -d /home/sparkuser -p spark
RUN echo "sparkuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir /home/sparkuser
RUN chown sparkuser:sparkuser /home/sparkuser

USER sparkuser
WORKDIR /home/sparkuser

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN sudo chown sparkuser:sparkuser get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py
RUN python3 -m pip install pandas matplotlib pyspark pyarrow grpcio protobuf grpcio-status

RUN wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
RUN tar -zxvf spark-3.5.1-bin-hadoop3.tgz
RUN rm spark-3.5.1-bin-hadoop3.tgz
RUN mv spark-3.5.1-bin-hadoop3 spark
RUN sudo mv spark /

WORKDIR /spark
ADD ./start.sh . 
ADD config/fairscheduler.xml* /spark/conf
ADD config/log4j2.properties* /spark/conf
ADD config/metrics.properties* /spark/conf
ADD config/spark-defaults.conf* /spark/conf
ADD config/spark-env.sh* /spark/conf
ADD config/workers* /spark/conf
RUN sudo chown sparkuser:sparkuser ./start.sh
RUN sudo chmod +rwx ./start.sh
RUN echo "export PATH=/spark/bin:$PATH" >> ~/.bashrc