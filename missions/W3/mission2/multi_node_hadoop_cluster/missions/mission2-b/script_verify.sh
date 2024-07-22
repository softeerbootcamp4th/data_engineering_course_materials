#!/bin/bash

# Define the commands and their expected values
declare -a commands=(
  "hdfs getconf -confKey fs.defaultFS"
  "hdfs getconf -confKey hadoop.tmp.dir"
  "hdfs getconf -confKey io.file.buffer.size"
  "hdfs getconf -confKey dfs.replication"
  "hdfs getconf -confKey dfs.blocksize"
  "hdfs getconf -confKey dfs.namenode.name.dir"
  "hdfs getconf -confKey mapreduce.framework.name"
  "hdfs getconf -confKey mapreduce.jobhistory.address"  
  "hdfs getconf -confKey mapreduce.task.io.sort.mb"
  "hdfs getconf -confKey yarn.resourcemanager.address"
  "hdfs getconf -confKey yarn.nodemanager.resource.memory-mb"
  "hdfs getconf -confKey yarn.scheduler.minimum-allocation-mb"
)

declare -A expected_values=(
  ["fs.defaultFS"]="hdfs://namenode:9000"
  ["hadoop.tmp.dir"]="/hadoop/tmp"
  ["io.file.buffer.size"]="131072"
  ["dfs.replication"]="2"
  ["dfs.blocksize"]="134217728"
  ["dfs.namenode.name.dir"]="/hadoop/dfs/name"
  ["mapreduce.framework.name"]="yarn"
  ["mapreduce.jobhistory.address"]="namenode:10020"
  ["mapreduce.task.io.sort.mb"]="256"
  ["yarn.resourcemanager.address"]="namenode:8032"
  ["yarn.nodemanager.resource.memory-mb"]="8192"
  ["yarn.scheduler.minimum-allocation-mb"]="1024"
)


# Loop through the commands and check their values
for cmd in "${commands[@]}"; do
  # Extract the configuration key
  key=$(echo $cmd | awk '{print $NF}')
  expected=${expected_values[$key]} # Get the expected value

  # Execute the command and get the actual value
  actual=$($cmd 2>/dev/null)

  if [ "$actual" == "$expected" ]; then
    echo "PASS: [$cmd] -> $actual"
  else
    echo "FAIL: [$cmd] -> $actual (expected $expected)"
  fi
done