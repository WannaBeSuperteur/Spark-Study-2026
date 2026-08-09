
## 목차

* [1. 파티션 제어와 셔플링 개요](#1-파티션-제어와-셔플링-개요)
* [2. 셔플링 및 셔플 비용 최소화](#2-셔플링-및-셔플-비용-최소화)
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

## 2. 셔플링 및 셔플 비용 최소화

## 3. 적절한 파티션 개수 설정 공식

## 4. ```repartition``` vs. ```coalesce```

### 4-1. repartition

### 4-2. coalesce

## 참고 자료

* [[Spark Tuning] Spark의 Partition 개념, spark.sql.shuffle.partitions, coalesce() vs repartition(), partitionBy() 정리 - 데이터 엔지니어를 꿈꾸는 Spidy web블로그](https://spidyweb.tistory.com/312)
* [[Spark] 스파크에서 Shuffle 개념 - 과거의 나를 위해](https://pinggoopark.tistory.com/entry/Spark-%EC%8A%A4%ED%8C%8C%ED%81%AC%EC%97%90%EC%84%9C-Shuffle-%EA%B0%9C%EB%85%90)
