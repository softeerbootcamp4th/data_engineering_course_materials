#!/bin/bash

# configuration_modify.sh $HADOOP_HOME $CONTAINER_NAME $ROLE
./configuration_modify.sh usr/local/hadoop namenode namenode
./configuration_modify.sh usr/local/hadoop resourcemanager resourcemanager
./configuration_modify.sh usr/local/hadoop datanode1 datanode
./configuration_modify.sh usr/local/hadoop datanode2 datanode
./configuration_modify.sh usr/local/hadoop nodemanager1 nodemanager
./configuration_modify.sh usr/local/hadoop nodemanager2 nodemanager