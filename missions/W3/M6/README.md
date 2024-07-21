[아마존 리뷰 다운로드 링크](https://amazon-reviews-2023.github.io/)

W3M2에서 빌드한 base,master, worker 이미가 있다고 가정한다.

하둡 클러스터를 배포한다.

`docker-compose up -d`

필요한 파일을 다운로드 하고, 마스터 노드 컨테이너로 전송.
예시에서는 All_Beauty.jsonl 사용했음

`docker cp ./mapper.py master-container:/opt/hadoop/`

`docker cp ./reducer.py master-container:/opt/hadoop/`

`docker cp ./All_Beauty.jsonl master-container:/opt/hadoop/dataset.json`


마스터 컨테이너 터미널 접속(아래 명령어들은 마스터 컨테이너 터미널에 입력해야함)

`docker exec -it master-container bash`

dataset.json를 hdfs에 업로드

`hdfs dfs -put ./dataset.json /dataset.json`

`hdfs dfs -rm -r /hadoop/output/amazon/`


mapreduce job 실행.

`mapred streaming -mapper mapper.py -reducer reducer.py -input /dataset.json -output /hadoop/output/amazon -file ./mapper.py -file ./reducer.py`

결과 확인

`hdfs dfs -cat /hadoop/output/amazon/\*`

