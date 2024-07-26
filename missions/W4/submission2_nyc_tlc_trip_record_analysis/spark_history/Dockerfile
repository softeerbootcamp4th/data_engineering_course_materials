FROM spark_base

# Copy the master script
COPY history_entrypoint.sh $SPARK_HOME/history_entrypoint.sh
RUN chmod +x $SPARK_HOME/history_entrypoint.sh

EXPOSE 18080

CMD $SPARK_HOME/history_entrypoint.sh
