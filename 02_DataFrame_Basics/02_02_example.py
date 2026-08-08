
import os
import sys

from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"


if __name__ == '__main__':
    spark = SparkSession.builder.appName("02_02_example").getOrCreate()
    df = spark.read.csv("02_02_example.csv", header=True, inferSchema=True)

    print('==== 1. 데이터셋 정보 보기 ====')

    # df 전체 보기
    print("1-1. df 전체 보기")
    df.show()

    # df의 위쪽 5개의 row만 보기
    print("1-2. df의 위쪽 5개의 row만 보기")
    df.limit(num=5).show()

    # df의 위쪽 1개의 row만 보기
    print("1-3. df의 위쪽 1개의 row만 보기")
    row = df.head()
    print(row)

    # df의 위쪽 3개의 row만 list 형태로 보기
    print("1-4. df의 위쪽 3개의 row만 list 형태로 보기")
    row = df.head(3)
    print(row)

    # df의 행 개수, 열 개수 구하기
    print("1-5. df의 행 개수, 열 개수 구하기")
    row_count = df.count()
    column_count = len(df.columns)
    print(f'행 개수 {row_count}, 열 개수 {column_count}')
