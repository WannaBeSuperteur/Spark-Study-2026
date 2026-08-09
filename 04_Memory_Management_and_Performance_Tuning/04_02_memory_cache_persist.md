
## 목차

* [1. 메모리 캐싱 개요](#1-메모리-캐싱-개요)
* [2. 메모리 캐싱 전략: ```cache()``` vs. ```persist()```](#2-메모리-캐싱-전략-cache-vs-persist)
  * [2-1. caching 사용 시 속도 실험 결과](#2-1-caching-사용-시-속도-실험-결과)

## 1. 메모리 캐싱 개요

* Spark에서는 **action 연산자 수행 시 데이터가 로드** 되며, 이때 **action 실행 시마다 로드하지 않고, 데이터를 메모리에 상주** 시킬 수 있다.
  * 즉, RDD를 **Executor 메모리/디스크** 보관 후 재사용하는 개념이다.
  * 이것을 **Spark Cache (여기서는 '메모리 캐싱')** 라고 한다.

## 2. 메모리 캐싱 전략: ```cache()``` vs. ```persist()```

메모리 캐싱 전략으로 잘 알려진 ```cache()``` 와 ```persist()``` 를 비교하면 다음과 같다.

* 공통점
  * RDD 를 Memory 또는 Disk 에 저장함
  * action 연산자 반복 수행이 예상될 때 사용한다.
* 차이점

| 구분            | ```cache()``` | ```persist()```                                                                                     |
|---------------|---------------|-----------------------------------------------------------------------------------------------------|
| 저장 위치         | **메모리** 한정    | **Storage Level** 지정 가능 (메모리, 디스크 등)                                                                |
| Storage Level | 없음            | - ```MEMORY_ONLY``` (메모리 한정)<br>- ```MEMORY_AND_DISK``` (메모리 & 디스크)<br>- ```DISK_ONLY``` (디스크에만 저장) |

* Best Practice
  * 머신러닝 모델 학습 시, **데이터를 넣기 전에 미리 cache** 하는 것이 좋다.
  * 꼭 필요한 것만 캐시한다. (예를 들어, ML 모델 학습 시 ```target``` ```feature``` 2개의 컬럼만 캐시)
  * 더 이상 필요하지 않으면 반드시 ```cached_df.unpersist()``` 로 ```unpersist``` 처리한다.
  * 디스크에는 되도록 저장하지 않는다. (hadoop 저장 데이터보다 **느릴 수 있음**)

* 참고
  * **checkpointing** 을 통해, RDD를 외부 저장소 (HDFS, S3) 에 저장할 수 있다.
    * 이때 Spark 앱 종료 후에도 데이터가 여전히 남아 있다.
  * SQL로도 캐싱이 가능하다.
    * ```spark.sql("cache table table_name")``` 을 통해 ```table_name``` 테이블 캐시 가능
    * 이때 캐시에서 테이블을 제거하려면 ```spark.sql("uncache table table_name")``` 과 같이 하면 된다.

* **캐시된 object는 새 변수에 할당** 하는 것이 좋다.
  * Driver Node에서는 **캐시된 데이터를 object에 할당 시, 여러 clsuter의 데이터에 매핑** 된다. 
  * 이후 해당 object에 다른 데이터 할당 시, **캐시된 데이터를 더 이상 사용 불가 (Executor에 남음)** 하기 때문이다.

### 2-1. caching 사용 시 속도 실험 결과

* [실험 코드](04_02_example.py)

* 코드 실행 결과

* 속도 실험 비교 (caching 없음 vs. ```cache()``` vs. ```persist()```)

## 참고 자료

* [[Spark] cache() 와 persist() - 🐥](https://quackstudy.tistory.com/entry/Spark-cache%EC%99%80-persist)
* [Spark : Cache(Persist) Deep Dive 해보기 - gorany](https://velog.io/@gorany/Spark-CachePersist-Deep-Dive-%ED%95%B4%EB%B3%B4%EA%B8%B0)
