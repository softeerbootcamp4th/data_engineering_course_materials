FROM python:3.10-bullseye

# Set environment variables
ENV SPARK_VERSION=3.4.3
ENV HADOOP_VERSION=3
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Install dependencies and Python, Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk curl vim ssh python3-pip && \
    pip3 install pandas numpy pyarrow pyspark && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make Spark conf directory
RUN mkdir -p $SPARK_HOME
WORKDIR $SPARK_HOME

# Download and install Spark with Hadoop
RUN curl -L -o /tmp/spark.tgz https://downloads.apache.org/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz && \
    tar -xvzf /tmp/spark.tgz -C /opt && \
    mv /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION/* $SPARK_HOME && \
    rm /tmp/spark.tgz && \
    rm -rf /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION

# Grant execute permissions to the owner
RUN chmod u+x $SPARK_HOME/sbin/* && \
    chmod u+x $SPARK_HOME/bin/*

# Copy config
COPY spark-defaults.conf "$SPARK_HOME/conf"
COPY spark-env.sh "$SPARK_HOME/conf"
RUN echo "export JAVA_HOME=$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')" >> $SPARK_HOME/conf/spark-env.sh

# Create alias for pyspark and spark-shell
RUN echo "alias pyspark='$SPARK_HOME/bin/pyspark'" >> ~/.bashrc && \
    echo "alias spark-shell='$SPARK_HOME/bin/spark-shell'" >> ~/.bashrc

# Entry point
CMD ["bash"]
