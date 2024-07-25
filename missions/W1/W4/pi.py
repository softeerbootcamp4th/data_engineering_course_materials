from pyspark.sql import SparkSession
import time
import os

spark = SparkSession.builder.appName("PythonPi").getOrCreate()

partitions = 2
n = 100000 * partitions

def f(_):
    from random import random
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x**2 + y**2 <= 1 else 0

count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(lambda a, b: a + b)
pi = 4.0 * count / n

print("Pi is roughly %f" % pi)

# 결과를 파일로 저장

timestamp = time.strftime("%Y%m%d%H%M%S")
output_path = "/usr/local/spark/work-dir/montecarlo_result_{}.csv".format(timestamp)

with open(output_path, "w") as f:
    f.write("Pi is roughly %f\n" % pi)

# 파일이 생성되었는지 확인
if os.path.exists(output_path):
    print(f"Result file created: {output_path}")
else:
    print("Failed to create result file")

spark.stop()
