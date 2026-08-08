
## 목차

* [1. 데이터셋 정보 보기 ```show()``` ```limit()``` ```head()``` ```count()```](#1-데이터셋-정보-보기-show-limit-head-count)
* [2. 특정 컬럼의 데이터 추출, 정렬하기 ```select()``` ```filter()``` ```where()``` ```orderBy()```](#2-특정-컬럼의-데이터-추출-정렬하기-select-filter-orderby)
* [3. 데이터 그룹핑하기 ```groupBy()``` ```agg()```](#3-데이터-그룹핑하기-groupby-agg)
* [4. 컬럼 데이터 변환하기 ```withColumn()```](#4-컬럼-데이터-변환하기-withcolumn)
* [5. column 삭제하기 ```drop()```](#5-column-삭제하기-drop)
* [6. 결측치 row 찾고 대체하기 ```isNull()``` ```fillna()```](#6-결측치-row-찾고-대체하기-isnull-fillna)

## 1. 데이터셋 정보 보기 ```show()``` ```limit()``` ```head()``` ```count()```

**1-1. ```show()``` 함수로 DataFrame 미리보기**

* 예제 코드

```python
# df 전체 보기
print("1-1. df 전체 보기")
df.show()
```

* 코드 실행 결과

```
1-1. df 전체 보기
+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|        Genie|  male| 40|1986-08-08|            false| 90.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|         NULL|  male| 37|1989-01-01|             true| NULL|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
+-------------+------+---+----------+-----------------+-----+
```

**1-2. ```limit()``` 함수로 상위 N개의 row만 보기**

* 예제 코드

```python
# df의 위쪽 5개의 row만 보기
print("1-2. df의 위쪽 5개의 row만 보기")
df.limit(num=5).show()
```

* 코드 실행 결과

```
1-2. df의 위쪽 5개의 row만 보기
+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
+-------------+------+---+----------+-----------------+-----+
```

**1-3. ```head()``` 함수로 DataFrame의 row 확인하기**

* 예제 코드

```python
# df의 위쪽 1개의 row만 보기
print("1-3. df의 위쪽 1개의 row만 보기")
row = df.head()
print(row)

# df의 위쪽 3개의 row만 list 형태로 보기
print("1-4. df의 위쪽 3개의 row만 list 형태로 보기")
row = df.head(3)
print(row)
```

* 코드 실행 결과

```
1-3. df의 위쪽 1개의 row만 보기
Row(name='Oh-LoRA', gender='female', age=22, birthday=datetime.date(2003, 10, 11), used_as_character=True, score=85.5)
1-4. df의 위쪽 3개의 row만 list 형태로 보기
[Row(name='Oh-LoRA', gender='female', age=22, birthday=datetime.date(2003, 10, 11), used_as_character=True, score=85.5),
 Row(name='An Yujin', gender='female', age=22, birthday=datetime.date(2003, 9, 1), used_as_character=False, score=90.1),
 Row(name='Jang Wonyoung', gender='female', age=21, birthday=datetime.date(2004, 8, 31), used_as_character=True, score=83.1)]
```

**1-4. ```count()``` 함수 등으로 행, 열 개수 확인하기**

* 예제 코드

```python
# df의 행 개수, 열 개수 구하기
print("1-5. df의 행 개수, 열 개수 구하기")
row_count = df.count()
column_count = len(df.columns)
print(f'행 개수 {row_count}, 열 개수 {column_count}')
```

* 코드 실행 결과

```
1-5. df의 행 개수, 열 개수 구하기
행 개수 10, 열 개수 6
```

## 2. 특정 컬럼의 데이터 추출, 정렬하기 ```select()``` ```filter()``` ```where()``` ```orderBy()```

**2-1. ```select()``` 함수로 특정 컬럼의 데이터 추출하기**

* 예제 코드

```python
# 특정 컬럼의 데이터 추출하기
print("2-1. 특정 컬럼의 데이터 추출하기")
df.select('name').show()
df.select(df['name']).show()
df.select(df.name).show()
```

* 코드 실행 결과 (모두 동일)

```
2-1. 특정 컬럼의 데이터 추출하기
+-------------+
|         name|
+-------------+
|      Oh-LoRA|
|     An Yujin|
|Jang Wonyoung|
|   Kim Minjae|
|    Lee Minsu|
|         Gini|
|        Genie|
|    Namoo Kim|
|         NULL|
|     Mr. Null|
+-------------+
```

**2-2. ```filter()```, ```where()``` 함수로 특정 조건을 만족시키는 데이터 추출하기**

* 예제 코드

```python
# 특정 조건을 만족시키는 데이터 추출하기
print("2-2. 특정 조건을 만족시키는 데이터 추출하기")
df.filter(df['age'] >= 25).show()
df.filter(df.age >= 25).show()
df.filter('age >= 25').show()
df.where('age >= 25').show()
```

* 코드 실행 결과 (모두 동일)

```
2-2. 특정 조건을 만족시키는 데이터 추출하기
+----------+------+---+----------+-----------------+-----+
|      name|gender|age|  birthday|used_as_character|score|
+----------+------+---+----------+-----------------+-----+
|Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
| Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|     Genie|  male| 40|1986-08-08|            false| 90.0|
| Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|      NULL|  male| 37|1989-01-01|             true| NULL|
+----------+------+---+----------+-----------------+-----+
```

**2-3. ```filter()```, ```where()``` 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)**

* 예제 코드

```python
# 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)
print("2-3. 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)")
cond1 = col('age') >= 25
cond2 = col('used_as_character')
df.filter(cond1 & cond2).show()
df.where(cond1 & cond2).show()
```

* 코드 실행 결과 (모두 동일)

```
2-3. 특정 조건을 만족시키는 데이터 추출하기 (AND 조건)
+----------+------+---+----------+-----------------+-----+
|      name|gender|age|  birthday|used_as_character|score|
+----------+------+---+----------+-----------------+-----+
|Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|      NULL|  male| 37|1989-01-01|             true| NULL|
+----------+------+---+----------+-----------------+-----+
```

**2-4. ```filter()```, ```where()``` 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)**

* 예제 코드

```python
# 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)
print("2-4. 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)")
df.filter(cond1 | cond2).show()
df.where(cond1 | cond2).show()
```

* 코드 실행 결과 (모두 동일)

```
2-4. 특정 조건을 만족시키는 데이터 추출하기 (OR 조건)
+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|        Genie|  male| 40|1986-08-08|            false| 90.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|         NULL|  male| 37|1989-01-01|             true| NULL|
+-------------+------+---+----------+-----------------+-----+
```

**2-5. 응용: SQL의 LIKE 구문처럼 사용하기**

* 예제 코드

```python
# SQL의 LIKE 구문처럼 사용하기
print("2-5. 응용: SQL의 LIKE 구문처럼 사용하기")
df.where("name LIKE '%N%' OR name LIKE '%n%'").show()
```

* 코드 실행 결과

```
2-5. 응용: SQL의 LIKE 구문처럼 사용하기
+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|        Genie|  male| 40|1986-08-08|            false| 90.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
+-------------+------+---+----------+-----------------+-----+
```

**2-6. ```orderBy()``` 함수로 특정 컬럼 값 기준 데이터 정렬하기**

* 예제 코드

```python
# 특정 컬럼 값 기준 데이터 정렬하기
print("2-6. 특정 컬럼 값 기준 데이터 정렬하기")
df.orderBy("Age", ascending=True).show()
df.orderBy(col("Age"), ascending=False).show()
df.orderBy(col("Age").desc()).show()
df.orderBy(col("Age"), col("name").desc()).show()
```

* 코드 실행 결과

```
2-6. 특정 컬럼 값 기준 데이터 정렬하기
+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|         NULL|  male| 37|1989-01-01|             true| NULL|
|        Genie|  male| 40|1986-08-08|            false| 90.0|
+-------------+------+---+----------+-----------------+-----+

+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|        Genie|  male| 40|1986-08-08|            false| 90.0|
|         NULL|  male| 37|1989-01-01|             true| NULL|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
+-------------+------+---+----------+-----------------+-----+

+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|        Genie|  male| 40|1986-08-08|            false| 90.0|
|         NULL|  male| 37|1989-01-01|             true| NULL|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
+-------------+------+---+----------+-----------------+-----+

+-------------+------+---+----------+-----------------+-----+
|         name|gender|age|  birthday|used_as_character|score|
+-------------+------+---+----------+-----------------+-----+
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|
|         Gini|female| 22|2004-02-03|            false| 99.9|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|
|         NULL|  male| 37|1989-01-01|             true| NULL|
|        Genie|  male| 40|1986-08-08|            false| 90.0|
+-------------+------+---+----------+-----------------+-----+
```

## 3. 데이터 그룹핑하기 ```groupBy()``` ```agg()```

**3-1. ```groupBy()``` 함수로 특정 컬럼을 기준으로 그룹핑하고, 최대/최소/평균 집계하기**

* 예제 코드

```python
# 3-1. 특정 컬럼을 기준으로 그룹핑하고, 최대/최소/평균 집계하기
print("3-1. 특정 컬럼을 기준으로 그룹핑하고, 최대/최소/평균 집계하기")
df.groupBy("gender").max("score").show()
df.groupBy("gender").min("score").show()
df.groupBy("gender").avg("score").show()
df.groupBy("gender", "used_as_character").max("score").show()
df.groupBy(["gender", "used_as_character"]).max("score").show()
```

* 코드 실행 결과

```
3-1. 특정 컬럼을 기준으로 그룹핑하고, 최대/최소/평균 집계하기
+------+----------+
|gender|max(score)|
+------+----------+
|  NULL|      NULL|
|female|      99.9|
|  male|      90.0|
+------+----------+

+------+----------+
|gender|min(score)|
+------+----------+
|  NULL|      NULL|
|female|      83.1|
|  male|      78.0|
+------+----------+

+------+----------+
|gender|avg(score)|
+------+----------+
|  NULL|      NULL|
|female|     89.65|
|  male|      83.2|
+------+----------+

+------+-----------------+----------+
|gender|used_as_character|max(score)|
+------+-----------------+----------+
|  NULL|             NULL|      NULL|
|  male|            false|      90.0|
|female|             true|      85.5|
|female|            false|      99.9|
|  male|             true|      84.0|
+------+-----------------+----------+

+------+-----------------+----------+
|gender|used_as_character|max(score)|
+------+-----------------+----------+
|  NULL|             NULL|      NULL|
|  male|            false|      90.0|
|female|             true|      85.5|
|female|            false|      99.9|
|  male|             true|      84.0|
+------+-----------------+----------+
```

**3-2. ```groupBy()``` 함수로 특정 컬럼을 기준으로 그룹핑하고, ```agg()``` 함수로 여러 개의 정보 집계하기**

* 예제 코드

```python
# 3-2. 특정 컬럼을 기준으로 그룹핑하고, 여러 개의 정보 집계하기
print("3-2. 특정 컬럼을 기준으로 그룹핑하고, 여러 개의 정보 집계하기")
df.groupBy(col("gender")) \
    .agg(F.max("score").alias("max_score"),
         F.min("score").alias("min_score"),
         F.avg("score").alias("avg_score")) \
    .show()

df.groupBy(col("gender"), col("used_as_character")) \
    .agg(F.max("score").alias("max_score"),
         F.min("score").alias("min_score"),
         F.avg("score").alias("avg_score")) \
    .show()
```

* 코드 실행 결과

```
3-2. 특정 컬럼을 기준으로 그룹핑하고, 여러 개의 정보 집계하기
+------+---------+---------+---------+
|gender|max_score|min_score|avg_score|
+------+---------+---------+---------+
|  NULL|     NULL|     NULL|     NULL|
|female|     99.9|     83.1|    89.65|
|  male|     90.0|     78.0|     83.2|
+------+---------+---------+---------+

+------+-----------------+---------+---------+-----------------+
|gender|used_as_character|max_score|min_score|        avg_score|
+------+-----------------+---------+---------+-----------------+
|  NULL|             NULL|     NULL|     NULL|             NULL|
|  male|            false|     90.0|     78.0|82.93333333333334|
|female|             true|     85.5|     83.1|             84.3|
|female|            false|     99.9|     90.1|             95.0|
|  male|             true|     84.0|     84.0|             84.0|
+------+-----------------+---------+---------+-----------------+
```

## 4. 컬럼 데이터 변환하기 ```withColumn()```

**4-1. 나이대 구하기 (```floor```, ```cast```, ```concat```, ```lit``` 함수 이용)**

* 예제 코드

```python
print("4-1. 나이대 구하기 (floor, cast, concat, lit 함수 이용)")
new_df = df.select("*")  # 대규모 데이터에서는 필요한 컬럼만 선택하는 것이 권장됨
new_df = new_df.withColumn("age_group",
                           concat((floor(col("age") / 10) * 10).cast("integer"), lit("대")))
new_df.show()
```

* 함수 설명

| 함수           | 설명                                                   |
|--------------|------------------------------------------------------|
| ```floor```  | 실수를 내림하여 정수 반환                                       |
| ```cast```   | ```value.cast(type)``` 형식으로 해당 값을 ```type``` 형식으로 변환 |
| ```concat``` | ```concat(a, b)``` 형식으로 a와 b를 그대로 연결 (concatenate)   |
| ```lit```    | 다른 언어의 data type을 **Spark data type 에 맞게 변환**        |

* 코드 실행 결과

```
4-1. 나이대 구하기 (floor, cast, concat, lit 함수 이용)
+-------------+------+---+----------+-----------------+-----+---------+
|         name|gender|age|  birthday|used_as_character|score|age_group|
+-------------+------+---+----------+-----------------+-----+---------+
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     20대|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|     20대|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|     20대|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     30대|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|     20대|
|         Gini|female| 22|2004-02-03|            false| 99.9|     20대|
|        Genie|  male| 40|1986-08-08|            false| 90.0|     40대|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|     30대|
|         NULL|  male| 37|1989-01-01|             true| NULL|     30대|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|     20대|
+-------------+------+---+----------+-----------------+-----+---------+
```

**4-2. 정확한 나이 구하기 (```current_date```, ```months_between``` 함수 이용)**

* 예제 코드

```python
# 4-2. 정확한 나이 구하기 (current_date, months_between 함수 이용)
print("4-2. 정확한 나이 구하기 (current_date, months_between 함수 이용)")
new_df = df.withColumn("exact_age",
                        round(months_between(current_date(), col("birthday")) / 12, 1))
new_df.show()
```

* 함수 설명

| 함수                   | 설명                                                                                 |
|----------------------|------------------------------------------------------------------------------------|
| ```current_date```   | 오늘 날짜 반환                                                                           |
| ```months_between``` | ```months_between(date1, date2)``` 로 ```date1 - date2``` 의 **정확한 달 수 (months)** 반환 |

* 코드 실행 결과

```
4-2. 정확한 나이 구하기 (current_date, months_between 함수 이용)
+-------------+------+---+----------+-----------------+-----+---------+
|         name|gender|age|  birthday|used_as_character|score|exact_age|
+-------------+------+---+----------+-----------------+-----+---------+
|      Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     22.8|
|     An Yujin|female| 22|2003-09-01|            false| 90.1|     22.9|
|Jang Wonyoung|female| 21|2004-08-31|             true| 83.1|     21.9|
|   Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     30.0|
|    Lee Minsu|  male| 25|2001-08-08|            false| 78.0|     25.0|
|         Gini|female| 22|2004-02-03|            false| 99.9|     22.5|
|        Genie|  male| 40|1986-08-08|            false| 90.0|     40.0|
|    Namoo Kim|  male| 35|1991-08-08|            false| 80.8|     35.0|
|         NULL|  male| 37|1989-01-01|             true| NULL|     37.6|
|     Mr. Null|  NULL| 20|2006-01-01|             NULL| NULL|     20.6|
+-------------+------+---+----------+-----------------+-----+---------+
```

## 5. column 삭제하기 ```drop()```

**5-1. 1개의 컬럼 삭제하기**

* 예제 코드

```python
# 5-1. 특정 컬럼 삭제
print("5-1. 특정 컬럼 삭제")
df.drop("birthday").show()
```

* 실행 결과

```
5-1. 특정 컬럼 삭제
+-------------+------+---+-----------------+-----+
|         name|gender|age|used_as_character|score|
+-------------+------+---+-----------------+-----+
|      Oh-LoRA|female| 22|             true| 85.5|
|     An Yujin|female| 22|            false| 90.1|
|Jang Wonyoung|female| 21|             true| 83.1|
|   Kim Minjae|  male| 30|             true| 84.0|
|    Lee Minsu|  male| 25|            false| 78.0|
|         Gini|female| 22|            false| 99.9|
|        Genie|  male| 40|            false| 90.0|
|    Namoo Kim|  male| 35|            false| 80.8|
|         NULL|  male| 37|             true| NULL|
|     Mr. Null|  NULL| 20|             NULL| NULL|
+-------------+------+---+-----------------+-----+
```

**5-2. 여러 개의 컬럼 삭제하기**

* 예제 코드

```python
# 5-2. 한번에 여러 컬럼 삭제
print("5-2. 한번에 여러 컬럼 삭제")
df.drop("birthday", "used_as_character").show()
```

* 실행 결과

```
+-------------+------+---+-----+
|         name|gender|age|score|
+-------------+------+---+-----+
|      Oh-LoRA|female| 22| 85.5|
|     An Yujin|female| 22| 90.1|
|Jang Wonyoung|female| 21| 83.1|
|   Kim Minjae|  male| 30| 84.0|
|    Lee Minsu|  male| 25| 78.0|
|         Gini|female| 22| 99.9|
|        Genie|  male| 40| 90.0|
|    Namoo Kim|  male| 35| 80.8|
|         NULL|  male| 37| NULL|
|     Mr. Null|  NULL| 20| NULL|
+-------------+------+---+-----+
```

## 6. 결측치 row 찾고 대체하기 ```isNull()``` ```fillna()```

## 참고 자료

* [[PySpark] Spark의 DataFrame API를 알아보자! (1) - 앎의 공간](https://techblog-history-younghunjo1.tistory.com/498)
* [[PySpark] Spark의 DataFrame API를 알아보자! (2) - 앎의 공간](https://techblog-history-younghunjo1.tistory.com/499)