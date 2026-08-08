
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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

    print('==== 2. 특정 컬럼의 데이터 추출, 정렬하기 ====')

    # 특정 컬럼의 데이터 추출하기
    print("2-1. 특정 컬럼의 데이터 추출하기")
    df.select('name').show()
    df.select(df['name']).show()
    df.select(df.name).show()

    # 특정 조건을 만족시키는 데이터 추출하기
    print("2-2. 특정 조건을 만족시키는 데이터 추출하기")
    df.filter(df['age'] >= 25).show()
    df.filter(df.age >= 25).show()
    df.filter('age >= 25').show()
    df.where('age >= 25').show()

    # 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)
    print("2-3. 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)")
    cond1 = col('age') >= 25
    cond2 = col('used_as_character')
    df.filter(cond1 & cond2).show()
    df.where(cond1 & cond2).show()

    # 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)
    print("2-4. 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)")
    df.filter(cond1 | cond2).show()
    df.where(cond1 | cond2).show()

    # SQL의 LIKE 구문처럼 사용하기
    print("2-5. 응용: SQL의 LIKE 구문처럼 사용하기")
    df.where("name LIKE '%N%' OR name LIKE '%n%'").show()

    # 특정 컬럼 값 기준 데이터 정렬하기
    print("2-6. 특정 컬럼 값 기준 데이터 정렬하기")
    df.orderBy("Age", ascending=True).show()
    df.orderBy(col("Age"), ascending=False).show()
    df.orderBy(col("Age").desc()).show()
    df.orderBy(col("Age"), col("name").desc()).show()
