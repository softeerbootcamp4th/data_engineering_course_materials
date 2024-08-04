FROM base

RUN mkdir -p $HADOOP_HOME/dfs/name

ADD --chown=hadoop:users ./start.sh ./start.sh

# 8088 : yarn resource manager Web UI
# 8030 : yarn scheduler interface
# 8032 : yarn resource manager IPC port
# 9000 : IPC port (namenode <> datanode 통신을 위한 포트)
# docker container간 통신만 하면 되기때문에 local port와 매핑해줄 필요 없음
# 9870 : NameNode HTTP web ui
# 8020 : cleint request
EXPOSE 9000 9870 8088 8032 8030 8020

CMD ["/bin/sh", "./start.sh", "/opt/hadoop/dfs/name"]