$SPARK_HOME/sbin/start-worker.sh spark://$SPARK_MASTER_HOST:7077
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.worker.Worker-1-$(hostname).out
