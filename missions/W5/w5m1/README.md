# TLC 데이터셋 분석

PySpark를 사용하여 뉴욕시 택시(TLC) 데이터셋 분석하기

## 프로젝트 개요

이 프로젝트는 PySpark를 사용하여 TLC 데이터셋에서 다음과 같은 분석을 수행합니다:

- 총 여행 횟수 계산
- 총 요금 수익 계산
- 평균 여행 거리 계산
- 일별 여행 횟수와 수익 계산


## 데이터 로드 및 전처리

`read_data` 함수는 지정된 파일 경로에서 데이터를 읽어오며, Parquet 파일 형식의 데이터를 사용합니다.
데이터는 특정 날짜 범위 내에서 필터링되며, 잘못된 데이터는 `clean_data` 함수를 통해 제거됩니다.

## 분석 작업

- **총 여행 횟수 계산**: 클린된 RDD에서 총 여행 횟수를 계산합니다.
- **총 요금 수익 계산**: 각 여행의 요금, 혼잡 할증료, 공항 요금을 합산하여 총 수익을 계산합니다.
- **평균 여행 거리 계산**: 총 여행 거리의 합계를 여행 횟수로 나누어 평균 여행 거리를 계산합니다.
- **일별 여행 횟수와 수익 계산**: 여행 날짜별로 그룹화하여 일별 총 여행 횟수와 수익을 계산합니다.

## DAG 시각화

![DAG Visualization](https://github.com/user-attachments/assets/6d8a9ba6-56bf-47fd-8cd5-c06f92e96761)

위의 DAG 시각화는 Spark 작업의 실행 단계를 보여줍니다. DAG는 Parquet 파일 스캔, 데이터 병합, 필터링 및 기타 변환 작업을 포함합니다.

## 작업 실행 결과

Spark UI에서 작업 실행 결과를 확인할 수 있습니다:

![Spark Jobs](https://github.com/user-attachments/assets/2987cadc-c4c1-4b9e-96b6-51a04efeca6f)

- **작업 타임라인**: 각 작업의 실행 시간과 성공 여부를 보여줍니다.
- **완료된 작업**: 각 작업의 세부 정보와 메트릭을 확인할 수 있습니다.

## 실행 단계 분석

각 작업의 실행 단계는 아래와 같은 메트릭을 포함합니다:

![Stages for All Jobs](https://github.com/user-attachments/assets/6efa2030-5cd2-473d-8b3e-9e4f9e3abad5)
- **완료된 단계**: 작업의 각 단계에 대한 입력, 출력, 셔플 읽기/쓰기 정보.
- **단계 세부 정보**: 각 단계의 작업 수와 성공률을 보여줍니다.

## 결과 출력 예시

```plaintext
Total trip count sum: 123456
Total fee sum: 789123.45
Average Trip Distance: 5.67

Date: 2024-01-01, Total Trips: 456, Total Cost: 12345.67
Date: 2024-01-02, Total Trips: 789, Total Cost: 23456.78
...
```

## 참고 자료

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [TLC Trip Record Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
