# Apache Spark Standalone Cluster using Docker

## 구성 요소
- **Dockerfile**: Spark와 필요한 종속성을 포함하는 Docker 이미지 빌드
- **docker-compose.yml**: 마스터와 워커 노드를 설정하고 네트워크를 구성
- **entrypoint.sh**: 컨테이너 시작 시 마스터 또는 워커 노드를 초기화
- **submit.sh**: Spark 작업을 클러스터에 제출

## 사용 방법

1. **Docker 이미지 빌드**

```bash
docker build -t spark-image .
```

2. **Docker Compose를 사용하여 클러스터 시작**
```bash
docker-compose up -d
```

3. **Spark 작업 제출**

```bash
docker exec -it spark-master /bin/bash
/opt/spark/submit.sh
```

4. **결과 확인**
    ### 작업 실행 후, 마스터 노드의 로그를 통해 결과를 확인할 수 있습니다:
```bash
docker logs spark-master
```
    ### 로그에서 "Pi is roughly 3.141320"와 같은 메시지를 찾아 파이(π) 값을 확인합니다.

5. **Web UI 접속해 확인**
    - 마스터 UI: `http://localhost:8080`
    - 작업 UI: `http://localhost:4040` (작업 실행 중에만 접근 가능)

6. **클러스터 종료**

```bash
docker-compose down
```

## 문제 발생 시 로그 확인

```bash
docker logs <container_name>
```