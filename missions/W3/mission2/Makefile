clean:
	docker stop hadoop-master
	docker stop hadoop-slave1
	docker stop hadoop-slave2
	docker rm hadoop-master
	docker rm hadoop-slave1
	docker rm hadoop-slave2
	docker rmi mission2-multi_node_hadoop_cluster
	docker volume prune -a