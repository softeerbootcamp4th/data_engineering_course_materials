from operator import add

from pyspark import SparkFiles
from pyspark.sql import SparkSession


if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("WordCount")\
        .getOrCreate()

    filepath = SparkFiles.get('pg74102.txt')
    with open(filepath, 'r') as f:
        data = f.readlines()

    rdd = spark.sparkContext.parallelize(data)
    lines = rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()

    df = spark.createDataFrame(
        output,
        schema='word string, count int',
    )

    df.show()

    df.write.csv('userdata/output_wordcount')

    spark.stop()
