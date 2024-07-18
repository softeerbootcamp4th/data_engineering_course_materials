#!/bin/bash

sudo service ssh start
./sbin/start-dfs.sh
./sbin/start-yarn.sh
/bin/bash