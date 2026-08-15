

import os
import sys
import time

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


def spark_ui_example(df):
    df = df.withColumn("score_range",
                       F.concat((F.floor(F.col("score") / 5) * 5).cast("integer"), F.lit("점 대")))
    df = df.withColumn("passed",
                       F.when(F.col("score") >= 75, "pass").otherwise("fail"))
    df = df.filter(df["passed"] == "pass")

    print('==== TEST 1 ====')
    df.limit(20).show()
    print('==== TEST 2 ====')
    df.filter(df["score"] == 80.0).show()

    print(f'passed count: {df.count()}')


if __name__ == '__main__':
    spark = SparkSession.builder.appName("04_04_example").getOrCreate()
    print(f"Spark UI URL: {spark.sparkContext.uiWebUrl}")

    df_path = os.path.join(parent_dir, "02_DataFrame_Basics", "02_03_example_2.csv")
    df = spark.read.csv(df_path, header=True, inferSchema=True)

    print('==== SPARK UI EXAMPLE ====')
    spark_ui_example(df)

    time.sleep(24 * 60 * 60)
    spark.stop()