# Docker 이미지를 AWS EC2에 배포하기

## AWS EC2 생성

- user-data

```bash
#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
```

## Docker 이미지 빌드

```bash
docker build -t myapp:latest . 
```

## AWS ECR 로그인을 위해 AWS CLI 설치

- 로컬 컴퓨터에 Homebrew 설치
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- Homebrew를 PATH에 추가 및 확인
```bash
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/admin/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
brew --version
```

- AWS CLI 설치 및 확인
```bash
brew install awscli
aws --version
```

## AWS CLI 구성

```bash
aws configure
AWS Access Key ID [None]: <your-access-key-id>
AWS Secret Access Key [None]: <your-secret-access-key>
Default region name [None]: <your-region>
Default output format [None]: json
```  

## Docker 이미지 태그 및 푸시

- AWS ECR 로그인
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

- Docker 이미지 태그
```bash
docker tag myapp:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/myapp:latest
```

- Docker 이미지 푸시
```bash
docker push <your-account-id>.dkr.ecr.ap-southeast-2.amazonaws.com/myapp:latest
```

## EC2 인스턴스에서 Docker 이미지 풀링 및 실행

- EC2 인스턴스에 SSH로 접속
```bash
ssh -i path/to/your_key_pair.pem ec2-user@your_ec2_instance_public_dns

ssh -i /Users/admin/HMG/user-mykey.pem ec2-user@ec2-13-236-93-6.ap-southeast-2.compute.amazonaws.com
```

- AWS ECR 로그인
```bash
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.ap-southeast-2.amazonaws.com
```

- Docker 이미지 풀링
```bash
docker pull <your-account-id>.dkr.ecr.ap-southeast-2.amazonaws.com/myapp:latest
```

- Jupyter Notebook 실행
```bash
docker run -d -p 8888:8888 <your-account-id>.dkr.ecr.ap-southeast-2.amazonaws.com/myapp:latest
```