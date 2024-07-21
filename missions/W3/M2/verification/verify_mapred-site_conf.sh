#!/bin/bash

check_conf() {
  local key=$1
  local expected_value=$2
  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)

  if [ "$actual_value" == "$expected_value" ]; then
    echo "PASS: ['hadoop', 'getconf', '-confKey', '$key'] -> $actual_value"
  else
    echo "FAIL: ['hadoop', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)"
  fi
}

check_conf mapreduce.framework.name yarn
check_conf mapreduce.jobhistory.address namenode:10020
check_conf mapreduce.task.io.sort.mb 256
check_conf yarn.app.mapreduce.am.env HADOOP_MAPRED_HOME=/usr/local/hadoop
check_conf mapreduce.map.env HADOOP_MAPRED_HOME=/usr/local/hadoop
check_conf mapreduce.reduce.env HADOOP_MAPRED_HOME=/usr/local/hadoop
