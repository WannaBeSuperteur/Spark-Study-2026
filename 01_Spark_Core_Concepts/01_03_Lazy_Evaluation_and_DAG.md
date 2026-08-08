
## 목차

* [1. Lazy Evaluation](#1-lazy-evaluation)
  * [1-1. Lazy vs. Eager Evaluation](#1-1-lazy-vs-eager-evaluation)
* [2. 2가지 type의 Dependency](#2-2가지-type의-dependency)
* [3. DAG (Directed Acyclic Graph)](#3-dag-directed-acyclic-graph)

## 1. Lazy Evaluation

**Lazy Evaluation** 이란, **Transformation 단계에서는 실행하지 않고 Action 단계에서 실행** 하는 것을 의미한다.

* Transformation 과 Action ([참고](01_02_RDD_DataFrame_Dataset.md#1-1-rdd))

| 구분             | 설명                                    |
|----------------|---------------------------------------|
| Transformation | 데이터를 단순히 처리하는 것 (map, reduce, join 등) |
| Action         | **Transformation 의 결과를 저장** 하는 것      |

### 1-1. Lazy vs. Eager Evaluation

* Eager Evaluation (즉시 실행) 을 하게 된다면, **DAG 최적화가 불가능** 하다는 단점이 있다.
  * 실제로 **Pandas 에서는 Eager 방식을 사용** 한다.

## 2. 2가지 type의 Dependency

* Action을 통해 **RDD를 실제로 생성** 할 때, 그 생성 방법 (경로, 계획) 을 최적화하려면 **각 노드의 데이터 셔플이 최소한** 으로 일어나야 한다.
  * Lazy Evaluation은 이와 같이 **최적의 RDD 생성 경로를 찾는 것** 이라고 볼 수 있다.
* RDD 생성 방법의 의존성 (Dependency) 은 다음과 같이 구분된다.

| 구분                | 설명                          | 특징             | 예시                                 |
|-------------------|-----------------------------|----------------|------------------------------------|
| Narrow Dependency | **1개의 Node** 에서 작업 수행 가능    | 해당 노드에서 복원도 가능 | ```map``` ```filter``` ```union``` |
| Wide Dependency   | **여러 개의 Node** 를 거쳐서 작업을 수행 | 속도가 **비교적 느림** | ```groupByKey```                   |

## 3. DAG (Directed Acyclic Graph)

**DAG (Directed Acyclic Graph)** 은 **Action을 통해 RDD를 실제 생성하는 계획을 그래프 형태로 나타낸 것** 이다.

* 그래프 알고리즘에서의 DAG과 같이 **단일 방향성으로 루프가 없는 형태의 그래프** 이다.
* Action 이 호출될 때 **DAG 최적화 → DAG 실행** 이 이루어진다.

## 참고 자료

* [Spark 이해하기(RDD, DAG, Lazy Evaluation) - devvon](https://pickwon.tistory.com/93)
* [Lazy Evaluation 이란? - Steadily](https://kkh1902.tistory.com/213)
* [Spark RDD, DAG란? - 내가 보기 위한 기록](https://sunrise-min.tistory.com/entry/Spark-RDD-DAG%EB%9E%80)
