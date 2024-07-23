## Building Spark Standalone Cluster on Docker

### Project Structure

```
📦submission1_standalone_cluster_on_docker
┣ 📂 spark_base
┃ ┣ 📜 Dockerfile
┃ ┣ 📜 spark-defaults.conf
┃ ┣ 📜 spark-env.sh
┣ 📂 spark_history
┃ ┣ 📜 Dockerfile
┃ ┣ 📜 history_entrypoint.sh
┣ 📂 spark_master
┃ ┣ 📜 Dockerfile
┃ ┣ 📜 master_entrypoint.sh
┃ ┣ 📜 montecarlo.py
┃ ┣ 📜 spark_submit_example.sh
┣ 📂 spark_worker
┃ ┣ 📜 Dockerfile
┃ ┣ 📜 worker_entrypoint.sh
┣ 📜 docker-compose.yml
┣ 📜 Makefile
┗ 📜 README.md
```

### Usage

- build and run container
    ```bash
    make up
    ```

- stop and remove container
    ```bash
    make down
    ```

- remove container with base image
    ```bash
    make down_all
    ```

- remove volume
    ```bash
    make down_volume
    ```

### spark-submit 
```bash
sh examples/test/spark_submit_example.sh
```

### Result
- spark_submit result
    <img src="https://github.com/user-attachments/assets/2ab1c014-13fa-4459-87af-78f66f133f96">

- check spark status in webUI(localhost:8080) and logs(localhost:18080) 
    <img src="https://github.com/user-attachments/assets/bce67c38-4dc1-4d7a-a57f-8b3b06227bcb">