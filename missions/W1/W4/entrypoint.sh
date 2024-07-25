# scp -r ~/.ssh root@spark-worker1::~/
# scp -r ~/.ssh root@spark-worker2:~/

$SPARK_HOME/sbin/start-master.sh -h $SPARK_MASTER_HOST
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.master.Master-1-$(hostname).out