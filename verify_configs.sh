#!/bin/bash

HADOOP_CONF_DIR=$1

# 검증 함수
verify_config() {
    local command=$1
    local conf_key=$2
    local expected_value=$3

    local value=$($command getconf -confKey $conf_key 2>/dev/null)
    if [[ $? -ne 0 ]]; then
        echo "FAIL: ['$command', 'getconf', '-confKey', '$conf_key'] -> Error getting value"
        return
    fi

    if [[ "$value" == "$expected_value" ]]; then
        echo "PASS: ['$command', 'getconf', '-confKey', '$conf_key'] -> $value"
    else
        echo "FAIL: ['$command', 'getconf', '-confKey', '$conf_key'] -> $value (expected $expected_value)"
    fi
}

echo "Verifying configuration changes..."

# 각 구성 파일 및 속성 검증
verify_config hdfs fs.defaultFS hdfs://namenode:9000
verify_config hdfs hadoop.tmp.dir /hadoop/tmp
verify_config hdfs io.file.buffer.size 131072
verify_config hdfs dfs.replication 2
verify_config hdfs dfs.blocksize 134217728
verify_config hdfs dfs.namenode.name.dir /hadoop/dfs/name
verify_config hdfs mapreduce.task.io.sort.mb 256
verify_config hdfs mapreduce.framework.name yarn
verify_config hdfs mapreduce.jobhistory.address namenode:10020

verify_config hdfs yarn.resourcemanager.address namenode:8032
verify_config hdfs yarn.nodemanager.resource.memory-mb 8192
verify_config hdfs yarn.scheduler.minimum-allocation-mb 1024

# Replication factor 검증
replication_factor=$(hdfs getconf -confKey dfs.replication 2>/dev/null)
if [[ "$replication_factor" == "2" ]]; then
    echo "PASS: Replication factor is 2"
else
    echo "FAIL: Replication factor is $replication_factor (expected 2)"
fi

echo "Configuration verification completed."
