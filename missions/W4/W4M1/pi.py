# pi.py
from pyspark.sql import SparkSession
import random


def inside(p):
    x, y = random.random(), random.random()
    return x * x + y * y < 1


spark = SparkSession.builder.appName("Pi Estimation").getOrCreate()

num_samples = 10000000
count = spark.sparkContext.parallelize(range(0, num_samples)).filter(inside).count()
pi = 4 * count / num_samples
print(f"Pi is roughly {pi}")

# 결과를 CSV 파일로 저장
df = spark.createDataFrame([(pi,)], ["pi_estimate"])
df.write.csv("file:///opt/spark/output/pi_estimate.csv")

spark.stop()
