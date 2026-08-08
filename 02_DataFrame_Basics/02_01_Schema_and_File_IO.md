
## 목차

* [1. PySpark 의 스키마](#1-pyspark-의-스키마)
* [2. inferSchema](#2-inferschema)
  * [2-1. inferSchema 가 성능을 떨어뜨린다](#2-1-inferschema-가-성능을-떨어뜨린다) 
* [3. StructType 과 StructField](#3-structtype-과-structfield)

## 1. PySpark 의 스키마

* PySpark 에서 스키마는 **데이터프레임의 컬럼명 및 데이터 타입을 정의** 한 것이다.
* 스키마를 미리 정의하는 경우가 많은데, 그 이유는 다음과 같다.
  * Spark가 data type을 추측하지 않게 하여, **스키마 확정을 위한 Job 생성 방지**
  * 데이터와 **스키마와 맞지 않는** 문제의 조기 발견 및 해결

## 2. inferSchema

PySpark에서 ```inferSchema=True``` 로 하면, **PySpark가 각 컬럼의 data type을 자동으로 탐지** 하게 할 수 있다.

* 예시 데이터 ([02_01_example.csv](02_01_example.csv))

```csv
name,gender,age,birthday,used_as_character,score
Oh-LoRA,female,22,2003-10-11,True,85.5
An Yujin,female,22,2003-09-01,False,90.1
Jang Wonyoung,female,21,2004-08-31,True,83.1
Kim Minjae,male,30,1996-08-08,True,84.0
Lee Minsu,male,25,2001-08-08,False,78.0
Gini,female,22,2004-02-03,False,99.9
Genie,male,40,1986-08-08,False,90.0
Namoo Kim,male,35,1991-08-08,False,80.8
```

* inferSchema 미 사용 결과

```
==== run WITHOUT inferSchema ====
root
 |-- name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: string (nullable = true)
 |-- birthday: string (nullable = true)
 |-- used_as_character: string (nullable = true)
 |-- score: string (nullable = true)
```

* inferSchema 사용 결과

```
root
 |-- name: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- birthday: date (nullable = true)
 |-- used_as_character: boolean (nullable = true)
 |-- score: double (nullable = true)
```

### 2-1. inferSchema 가 성능을 떨어뜨린다

* inferSchema 를 사용하는 경우, **Spark가 각 column의 type을 알기 위해 데이터를 스캔** 해야 하므로 시간이 오래 걸린다.
  * 단, 이때 ```.option("samplingRatio", 0.1)``` 처럼 **스캔할 데이터의 비율을 지정** 하여 최적화할 수 있다. 
* 실제 실험 결과 (500 회 기준)

| 구분               | inferSchema "미 사용" 시 | inferSchema "사용" 시 |
|------------------|----------------------|--------------------|
| 평균 시간 (초)        | **0.0863**           | **0.1038**         |
| 표준편차 (초)         | 0.0125               | 0.0144             |
| 평균의 95% 신뢰구간 (초) | [0.0852, 0.0874]     | [0.1025, 0.1050]   |

```python
 === 함수: run_wo_inferschema ===
마지막 500 회 평균: 0.08625811740057543, 표준편차: 0.012457307515036842, 95% 신뢰구간: [0.0852, 0.0874]

 === 함수: run_with_inferschema ===
마지막 500 회 평균: 0.10379077899851837, 표준편차: 0.014364622914445114, 95% 신뢰구간: [0.1025, 0.105]
```

## 3. StructType 과 StructField

스키마를 정의할 때는 다음과 같이 **StructType** 과 **StructField** 를 이용한다.

```python
from pyspark.sql.types import StructType, StructField

schema = StructType(
    [
        StructField("column_name1", OOOType(), nullable=(True or False))
        ...
        StructField("column_nameN", OOOType(), nullable=(True or False))
    ]
)
```

* 예시 및 실행 결과 ([02_01_example_2.py](02_01_example_2.py))

```python
data = [("Oh-LoRA", "female", 22, datetime.strptime("2003-10-11", "%Y-%m-%d"), True, 85.5),
        ("Rozy", "female", 22, datetime.strptime("2021-08-19", "%Y-%m-%d"), False, 83.9)]

schema = StructType(
    [
        StructField("name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("birthday", DateType(), True),
        StructField("used_as_character", BooleanType(), True),
        StructField("score", DoubleType(), True)
    ]
)
df = spark.createDataFrame(data, schema=schema, verifySchema=True)
df.show()
```

```
+-------+------+---+----------+-----------------+-----+
|   name|gender|age|  birthday|used_as_character|score|
+-------+------+---+----------+-----------------+-----+
|Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|   Rozy|female| 22|2021-08-19|            false| 83.9|
+-------+------+---+----------+-----------------+-----+
```

## 참고 자료

* [[러닝 스파크] 데이터프레임 스키마 - IBOK](https://bo-10000.tistory.com/197)
* [InferSchema in PySpark: A Beginner's Guide - Spark Playground](https://www.sparkplayground.com/blog/inferschema-in-pyspark)
