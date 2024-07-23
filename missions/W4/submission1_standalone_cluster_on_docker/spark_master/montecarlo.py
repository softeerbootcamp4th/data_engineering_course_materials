from pyspark.sql import SparkSession
import random


def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1


if __name__ == "__main__":
    spark = SparkSession.builder.appName("MonteCarloEstimation").getOrCreate()
    slices = 100
    n = 100000 * slices
    count = spark.sparkContext.parallelize(
        range(1, n + 1), slices).filter(inside).count()
    pi = 4.0 * count / n
    print(f"Pi is roughly {pi}")
    spark.stop()
