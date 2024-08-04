FROM base

# datanode data directory
RUN mkdir -p $HADOOP_HOME/dfs/data
# nodemamager data directory
RUN mkdir -p $HADOOP_HOME/yarn/data

# 9864 : datanode web UT port
# 9866 : The datanode server address and port for data transfer.
# 8042 : yarn nodemanager webapp address
# 8040 : arn.nodemanager.localizer.address
EXPOSE 9864 9866 8042
ADD --chown=hadoop:users ./start.sh ./start.sh
CMD ["/bin/sh", "./start.sh"]