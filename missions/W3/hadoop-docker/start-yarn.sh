#!/bin/bash

# Start YARN resourcemanager
$HADOOP_HOME/bin/yarn --daemon start resourcemanager

# Start YARN nodemanager
$HADOOP_HOME/bin/yarn --daemon start nodemanager
