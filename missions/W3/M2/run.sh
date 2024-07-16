#!/bin/bash

docker compose down
docker build -t base ./base
docker build -t master ./master
docker build -t worker ./worker
docker compose up -d