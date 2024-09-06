#!/bin/bash

CONTAINER_NAME="spark-master"
SPARK_HOME=/usr/local/spark

docker exec -it --user hadoop $CONTAINER_NAME bash -c "
  sudo apt install jupyter -y
  pip install pyspark
  "
    


