from pyspark.sql import SparkSession
from pyspark.sql.functions import concat, lit

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("HDFS Read/Write Example") \
    .getOrCreate()

# HDFS로부터 데이터 읽기
input_path = "hdfs:///user/root/text.txt"
df = spark.read.text(input_path)

# 데이터 처리: 모든 라인의 앞에 'Processed: '를 추가
processed_df = df.withColumn("value", concat(lit("Processed: "), df["value"]))

# 처리된 데이터를 HDFS에 저장
output_path = "hdfs:///user/root/output/"
processed_df.write.mode("overwrite").text(output_path)

# Spark 세션 종료
spark.stop()
