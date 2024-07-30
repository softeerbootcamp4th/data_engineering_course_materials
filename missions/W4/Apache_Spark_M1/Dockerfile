# Base Image Setting_Docker Imagle Build
FROM openjdk:8-jdk-slim

# Set Environment Variables
ENV SPARK_VERSION=3.2.1
ENV HADOOP_VERSION=3.2
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Install Pakages
RUN apt-get update && apt-get install -y python3 python3-pip curl
RUN apt-get -y install procps
RUN rm -rf /var/lib/apt/lists/*
    
# Download and Install Spark
RUN curl -L "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | tar -xz -C /opt/
RUN mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME

# Copy entrypoint script
COPY entrypoint.sh /opt/
COPY pi.py /opt/spark/
COPY spark-submit.sh /opt/
RUN chmod +x /opt/entrypoint.sh
RUN chmod +x /opt/spark-submit.sh

# Create a non-root user and set permissions
RUN useradd -ms /bin/bash sparkuser
RUN chown -R sparkuser:sparkuser /opt/spark
RUN chown sparkuser:sparkuser /opt/entrypoint.sh
RUN chown sparkuser:sparkuser /opt/spark-submit.sh

# Switch to non-root user
USER sparkuser

# Set entrypoint
ENTRYPOINT ["/opt/entrypoint.sh"]