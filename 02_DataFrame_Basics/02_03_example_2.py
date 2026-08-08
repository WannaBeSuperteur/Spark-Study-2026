
from __future__ import annotations

from time import perf_counter
from functools import wraps
from collections import defaultdict
import statistics

import math
import os
import sys

import numpy as np
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf, pandas_udf

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

ELAPSED_TIMES = defaultdict(list[float])
TOTAL_TESTS = 70
VALID_TESTS = 50


def time_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = perf_counter()
        func(*args, **kwargs)
        elapsed_time = perf_counter() - start_at
        ELAPSED_TIMES[func.__name__].append(elapsed_time)
        print(f'{func.__name__} execution time: {elapsed_time} seconds')
    return wrapper


@udf(returnType=DoubleType())
def python_udf_function(value: float) -> float:
    x = (value - 40.0) / 10.0
    for _ in range(20):
        x = math.sin(x) + math.cos(x * 2) + math.tan(x * 3)
    return x


@pandas_udf(DoubleType())
def pandas_udf_function(series: pd.Series) -> pd.Series:
    x = (series - 40.0) / 10.0
    for _ in range(20):
        x = np.sin(x) + np.cos(x * 2) + np.tan(x * 3)
    return x


@time_checker
def run_with_python_udf(df):
    new_df = df.withColumn("converted_score", python_udf_function("score"))
    new_df.select(F.sum("converted_score")).collect()  # action 호출 -> 실제 연산 시간 측정 가능


@time_checker
def run_with_pandas_udf(df):
    new_df = df.withColumn("converted_score", pandas_udf_function("score"))
    new_df.select(F.sum("converted_score")).collect()  # action 호출 -> 실제 연산 시간 측정 가능


if __name__ == '__main__':
    spark = SparkSession.builder.appName("02_03_example").getOrCreate()
    df = spark.read.csv("02_03_example_2.csv", header=True, inferSchema=True)
    df.cache()
    df.count()  # CSV 읽기 시간 제거

    for _ in range(TOTAL_TESTS):
        print('==== run with PYTHON udf ====')
        run_with_python_udf(df)

        print('==== run with PANDAS udf ====')
        run_with_pandas_udf(df)

    for func_name in ['run_with_python_udf', 'run_with_pandas_udf']:
        print(f'\n === 함수: {func_name} ===')
        valid_stats = ELAPSED_TIMES[func_name][-VALID_TESTS:]

        valid_mean = statistics.mean(valid_stats)
        valid_std = statistics.stdev(valid_stats)
        valid_95pct_min = round(valid_mean - 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct_max = round(valid_mean + 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct = f'[{valid_95pct_min}, {valid_95pct_max}]'

        print(f'마지막 {VALID_TESTS} 회 평균: {valid_mean}, 표준편차: {valid_std}, 95% 신뢰구간: {valid_95pct}')
