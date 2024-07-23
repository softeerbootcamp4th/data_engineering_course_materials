FROM spark_base

# Copy the master script
COPY master_entrypoint.sh $SPARK_HOME/master_entrypoint.sh
RUN chmod +x $SPARK_HOME/master_entrypoint.sh

RUN mkdir -p $SPARK_HOME/examples/test
COPY montecarlo.py $SPARK_HOME/examples/test/montecarlo.py
COPY spark_submit_example.sh $SPARK_HOME/examples/test/spark_submit_example.sh

# Set environment variables
EXPOSE 8080 7077

CMD $SPARK_HOME/master_entrypoint.sh