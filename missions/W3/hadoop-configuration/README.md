






# HDFS, YARN, MapReduce 관련 포트 정리
##  Expose HDFS ports for NameNode
### RPC(Client communication) / Web UI / Service RPC / Backup Node(optional_ / Journal Node(HA 설정)
EXPOSE 8020, 9870, 8022, 50100, 8485
## Expose HDFS ports for
### Data Transfer / Web UI / IPC
EXPOSE 9866, 9864, 9867
## Expose YARN ports for ResourceManager
### Scheduler / RM / ResourceTracker / AM / Web UI
EXPOSE 8030, 8031, 8032, 8033, 8088
## Expose YARN ports for NodeManager
### Localizer / Web UI / Shuffle
EXPOSE 8040, 8042, 13562
## Expose MapReduce port for JobHistoryServer
EXPOSE 19888  # Web UI Port