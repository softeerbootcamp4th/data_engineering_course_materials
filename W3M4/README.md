# Twitter Sentiment Analysis using MapReduce

## Directory

```
+ twitter_sentiment_analysis_using_mapreduce
    - tweets_mapper.py
    - tweets_reducer.py
    - tweets_mapred_script.sh
    - tweets.csv
    - tweets_sample.csv (디버그용 작은 샘플)
    + tweets_output
        - _SUCCESS
        - part-00000 (결과)
    + node
        - Dockerfile
        - hadoop-3.3.6.tar.gz
        - start-hadoop.sh
        + config
            - core-site.xml
            - hdfs-site.xml
            - mapred-site.xml
            - yarn-site.xml
    - docker-compose.yml
```

```
# container directory - 컨테이너 로컬에선 temp 폴더만 사용

+ temp
    - tweets.csv
    - tweets_mapper.py
    - tweets_reducer.py
    + tweets_output (mapreduce 작업 이후 생성된 디렉터리를 컨테이너 로컬 파일 시스템으로 가져옴)
        - _SUCCESS
        - part-00000
```

```
# hdfs directory 

+ tweets_dir
    - tweets.csv
+ tweets_output (mapred 작업 후 생성 - 미리 존재하면 안됨 !)
    - _SUCCESS
    - part-00000
```

### tweets_mapper.py

```python
#!/usr/bin/env python3

import csv
import sys
import re

def classify(text, positive_keywords, negative_keywords):
    # lower
    text = text.lower()
    # divide
    words = re.findall(r'\w+', text)
    positive_matches = any(key in words for key in positive_keywords)
    negative_matches = any(key in words for key in negative_keywords)
    if positive_matches and not negative_matches:
        return 'positive'
    elif negative_matches and not positive_matches:
        return 'negative'
    else:
        return 'neutral'

def main():

    # predefined keywords !

    positive_keywords = {"happy", "great", "love", "excellent", "good"}
    negative_keywords = {"sad", "bad", "hate", "terrible", "worse"}
    
    reader = csv.reader(sys.stdin)
    for row in reader:
        tweet_text = row[5]
        sentiment = classify(tweet_text, positive_keywords, negative_keywords)
        print(f'{sentiment}\t1')

if __name__ == "__main__":
    main()
```

- mapper에서 에러 발생을 확인 (yarn 8088 웹 인터페이스 참고, application 확인)
- `cat tweets.csv | python3 tweets_mapper.py | sort | python3 tweets_reducer.py`
    - 모든 라인 전수조사했지만 로직에는 문제가 없음을 확인
- `#!/usr/bin/env python3` <= 필수 !!!!!!!!!!(3시간은 소중합니다)
    - #! 은 주석이 아니라 이 자체가 하나의 기호(SheBang)
    - #! 은 2 Byte 의 매직 넘버 (Magic Number) 로 스크립트의 맨 앞에서 이 파일이 어떤 명령어 해석기의 명령어 집합인지를 시스템에 알려주는 역할

### tweets_reducer.py

```python
#!/usr/bin/env python3

import sys

def read_input(file):
    for line in file:
        yield line.strip().split('\t')

def main():
    current_word = None
    current_count = 0
    word = None

    data = read_input(sys.stdin)
    for word, count in data:
        try:
            count = int(count)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f'{current_word}\t{current_count}')
            current_count = count
            current_word = word

    if current_word == word:
        print(f'{current_word}\t{current_count}')

if __name__ == "__main__":
    main()
```

## tweets_mapred_script.sh

- 과정 요약
    
    1. 컨테이너 내부로 tweets, mapper, reducer 복사
    2. HDFS에 tweets 업로드
    3. MapReduce 실행
    4. 결과를 호스트 머신으로 가져옴


```sh
#!/bin/bash


##### 컨테이너 내부로 tweets, mapper, reducer 복사

# tweets.csv 컨테이너 내부로 복사
docker cp tweets.csv hadoop-master:/temp

# mapper, reducer 컨테이너 내부로 복사
docker cp tweets_mapper.py hadoop-master:/temp/tweets_mapper.py 
docker cp tweets_reducer.py hadoop-master:/temp/tweets_reducer.py

### 해당 파일들을 실행 가능한 파일로 변경 (chmod +x)
### !!!!!! #!/usr/bin/env python3 필수 !!!!!!!!
docker exec -it hadoop-master sudo chmod +x /temp/tweets_mapper.py /temp/tweets_reducer.py

##### HDFS에 tweets 옮기기

# hdfs에 tweets directory 생성
docker exec -it hadoop-master hdfs dfs -mkdir -p /tweets_dir

# 해당 디렉토리로 tweets 옮기기
docker exec -it hadoop-master hdfs dfs -put /temp/tweets.csv /tweets_dir


##### MapReduce 작업 실행
# tweets_output 디렉토리는 생성됨
docker exec -it hadoop-master hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /tweets_dir/tweets.csv \
  -output /tweets_output \
  -mapper tweets_mapper.py \
  -reducer tweets_reducer.py \
  -file /temp/tweets_mapper.py \
  -file /temp/tweets_reducer.py


##### 호스트 머신으로 결과 가져오기

# 컨테이너 로컬 파일 시스템의 /temp의 소유권을 hadoopuser로 변경
docker exec -it hadoop-master sudo chown hadoopuser:hadoopuser temp

# HDFS의 tweets_output 디렉토리를 컨테이너의 로컬 디렉토리로 가져옴
docker exec -it hadoop-master hdfs dfs -get /tweets_output /temp

# 결과를 호스트 머신(Mac)의 현재 폴더로 가져옴
docker cp hadoop-master:/temp/tweets_output .
```
