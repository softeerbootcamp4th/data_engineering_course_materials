#!/bin/bash

./build_and_run_hadoop_services.sh

cd change-config
./apply_all.sh

cd ../verification
./python3 run build-verify-scrips.py
./configuration_verify.sh usr/local/hadoop namenode

cd ../mapreduce
./test_mapreduce.sh usr/local/hadoop namenode