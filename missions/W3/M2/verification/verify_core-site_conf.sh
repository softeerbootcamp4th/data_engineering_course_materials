#!/bin/bash

check_conf() {
  local key=$1
  local expected_value=$2
  local actual_value=$(hdfs getconf -confKey $key 2>/dev/null)

  if [ "$actual_value" == "$expected_value" ]; then
    echo "PASS: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value"
  else
    echo "FAIL: ['hdfs', 'getconf', '-confKey', '$key'] -> $actual_value (expected $expected_value)"
  fi
}

check_conf fs.defaultFS hdfs://namenode:9000
check_conf hadoop.tmp.dir /hadoop/tmp
check_conf io.file.buffer.size 131072
