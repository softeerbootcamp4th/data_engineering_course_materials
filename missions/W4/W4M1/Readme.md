## Docker image build

```bash
docker-compose build
```

<br>
<br>

## Docker container run

```bash
docker-compose up -d
```

<br>
<br>

## Data Operations

- 파이썬 파일 실행

```bash
/opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/scripts/pi.py
```

<img width="220" alt="스크린샷 2024-07-25 오후 6 09 25" src="https://github.com/user-attachments/assets/34fdf43c-dc78-4c05-be95-b587fbf0e911">

<img width="1728" alt="스크린샷 2024-07-25 오후 6 10 02" src="https://github.com/user-attachments/assets/8cc44f71-56a9-40a1-997c-14d6fdefac08">

<img width="1728" alt="스크린샷 2024-07-25 오후 6 10 11" src="https://github.com/user-attachments/assets/a9b7cea1-9af8-4f37-91b8-87929bfd495e">

<br>

## Error

- 아래와 같이 쓰면 로컬에서 돌아감 - worker 노드를 쓰지 않음, Web에 완료되었다고 뜨지 않음

```bash
/opt/spark/bin/spark-submit /opt/spark/scripts/pi.py
```

<br>
