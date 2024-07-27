from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Python_Pi").getOrCreate()

    partitions = 2
    n = 100000 * partitions

    def f(_):
        import random
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        return 1 if x ** 2 + y ** 2 < 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(lambda a, b: a + b)
    print("Pi is ~~ %f" % (4.0 * count / n))

    spark.stop()
