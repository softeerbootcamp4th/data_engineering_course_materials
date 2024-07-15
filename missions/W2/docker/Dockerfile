# Base image
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
# Install dependencies
RUN pip install -r requirements.txt

# Git 설치
RUN apt-get update
RUN apt-get install -y git

# 스크립트 추가
COPY start.sh .
RUN chmod +x start.sh

# Expose the port Jupyter Lab will run on
EXPOSE 8889

# Command to run Jupyter Lab
CMD ["./start.sh"]
