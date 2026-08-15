## 목차

* [1. Driver OOM, Executor OOM의 차이](#1-driver-oom-executor-oom의-차이)
  * [1-1. Driver OOM](#1-1-driver-oom)
  * [1-2. Executor OOM](#1-2-executor-oom)
* [2. Memory Overhead 설정 방법](#2-memory-overhead-설정-방법)

## 1. Driver OOM, Executor OOM의 차이

Driver OOM과 Executor OOM은 **Spark 에서 발생하는 OOM의 2가지 유형** 이다.

* 참고: [Driver와 Executor](../01_Spark_Core_Concepts/01_01_Spark_Cluster_Architecture.md#1-1-driver와-executor)

| 구분           | 설명                                 | 주요 원인                                    |
|--------------|------------------------------------|------------------------------------------|
| Driver OOM   | **Driver** 에서 발생하는 Out of Memory   | Driver 에서 **큰 데이터** 를 수집하거나, 큰 데이터를 처리 시 |
| Executor OOM | **Executor** 에서 발생하는 Out of Memory | Executor 가 **할당된 양의 데이터를 처리하는 데 실패** 시   |

### 1-1. Driver OOM

**Driver OOM** 은 **Driver 가 큰 양의 데이터를 수집 또는 처리** 할 때 발생하는 Out of Memory 이다.

* Driver OOM 발생하는 케이스의 예시
  * 큰 DataFrame 에 대해, ```df.collect()``` 또는 ```toPandas()``` 실시 시
  * 메모리에 거대하거나 복잡한 DAG 이 저장될 때

* Driver OOM 방지 방법
  * Driver 에서 **큰 양의 데이터셋 수집은 하지 않는다.**
  * ```collect()``` 를 호출하기 전에 **필터링 또는 샘플링** 을 한다.
  * ```--driver-memory``` 를 이용하여 Driver memory 의 양 자체를 늘린다.

### 1-2. Executor OOM

**Executor OOM** 은 **Executor 가 할당된 양의 데이터를 처리하는 데 실패** 했을 때 발생한다.

* Executor OOM 발생 케이스 예시
  * ```shuffle```, ```join``` 또는 ```aggregation``` 이 매우 클 때
  * 큰 DataFrame을 캐시 (또는 ```persist```) 처리할 때
  * [Data Skew](../04_Memory_Management_and_Performance_Tuning/04_03_Join_and_Data_Skew.md#1-data-skew의-개념)
  * shuffle buffer 또는 [UDF](../02_DataFrame_Basics/02_03_Builtin_vs_UDF.md#1-pyspark-사용자-정의-함수-udf) 에 할당된 메모리 부족

* Executor OOM 방지 방법
  * [Data Skew 방지](../04_Memory_Management_and_Performance_Tuning/04_03_Join_and_Data_Skew.md#2-data-skew의-해결-방법) 방법들 ([repartition](../04_Memory_Management_and_Performance_Tuning/04_01_Partition_shuffling_repartition_coalesce.md#4-1-repartition) 등) 
  * 블필요한 **큰 데이터셋 캐싱** 을 하지 않는다.
  * [Broadcast Join](../04_Memory_Management_and_Performance_Tuning/04_03_Join_and_Data_Skew.md#2-3-broadcast-join) 사용
  * ```--executor-memory``` 를 이용하여 Executor memory 의 양 자체를 늘린다.

## 2. Memory Overhead 설정 방법

* Executor 의 경우, ```--executor-memory={N}g --conf spark.executor.memoryOverhead={M}g``` 와 같은 설정을 통해 overhead 를 사용할 수 있다.
  * 이때, Yarn에 예약되는 메모리는 ```N + M``` GB 이고, 다음과 같이 배정된다.

| on-heap<br>(일반적인 heap 영역, 가비지 컬렉션 적용) | off-heap<br>(힙 메모리 바깥, 가비지 컬렉션 미 적용) | Yarn 메모리 할당량   |
|---------------------------------------|--------------------------------------|----------------|
| ```N``` GB                            | ```M``` GB                           | ```N + M``` GB |

* 그냥 ```--executor-memory={N}g``` 라고만 하면 다음과 같이 할당된다.

| on-heap    | off-heap | Yarn 메모리 할당량         |
|------------|----------|----------------------|
| ```N``` GB | 약간의 메모리  | ```N``` GB + 약간의 메모리 |

* OOM 대응 방법
  * GC (가비지 컬렉션) 자주 발생 시, **on-heap이 부족** 함을 의미하므로 ```--executor-memory={N}g``` 의 ```N``` 값을 늘린다.
  * GC는 자주 발생하지 않지만 **yarn에 의해 executor 중단** 시, memory overhead 를 늘린다.

## 참고 자료

* [What is OOM (Out of Memory)? - Jnanaranjan pradhan (LinkedIn)](https://www.linkedin.com/posts/jnanaranjanpradhan_what-is-oom-out-of-memory-out-of-memory-share-7324039571321565185-Pelh/)
* [spark memoryOverhead 설정에 대한 이해 - Jason Heo's Blog](https://jason-heo.github.io/bigdata/2020/10/24/understanding-spark-memoryoverhead-conf.html)
