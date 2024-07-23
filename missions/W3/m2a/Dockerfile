FROM hadoop-base:latest

USER hadoopuser

# Hadoop 환경 설정 파일 복사
COPY --chown=hadoopuser:hadoopuser config/* $HADOOP_HOME/etc/hadoop/

# 포트 노출
EXPOSE 9870 8088 9864

# Hadoop 시작 스크립트 복사 및 실행 권한 설정
COPY --chown=hadoopuser:hadoopuser start-node.sh /usr/local/bin/start-node.sh
RUN chmod +x /usr/local/bin/start-node.sh

# 기본 명령어 설정
CMD ["/usr/local/bin/start-node.sh"]
