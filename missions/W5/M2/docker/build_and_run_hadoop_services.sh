#!/bin/bash

# Build Docker images
echo "Building Spark image..."
docker build -t spark .


# Start services using docker-compose
# echo "Starting Hadoop services..."
docker-compose up -d
