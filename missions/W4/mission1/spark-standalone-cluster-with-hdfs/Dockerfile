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
    python3-pip \ 
    ssh \
    openssh-server && \
    apt-get clean 
    # rm -rf /var/lib/apt/lists/*

RUN useradd -m spark_user && echo "spark_user:supergroup" | chpasswd && adduser spark_user sudo && echo "spark_user     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && cd /usr/bin/ && sudo ln -s python3 python
RUN sudo useradd -m hduser && echo "hduser:supergroup" | chpasswd && adduser hduser sudo && echo "hduser     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chmod 777 /root/.bashrc

ENV HDFS_NAMENODE_USER hduser
ENV HDFS_DATANODE_USER hduser
ENV HDFS_SECONDARYNAMENODE_USER hduser
ENV YARN_RESOURCEMANAGER_USER hduser
ENV YARN_NODEMANAGER_USER hduser
ENV SPARK_HOME=${SPARK_HOME:-"/home/spark_user/spark"}
ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/home/hduser/hadoop-$HADOOP_VERSION

USER spark_user
RUN sudo chown -R spark_user /home/spark_user

WORKDIR /home/spark_user

RUN sudo mkdir -p ${SPARK_HOME} 

RUN sudo curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
 && sudo tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory /home/spark_user/spark --strip-components 1 \
 && sudo rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz

COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

RUN sudo chown -R spark_user /home/spark_user
RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

RUN mkdir -p ${SPARK_HOME}/spark-events

COPY scripts/* .
RUN mkdir code
RUN sudo chmod +x entrypoint.sh && \
    sudo chmod +x mission1.sh && \
    sudo chmod +x pi_modified.py

USER hduser
WORKDIR /home/hduser
RUN mkdir -p /home/hduser/data/namenode
RUN mkdir /home/hduser/data/datanode
RUN sudo chown -R hduser /home/hduser

RUN curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | gunzip \
  | tar -x -C /home/hduser/ \
 && rm -rf ${HADOOP_HOME}/share/doc


RUN echo "export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# ssh without key
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P '' && \
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
chmod 0600 ~/.ssh/authorized_keys

RUN mkdir $HADOOP_HOME/logs
COPY hadoop_config/* /tmp/

RUN sudo cp /tmp/ssh_config /etc/ssh/ssh_config && \
    sudo mv /tmp/ssh_config ~/.ssh/ssh_config && \
    sudo mv /tmp/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
    sudo mv /tmp/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml && \ 
    sudo mv /tmp/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml && \
    sudo mv /tmp/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml && \
    sudo mv /tmp/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml && \
    sudo mv /tmp/slaves $HADOOP_HOME/etc/hadoop/slaves && \
    sudo mv /tmp/start-hadoop.sh ~/start-hadoop.sh && \
    sudo mv /tmp/path_setup.sh ~/path_setup.sh 

RUN sudo chmod +x $HADOOP_HOME/sbin/start-dfs.sh && \
    sudo chmod +x $HADOOP_HOME/sbin/start-yarn.sh && \
    sudo chmod +x ~/start-hadoop.sh && \
    sudo chmod +x ~/path_setup.sh

RUN sudo chown -R hduser /home/hduser

USER spark_user
WORKDIR /home/spark_user
CMD ["sh", "-c", "entrypoint.sh"]