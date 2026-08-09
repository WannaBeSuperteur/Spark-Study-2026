
from __future__ import annotations

from time import perf_counter
from functools import wraps
from collections import defaultdict
import statistics

import math
import os
import sys

from pyspark import StorageLevel
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

ELAPSED_TIMES = defaultdict(list[float])
TOTAL_TESTS = 300
VALID_TESTS = 200


def time_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = perf_counter()
        func(*args, **kwargs)
        elapsed_time = perf_counter() - start_at
        ELAPSED_TIMES[func.__name__].append(elapsed_time)
        print(f'{func.__name__} execution time: {elapsed_time} seconds')
    return wrapper


def run_common_action(df):
    df = df.withColumn("pass_or_fail",
                       F.when(F.col("score") >= 80, "pass").otherwise("fail"))
    df = df.filter(df["pass_or_fail"] == "pass")
    print(f'passed count: {df.count()}')


@time_checker
def run_without_caching(df):
    run_common_action(df)


@time_checker
def run_with_cache(df):
    run_common_action(df)


@time_checker
def run_with_persist(df):
    run_common_action(df)


if __name__ == '__main__':
    spark = SparkSession.builder.appName("04_02_example").getOrCreate()
    df_path = os.path.join(parent_dir, "02_DataFrame_Basics", "02_03_example_2.csv")

    # 1. Run without caching

    print('==== run WITHOUT CACHING ====')
    for _ in range(TOTAL_TESTS):
        df_uncached = spark.read.csv(df_path, header=True, inferSchema=True)
        run_without_caching(df_uncached)

    # 2. Run with caching (cache)

    print('==== run with CACHE ====')
    df_cached = spark.read.csv(df_path, header=True, inferSchema=True).cache()
    df_cached.count()  # cold start (메모리에 캐시 적재)
    for _ in range(TOTAL_TESTS):
        run_with_cache(df_cached)
    df_cached.unpersist()

    # 3. Run with persist (with MEMORY_AND_DISK Storage Level)

    print('==== run with PERSIST ====')
    df_persist = (spark.read.csv(df_path, header=True, inferSchema=True)
                  .persist(StorageLevel.MEMORY_AND_DISK))
    df_persist.count()  # cold start (메모리에 캐시 적재)
    for _ in range(TOTAL_TESTS):
        run_with_persist(df_persist)
    df_persist.unpersist()

    # 4. Aggregate & Show Test Result

    for func_name in ['run_without_caching', 'run_with_cache', 'run_with_persist']:
        print(f'\n === 함수: {func_name} ===')
        valid_stats = ELAPSED_TIMES[func_name][-VALID_TESTS:]

        valid_mean = statistics.mean(valid_stats)
        valid_std = statistics.stdev(valid_stats)
        valid_95pct_min = round(valid_mean - 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct_max = round(valid_mean + 1.96 * valid_std / math.sqrt(VALID_TESTS), 4)
        valid_95pct = f'[{valid_95pct_min}, {valid_95pct_max}]'

        print(f'마지막 {VALID_TESTS} 회 평균: {valid_mean}, 표준편차: {valid_std}, 95% 신뢰구간: {valid_95pct}')
