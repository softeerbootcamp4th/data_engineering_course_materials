#!/bin/bash

# Build Docker images
echo "Building Hadoop datanode image..."
docker build -t hadoop-datanode -f Dockerfile.datanode .

echo "Building Hadoop namenode image..."
docker build -t hadoop-namenode -f Dockerfile.namenode .

echo "Building Hadoop resourcemanager image..."
docker build -t hadoop-resourcemanager -f Dockerfile.resourcemanager .

echo "Building Hadoop nodemanager image..."
docker build -t hadoop-nodemanager -f Dockerfile.nodemanager .

# Start services using docker-compose
echo "Starting Hadoop services..."
docker-compose up -d
