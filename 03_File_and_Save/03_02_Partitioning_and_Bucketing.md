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

## 3. Bucketing

**Bucketing (버케팅)** 은 **데이터프레임을 특정 ID 컬럼 기준으로 분할** 하여 테이블로 저장하는 것이다.

* Bucketing 의 방법
  * 먼저 ```bucket 개수``` 및 ```ID 컬럼``` 을 지정한다.
  * 컬럼 값 기준으로 **해싱 후 bucket 개수로 그 값을 나눠서** 특정 레코드가 가야 할 테이블을 결정한다.
* Bucketing 의 장점
  * 저장된 테이블을 **추후에는 그냥 로딩하여 사용** 하면 되므로, **반복 처리 시간이 단축** 된다. 

### 3-1. Bucketing 실습

* Bucketing 을 위해서는 ```DataFrameWriter``` 의 ```bucketBy``` 함수를 이용한다.

## 참고 자료

* [26. Spark 내부 동작(Bucketing과 Partitioning) - 데이터엔지니어스터디](https://dataengineerstudy.tistory.com/244)
