FROM base
ENV SPARK_FILE_NAME=spark-3.5.1-bin-hadoop3
ENV SAPRK_URL=https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz

RUN sudo apt install -y dumb-init

# spark setting
RUN wget $SAPRK_URL
RUN tar -xvzf $SPARK_FILE_NAME.tgz && rm $SPARK_FILE_NAME.tgz
RUN mv $SPARK_FILE_NAME /opt
RUN ln -s /opt/$SPARK_FILE_NAME /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# spark history log directory
RUN mkdir $SPARK_HOME/eventLog

WORKDIR $SPARK_HOME
# 8080 : master web UI
# 8081 : worker web UI
# 7077 : service port for master
EXPOSE 8080 7077 8081

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
