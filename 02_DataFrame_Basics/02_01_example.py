
from __future__ import annotations

from time import perf_counter
from functools import wraps
from collections import defaultdict
import statistics

import math
import os
import sys
from pyspark.sql import SparkSession

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

ELAPSED_TIMES = defaultdict(list[float])
TOTAL_TESTS = 700
VALID_TESTS = 500


def time_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = perf_counter()
        func(*args, **kwargs)
        elapsed_time = perf_counter() - start_at
        ELAPSED_TIMES[func.__name__].append(elapsed_time)
        print(f'{func.__name__} execution time: {elapsed_time} seconds')
    return wrapper


@time_checker
def run_wo_inferschema(spark):
    df = (spark.read
          .option("header", True)
          .option("inferSchema", False)
          .csv("02_01_example.csv"))
    df.printSchema()


@time_checker
def run_with_inferschema(spark):
    df = (spark.read
          .option("header", True)
          .option("inferSchema", True)
          .csv("02_01_example.csv"))
    df.printSchema()


if __name__ == '__main__':
    spark = SparkSession.builder.appName("02_01_example").getOrCreate()

    for _ in range(TOTAL_TESTS):
        print('==== run WITHOUT inferSchema ====')
        run_wo_inferschema(spark)

        print('==== run WITH inferSchema ====')
        run_with_inferschema(spark)

    for func_name in ['run_wo_inferschema', 'run_with_inferschema']:
        print(f'\n === 함수: {func_name} ===')
        valid_stats = ELAPSED_TIMES[func_name][-VALID_TESTS:]

        valid_mean = statistics.mean(valid_stats)
        valid_std = statistics.stdev(valid_stats)
        valid_95pct_min = round(valid_mean - 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct_max = round(valid_mean + 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct = f'[{valid_95pct_min}, {valid_95pct_max}]'

        print(f'마지막 {VALID_TESTS} 회 평균: {valid_mean}, 표준편차: {valid_std}, 95% 신뢰구간: {valid_95pct}')
