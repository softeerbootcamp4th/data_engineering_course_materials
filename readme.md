# sentiment

**Mapper**

- csv로 저장된 파일에서 review가 적힌 Data 추출
- 추출한 데이터내 사전에 정의한 감정, 긍정 / 부정 / 중립 으로 분류하는 작업
- {긍정 / 부정 / 중립 : 1} 형식으로 Key-Value Mapping 작업

**Reducer**

- Mapper의 결과를 받아와 각 감정 카테고리에 대한 빈도 카운트

### 파일업로드

```python
hdfs dfs -put /usr/local/hadoop/sentiment.csv /input

/usr/local/hadoop/sentiment.txt
```

### 맵리듀스 실행

```python
/usr/local/hadoop/sbin/mapreducer4.sh
```

### 결과출력
![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6ec20228-be51-4a9f-a5f2-85b8c55a6714/276c4ce5-a62c-4484-887b-b1b249f2ac9c/Untitled.png)