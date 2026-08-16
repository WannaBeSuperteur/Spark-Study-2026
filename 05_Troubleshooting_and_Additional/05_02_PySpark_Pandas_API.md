
## 목차

* [1. ```pyspark.pandas``` 모듈 개요](#1-pysparkpandas-모듈-개요)
* [2. ```pyspark.pandas``` 모듈 사용법](#2-pysparkpandas-모듈-사용법)
  * [2-1. Object 생성](#2-1-object-생성)
  * [2-2. Missing data 처리](#2-2-missing-data-처리)
  * [2-3. Grouping (```groupby```)](#2-3-grouping-groupby)
  * [2-4. Plotting (데이터 시각화)](#2-4-plotting-데이터-시각화)
* [3. csv, parquet 으로 읽고 쓰기](#3-csv-parquet-으로-읽고-쓰기)
* [4. Spark 에서의 설정 적용하기](#4-spark-에서의-설정-적용하기)

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

### 2-2. Missing data 처리

### 2-3. Grouping (```groupby```)

### 2-4. Plotting (데이터 시각화)

## 3. csv, parquet 으로 읽고 쓰기

## 4. Spark 에서의 설정 적용하기

## 참고 자료

* [Quickstart: Pandas API on Spark - Apache Spark 공식 문서](https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_ps.html)
