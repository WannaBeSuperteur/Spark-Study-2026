
import os
import sys

from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_file_path))

os.environ["HADOOP_HOME"] = os.path.join(parent_dir, "hadoop")
os.environ["PATH"] += os.pathsep + os.path.join(parent_dir, r"hadoop\bin")

print(f'current_file_path: {current_file_path}')
print(f'parent_dir: {parent_dir}')


if __name__ == '__main__':
    spark = SparkSession.builder.appName("03_02_example").getOrCreate()
    df_path = os.path.join(parent_dir, "02_DataFrame_Basics", "02_03_example_2.csv")
    df = spark.read.csv(df_path, header=True, inferSchema=True)

    print('==== COALESCE EXAMPLE ====')
    (df.coalesce(100)
     .write
     .format("parquet")
     .mode("overwrite")
     .save("04_01_coalesce_example/output"))

    print('==== REPARTITION EXAMPLE ====')
    (df.repartition(100)
     .write
     .format("parquet")
     .mode("overwrite")
     .save("04_01_repartition_example/output"))
