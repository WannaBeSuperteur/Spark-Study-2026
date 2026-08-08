
## 목차

* [1. 데이터셋 정보 보기 ```show()``` ```limit()``` ```head()``` ```count()```](#1-데이터셋-정보-보기-show-limit-head-count)
* [2. 특정 컬럼의 데이터 추출, 정렬하기 ```select()``` ```filter()``` ```orderBy()```](#2-특정-컬럼의-데이터-추출-정렬하기-select-filter-orderby)
* [3. 데이터 그룹핑하기 ```groupBy()``` ```agg()```](#3-데이터-그룹핑하기-groupby-agg)
* [4. 컬럼 데이터 변환하기 ```withColumn()```](#4-컬럼-데이터-변환하기-withcolumn)
* [5. row, column 삭제하기 ```drop()```](#5-row-column-삭제하기-drop)
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

## 2. 특정 컬럼의 데이터 추출, 정렬하기 ```select()``` ```filter()``` ```orderBy()```

## 3. 데이터 그룹핑하기 ```groupBy()``` ```agg()```

## 4. 컬럼 데이터 변환하기 ```withColumn()```

## 5. row, column 삭제하기 ```drop()```

## 6. 결측치 row 찾고 대체하기 ```isNull()``` ```fillna()```

## 참고 자료

* [[PySpark] Spark의 DataFrame API를 알아보자! (1) - 앎의 공간](https://techblog-history-younghunjo1.tistory.com/498)
* [[PySpark] Spark의 DataFrame API를 알아보자! (2) - 앎의 공간](https://techblog-history-younghunjo1.tistory.com/499)