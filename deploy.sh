#!/bin/bash

echo " Starting Deployment..."

# Pull the latest Docker image from DockerHub
docker pull your_dockerhub_username/lone-mlops:latest

# Stop and remove old container if running
docker stop iris-app 2>/dev/null || true
docker rm iris-app 2>/dev/null || true

# Run new container
docker run -d \
  --name lone-app \
  -p 8000:8000 \
  --restart always \
  your_dockerhub_username/lone-mlops:latest

echo " Deployment Complete! App running on port 8000"