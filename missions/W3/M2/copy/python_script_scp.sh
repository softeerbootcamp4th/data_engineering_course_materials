#!/bin/bash

scp -P 2222 ./mapper.py hadoop@localhost:~
scp -P 2222 ./reducer.py hadoop@localhost:~
scp -P 2222 ./input.txt hadoop@localhost:~
scp -P 2222 ./wordcount.sh hadoop@localhost:~

