#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 571495482396.dkr.ecr.ap-northeast-2.amazonaws.com
docker pull 571495482396.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-w2m6:latest
docker run -p 8888:8888  --rm 571495482396.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-w2m6:latest