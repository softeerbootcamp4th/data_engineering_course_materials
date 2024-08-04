### tlc.ipynb 코드를 전부 돌린 후 localhost:4050의 모습

<img width="1728" alt="스크린샷 2024-08-04 오후 4 10 28" src="https://github.com/user-attachments/assets/b7f15077-5076-44c1-87be-034f32d350b7">


<br>
<br>

### tlc.ipynb 코드를 전부 돌린 후 DAG의 모습

<img width="675" alt="스크린샷 2024-08-04 오후 4 12 15" src="https://github.com/user-attachments/assets/21a6ab62-fb2d-4a6e-b4b7-fe0ed871a19d">

- 3개의 Stage가 만들어짐
  - union(), reduceByKey(), sortByKey() <- Wide transformation
  - 대체로 시간이 오래 걸림
- 중간중간에 filter(), map() Narrow transformation이 일어남
- 중간중간에 count(), sum(), collect() Action도 일어남
