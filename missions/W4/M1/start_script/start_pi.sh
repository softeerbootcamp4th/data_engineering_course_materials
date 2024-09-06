#!/bin/bash

# Define the directory
LOG_DIR="/usr/local/spark/data/test_log"

# Create the directory if it does not exist
mkdir -p "$LOG_DIR"

# Get the current date and time
CURRENT_TIME=$(date "+%Y-%m-%d_%H-%M-%S")

# Define the log file with date and time
LOG_FILE="$LOG_DIR/PI_OUTPUT_$CURRENT_TIME.log"

# Start the Spark example job and redirect stdout and stderr to the log file
$SPARK_HOME/bin/spark-submit --master spark://spark-master:7077 $SPARK_HOME/examples/src/main/python/pi.py > "$LOG_FILE" 2>&1
$SPARK_HOME/bin/spark-submit --master spark://spark-master:7077 status_api_demo.py > "/usr/local/spark/data/test_log/status_api" 2>&1

$SPARK_HOME/bin/spark-submit --conf spark.eventLog.enabled=true --conf spark.eventLog.dir=hdfs://path_to_eventlog_directory your_spark_job.py
