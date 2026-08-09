
## 목차

* [1. 파티션 제어와 셔플링 개요](#1-파티션-제어와-셔플링-개요)
* [2. 셔플링 및 셔플 성능 최적화](#2-셔플링-및-셔플-성능-최적화)
  * [2-1. Shuffle 성능 최적화](#2-1-shuffle-성능-최적화) 
* [3. 적절한 파티션 개수 설정 공식](#3-적절한-파티션-개수-설정-공식)
* [4. ```repartition``` vs. ```coalesce```](#4-repartition-vs-coalesce)
  * [4-1. repartition](#4-1-repartition)
  * [4-2. coalesce](#4-2-coalesce)

## 1. 파티션 제어와 셔플링 개요

* **Partition (파티션)** 은 RDD 또는 Dataset을 구성하는 **가장 작은 단위의 객체** 이ㅏㄷ.
  * NOTE: ```1 Core = 1 Task = 1 Partition``` 
* **Partitioning (파티셔닝)** 은 데이터를 **여러 cluster node로 분할** 하는 메커니즘이다.
* 다음과 같은 관계 때문에, **Partition 크기 조절이 Spark 성능 및 메모리 점유량에 큰 영향** 을 미친다.
  * ```(Partition 개수) = (Core 개수)```
  * ```(Partition의 크기) = (메모리 크기)```
* 다음과 같이 **Partition 개수 상향** 은 **Task 당 메모리 감소 및 병렬화 정도 향상** 으로 이어진다.
  * ```Partition의 개수가 많아질수록 → 각 Partition의 크기가 작아짐``` 

Partition의 종류는 다음과 같다.

| 종류                    | 설명                               |
|-----------------------|----------------------------------|
| **Input** Partition   | 데이터를 Spark 작업에 **read** 할 때 생성   |
| **Output** Partition  | 작업의 **결과를 저장** 하는 파티션            |
| **Shuffle** Partition | 데이터의 **re-shuffling** 시 생성되는 파티션 |

## 2. 셔플링 및 셔플 성능 최적화

**셔플링 (Shuffling)** 은 대규모 데이터의 분산 처리 시, **데이터 재분배 (Data Re-distribution) 또는 재파티셔닝 (Shuffle)** 을 의미한다.

* 대규모 네트워크 및 디스크 I/O가 발생한다.

**1. Shuffle의 주요 개념**

| 주요 개념                         | 설명                                                                                                                             |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| 데이터 재분배 (Partition Shuffling) | Spark는 RDD를 여러 파티션으로 나누는데, **기존 파티션 구조로 작업 불가능한 상황** 발생 가능<br>- 이를 해결하기 위해 **기존 파티션 경계를 넘어서 데이터를 이동** 시키는 것을 **Shuffle** 이라고 함 |
| 스테이지 (Stage) 경계               | Shuffle 발생 지점에서 **Job이 여러 stage로 나뉘고**, 해당 stage 간 **shuffle 데이터 전송** 발생                                                       |
| 비용 (cost)                     | - **네트워크 전송** (데이터를 네트워크를 통해 executor 노드로 전송)<br>- **디스크 I/O** (중간 결과 디스크 기록 + 역직렬화 + 압축 + 해제)                                 |

**2. Shuffle 동작 방식**

| 구분            | Read/Write        | 설명                                                                      |
|---------------|-------------------|-------------------------------------------------------------------------|
| **Map** 단계    | Shuffle **Write** | key 또는 partition에 따라 데이터를 **bucket으로 분할 → 디스크로 저장**                     |
| **Reduce** 단계 | Shuffle **Read**  | 각자 필요한 key 또는 partition의 **Shuffle 조각을 읽어서 → 최종 연산 수행 (group, join 등)** |

### 2-1. Shuffle 성능 최적화

Shuffle 성능 최적화를 위해서는 다음과 같은 전략을 고려할 수 있다.

| 전략                                     | 설명                                                                                                |
|----------------------------------------|---------------------------------------------------------------------------------------------------|
| [파티션 수를 적절히 설정](#3-적절한-파티션-개수-설정-공식)   | - 너무 많으면 → 너무 많은 shuffle 파일 생성 → **디스크 I/O 등 증가**<br>- 너무 적으면 → **병렬성 감소, 속도 저하**                 |
| Wide Transformation 연산 최소화             | - shuffle이 없는 연산 (```mapPartitions``` ```map``` 등) 활용<br>- 불필요한 ```groupByKey``` ```join``` 등을 줄임 |
| 데이터 스큐 (Data Skew, 특정 키에 데이터 몰림) 현상 해결 | **특정 node에 부하 집중** 되는 현상 방지                                                                       |
| 메모리 및 네트워크 튜닝                          | **Executor 메모리** 확대를 통한 메모리 spill 감소                                                              |
| 압축, Serializer 설정                      | -                                                                                                 |

## 3. 적절한 파티션 개수 설정 공식

* 셔플에 사용되는 파티션 개수는 **Shuffle Partition 1개당 100~200MB 정도** 가 되도록 하는 것이 적당하다.
* 관련 설정

| 설정                                                              | 설명                                    | 기본값                               |
|-----------------------------------------------------------------|---------------------------------------|-----------------------------------|
| ```spark.conf.set("spark.sql.shuffle.partitions", N)```         | 셔플에 사용되는 파티션 개수                       | ```N``` = 200                     |
| ```spark.conf.set("spark.sql.files.maxPartitionBytes",bytes)``` | 파티션 파일의 최대 크기 (해당 크기보다 크면 쪼개면서 파일 읽음) | ```bytes``` = 134,217,728 (128MB) |

## 4. ```repartition``` vs. ```coalesce```

transformation 연산 (```filter()``` 등) 수행 시, **최초에 설정한 파티션 개수가 적합하지 않을** 수 있음

* 이때, 파티션 개수 조절하는 option 사용 가능
* ```groupBy``` 등 집계 후 **데이터 크기가 작아지면**, 파일 수를 늘리기 위해 **Partition 개수를 줄여야 할** 수 있음
  * 이를 위해 ```repartition``` ```coalesce``` 를 사용

| 함수                  | 역할                 | 사용법                     |
|---------------------|--------------------|-------------------------|
| ```repartition()``` | 파티션 수 **증가 또는 감소** | ```df.repartition(n)``` |
| ```coalesce()```    | 파티션 수 **감소**       | ```df.coalesce(n)```    |

### 4-1. repartition

```repartition()``` 함수는 **정확히 ```numPartitions``` 개의 파티션을 갖는 RDD** 를 반환한다. **(파티션 간 데이터 균등 보장)**

```python
print('==== REPARTITION EXAMPLE ====')
    (df.repartition(100)
     .write
     .format("parquet")
     .mode("overwrite")
     .save("04_01_repartition_example/output"))
```

### 4-2. coalesce

```coalesce()``` 함수는 **기존의 파티션들을 ```numPartitions``` 개 이하의 파티션을 갖도록 합친** 것을 반환한다. **(파티션 간 데이터 양 편향, 즉 data skew 가능)**

```python
    print('==== COALESCE EXAMPLE ====')
    (df.coalesce(100)
     .write
     .format("parquet")
     .mode("overwrite")
     .save("04_01_coalesce_example/output"))
```

## 참고 자료

* [[Spark Tuning] Spark의 Partition 개념, spark.sql.shuffle.partitions, coalesce() vs repartition(), partitionBy() 정리 - 데이터 엔지니어를 꿈꾸는 Spidy web블로그](https://spidyweb.tistory.com/312)
* [[Spark] 스파크에서 Shuffle 개념 - 과거의 나를 위해](https://pinggoopark.tistory.com/entry/Spark-%EC%8A%A4%ED%8C%8C%ED%81%AC%EC%97%90%EC%84%9C-Shuffle-%EA%B0%9C%EB%85%90)
