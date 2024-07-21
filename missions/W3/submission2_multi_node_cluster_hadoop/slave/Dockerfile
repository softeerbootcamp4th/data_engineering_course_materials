FROM hadoop_base:latest

# Config 파일 복사
COPY config/* $HADOOP_HOME/etc/hadoop/
RUN chown -R hdfs:hadoop $HADOOP_HOME/etc/hadoop

# 쉘 파일 복사
COPY slave_entrypoint.sh /usr/local/bin/slave_entrypoint.sh
RUN chmod +x /usr/local/bin/slave_entrypoint.sh

# 실행
CMD service ssh start && usr/local/bin/slave_entrypoint.sh