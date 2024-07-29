#!/usr/bin/env bash

docker volume rm hadoop-master-data hadoop-slave1-data hadoop-slave2-data
docker volume create hadoop-master-data
docker volume create hadoop-slave1-data
docker volume create hadoop-slave2-data