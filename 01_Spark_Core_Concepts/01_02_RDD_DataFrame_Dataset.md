
## 목차

* [1. RDD vs. DataFrame vs. Dataset 비교](#1-rdd-vs-dataframe-vs-dataset-비교)
  * [1-1. RDD](#1-1-rdd)
  * [1-2. DataFrame](#1-2-dataframe)
  * [1-3. Dataset](#1-3-dataset)
* [2. 참고: Spark SQL](#2-참고-spark-sql)

## 1. RDD vs. DataFrame vs. Dataset 비교

| 구분            | RDD                                                                                            | DataFrame                  | Dataset                                                                    |
|---------------|------------------------------------------------------------------------------------------------|----------------------------|----------------------------------------------------------------------------|
| 기본 설명         | 클러스터 내의 여러 노드에 분산된, **변경 불가능한** 데이터 집합                                                         | 변경 불가능한 집합 (단, 테이블 컬럼 존재)  | Spark 2.0 부터 **DataFrame 과 통합됨**<br>- ```DataFrame = Dataset[Row]```       |
| 일반적인 use case | - Transformation, Action, Upsert 등 사용 시<br>- 비구조화 형태의 데이터 (미디어 등)<br>- **함수형 프로그래밍** 으로 데이터 조작 |                            | - DataFrame 조작을 통해 **원하는 작업 불가능** 시<br>- ```type-safety``` 에 따른 비용 감당 가능 시 |
| 변경 불가능        | **O**                                                                                          | **O**                      | **O**                                                                      |
| 스키마 존재 여부     | **X**                                                                                          | **O**                      | **O**                                                                      |
| 성능 최적화        | **X**<br>(쿼리 최적화 없음, UDF에서 인터프리터-JVM 간 통신으로 속도 저하 등)                                           | **O**                      | **O**                                                                      |
| 생성 방법         | ```sc = spark.SparkContext``` 로 객체 생성                                                          | ```SparkSession``` 을 통한 생성 | ```DataFrame = Dataset[Row]```                                             |

### 1-1. RDD

**RDD (Resilient Distributed Dataset)** 은 Spark Core 에서 **클러스터 내의 여러 노드에 분산된, 변경 불가능한 데이터 집합** 이다.

RDD는 클러스터 내의 여러 노드에 분산된, **변경 불가능한** 데이터 집합으로, 그 의미를 뜯어보면 다음과 같다.

| 구분          | 설명                              |
|-------------|---------------------------------|
| Resilient   | 분산된 데이터에 대한 **오류 복구** 능력        |
| Distributed | 데이터를 **분산하여 저장 (클러스터의 여러 노드에)** |
| Dataset     | 분산된 데이터 집합                      |

* RDD의 특징
  * 수정 불가능
  * 병렬적 처리
  * 다음과 같이 **Transformation** 및 **Action** 함수로 구성

| 구분                | 설명                                                                                                                         | 예시 함수                                                                                                      |
|-------------------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Transformation 함수 | RDD에서 새로운 RDD 생성 (Spark 동작 중 데이터 처리)                                                                                       | ```map``` ```filter``` ```flatMap``` ```join```                                                            |
| Action 함수         | RDD를 **RDD 외의 type으로 변환**<br>- **Transformation 결과 저장** 명령<br>- 해당 함수 실행 시, **RDD가 실제 동작으로 바뀌며, 값이 Driver 또는 외부 저장소에 저장됨** | ```count``` ```collect``` ```reduce``` ```save``` ```take``` ```top``` ```aggregate``` ```max``` ```min``` |

* RDD 생성 방법

```python
spark = SparkSession.builder.appName("test").getOrCreate()
sc = spark.SparkContext
lines = sc.textfile(...)  # 여기서 lines 는 RDD type이 됨
```

### 1-2. DataFrame

**DataFrame (데이터프레임)** 은 **SparkSession을 통해 생성되는 data type** 이다.

* 테이블 생성을 통해 **SQL Query 가 가능** 하기 때문에 대부분의 경우에 사용한다.
* DataFrame의 특징
  * 스키마 추상화
  * Pyspark에서 **UDF (사용자 정의 함수) 를 선언** 하는 경우, **속도 저하 가능**
  * 테이블 관련 연산 가능
  * **Transformation 과 Action 은 서로 분할됨**

### 1-3. Dataset

**Dataset (데이터셋)** 은 **DataFrame 조작으로는 원하는 작업을 수행할 수 없을 때** 사용한다.

* DataFrame은 dataset인데, 그 중 ```Row 타입```의 dataset이다. 즉, ```DataFrame = DataSet[Row]``` 이다.
* Dataset의 특징
  * 데이터 타입이 명시되어야 함
  * 스키마 추상화 (DataFrame과 동일)
  * **Python에서는 지원하지 않음**
  * 캐시 시 메모리 효율성이 **RDD에 비해 압도적으로 빠름** (실험 결과: RDD는 약 60GB, Dataset은 약 12~13GB)

## 2. 참고: Spark SQL

**Spark SQL** (```SparkSQL```) 은 **SQL 쿼리를 이용한 데이터 처리 모듈** 이다.

* SQL 문법은 ```ANSI SQL, HIVEQL``` 과 동일한 문법을 사용한다.
* DB에 생성된 테이블 뷰 등에 SQL 쿼리 실행 가능

## 참고 자료

* [[BigData] Spark( RDD vs DataFrame vs Dataset) + SparkSQL - 데이터 엔지니어를 꿈꾸는 Spidy web블로그](https://spidyweb.tistory.com/197)
* [Spark - RDD vs Dataframes vs Datasets - Small talks with something](https://timewizhan.tistory.com/entry/Spark-RDD-vs-Dataframes-vs-Datasets)
* [[Spark] RDD action & transformation + Dataframe의 연산 (operation) 분류](https://spidyweb.tistory.com/332)
