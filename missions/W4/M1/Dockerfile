# Base image
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y vim wget unzip ssh openjdk-8-jdk python3-pip rsync sudo net-tools

# Create Hadoop user
RUN useradd -ms /bin/bash spark
RUN echo "spark ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set environment variables
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-arm64
ENV SPARK_HOME /usr/local/spark
ENV PATH $PATH:$SPARK_HOME

# Download and install Hadoop
COPY /untracked/spark-3.5.1-bin-hadoop3.tgz $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz
RUN tar -zxvf $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz -C $SPARK_HOME/
RUN mv $SPARK_HOME/spark-3.5.1-bin-hadoop3/* $SPARK_HOME/
RUN rm -rf $SPARK_HOME/spark-3.5.1-bin-hadoop3.tgz
RUN mkdir -p $SPARK_HOME/data
RUN chown -R spark:spark $SPARK_HOME
# Change user
USER spark

# Set environment variables in .bashrc
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> ~/.bashrc && \
    echo "export PATH=\$PATH:\$SPARK_HOME" >> ~/.bashrc && \
    echo "export SPARK_HOME=/usr/local/spark" >> ~/.bashrc

# Start Hadoop datanode
COPY /start_script/start_spark.sh $SPARK_HOME/start_spark.sh
COPY /start_script/start_pi.sh $SPARK_HOME/start_pi.sh
RUN sudo chmod +x $SPARK_HOME/start_spark.sh
RUN sudo chmod +x $SPARK_HOME/start_pi.sh

# 시작 명령어 설정
CMD ["/usr/local/spark/start_spark.sh"]
