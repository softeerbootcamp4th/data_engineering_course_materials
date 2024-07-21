FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    wget curl net-tools vim openssh-server openssh-client sudo openjdk-11-jdk 
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=${PATH}:${JAVA_HOME}/bin

# Create a user
RUN useradd -ms /bin/bash hadoopuser

# Install SSH, sudo, and other necessary packages
RUN apt-get update && \
    apt-get install -y openssh-server sudo rsync && \
    mkdir /var/run/sshd

# Set root password
RUN echo 'root:root' | chpasswd

# Permit root login via SSH
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Allow password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Add hadoopuser to sudoers
RUN echo 'hadoopuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to hadoopuser and set up SSH keys
USER hadoopuser

RUN mkdir -p /home/hadoopuser/.ssh && \
    ssh-keygen -t rsa -P "" -f /home/hadoopuser/.ssh/id_rsa && \
    cat /home/hadoopuser/.ssh/id_rsa.pub >> /home/hadoopuser/.ssh/authorized_keys && \
    chmod 600 /home/hadoopuser/.ssh/authorized_keys

# Switch back to root for further setup
USER root

# Expose SSH port
EXPOSE 22 9870 8088

# Set limits
RUN echo 'hadoopuser  -  nproc  65536' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  nofile  65536' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  memlock  unlimited' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  stack  8192' >> /etc/security/limits.conf && \
    echo 'hadoopuser  -  rtprio  0' >> /etc/security/limits.conf

# Hadoop installation
COPY hadoop-3.4.0.tar.gz /temp/
RUN tar -xzvf /temp/hadoop-3.4.0.tar.gz -C /usr/local/ && \
    mv /usr/local/hadoop-3.4.0 /usr/local/hadoop && \
    chown -R hadoopuser:hadoopuser /usr/local/hadoop && \
    rm /temp/hadoop-3.4.0.tar.gz

# Config
COPY config/* /usr/local/hadoop/etc/hadoop/
RUN chown -R hadoopuser:hadoopuser /usr/local/hadoop/etc/hadoop/

# Set Hadoop environment variables
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_INSTALL=/usr/local/hadoop
ENV HADOOP_MAPRED_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_HOME=/usr/local/hadoop
ENV HADOOP_HDFS_HOME=/usr/local/hadoop
ENV YARN_HOME=/usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR=/usr/local/hadoop/lib/native
ENV PATH=$PATH:/usr/local/hadoop/sbin:/usr/local/hadoop/bin
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

# Copy the start script
COPY start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh

# Switch to hadoopuser
USER hadoopuser
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64' >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
CMD ["/usr/local/bin/start-hadoop.sh"]
