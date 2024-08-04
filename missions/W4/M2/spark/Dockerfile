# spark/Dockerfile
FROM bde2020/spark-base:2.4.0-hadoop2.7

COPY start-spark.sh /

RUN chmod +x /start-spark.sh

CMD ["/start-spark.sh"]
