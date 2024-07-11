git clone https://github.com/nothingmin/softeer
docker build --platform linux/amd64 -t softeer-w2m6 .
docker tag softeer-w2m6:latest 571495482396.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-w2m6:latest
docker push 571495482396.dkr.ecr.ap-northeast-2.amazonaws.com/softeer-w2m6:latest
