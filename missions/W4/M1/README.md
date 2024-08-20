run "build_and_run_hadoop_services.sh" file
then "start_script/start_spark.sh" would be run automatically

you can run 'start_pi.sh' in the docker spark-master container.
"start_pi.sh" is in "$SPARK_HOME/start_pi.sh"
$SPARK_HOME = /usr/local/spark