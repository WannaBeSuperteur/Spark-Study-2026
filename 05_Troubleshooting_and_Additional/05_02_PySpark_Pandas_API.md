
## 목차

* [1. ```pyspark.pandas``` 모듈 개요](#1-pysparkpandas-모듈-개요)
* [2. ```pyspark.pandas``` 모듈 사용법](#2-pysparkpandas-모듈-사용법)
  * [2-1. Object 생성](#2-1-object-생성)
  * [2-2. Missing data 처리](#2-2-missing-data-처리)
  * [2-3. Grouping (```groupby```)](#2-3-grouping-groupby)
  * [2-4. Plotting (데이터 시각화)](#2-4-plotting-데이터-시각화)
* [3. csv, parquet 으로 읽고 쓰기](#3-csv-parquet-으로-읽고-쓰기)

## 1. ```pyspark.pandas``` 모듈 개요

```pyspark.pandas``` 모듈은 **기존에 Pandas 로 작성한 코드를 적은 양의 변경으로 PySpark 에서 분산 처리** 하기 위한 라이브러리이다.

* 일반적으로 다음과 같이 라이브러리를 import 하여 사용한다.

```python
import pandas as pd
import numpy as np
import pyspark.pandas as ps
from pyspark.sql import SparkSession
```

## 2. ```pyspark.pandas``` 모듈 사용법

### 2-1. Object 생성

* Series 생성

```python
print('== 1 ==')
test_series = ps.Series([10, 255, 1.23, np.nan])
print(test_series)
```

* DataFrame 생성

```python
print('== 2 ==')
test_df = ps.DataFrame(df_dict)
print(test_df)
```

* Pandas DataFrame을 Spark DataFrame 으로 변환

```python
# 3. Pandas DataFrame을 Spark DataFrame 으로 변환
print('== 3 ==')
pandas_df = pd.DataFrame(df_dict)
print(pandas_df)
ps_df = ps.from_pandas(pandas_df)
print(ps_df)
```

* Pandas DataFrame 으로부터 Spark DataFrame 생성

```python
print('== 4 ==')
spark_df = spark.createDataFrame(pandas_df)
spark_df.show()
```

### 2-2. Missing data 처리

* ```dropna``` : missing data 가 있는 row 를 제외하고 표시
* ```fillna``` : missing data 를 특정 값으로 채우기

```python
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
```

* 실행 결과

```
==== 02. MISSING DATA TEST ====
== 1 ==
            name  age  score
0        Oh-LoRA   22   81.5
1       An Yujin   22   90.1
2  Jang Wonyoung   21   83.1
3      Apple Boy   26    NaN
4     Apple Girl   25    NaN
            name  age  score
0        Oh-LoRA   22   81.5
1       An Yujin   22   90.1
2  Jang Wonyoung   21   83.1
            name  age  score
0        Oh-LoRA   22   81.5
1       An Yujin   22   90.1
2  Jang Wonyoung   21   83.1
3      Apple Boy   26   80.0
4     Apple Girl   25   80.0
```

### 2-3. Grouping (```groupby```)

* ```groupby``` 를 사용하여, 특정 컬럼을 기준으로 데이터를 grouping 할 수 있음

```python
print('== 2 ==')
print(ps_df_drop_name_gender.groupby('real').sum())
print(ps_df_drop_name_gender.groupby('real').max())
print(ps_df_drop_name_gender.groupby('real').mean())

print('== 3 ==')
print(ps_df_drop_name.groupby(['real', 'gender']).sum())
print(ps_df_drop_name.groupby(['real', 'gender']).max())
print(ps_df_drop_name.groupby(['real', 'gender']).mean())
```

* 실행 결과

```
== 2 ==
       age  score
real
False   73  246.3
True    43  173.2
       age  score
real
False   26   82.8
True    22   90.1
             age  score
real
False  24.333333   82.1
True   21.500000   86.6
== 3 ==
              age  score
real  gender
False female   47  164.3
True  female   43  173.2
False male     26   82.0
              age  score
real  gender
False female   25   82.8
True  female   22   90.1
False male     26   82.0
               age  score
real  gender
False female  23.5  82.15
True  female  21.5  86.60
False male    26.0  82.00
```

### 2-4. Plotting (데이터 시각화)

```python
print('== 1 ==')
test_series_ps.plot()

print('== 2 ==')
test_series_ps.cummax().plot()
```

## 3. csv, parquet 으로 읽고 쓰기

```python
print('[ Spark IO test ]')
ps_df.spark.to_spark_io('test.orc', format='orc')
print(ps.read_spark_io('test.orc', format='orc').head(2))
print('[ Spark IO test finished ]')
```

* 실행 결과

```
[ Spark IO test ]
            name  age  score                                                    
0  Jang Wonyoung   21   83.1
1        Oh-LoRA   22   81.5
[ Spark IO test finished ]
```

## 참고 자료

* [Quickstart: Pandas API on Spark - Apache Spark 공식 문서](https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_ps.html)
