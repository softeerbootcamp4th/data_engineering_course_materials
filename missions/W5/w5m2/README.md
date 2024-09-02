# TLC 데이터셋 스파크 분석

PySpark를 사용하여 뉴욕시 택시(TLC) 데이터셋 분석하기

## 데이터 

- **픽업 시간** (`tpep_pickup_datetime`): 여행 시작 시간
- **하차 시간** (`tpep_dropoff_datetime`): 여행 종료 시간
- **승객 수** (`passenger_count`): 여행 중 승객 수
- **여행 거리** (`trip_distance`): 여행 거리
- **총 요금** (`total_amount`): 총 여행 요금
- **혼잡 추가 요금** (`congestion_surcharge`): 혼잡 때 추가되는 요금
- **공항 요금** (`airport_fee`): 공항으로 가는 여행에 부과되는 요금

## 데이터 전처리 및 분석

- 데이터 클린징: 비현실적인 데이터(예: 승객 수가 0)의 제거
- 기본적인 통계 계산: 평균, 최대, 최소 등
- 날씨 데이터와의 결합하여 최종 데이터 추출


## 분석 결과

- 21년도 1월부터 3월까지 총 여행 횟수 및 승객이 2명 이상인 여행의 횟수
- 21년도 1월부터 3월까지 총 수익
- 21년도 1월부터 3월까지 평균 여행 시간
- 21년도 1월부터 3월까지 강수 여부 및 온도에 따른 여행 기간 및 요금  

## 스파크 UI 스크린샷

![Spark Jobs](https://github.com/user-attachments/assets/3baf6a7f-dc6c-42ba-b9b1-2ebaa486775c)
![DAG Visualization](https://github.com/user-attachments/assets/7704b75d-eb41-4418-baa8-f0f647992ffa)
![Stages for All Jobs](https://github.com/user-attachments/assets/a54a6421-b8ef-48f0-a3f7-08abb751732b)

## 참고 문헌

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)