
## 목차

* [1. 행 기반 (csv, JSON), 열 기반 (Parquet) 포맷 차이](#1-행-기반-csv-json-열-기반-parquet-포맷-차이)
* [2. 각 포맷 별 특징](#2-각-포맷-별-특징)
  * [2-1. Parquet](#2-1-parquet)
  * [2-2. ORC](#2-2-orc)
* [3. 압축 알고리즘 (Snappy vs. Zlib)](#3-압축-알고리즘-snappy-vs-zlib)
* [4. 참고 자료](#4-참고-자료)

## 1. 행 기반 (csv, JSON), 열 기반 (Parquet) 포맷 차이

* **행 기반** 포맷과 **열 기반** 포맷을 비교하면 다음과 같다.

| 구분 (데이터 저장 방식) | 행 기반 포맷                         | 열 기반 포맷                 |
|----------------|---------------------------------|-------------------------|
| 최적화된 부분        | 쓰기 (write)                      | 읽기 (read)               |
| 예시             | ```csv``` ```JSON``` ```Avro``` | ```Parquet``` ```ORC``` |
| 적합한 쿼리         | Full Scan, 모든 컬럼 사용 쿼리          | 일부 컬럼 스캔 시              |
| 압축률            | 비교적 낮음                          | **비교적 좋음**              |

* 열 기반이 행 기반보다 읽기에 더 최적화된 이유는, **수많은 열들 중 우리가 찾고자 하는 열만 선택** 해서 찾으면 되기 때문이다.

## 2. 각 포맷 별 특징

* 각 포맷 별 특징을 요약하면 다음과 같다.

| 구분      | 특징                                              |
|---------|-------------------------------------------------|
| Parquet | 큰 데이터셋에서의 쿼리 성능 및 데이터 분석을 최적화할 수 있는 **열 기반** 포맷 |
| ORC     | **Hadoop 기반 빅데이터 처리** 에 최적화된 컬럼 기반 포맷           |

* Parquet과 ORC 모두, **열 기반** 이며, **Avro 와 함께 하둡에 최적화** 되어 있다는 것이 특징이다.

### 2-1. Parquet

**Parquet** 은 **큰 데이터셋에서의 쿼리 성능 및 데이터 분석/프로세싱을 최적화** 하기 위해 설계된 포맷이다.

* 핵심 특징
  * 데이터를 **컬럼 단위** 로 organize 함
  * **효율적인 압축**
  * 쿼리 최적화를 위해, **스키마와 통계 정보를 메타데이터 형태로 저장**
  * Apache Hadoop 과 호환성 높음 (Apache Hive 등 도구 포함)
* 주요 사용처
  * **빅 데이터 처리** 프레임워크 (Apache Hive, Apache Spark 등)
  * **쿼리 성능 및 효율적인 데이터 저장** 이 필수적인 데이터 웨어하우스 시스템

### 2-2. ORC

**ORC** 는 **Hadoop 기반 빅데이터 처리에 특화된 컬럼 형태의 저장 포맷** 이다.

* 핵심 특징
  * 다른 포맷들에 비해 **좋은 성능 및 압축 효율** 을 보여줌
  * 고도로 최적화된 **열 기반 포맷** 형태로 데이터 저장
* 주요 사용처
  * **복잡한 쿼리 및 aggregation** 이 필요한 워크플로우
  * **Apache Hive 기반** 데이터 웨어하우스 등
  * **배치 프로세싱** 및 ETL (Extract, Transform, Load) 파이프라인

## 3. 압축 알고리즘 (Snappy vs. Zlib)

압축 알고리즘 중 **Snappy** 와 **Zlib** 의 특징은 다음과 같다.

| 구분    | Snappy                     | Zlib                  |
|-------|----------------------------|-----------------------|
| 압축 성능 | 압축 및 해제가 **빠름**            | 압축 및 해제가 **상대적으로 느림** |
| 압축률   | 비교적 낮음 **(1.5 - 2.5배)**    | 비교적 높음 **(2.5 - 5배)** |
| 호환성   | Parquet & ORC 포맷 **연동 가능** | 좌동                    |

## 4. 참고 자료

* [빅쿼리 데이터 로딩 포맷 비교 CSV | JSON | Parquet | AVRO - 오몰내알](https://kgw7401.tistory.com/74)
* [데이터 압축: Parquet/ORC 포맷, Snappy/Zlib 압축 알고리즘: 컬럼 지향 포맷과 코덱 선택의 실무 최적화 - GilliLab - 정보관리기술사 노트](https://rupijun.tistory.com/entry/%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%95%95%EC%B6%95-ParquetORC-%ED%8F%AC%EB%A7%B7-SnappyZlib-%EC%95%95%EC%B6%95-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%BB%AC%EB%9F%BC-%EC%A7%80%ED%96%A5-%ED%8F%AC%EB%A7%B7%EA%B3%BC-%EC%BD%94%EB%8D%B1-%EC%84%A0%ED%83%9D%EC%9D%98-%EC%8B%A4%EB%AC%B4-%EC%B5%9C%EC%A0%81%ED%99%94)
* [A Comparative Analysis of Avro, Parquet, and ORC: Understanding the Differences - Parijat Bose (LinkedIn)](https://www.linkedin.com/pulse/comparative-analysis-avro-parquet-orc-understanding-differences-bose/)
