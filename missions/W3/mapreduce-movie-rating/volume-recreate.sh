#!/usr/bin/env bash

docker volume rm hdfs-master hdfs-slave-1 hdfs-slave-2
docker volume create hdfs-master
docker volume create hdfs-slave-1
docker volume create hdfs-slave-2




