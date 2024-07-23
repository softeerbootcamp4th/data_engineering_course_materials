#!/bin/bash

check_conf() {
  local key=$1
  local expected_value=$2
  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)

  if [ "$actual_value" == "$expected_value" ]; then
    echo "PASS: ['yarn', 'getconf', '-confKey', '$key'] -> $actual_value"
  else
    echo "FAIL: ['yarn', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)"
  fi
}

check_conf yarn.nodemanager.aux-services mapreduce_shuffle
check_conf yarn.resourcemanager.hostname resourcemanager
check_conf yarn.resourcemanager.address resourcemanager:8032
check_conf yarn.nodemanager.resource.memory-mb 8192
check_conf yarn.scheduler.minimum-allocation-mb 1024
