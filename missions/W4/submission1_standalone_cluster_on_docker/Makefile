down:
	docker compose down 
	docker rmi submission1_standalone_cluster_on_docker-spark-master:latest
	docker rmi submission1_standalone_cluster_on_docker-spark-worker1:latest
	docker rmi submission1_standalone_cluster_on_docker-spark-worker2:latest
	docker rmi submission1_standalone_cluster_on_docker-spark-history:latest

down_all:
	make down
	docker rmi spark_base:latest

down_volume:
	docker volume rm submission1_standalone_cluster_on_docker_spark-logs
	docker volume rm submission1_standalone_cluster_on_docker_spark-master
	docker volume rm submission1_standalone_cluster_on_docker_spark-worker1
	docker volume rm submission1_standalone_cluster_on_docker_spark-worker2

up: 
	docker build -t spark_base spark_base
	docker compose up -d
