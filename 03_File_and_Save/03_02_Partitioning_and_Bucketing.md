## 목차

* [1. Partitioning 및 Bucketing 개요](#1-partitioning-및-bucketing-개요)
* [2. Partitioning](#2-partitioning)
  * [2-1. Partitioning 실습](#2-1-partitioning-실습)
* [3. Bucketing](#3-bucketing)
  * [3-1. Bucketing 실습](#3-1-bucketing-실습)

## 1. Partitioning 및 Bucketing 개요

**Partitioning 및 Bucketing** 은 **HDFS 데이터, 입력 파티션 등을 최적화하는 기법** 이다.

* 이를 통해 **시간 및 메모리를 단축** 할 수 있다.
* Partitioning과 Bucketing 비교

| 구분         | Partitioning                                                           | Bucketing                                              |
|------------|------------------------------------------------------------------------|--------------------------------------------------------|
| 기본 설명      | 데이터를 **Partition Key 기반 폴더 (파티션)** 구조로 **분할 저장** (Hive 기반)             | DataFrame을 **특정 ID 컬럼** 기준으로 나눠서 테이블로 저장               |
| 성능 향상      | - 데이터 읽기 최적화 **(스캐닝 과정 생략)**<br>- Retention Policy 적용 시 **데이터 관리 쉬워짐** | DataFrame의 **ID 별 데이터 저장 테이블** 을 로딩하여, **반복 처리 시간 절약** |
| Hive 메타스토어 | 사용 필요 (```saveAsTable```)                                              | 좌동                                                     |
| 최적화        | **반복 처리** 에 최적화                                                        | **반복 처리** 에 최적화                                        |
| 관련 함수      | ```DataFrameWriter``` 의 ```partitionBy```                              | ```DataFrameWriter``` 의 ```bucketBy```                 | 

## 2. Partitioning

**Partitioning (파티셔닝, File System Partitioning)** 은 **데이터를 Partition Key에 기반한 폴더 구조로 분할 저장** 하는 것이다.

* 이때 Partitioning은 **Hive의 개념 (DataFrame의 개념이 아님)** 이다.
* Partitioning 의 방법
  * 데이터 자체를 폴더 구조 (예: 연도-월-일-시-분) 로 저장
* Partitioning 의 장점
  * **데이터 읽기 과정 최적화 (스캐닝 과정 감소 or 생략)** 가능
  * 데이터 관리 쉬워짐 (Retention Policy 적용 시)
    * 로그 파일을 1년 동안만 저장 후 삭제하는 등

### 2-1. Partitioning 실습

* Partitioning 을 위해서는 ```DataFrameWriter``` 의 ```partitionBy``` 함수를 사용한다.
  * 이때, Partition Key는 **cardinality (가능한 값의 개수) 가 작은 것** 을 선택하는 것이 좋다. (많은 파일 생성 방지를 위해)
* [Python 실습 코드](03_02_example.py)

```python
def partitioning_example(df, spark):
    output_dir = "03_02_partitioning_example/output"

    # partition 데이터 쓰기
    print('write ...')
    df_with_partition = (df
                         .withColumn("id_digit_2", F.substring(F.col("id"), 6, 1))
                         .withColumn("id_digit_1", F.substring(F.col("id"), 7, 1)))
    df_with_partition.limit(20).show()

    (df_with_partition.write
        .mode("overwrite")
        .partitionBy("id_digit_2", "id_digit_1")
        .parquet(output_dir))

    # partition 된 데이터 읽기
    print('read ...')
    df = spark.read.parquet(os.path.join(output_dir, "id_digit_2=1", "id_digit_1=2"))
    df.limit(20).show()
```

* 실행 결과

```
==== PARTITIONING EXAMPLE ====                                                  
write ...
+-------+-----+----------+----------+
|     id|score|id_digit_2|id_digit_1|
+-------+-----+----------+----------+
|A000001| 88.3|         0|         1|
|A000002| 96.0|         0|         2|
|A000003| 88.8|         0|         3|
|A000004| 79.7|         0|         4|
|A000005| 84.4|         0|         5|
|A000006| 90.0|         0|         6|
|A000007| 98.7|         0|         7|
|A000008| 86.8|         0|         8|
|A000009| 80.7|         0|         9|
|A000010| 93.0|         1|         0|
|A000011| 91.7|         1|         1|
|A000012| 91.3|         1|         2|
|A000013| 54.6|         1|         3|
|A000014| 96.1|         1|         4|
|A000015| 81.8|         1|         5|
|A000016| 52.5|         1|         6|
|A000017| 52.3|         1|         7|
|A000018| 84.5|         1|         8|
|A000019| 79.6|         1|         9|
|A000020| 97.5|         2|         0|
+-------+-----+----------+----------+

read ...                                                                        
+-------+-----+
|     id|score|
+-------+-----+
|A000012| 91.3|
|A000112| 92.1|
|A000212| 82.1|
|A000312| 88.5|
|A000412| 73.1|
|A000512| 81.6|
|A000612| 93.7|
|A000712| 94.1|
|A000812| 59.0|
|A000912| 70.2|
|A001012| 95.4|
|A001112| 96.1|
|A001212| 80.4|
|A001312| 74.0|
|A001412| 73.7|
|A001512| 76.6|
|A001612| 52.6|
|A001712| 77.5|
|A001812| 66.8|
|A001912| 92.4|
+-------+-----+
```

## 3. Bucketing

**Bucketing (버케팅)** 은 **데이터프레임을 특정 ID 컬럼 기준으로 분할** 하여 테이블로 저장하는 것이다.

* Bucketing 의 방법
  * 먼저 ```bucket 개수``` 및 ```ID 컬럼``` 을 지정한다.
  * 컬럼 값 기준으로 **해싱 후 bucket 개수로 그 값을 나눠서** 특정 레코드가 가야 할 테이블을 결정한다.
* Bucketing 의 장점
  * 저장된 테이블을 **추후에는 그냥 로딩하여 사용** 하면 되므로, **반복 처리 시간이 단축** 된다. 

### 3-1. Bucketing 실습

* Bucketing 을 위해서는 ```DataFrameWriter``` 의 ```bucketBy``` 함수를 이용한다.
* [Python 실습 코드](03_02_example.py)

```python
def bucketing_example(df, spark):
    table_name = "03_02_bucketing_example"
    prime_number = 17

    # 기존 테이블 및 warehouse 제거
    spark.sql(f"DROP TABLE IF EXISTS {table_name}")

    warehouse_dir = f'spark-warehouse/{table_name}'
    if os.path.exists(warehouse_dir):
        shutil.rmtree(warehouse_dir)

    # bucket 데이터 쓰기
    print('write ...')
    df_with_id_column = (df
                         .withColumn("id_column", F.substring(F.col("id"), 2, 6)))
    df_with_id_column.limit(20).show()

    (df_with_id_column.write
        .mode("overwrite")
        .bucketBy(prime_number, "id_column")
        .saveAsTable(table_name))

    # bucket 된 데이터 읽기
    print('read ...')
    df = spark.read.table(table_name)
    df = df.withColumn("mod", F.col("id_column").cast("integer") % prime_number)
    df.limit(20).show()
```

* 실행 결과

```
==== BUCKETING EXAMPLE ====
write ...
+-------+-----+---------+
|     id|score|id_column|
+-------+-----+---------+
|A000001| 88.3|   000001|
|A000002| 96.0|   000002|
|A000003| 88.8|   000003|
|A000004| 79.7|   000004|
|A000005| 84.4|   000005|
|A000006| 90.0|   000006|
|A000007| 98.7|   000007|
|A000008| 86.8|   000008|
|A000009| 80.7|   000009|
|A000010| 93.0|   000010|
|A000011| 91.7|   000011|
|A000012| 91.3|   000012|
|A000013| 54.6|   000013|
|A000014| 96.1|   000014|
|A000015| 81.8|   000015|
|A000016| 52.5|   000016|
|A000017| 52.3|   000017|
|A000018| 84.5|   000018|
|A000019| 79.6|   000019|
|A000020| 97.5|   000020|
+-------+-----+---------+

read ...                                                                        
+-------+-----+---------+---+
|     id|score|id_column|mod|
+-------+-----+---------+---+
|A000005| 84.4|   000005|  5|
|A000027| 40.2|   000027| 10|
|A000036| 97.6|   000036|  2|
|A000057| 85.0|   000057|  6|
|A000064| 85.2|   000064| 13|
|A000077| 73.6|   000077|  9|
|A000086| 93.0|   000086|  1|
|A000117| 83.3|   000117| 15|
|A000137| 80.7|   000137|  1|
|A000144| 82.5|   000144|  8|
|A000163| 74.2|   000163| 10|
|A000195| 96.0|   000195|  8|
|A000196| 72.0|   000196|  9|
|A000204| 40.6|   000204|  0|
|A000217| 89.4|   000217| 13|
|A000244| 78.4|   000244|  6|
|A000303| 93.8|   000303| 14|
|A000307| 73.3|   000307|  1|
|A000330| 75.7|   000330|  7|
+-------+-----+---------+---+
```

## 참고 자료

* [26. Spark 내부 동작(Bucketing과 Partitioning) - 데이터엔지니어스터디](https://dataengineerstudy.tistory.com/244)
