FROM base

HEALTHCHECK CMD curl -f http://localhost:9864/ || exit 1

# copy config file
ADD hdfs-site.xml $HADOOP_CONF_DIR

# datanode data directory
RUN mkdir $HADOOP_HOME/dfs/data

# nodemamager data directory
RUN mkdir -p $HADOOP_HOME/yarn/data

# 9864 : datanode web UT port
# 9866 : The datanode server address and port for data transfer.
# 8042 : yarn nodemanager webapp address
# 8040 : arn.nodemanager.localizer.address
EXPOSE 9864 9866 8042

ADD start.sh /start.sh
RUN chmod a+x /start.sh

CMD ["/start.sh"]