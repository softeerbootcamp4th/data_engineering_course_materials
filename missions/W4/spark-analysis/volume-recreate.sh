#!/usr/bin/env bash

pwd=$PWD
docker volume rm "$(basename $pwd)_hadoop-master-data" \
"$(basename $pwd)_hadoop-slave1-data" \
"$(basename $pwd)_hadoop-slave2-data"
docker volume create "$(basename $pwd)_hadoop-master-data"
docker volume create "$(basename $pwd)_hadoop-slave1-data"
docker volume create "$(basename $pwd)_hadoop-slave2-data"