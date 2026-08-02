
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

