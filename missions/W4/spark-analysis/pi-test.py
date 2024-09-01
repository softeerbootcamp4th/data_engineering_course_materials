import sys
from random import random
from operator import add

from pyspark.sql import SparkSession

if __name__ == "__main__":
    """
        Usage: pi [partitions] [output_path]
    """
    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .getOrCreate()

    # 파티션 개수는 첫 번째 명령줄 인자로 받습니다. 기본값은 2입니다.
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    # 출력 경로는 두 번째 명령줄 인자로 받습니다.
    output_path = sys.argv[2]

    n = 100000 * partitions

    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    pi_value = 4.0 * count / n
    print("Pi is roughly %f" % pi_value)

    # 결과를 데이터프레임으로 변환합니다.
    result_df = spark.createDataFrame([(pi_value,)], ["Pi Value"])

    # 결과를 지정된 출력 경로에 CSV 형식으로 저장합니다.
    result_df.write.mode("overwrite").parquet(output_path)

    spark.stop()
