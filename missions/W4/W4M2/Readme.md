## Analyze
- 2022년 7월 TLC 데이터로 진행

<br>
<br>

## Docker container run

```bash
docker-compose up -d
```

<br>
<br>

## Data Operations

- hadoop 컨테이너에서 실행
- parquet, csv 파일 hdfs에 업로드

```bash
/opt/hadoop/pi/upload.sh
```

<br>

- spark-master 컨테이너에서 실행
- TLC 데이터 분석
  - 택시 여행 평균 거리 계산
  - 택시 여행 평균 시간 계산
  - 택시 여행 피크 타임 계산
  - 강수량에 따른 평균 택시 여행 시간과 거리 계산
  - 기온에 따른 평균 택시 여행 시간과 거리 계산

```bash
jupyter nbconvert --to notebook --execute /opt/spark/pi/analyze.ipynb --output /opt/spark/pi/analyze_output
```

<br>

- 로컬에서 실행
- 실행 완료된 analyze.ipynb 로컬로 복사

```bash
docker cp spark-master:/opt/spark/pi/analyze_output.ipynb ./spark-master/analyze_output.ipynb
```

<br>

## 결과

1. 택시를 평균 17.82분 탑승하고 평균 3.69마일 이동했음
<img width="294" alt="스크린샷 2024-08-02 오후 10 01 36" src="https://github.com/user-attachments/assets/2626c0f4-ca79-4759-abe2-9f22162f97ed">


2. 18:00이 피크 타임 이였음
    - 퇴근 시간 때문이라 생각
![peak_time](https://github.com/user-attachments/assets/c2c34181-588e-47ff-8d5e-552fdbdd3e24)


3. 강한 비가 오면 짧은 거리, 짧은 시간에도 택시를 탑승함
    - 몇몇 사람들은 평소에 걸어갈 거리 비오면 택시타고 간다고 생각
    - 나역시도 그럴떄 있음
![rain](https://github.com/user-attachments/assets/e2896b49-4585-4a8c-a919-38ba23a9a759)


4. 너무 더운 날에는 짧은 거리, 짧은 시간에도 택시를 탑승함
   - 몇몇 사람들은 평소에 걸어갈 거리 너무 더우면 택시타고 간다고 생각
   - 나역시도 그럴떄 있음
![temperature](https://github.com/user-attachments/assets/c55b5700-da7d-49f4-be65-65fb8bd454b0)


## Error

- 너무 많은 데이터를 하면 java heap 메모리 초과 에러
~~~
PySpark: java.lang.OutofMemoryError: Java heap space
~~~
-> 명확한 해결방법을 아직 찾지 못했음... (현재는 데이터의 개수를 조금 줄였다.)


<br>


## 출처

날씨 출처<br>
https://www.kaggle.com/datasets/aadimator/nyc-weather-2016-to-2022

TLC 출처<br>
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
