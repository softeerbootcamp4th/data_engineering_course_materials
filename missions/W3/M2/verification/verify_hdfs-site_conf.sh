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

check_conf dfs.replication 2
check_conf dfs.namenode.name.dir file:///hadoop/dfs/name
check_conf dfs.datanode.data.dir file:///hadoop/dfs/data
