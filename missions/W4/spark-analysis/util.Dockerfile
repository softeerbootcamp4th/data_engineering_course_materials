FROM jnamu/hadoop-cluster-node

RUN apt-get install -y vim && \
    pip3 install pandas numpy pyarrow matplotlib seaborn jupyter

COPY configs/* $HADOOP_CONF_DIR/
COPY scripts/* /usr/local/bin/
COPY examples/* /home/hdfs/examples/
COPY jupyter-file/* /root/
RUN chmod +x /usr/local/bin/*.sh

WORKDIR $SPARK_HOME


