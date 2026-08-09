
## 목차

* [1. Data Skew의 개념](#1-data-skew의-개념)
  * [1-1. Data Skew의 근본 원인](#1-1-data-skew의-근본-원인)
* [2. Data Skew의 해결 방법](#2-data-skew의-해결-방법)
  * [2-1. AQE (Adaptive Query Execution)](#2-1-aqe-adaptive-query-execution)
  * [2-2. Salting](#2-2-salting)
  * [2-3. Broadcast Join](#2-3-broadcast-join)
  * [2-4. 기타 해결 방법 및 해결 방법 선택 가이드](#2-4-기타-해결-방법-및-해결-방법-선택-가이드)

## 1. Data Skew의 개념

* **Data Skew** 는 Spark 에서 데이터를 여러 파티션에 분배할 때, **균등 분배가 되지 않아서 특정 파티션에 데이터가 편중** 되는 것이다.
* Data Skew가 문제가 되는 이유는 다음과 같다.
  * 전체 작업의 종료 시점은 **가장 늦게 끝나는 task (= 처리할 데이터가 가장 많은 task)** 에 의해 결정됨
  * 게다가 처리할 데이터가 가장 많은 task의 경우 **OOM 발생 가능**

### 1-1. Data Skew의 근본 원인

Data Skew의 근본적인 원인은 다음과 같다.

* key 값의 분포가 균등하지 않지만, **시스템은 이 key 값 기준으로 데이터 분배**
* ```hash(key)``` 와 같이 해시 함수를 사용하더라도, **특정 key에 속하는 row가 많으면** 해당 파티션에 데이터가 몰리게 됨

실제 예시는 다음과 같다.

```
# 아래 데이터를 "GROUP BY server_region 으로 집계"할 때,
  server_region = 0 을 처리하는 Task 가 다른 Task 에 비해 '할 일'이 압도적으로 많다.

SELECT server_region, COUNT(*) as log_count
FROM system_logs
GROUP BY server_region

+-------------+---------+
|server_region|log_count|
+-------------+---------+
|            0| 30000000|
|            1|  4500000|
|            2|  2250000|
|            3|  3100000|
|          ...|      ...|
|           99|    50000|
+-------------+---------+
```

* 이외에도 다음과 같은 경우들이 있다.
  * ```NULL```, 기본값 등이 **같은 해시값을 가져서 특정 파티션에 몰리는** 경우
  * SQL의 ```JOIN``` 시 한쪽 테이블에 데이터가 편중되는 경우
  * **시계열 데이터** 에서 특정 시간대 (피크/이벤트 시간대 등) 에 데이터가 편중되는 경우
* **멱법칙 (Power Law)** 을 따르는 데이터 (인스타 팔로워 수 등) 의 경우

## 2. Data Skew의 해결 방법

Data Skew의 해결 방법에는 다음과 같은 것들이 있다.

| 구분                             | 설명                                                          |
|--------------------------------|-------------------------------------------------------------|
| AQE (Adaptive Query Execution) | **런타임 통계 기반** Skew 자동 감지 및 처리                               |
| Salting                        | Skew된 key에 **랜덤 접미사** 를 추가하여 **여러 파티션으로 분산 후 부분 → 최종 집계**   |
| Broadcast Join                 | JOIN 대상 중 **작은 쪽 테이블 전체를 Driver가 수집** 후 **모든 Executor에 복사** |

### 2-1. AQE (Adaptive Query Execution)

**AQE (Adaptive Query Execution)** 는 **런타임 통계에 기반하여 Skew를 자동 감지 및 처리** 한다.

* AQE의 핵심 동작 과정
  * Skew 된 파티션을 **정해진 크기로 분할**
  * 반대쪽 테이블의 **해당 파티션 복제** → 각각의 분할된 Task와 JOIN
* AQE의 한계점
  * ```Aggregation Skew (groupBy)``` 자동 처리 안됨
  * Spark 3.0+ 에서만 사용 가능

### 2-2. Salting

**Salting** 은 **Skew 된 키에 랜덤 접미사를 추가** 하여 여러 파티션으로 나누고, 이 파티션에 대해 **부분 집계 → 최종 집계 순서대로 실시** 하는 것이다.

* Salting의 장점
  * ```Aggregation Skew (groupBy)``` 적용 가능
  * **Spark 버전 무관** 하게 적용 가능
  * 분산 정도를 제어 가능
* Salting의 단점
  * 코드 복잡도 증가
  * 메모리/네트워크 비용 추가 (작은 테이블 복제로 인한 비용)

### 2-3. Broadcast Join

**Broadcast Join** 은 다음과 같이 동작한다.

* **1.** JOIN 대상 테이블 중 **작은 테이블 전체를 Driver가 수집**
* **2.** 이것을 **모든 Executor 에 복사, 즉 broadcast**

참고로 이때 **shuffle이 발생하지 않기 때문에 파티셔닝 자체가 불필요** 하다.

* 즉, 큰 테이블의 경우 **각 Executor 가 로컬 Join을 실시** 한다.

### 2-4. 기타 해결 방법 및 해결 방법 선택 가이드

이외의 해결 방법은 다음과 같다.

* 파티션 재분배 (다른 키 조합, 랜덤 등의 다른 기준으로 재파티셔닝 실시)
* Null/Default 값의 별도 처리

해결 방법을 선택하기 위한 가이드라인은 다음과 같다.

| 조건                                     | 해결 방법                  |
|----------------------------------------|------------------------|
| JOIN 에서 발생 + 한쪽 테이블이 **수백 MB 이하로 작음**  | Broadcast Join         |
| JOIN 에서 발생 + Spark 3.0+                | AQE                    |
| JOIN 에서 발생 + Spark 2.x (또는 AQE로 해결 실패) | Salting                |
| NULL, Default 값에 집중됨                   | NULL, Default 값의 별도 처리 |

## 참고 자료

* [Data Skew 진단과 해결 - kghworks](https://kghworks.tistory.com/253)