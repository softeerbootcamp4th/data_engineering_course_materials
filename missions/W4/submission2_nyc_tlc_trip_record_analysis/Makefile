down:
	docker compose down 
	docker rmi submission2_nyc_tlc_trip_record_analysis-spark-master:latest
	docker rmi submission2_nyc_tlc_trip_record_analysis-spark-worker1:latest
	docker rmi submission2_nyc_tlc_trip_record_analysis-spark-worker2:latest
	docker rmi submission2_nyc_tlc_trip_record_analysis-spark-history:latest
	docker rmi submission2_nyc_tlc_trip_record_analysis-hadoop-single:latest

down_all:
	make down
	docker rmi spark_base:latest

down_volume:
	docker volume rm submission2_nyc_tlc_trip_record_analysis_spark-logs
	docker volume rm submission2_nyc_tlc_trip_record_analysis_spark-master
	docker volume rm submission2_nyc_tlc_trip_record_analysis_spark-worker1
	docker volume rm submission2_nyc_tlc_trip_record_analysis_spark-worker2
	docker volume rm submission2_nyc_tlc_trip_record_analysis_hadoop-single

up: 
	docker build -t spark_base spark_base
	docker compose up -d
