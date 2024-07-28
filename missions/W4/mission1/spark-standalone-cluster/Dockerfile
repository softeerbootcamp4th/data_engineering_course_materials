FROM ubuntu:22.04

ARG SPARK_VERSION=3.3.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      python3.9 \
      python3-pip \ 
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m spark_user && echo "spark_user:supergroup" | chpasswd && adduser spark_user sudo && echo "spark_user     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python
USER spark_user

ENV SPARK_HOME=${SPARK_HOME:-"/home/spark_user/spark"}

RUN sudo mkdir -p ${SPARK_HOME}

RUN sudo curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
 && sudo tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory /home/spark_user/spark --strip-components 1 \
 && sudo rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz

# COPY requirements/requirements.txt .
# RUN pip3 install -r requirements.txt
RUN pip3 install pyspark

ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

RUN sudo chown -R spark_user /home/spark_user
RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
RUN mkdir -p ${SPARK_HOME}/spark-events

WORKDIR /home/spark_user
COPY scripts/* .

RUN sudo chmod +x entrypoint.sh && \
    sudo chmod +x mission1.sh && \
    sudo chmod +x pi_modified.py

CMD ["sh", "-c", "entrypoint.sh"]