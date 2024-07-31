#! /bin/bash

cd ~
spark-submit pi_modified.py
echo
echo
echo
echo "===== [result of pi_modified.py] ====="
cat pi_result.csv