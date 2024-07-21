#!/bin/bash

unset YARN_LOG_DIR

# Start YARN resourcemanager
#$HADOOP_HOME/bin/yarn --daemon start resourcemanager

# Start YARN nodemanager
$HADOOP_HOME/bin/yarn --daemon start nodemanager

# Keep the container running
tail -f /dev/null