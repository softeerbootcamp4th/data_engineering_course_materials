## Amazon Product Review using MapReduce

### Funtional Requirements

- 데이터 처리
    - ~~hdfs에서 입력 데이터를 올바르게 읽어야 함~~
    - ~~Mapper는 각 레코드를 처리하고 제품 ID와 등급에 관련된 Key-Value 값을 보내야 함~~
    - ~~Reducer는 Mapper의 Key-Value 결과를 집계하여 각 제품에 대한 리뷰 수 및 평균 평점을 계산하고  출력해야 함.~~
- 프로그램 실행
    - ~~MapReduce 작업은 Hadoop에서 오류없이 실행되어야 함.~~
    - ~~입력 데이터를 효율적으로 처리하고 정확한 결과를 생성해야 함.~~
- 결과 출력
    - ~~결과물은 HDFS에 저장된 txt 파일이어야 함.~~
    - ~~출력 파일의 각 줄에는 영화 ID와 평균 평점이 포함되어야 함.~~
    - ~~출력은 HDFS에서 검색하고 읽을 수 있어야 함.~~

### Mapper

- Python Script를 활용하여 Mapper 클래스를 구현하고, 이를 활용s하여 Map 작업을 수행합니다.
- csv로 저장된 파일을 한 줄씩 읽어와 제품 ID와 평점이 적힌 column Data를 추출합니다.

### Reducer

- Python Script를 활용하여 Reducer 클래스를 구현하고, 이를 활용하여 Reduce 작업을 수행합니다.
- Mapper의 결과를 받아와 각 제품에 대한 리뷰 수 및 평균 평가를 계산하여  결과를 출력합니다.

### 실행 및 결과 확인

- `download_review.sh`를 통해 MapReduce에 필요한 데이터를 다운받습니다.
    
    ![스크린샷 2024-07-19 오후 10.22.23.png](https://github.com/user-attachments/assets/4bb68a92-12e8-4b0a-8ef8-db7aace31657)
    
- `hdfs dfs -ls /amazon_review`를 통해 파일을 확인합니다.
    
    ![스크린샷 2024-07-19 오후 10.22.56.png](https://github.com/user-attachments/assets/fd1647de-ad3d-464f-ae9c-35e7e611f9d5)
    
- `product_review.sh`를 실행하여 MapReduce 과정을 수행합니다.
    
    ![스크린샷 2024-07-19 오후 10.23.23.png](https://github.com/user-attachments/assets/7b3be121-f6df-4af8-9e2f-4231c68618e7)

    
- `hdfs dfs -ls /amazon_review_wordcount`를 통해 두 개의 파티션이 생성되었습니다.
    
    ![스크린샷 2024-07-19 오후 10.24.09.png](https://github.com/user-attachments/assets/62b52c34-d4b2-4cc3-8757-471050bbbf7b)
    
- `hdfs dfs -cat /amazon_review_wordcount/part-00000`를 통해 결과를 확인합니다.

    ![스크린샷 2024-07-19 오후 10.26.00.png](https://github.com/user-attachments/assets/afc0495e-c57d-49ed-9742-bc047716e5c1)
### Reference Link

- Amazon Review Link: https://amazon-reviews-2023.github.io/