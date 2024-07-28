#!/bin/bash

## spark_image/start-spark.sh

# master -> start-master.sh / worker
if [ "$HOSTNAME" == "spark-master" ]; then
    $SPARK_HOME/sbin/start-master.sh
else
    $SPARK_HOME/sbin/start-worker.sh spark://spark-master:7077
fi

# Keep the container running
tail -f /dev/null