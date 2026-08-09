
import os
import sys
import shutil

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_file_path))

print(f'current_file_path: {current_file_path}')
print(f'parent_dir: {parent_dir}')

os.environ["HADOOP_HOME"] = os.path.join(parent_dir, "hadoop")
os.environ["PATH"] += os.pathsep + os.path.join(parent_dir, r"hadoop\bin")


def partitioning_example(df, spark):
    output_dir = "03_02_partitioning_example/output"

    # partition 데이터 쓰기
    print('write ...')
    df_with_partition = (df
                         .withColumn("id_digit_2", F.substring(F.col("id"), 6, 1))
                         .withColumn("id_digit_1", F.substring(F.col("id"), 7, 1)))
    df_with_partition.limit(20).show()

    (df_with_partition.write
        .mode("overwrite")
        .partitionBy("id_digit_2", "id_digit_1")
        .parquet(output_dir))

    # partition 된 데이터 읽기
    print('read ...')
    df = spark.read.parquet(os.path.join(output_dir, "id_digit_2=1", "id_digit_1=2"))
    df.limit(20).show()


def bucketing_example(df, spark):
    table_name = "03_02_bucketing_example"
    prime_number = 17

    # 기존 테이블 및 warehouse 제거
    spark.sql(f"DROP TABLE IF EXISTS {table_name}")

    warehouse_dir = f'spark-warehouse/{table_name}'
    if os.path.exists(warehouse_dir):
        shutil.rmtree(warehouse_dir)

    # bucket 데이터 쓰기
    print('write ...')
    df_with_id_column = (df
                         .withColumn("id_column", F.substring(F.col("id"), 2, 6)))
    df_with_id_column.limit(20).show()

    (df_with_id_column.write
        .mode("overwrite")
        .bucketBy(prime_number, "id_column")
        .saveAsTable(table_name))

    # bucket 된 데이터 읽기
    print('read ...')
    df = spark.read.table(table_name)
    df = df.withColumn("mod", F.col("id_column").cast("integer") % prime_number)
    df.limit(20).show()


if __name__ == '__main__':
    spark = SparkSession.builder.appName("03_02_example").getOrCreate()
    df_path = os.path.join(parent_dir, "02_DataFrame_Basics", "02_03_example_2.csv")
    df = spark.read.csv(df_path, header=True, inferSchema=True)

    print('==== PARTITIONING EXAMPLE ====')
    partitioning_example(df, spark)

    print('==== BUCKETING EXAMPLE ====')
    bucketing_example(df, spark)
