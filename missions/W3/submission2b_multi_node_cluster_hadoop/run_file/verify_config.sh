#!/bin/bash

# Set Hadoop environment variables
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Function to get Hadoop configuration value
get_hadoop_conf_value() {
    local conf_key=$1
    local value
    value=$(hdfs getconf -confKey "$conf_key" 2>/dev/null)
    if [[ $? -ne 0 || -z "$value" ]]; then
        echo "Error: Unable to get configuration value for $conf_key" >&2
        exit 1
    fi
    echo "$value"
}

# Verify settings
verify_setting() {
    local conf_key=$1
    local expected_value=$2
    local actual_value
    actual_value=$(get_hadoop_conf_value "$conf_key")
    if [[ "$actual_value" == "$expected_value" ]]; then
        echo "PASS: $conf_key is set to $expected_value"
    else
        echo "FAIL: $conf_key is set to $actual_value (expected $expected_value)"
    fi
}

# Verify specific Hadoop settings
verify_setting "fs.defaultFS" "hdfs://namenode:9000"
verify_setting "hadoop.tmp.dir" "/usr/local/hadoop/tmp"
verify_setting "io.file.buffer.size" "131072"
verify_setting "dfs.replication" "2"
verify_setting "dfs.blocksize" "134217728"
verify_setting "dfs.namenode.name.dir" "/hadoop/dfs/name"
verify_setting "mapreduce.framework.name" "yarn"
verify_setting "mapreduce.jobhistory.address" "namenode:10020"
verify_setting "mapreduce.task.io.sort.mb" "256"
verify_setting "yarn.resourcemanager.address" "namenode:8032"
verify_setting "yarn.nodemanager.resource.memory-mb" "8192"
verify_setting "yarn.scheduler.minimum-allocation-mb" "1024"

# Create a test file in HDFS and check replication factor
hdfs dfs -rm -f /tmp/testfile
echo "Creating test file in HDFS..."
echo "Hello Hadoop" > /tmp/testfile_local
hdfs dfs -put /tmp/testfile_local /tmp/testfile

replication_factor=$(hdfs fsck /tmp/testfile -files -blocks -racks | grep 'Total blocks' | awk '{print $8}')
if [[ "$replication_factor" == "2" ]]; then
    echo "PASS: Replication factor is set to 2"
else
    echo "FAIL: Replication factor is $replication_factor (expected 2)"
fi

# Run a simple MapReduce job (WordCount)
echo "Running WordCount MapReduce job..."
hdfs dfs -rm -r -f /tmp/wordcount_output
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /tmp/testfile /tmp/wordcount_output

# Check WordCount output
hdfs dfs -cat /tmp/wordcount_output/part-r-00000

# Query YARN ResourceManager for total available memory
total_memory=$(yarn node -list 2>/dev/null | grep -oP 'Total Memory: \K[0-9]+')
if [[ "$total_memory" == "8192" ]]; then
    echo "PASS: Total YARN memory is 8192 MB"
else
    echo "FAIL: Total YARN memory is $total_memory MB (expected 8192 MB)"
fi

echo "Validation completed."
