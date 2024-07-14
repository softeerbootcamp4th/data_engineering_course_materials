#!/bin/bash
# read more at https://docs.docker.com/engine/install/ubuntu/

apt-get update
apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker packages
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service and enable it to start on boot
systemctl start docker
systemctl enable docker

# Add the ubuntu user to the docker group
usermod -aG docker ubuntu

###################

# data product 클론
git clone --branch w1/m1-mtcars https://github.com/Neogr1/softeer_data_engineering.git /home/ubuntu/w1m1
git clone --branch w2/m5-word-cloud https://github.com/Neogr1/softeer_data_engineering.git /home/ubuntu/w2m5
mv /home/ubuntu/w1m1/missions/W1/mtcars.csv /home/ubuntu/mtcars.csv
mv /home/ubuntu/w1m1/missions/W1/mtcars.ipynb /home/ubuntu/w1m1_mtcars.ipynb
mv /home/ubuntu/w2m5/missions/W2/m5_sentiment_analysis.ipynb /home/ubuntu/w2m5_sentiment_analysis.ipynb
mv /home/ubuntu/w2m5/missions/W2/training.1600000.processed.noemoticon.csv /home/ubuntu/training.1600000.processed.noemoticon.csv
rm -rf /home/ubuntu/w1m1
rm -rf /home/ubuntu/w2m5

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
apt-get install unzip
unzip awscliv2.zip
./aws/install

# Configure AWS CLI
# IAM 역할 사용하도록 수정 필요
aws configure set aws_access_key_id {AWS_ACCESS_KEY_ID}
aws configure set aws_secret_access_key {AWS_SECRET_ACCESS_KEY}
aws configure set default.region ap-northeast-2

# Log in to ECR and pull the Docker image
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin {MY_AWS_ID}.dkr.ecr.ap-northeast-2.amazonaws.com
docker pull {MY_AWS_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-jupyter:latest 

# 도커 컨테이너 실행
docker run -d --name softeer-jupyter \
  --platform linux/amd64 \
  -p 8888:8888 \
  -v /home/ubuntu:/app \
  {MY_AWS_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-jupyter:latest \
  /bin/bash -c "cd /app && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''"