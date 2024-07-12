#!/bin/bash
# 로그 파일로 출력 설정
exec > /var/log/user-data.log 2>&1
set -x

# 업데이트 및 필요한 패키지 설치
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Docker GPG 키 추가
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Docker APT 리포지토리 추가
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Docker 설치
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Docker 시작 및 부팅 시 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker

# ubuntu 사용자를 docker 그룹에 추가
sudo usermod -aG docker ubuntu

docker