## Twitter Sentiment Analysis Using MapReduce

### Funtional Requirements

- 데이터 처리
    - ~~hdfs에서 입력 데이터를 올바르게 읽어야 함~~
    - ~~Mapper는 Twitt을 처리하고, 감정 분류를 위해 Key-Value 값을 보내야 함~~
    - ~~Reducer는 Mapper의 Key-Value 결과를 집계하여 감정 카테고리에 대한 총 개수를 출력해야 함.~~
- 프로그램 실행
    - ~~MapReduce 작업은 Hadoop에서 오류없이 실행되어야 함.~~
    - ~~입력 데이터를 효율적으로 처리하고 정확한 결과를 생성해야 함.~~
- 결과 출력
    - ~~결과물은 HDFS에 저장된 txt 파일이어야 함.~~
    - ~~출력 파일에는 ‘\t’ or ‘ ‘으로 구분된 단어와 해당 개수가 포함되어야 함.~~
    - ~~출력은 HDFS에서 검색하고 읽을 수 있어야 함.~~

### Mapper

- Python Script를 활용하여 Mapper 클래스를 구현하고, 이를 활용하여 Map 작업을 수행합니다.
- csv로 저장된 파일을 한 줄씩 읽어와 review가 적힌 column Data를 추출합니다.
- 추출한 데이터(텍스트) 내 사전에 정의한 긍정/부정 텍스트 여부를 판단하고, 긍정 / 부정 / 중립 총 세가지로 분류하는 작업을 진행합니다.
- {긍정 / 부정 / 중립 : 1} 형식으로 Key-Value Mapping 과정을 수행합니다.

### Reducer

- Python Script를 활용하여 Reducer 클래스를 구현하고, 이를 활용하여 Reduce 작업을 수행합니다.
- Mapper의 결과를 받아와 각 감정 카테고리에 대한 총 개수를 집계합니다.

### 실행 및 결과 확인

- `hdfs dfs -put sentiment_analysis.csv /sentiment`를 통해 파일을 업로드 합니다.
    
    ![스크린샷 2024-07-19 오후 4.56.56.png](https://github.com/user-attachments/assets/e2112f86-d9a8-40ec-b219-8131a362a9e7)
    
- `sentiment_analysis.sh`를 통해 MapReduce 작업을 수행합니다.
    
    ![스크린샷 2024-07-19 오후 4.58.47.png](https://github.com/user-attachments/assets/a7e52757-22db-41a8-bd61-3bb13d57c342)
    
- `hdfs dfs -ls /sentiment_wordcount`를 통해 2개의 파티션 파일이 생성되었습니다.
    
    ![스크린샷 2024-07-19 오후 5.08.08.png](https://github.com/user-attachments/assets/0406adfa-c40f-4242-adda-dc5c97b49a71)
    
- `hdfs dfs -cat /sentiment_wordcount/part-00000`을 통해 결과를 출력했습니다.

    ![스크린샷 2024-07-19 오후 5.10.49.png](https://github.com/user-attachments/assets/9e2bcd2d-8657-4875-aa03-cc672ab9e34b)