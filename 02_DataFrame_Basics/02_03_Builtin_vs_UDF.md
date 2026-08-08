
## 목차

* [1. PySpark 사용자 정의 함수 (UDF)](#1-pyspark-사용자-정의-함수-udf)
  * [1-1. UDF 가 직렬화 병목을 일으키는 이유](#1-1-udf-가-직렬화-병목을-일으키는-이유)
* [2. PySpark UDF 대신 사용할 것](#2-pyspark-udf-대신-사용할-것)
  * [2-1. 관련 Spark 내장 함수 및 그 사용법](#2-1-관련-spark-내장-함수-및-그-사용법)
  * [2-2. Pandas UDF 및 그 사용법](#2-2-pandas-udf-및-그-사용법)
* [3. 실무에서의 안티패턴 3가지](#3-실무에서의-안티패턴-3가지)

## 1. PySpark 사용자 정의 함수 (UDF)

* PySpark의 **UDF (User Defined Function)** 은 DataFrame, SQL 등에 사용 가능한 **사용자 정의 함수** 이다.
* 함수 등록 방법에 따른 사용 가능 범위

| 함수 등록 방법                        | 사용 가능 범위                        |
|---------------------------------|---------------------------------|
| ```pyspark.sql.functions.udf``` | **PySpark DataFrame** 에서만 사용 가능 |
| ```spark.udf.register```        | **SQL** 에서도 사용 가능               |

### 1-1. UDF 가 직렬화 병목을 일으키는 이유

* PySpark 에서 사용하기 위해 **Python UDF** 를 사용하면 다음과 같은 일이 발생한다.
  * **JVM (Java) 환경** 에서 동작하는 Spark는 **데이터를 JVM → Python 프로세스로 전달** 한다.
  * 이때 **직렬화** 가 발생한다.
  * 특히, Python UDF는 기본적으로 **각 행을 Python Worker로 하나씩 전송하고 결과를 수집** 하므로, **직렬화/역직렬화 횟수가 행의 개수 (수천만 회 이상) 와 같다.** 
* 위와 같은 과정에서 **직렬화 병목** 이 발생한다.

결론적으로, **Python UDF 는 좋지 않은 선택** 이고, 대안으로 **Pandas UDF (Series to Series)** 등을 사용할 수 있다.

## 2. PySpark UDF 대신 사용할 것

* PySpark 의 **Python UDF** 대신 사용할 수 있는 것은 다음과 같다.
  * Spark의 기본 내장 함수
  * **Pandas UDF**
* Databricks 는 **UDF는 내장 Spark 함수로 표현하기 어려운 로직에서만 사용** 할 것을 권고하고 있다.

### 2-1. 관련 Spark 내장 함수 및 그 사용법

UDF 대신 사용할 수 있는 Spark의 내장 함수는 다음과 같다.

* 중요한 것은 **UDF를 사용하기 전에, 내장 함수가 있는지 검토하는 것** 이다.
* 상세: [02_03_example.py](02_03_example.py)

**1. 조건문 (if-else) 대체**

* [F.when(...)](02_02_Core_Transformation_and_Action.md#7-조건-분기-when)

**2. 문자열 처리**

* [F.concat()](02_02_Core_Transformation_and_Action.md#4-컬럼-데이터-변환하기-withcolumn) (문자열 합치기)
* ```F.trim()``` ```F.ltrim()``` ```F.rtrim()```
  * 시작과 끝이 아닌 **중간 부분의 여러 개의 공백은 1개의 공백으로 바뀌지 않는다.** 
* ```F.lower()``` ```F.upper()```
* ```F.substring(컬럼, 시작위치, 추출개수)```
  * 시작 위치의 index 는 **0이 아닌 1부터** 시작

**3. 배열 처리 함수**

* ```F.transform()```
* ```F.explode()```

### 2-2. Pandas UDF 및 그 사용법

Pandas UDF 는 **실행할 함수에 ```@pandas_udf(OOOType())``` 를 적용** 하여 호출한다.

* Pandas UDF는 **batch 단위로 처리** 하므로, **대용량 데이터 (수십만 row 이상)** 의 경우 **최대 100배의 속도 향상** 이 있다.

```python
@pandas_udf(DoubleType())
def pandas_udf_function(series: pd.Series) -> pd.Series:
    x = (series - 40.0) / 10.0
    for _ in range(20):
        x = np.sin(x) + np.cos(x * 2) + np.tan(x * 3)
    return x

...

@time_checker
def run_with_pandas_udf(df):
    new_df = df.withColumn("converted_score", pandas_udf_function("score"))
    new_df.select(F.sum("converted_score")).collect()  # action 호출 -> 실제 연산 시간 측정 가능
```

* 속도 비교 결과

```
 === 함수: run_with_python_udf ===
마지막 50 회 평균: 10.575442625989671, 표준편차: 2.293753841072866, 95% 신뢰구간: [9.9396, 11.2112]

 === 함수: run_with_pandas_udf ===
마지막 50 회 평균: 5.805304092003499, 표준편차: 1.5115407414051387, 95% 신뢰구간: [5.3863, 6.2243]
```

## 3. 실무에서의 안티패턴 3가지

UDF를 실무에서 사용할 때의 주요 안티패턴은 다음과 같다.

* **매 행마다 DB 연결을 새로 생성** 하는 경우
  * 속도 극히 저하 및 연결 고갈 우려
* null 처리 누락
* UDF 사용 결과를 **다시 UDF 입력으로 사용** (체이닝)
  * 이 경우 **단일 Pandas UDF 또는 Arrow UDF** 로 통합하는 것이 좋다.

## 참고

* [[Pyspark/SparkSQL] UDF(User Defined Function) (사용자 정의 함수) - YSY의 데이터분석 블로그](https://ysyblog.tistory.com/370)
* [Databricks UDF 성능을 고려한 올바른 사용법 - GarionNachal](https://velog.io/@hyungki26/Databricks-UDF-%EC%84%B1%EB%8A%A5%EC%9D%84-%EA%B3%A0%EB%A0%A4%ED%95%9C-%EC%98%AC%EB%B0%94%EB%A5%B8-%EC%82%AC%EC%9A%A9%EB%B2%95)


