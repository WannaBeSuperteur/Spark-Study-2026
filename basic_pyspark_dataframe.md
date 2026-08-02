
* 코드

```python
import os
import sys

# set Environment Variable first, before importing pyspark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Windows host name
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"


from pyspark.sql import SparkSession

# create SparkSession
spark = SparkSession.builder.appName("test").getOrCreate()

# example data
data = [("Oh-LoRA", 22), ("Rozy", 22), ("Goddess", 25)]
columns = ["Name", "Age"]

# create & show Spark DataFrame
df = spark.createDataFrame(data, columns)
df.show()
```

* 코드 실행 결과

```python
(base) PS D:\Spark-Study-2026> python basic_pyspark_dataframe.py
WARNING: Using incubator modules: jdk.incubator.vector
26/08/02 20:21:48 WARN Shell: Did not find winutils.exe: java.io.FileNotFoundException: java.io.FileNotFoundException: HA
DOOP_HOME and hadoop.home.dir are unset. -see https://cwiki.apache.org/confluence/display/HADOOP2/WindowsProblems        
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/08/02 20:21:49 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java cla
sses where applicable
+-------+---+
|   Name|Age|
+-------+---+
|Oh-LoRA| 22|
|   Rozy| 22|
|Goddess| 25|
+-------+---+

(base) PS D:\Spark-Study-2026> 성공: PID 24632인 프로세스(PID 10048인 자식 프로세스)가 종료되었습니다.
성공: PID 10048인 프로세스(PID 4116인 자식 프로세스)가 종료되었습니다.
성공: PID 4116인 프로세스(PID 26796인 자식 프로세스)가 종료되었습니다.

(base) PS D:\Spark-Study-2026>
```

* 참고
  * 아래와 같이 환경 변수를 미리 설정하지 않으면 ```org.apache.spark.SparkException: Python worker failed to connect back.``` 오류가 발생할 수 있다.
  * 환경 변수는 **```from pyspark.sql import SparkSession``` 이전에 미리 설정** 되어야 한다.

```python
# set Environment Variable first, before importing pyspark
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Windows host name
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"
```
