FROM spark_base

# Copy the master script
COPY master_entrypoint.sh $SPARK_HOME/master_entrypoint.sh
RUN chmod +x $SPARK_HOME/master_entrypoint.sh

RUN mkdir -p $SPARK_HOME/examples/mission2
COPY shell_files/* $SPARK_HOME/examples/mission2
COPY mission2.ipynb $SPARK_HOME/examples/mission2

# Set environment variables
EXPOSE 8080 7077 8888

CMD $SPARK_HOME/master_entrypoint.sh