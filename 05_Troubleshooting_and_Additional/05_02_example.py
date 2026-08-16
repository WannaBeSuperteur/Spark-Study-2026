
import pandas as pd
import numpy as np
import pyspark.pandas as ps
from pyspark.sql import SparkSession

import os
import sys
import time

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"


def create_object_test(spark):
    df_dict = {
        'name': ['Oh-LoRA', 'An Yujin', 'Jang Wonyoung'],
        'age': [22, 22, 21],
        'score': [81.5, 90.1, 83.1]
    }

    # 1. Series 생성
    print('== 1 ==')
    test_series = ps.Series([10, 255, 1.23, np.nan])
    print(test_series)

    # 2. DataFrame 생성
    print('== 2 ==')
    test_df = ps.DataFrame(df_dict)
    print(test_df)

    # 3. Pandas DataFrame을 Spark DataFrame 으로 변환
    print('== 3 ==')
    pandas_df = pd.DataFrame(df_dict)
    print(pandas_df)
    ps_df = ps.from_pandas(pandas_df)
    print(ps_df)

    # 4. Pandas DataFrame -> Spark DataFrame 생성
    print('== 4 ==')
    spark_df = spark.createDataFrame(pandas_df)
    spark_df.show()

    # 5. 정렬
    print('== 5 ==')
    ps_df.sort_values(by='score')
    print(ps_df)
    print(ps_df.sort_values(by='score'))


def missing_data_test():
    df_dict_with_missing_data = {
        'name': ['Oh-LoRA', 'An Yujin', 'Jang Wonyoung', 'Apple Boy', 'Apple Girl'],
        'age': [22, 22, 21, 26, 25],
        'score': [81.5, 90.1, 83.1, np.nan, np.nan]
    }

    print('== 1 ==')
    pandas_df = pd.DataFrame(df_dict_with_missing_data)
    pyspark_df = ps.from_pandas(pandas_df)
    print(pyspark_df)
    print(pyspark_df.dropna(how='any'))
    print(pyspark_df.fillna(value=80.0))


def grouping_test():
    df_dict = {
        'name': ['Oh-LoRA', 'An Yujin', 'Jang Wonyoung', 'Apple Boy', 'Apple Girl'],
        'real': [False, True, True, False, False],
        'gender': ['female', 'female', 'female', 'male', 'female'],
        'age': [22, 22, 21, 26, 25],
        'score': [81.5, 90.1, 83.1, 82.0, 82.8]
    }

    print('== 1 ==')
    pandas_df = pd.DataFrame(df_dict)
    ps_df = ps.from_pandas(pandas_df)
    ps_df_drop_name = ps_df.drop(columns=["name"])
    ps_df_drop_name_gender = ps_df.drop(columns=["name", "gender"])

    print('== 2 ==')
    print(ps_df_drop_name_gender.groupby('real').sum())
    print(ps_df_drop_name_gender.groupby('real').max())
    print(ps_df_drop_name_gender.groupby('real').mean())

    print('== 3 ==')
    print(ps_df_drop_name.groupby(['real', 'gender']).sum())
    print(ps_df_drop_name.groupby(['real', 'gender']).max())
    print(ps_df_drop_name.groupby(['real', 'gender']).mean())


def plotting_test():
    test_series_pd = pd.Series([0.625, 0.75, 0.875, 0.875, 0.9375,
                                0.9375, 0.8125, 0.9688, 1.0, 0.9688,
                                1.0, 1.0])
    test_series_ps = pd.Series(test_series_pd)

    print('== 1 ==')
    test_series_ps.plot()

    print('== 2 ==')
    test_series_ps.cummax().plot()


if __name__ == '__main__':
    spark = SparkSession.builder.appName("05_02_example").getOrCreate()
    print(f"Spark UI URL: {spark.sparkContext.uiWebUrl}")

    print("\n==== 01. CREATE OBJECT TEST ====")
    create_object_test(spark)

    print("\n==== 02. MISSING DATA TEST ====")
    missing_data_test()

    print("\n==== 03. GROUPING TEST ====")
    grouping_test()

    print("\n==== 04. PLOTTING TEST ====")
    plotting_test()

    time.sleep(24 * 60 * 60)
    spark.stop()
