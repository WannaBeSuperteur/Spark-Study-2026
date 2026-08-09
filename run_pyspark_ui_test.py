# Written by Gemini + Fix time.sleep value
# Prompt:
# - Spark Web UI 접속 방법을 아주 자세히 알려줘 (Windows, PySpark 기반)

import time
from pyspark.sql import SparkSession

# SparkSession 생성 (이 시점에 Web UI가 시작됨)
spark = SparkSession.builder \
    .appName("MySparkApp") \
    .getOrCreate()

print("Spark UI가 시작되었습니다. 브라우저에서 접속해보세요.")
print(f"UI URL: {spark.sparkContext.uiWebUrl}")

# UI를 확인하는 동안 프로세스가 종료되지 않도록 300초(5분) -> 1일 대기
time.sleep(24 * 60 * 60)

# 작업 완료 후 종료
spark.stop()
