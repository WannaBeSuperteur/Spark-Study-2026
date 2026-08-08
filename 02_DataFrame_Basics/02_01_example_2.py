
import os
import sys
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType, StructField,
                               StringType, IntegerType, BooleanType, DoubleType, DateType)


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"

spark = SparkSession.builder.appName("02_01_example").getOrCreate()

data = [("Oh-LoRA", "female", 22, datetime.strptime("2003-10-11", "%Y-%m-%d"), True, 85.5),
        ("Rozy", "female", 22, datetime.strptime("2021-08-19", "%Y-%m-%d"), False, 83.9)]

schema = StructType(
    [
        StructField("name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("birthday", DateType(), True),
        StructField("used_as_character", BooleanType(), True),
        StructField("score", DoubleType(), True)
    ]
)
df = spark.createDataFrame(data, schema=schema, verifySchema=True)
df.show()
