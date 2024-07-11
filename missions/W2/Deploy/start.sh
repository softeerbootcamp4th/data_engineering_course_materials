#!/bin/bash

# Define the repository URL and the local directory
REPO_URL="https://github.com/YoonJunHyeok/softeer_wiki.git"
LOCAL_DIR="/app/softeer"

# Check if the local directory exists
if [ -d "$LOCAL_DIR" ]; then
  echo "Directory exists. Pulling the latest changes..."
  cd "$LOCAL_DIR"
  git pull
else
  echo "Directory does not exist. Cloning the repository..."
  git clone "$REPO_URL" "$LOCAL_DIR"
fi

jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''