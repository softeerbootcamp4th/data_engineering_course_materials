## python mapreduce 미션

### 컨테이너로 필요한 파일 전송

ebook을 컨테이너 안으로 전송

`docker cp ./Romeo_and_Juliet.txt master-container:/`

mapper 와 reducer 전송

`docker cp ./mapper.py master-container:/`

`docker cp ./reducer.py master-container:/`

### HDFS 디렉토리 생성

hdfs에 test용 디렉토리를 생성

`hadoop fs -mkdir -p /tmp/test/wordcount`

### 샘플 파일 생성


Romeo_and_Juliet.txt 파일을 hdfs의 wordcount 디렉토리 아래에 저장합니다.

`hadoop fs -put /Romeo_and_Juliet.txt /tmp/test/wordcount`

### Wordcount mapreduce job 생성

샘플 mapreduce를 실행합니다 wordcount는 Romeo_and_Juliet.txt 파일의 단어들을
센 후 /tmp/test_out 디렉토리에 저장합니다.

`mapred streaming -input /tmp/test/wordcount/Romeo_and_Juliet.txt -output /tmp/test/wordcount_out -mapper mapper.py -reducer reducer.py -file /mapper.py -file /reducer.py`

정상적으로 실행된다면 아래 [web ui](http://localhost:9870/)를 통해
mapreduce 작업이 돌아가고 있는 것을 확인할 수 있다.

## mapreduce 결과 확인

`hadoop fs -cat /tmp/test/wordcount_out/\*`

mapreduce 결과물은 wordcount_out 디렉토리 내에 part-r-0000* 과 같이 저장됩니다.

명령어를 통해 결과를 출력 할 수 있습니다.


## 요구 사항
1. [X] ebook을 wordcount 하는 파이썬 mapper, reducer 작성
2. 
