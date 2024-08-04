from pyspark import SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import isnan, when, count, col, isnull, avg, min
import pyspark.sql.functions as F
from operator import add

INPUT_FILE_PATH = 'hdfs://spark-master:9000/user/hduser/hdfs_data/fhvhv_tripdata_2023-01.parquet'
OUTPUT_DIR_PATH = 'hdfs://spark-master:9000/user/spark_user/W5M1_output/'
EXT='parquet'
NAME="TLC-2023-01"

def load_data_rdd(spark_session, file_path, extension, name):
    if extension=="csv":
        data_rdd = spark_session.read.csv(file_path).rdd
    elif extension=="parquet":
        data_rdd = spark_session.read.parquet(file_path).rdd
    else:
        raise NotImplementedError
    data_rdd.setName(name)
    return data_rdd


def remove_row_w_none_val(row):
    for val in row:
        if val is None:
            return
    return row


def remove_non_positive_fare(row):
    if row.base_passenger_fare > 0:
        return row
    else:
        return


def extract_and_convert_relevant_columns(row):
    return Row(pickup_datetime = row.pickup_datetime.date(), trip_miles = row.trip_miles, base_passenger_fare = row.base_passenger_fare)

if __name__=="__main__":
    spark = SparkSession.builder \
        .master('spark://spark-master:7077') \
        .appName('W5M1_script') \
        .config('spark.executor.memory', '6gb') \
        .config("spark.executor.cores", "5") \
        .getOrCreate()
    
    # Data Loading, Data Cleaning and Transformation
    data_rdd = load_data_rdd(spark, INPUT_FILE_PATH, EXT, NAME) \
                .filter(lambda row: remove_row_w_none_val(row)) \
                .filter(lambda row: remove_non_positive_fare(row)) \
                .map(lambda row: extract_and_convert_relevant_columns(row))
                
    # Aggregation Logic
    total_number_of_trips = data_rdd.count()
    total_revenue = data_rdd.map(lambda row: row.base_passenger_fare).reduce(add) 
    average_trip_distance = data_rdd.map(lambda row: row.trip_miles).mean()
    number_of_trips_per_day = data_rdd.map(lambda row: (row.pickup_datetime, 1)) \
                            .reduceByKey(add) \
                            .sortByKey(lambda row: row.pickup_datetime)
    total_revenue_per_day = data_rdd.map(lambda row: (row.pickup_datetime, row.base_passenger_fare)) \
                            .reduceByKey(add) \
                            .sortByKey(lambda row: row.pickup_datetime)
                            
    # Data Output
    # Save the output as text
    result = spark.sparkContext.parallelize([
        f"total_number_of_trips, {total_number_of_trips}",
        f"total_revenue, {total_revenue}",
        f"average_trip_distance, {average_trip_distance}",
    ])
    result.coalesce(1).saveAsTextFile(OUTPUT_DIR_PATH + "result.txt")
    
    # Save the output as pickle object
    number_of_trips_per_day.coalesce(1) \
        .saveAsPickleFile(OUTPUT_DIR_PATH + "number_of_trips_per_day")
    total_revenue_per_day.coalesce(1) \
        .saveAsPickleFile(OUTPUT_DIR_PATH + "total_revenue_per_day")
    
    # Display aggregation results
    print(f"total_number_of_trips: {total_number_of_trips} miles")  
    print(f"total_revenue: {round(total_revenue, 2)}$")
    print(f"average_trip_distance: {round(average_trip_distance, 2)} miles")
    print("-- number_of_trips_per_day --\n")
    number_of_trips_per_day.take(20)
    print("-- total_revenue_per_day --\n")    
    total_revenue_per_day.take(20)