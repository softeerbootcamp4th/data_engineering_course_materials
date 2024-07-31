# 요구사항
1. [ ] mapper.py : predefined keywords를 기반으로 트윗을 positive, negative, or neutral로 분류.
2. [ ] reducer.py : positive, negative, or neutral 각각의 count 출력 
3. [ ] 결과 확인 할 수 있어야 함.
4. [ ] 
5. [ ] 
6. [ ] 


# 사용법

W3M2에서 빌드한 base,master, worker 이미가 있다고 가정한다.


하둡 클러스터를 배포한다.

`docker-compose up -d`

필요한 파일을 다운로드 하고, 마스터 노드 컨테이너로 전송.

[tweets.csv 다운로드 링크
](https://www.kaggle.com/datasets/kazanova/sentiment140)


`docker cp ./mapper.py master-container:/opt/hadoop/`

`docker cp ./reducer.py master-container:/opt/hadoop/`

`docker cp ./tweets.csv master-container:/opt/hadoop/`

`docker cp ./afinn.sh master-container:/opt/hadoop/`

마스터 컨테이너 터미널 접속(아래 명령어들은 마스터 컨테이너 터미널에 입력해야함)

`docker exec -it master-container bash`

tweets.csv를 hdfs에 업로드

`hdfs dfs -put ./tweets.csv /tweets.csv`

`hdfs dfs -rm -r /hadoop/output/sentiments/`

afinn.sh를 실행

`sh ./afinn.sh`

mapreduce job 실행.

`mapred streaming -mapper mapper.py -reducer reducer.py -input /tweets.csv -output /hadoop/output/sentiments -file ./mapper.py -file ./reducer.py -file ./sentiment_env.zip`

결과 확인

`hdfs dfs -cat /hadoop/output/sentiments/\*`