### tlc.ipynb 코드를 전부 돌린 후 localhost:4050의 모습

<img width="1728" alt="스크린샷 2024-08-03 오후 10 30 17" src="https://github.com/user-attachments/assets/f2c132a5-bc0f-44d9-87c4-bca76c4f07c1">

- 중간에 union()이 4차례 시간을 가장 많이 소요함
- 한번 다른곳에 저장?했다면 긴 시간 4번을 1번으로 줄일 수 있을 것 같음

<br>
<br>

### tlc.ipynb 코드를 전부 돌린 후 DAG의 모습
<img width="1377" alt="스크린샷 2024-08-03 오후 10 25 36" src="https://github.com/user-attachments/assets/5657ba71-8bca-47cb-bc35-ff12a03331ed">

- 3번의 Stage가 만들어짐
  - union(), groupby(), orderby()
- 중간중간에 filter(), withColumn()등 Narrow transformation이 일어남
- 중간중간에 count(), collect()등 Action도 일어남

### 첫 Stage
<img width="1211" alt="스크린샷 2024-08-03 오후 10 30 44" src="https://github.com/user-attachments/assets/f9bb7024-3823-4999-b84c-7e01697c8ea9">

### 마지막 Stage
<img width="327" alt="스크린샷 2024-08-03 오후 10 31 03" src="https://github.com/user-attachments/assets/081160d0-be22-4231-b34c-7f473c7953df">
