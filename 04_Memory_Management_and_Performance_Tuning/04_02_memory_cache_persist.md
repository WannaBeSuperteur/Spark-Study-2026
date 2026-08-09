
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

```python
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
```

```python
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
```

* 코드 실행 결과

```
 === 함수: run_without_caching ===
마지막 200 회 평균: 0.39458962200093084, 표준편차: 0.04548085595366969, 95% 신뢰구간: [0.3883, 0.4009]

 === 함수: run_with_cache ===
마지막 200 회 평균: 0.09506691150250844, 표준편차: 0.02158726533368292, 95% 신뢰구간: [0.0921, 0.0981]

 === 함수: run_with_persist ===
마지막 200 회 평균: 0.09644972299807705, 표준편차: 0.01962772309825337, 95% 신뢰구간: [0.0937, 0.0992]
```

* 속도 실험 비교 (caching 없음 vs. ```cache()``` vs. ```persist()```)
  * 총 200 회 기준

| 구분               | caching "없음"     | "cache" 방식으로 캐싱  | "persist" 방식으로 캐싱 |
|------------------|------------------|------------------|-------------------|
| 평균 시간 (초)        | **0.3946**       | **0.0951**       | **0.0964**        |
| 표준편차 (초)         | 0.0455           | 0.0216           | 0.0196            |
| 평균의 95% 신뢰구간 (초) | [0.3883, 0.4009] | [0.0921, 0.0981] | [0.0937, 0.0992]  |

## 참고 자료

* [[Spark] cache() 와 persist() - 🐥](https://quackstudy.tistory.com/entry/Spark-cache%EC%99%80-persist)
* [Spark : Cache(Persist) Deep Dive 해보기 - gorany](https://velog.io/@gorany/Spark-CachePersist-Deep-Dive-%ED%95%B4%EB%B3%B4%EA%B8%B0)
