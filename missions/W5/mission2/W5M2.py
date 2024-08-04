from pyspark import SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import isnull, avg, min, date_format
from operator import add

INPUT_DATA_PATH = 'hdfs://spark-master:9000/user/hduser/hdfs_data/fhvhv_tripdata_2023-01.parquet'
OUTPUT_DIR_PATH = 'hdfs://spark-master:9000/user/spark_user/W5M2_output/'
EXT='parquet'

def load_dataframe(spark_session, file_path, extension):
    if extension=="csv":
        df = spark_session.read.csv(file_path)
    elif extension=="parquet":
        df = spark_session.read.parquet(file_path)
    else:
        raise NotImplementedError
    return df

if __name__=="__main__":
    spark = SparkSession.builder \
        .master('spark://spark-master:7077') \
        .appName('W5M2') \
        .config('spark.executor.memory', '8gb') \
        .config("spark.executor.cores", "5") \
        .getOrCreate()

    
    df = load_dataframe(spark, INPUT_DATA_PATH, EXT)
    
    # Data Cleaning
    df = df.na.drop('any').filter(df.driver_pay > 0).filter(df.base_passenger_fare > 0)
    
    # Data Transform
    df = df.withColumn("pickup_date", date_format(df.pickup_datetime,'yyyy-MM-dd'))
    df = df.select(df.pickup_date, df.base_passenger_fare, df.trip_miles)
    df.cache()
    
    short_trip_df = df.filter(df.trip_miles < 10)
    per_day_total_revenue_df = df.select(df.pickup_date, df.base_passenger_fare).groupBy(df.pickup_date).sum().orderBy(df.pickup_date)
    per_day_avg_trip_miles_df = df.select(df.pickup_date, df.trip_miles).groupBy(df.pickup_date).mean().orderBy(df.pickup_date)

    print("- The schema of the TLC DataFrame - \n", df.schema)
    
    # Data Actions
    ## Execute actions 
    print(short_trip_df.take(1))
    print(per_day_total_revenue_df.take(1))
    print(per_day_avg_trip_miles_df.take(1))
    
    ## Save results
    df.coalesce(1).write.csv(OUTPUT_DIR_PATH+"df")
    short_trip_df.coalesce(1).write.csv(OUTPUT_DIR_PATH+"short_trip_df")
    per_day_total_revenue_df.coalesce(1).write.csv(OUTPUT_DIR_PATH+"per_day_total_revenue_df")
    per_day_avg_trip_miles_df.coalesce(1).write.csv(OUTPUT_DIR_PATH+"per_day_avg_trip_miles_df")