#!usr/bin/env/ python3
  
from pyspark.sql import SparkSession
import random

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

if __name__ == "__main__":
    spark = SparkSession.builder.appName("PythonPi").getOrCreate()
    slices = 2
    n = 100000 * slices
    count = spark.sparkContext.parallelize(range(1, n + 1), slices).filter(inside).count()
    print(f"""
          \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n           
          estimated pi => {4.0 * count / n}
          \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
          """)
    spark.stop()

