
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, IntegerType

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"
os.environ["SPARK_LOCAL_HOSTNAME"] = "localhost"


def example_str_functions(df):

    # 1. F.concat()
    df_concat = df.withColumn("name_and_gender",
                              F.concat(df["name"], F.lit("_"), df["gender"]))
    df_concat.show()

    """
    결과:
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    |           name|gender|age|  birthday|used_as_character|score|   skill_codes|     name_and_gender|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    |        Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     [1, 2, 4]|      Oh-LoRA_female|
    |     An Yujin  |female| 22|2003-09-01|            false| 90.1|        [1, 3]|   An Yujin  _female|
    | Jang Wonyoung |female| 21|2004-08-31|             true| 83.1|        [1, 5]| Jang Wonyoung _f...|
    |     Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     [3, 6, 7]|     Kim Minjae_male|
    |    Lee   Minsu|  male| 25|2001-08-08|            false| 78.0|        [4, 8]|    Lee   Minsu_male|
    |           Gini|female| 22|2004-02-03|            false| 99.9|[1, 5, 10, 12]|         Gini_female|
    |        Genie  |  male| 40|1986-08-08|            false| 90.0|     [2, 3, 6]|        Genie  _male|
    |      Namoo Kim|  male| 35|1991-08-08|            false| 80.8|            []|      Namoo Kim_male|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    """

    # 2. F.trim(), F.ltrim(), F.rtrim()
    cols_to_add = {
        "ltrim": F.ltrim(df["name"]),
        "rtrim": F.rtrim(df["name"]),
        "trim": F.trim(df["name"])
    }
    df_trim = df.withColumns(cols_to_add)
    df_trim.show()

    """
    결과:
    +---------------+------+---+----------+-----------------+-----+--------------+--------------+--------------+-------------+
    |           name|gender|age|  birthday|used_as_character|score|   skill_codes|         ltrim|         rtrim|         trim|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------+--------------+-------------+
    |        Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     [1, 2, 4]|       Oh-LoRA|       Oh-LoRA|      Oh-LoRA|
    |     An Yujin  |female| 22|2003-09-01|            false| 90.1|        [1, 3]|    An Yujin  |      An Yujin|     An Yujin|
    | Jang Wonyoung |female| 21|2004-08-31|             true| 83.1|        [1, 5]|Jang Wonyoung | Jang Wonyoung|Jang Wonyoung|
    |     Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     [3, 6, 7]|    Kim Minjae|    Kim Minjae|   Kim Minjae|
    |    Lee   Minsu|  male| 25|2001-08-08|            false| 78.0|        [4, 8]|   Lee   Minsu|   Lee   Minsu|  Lee   Minsu|
    |           Gini|female| 22|2004-02-03|            false| 99.9|[1, 5, 10, 12]|          Gini|          Gini|         Gini|
    |        Genie  |  male| 40|1986-08-08|            false| 90.0|     [2, 3, 6]|       Genie  |         Genie|        Genie|
    |      Namoo Kim|  male| 35|1991-08-08|            false| 80.8|            []|     Namoo Kim|     Namoo Kim|    Namoo Kim|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------+--------------+-------------+
    """

    # 3. F.lower(), F.upper()
    cols_to_add = {
        "lower": F.lower(df["name"]),
        "upper": F.upper(df["name"])
    }
    df_lower_upper = df.withColumns(cols_to_add)
    df_lower_upper.show()

    """
    결과:
    +---------------+------+---+----------+-----------------+-----+--------------+---------------+---------------+
    |           name|gender|age|  birthday|used_as_character|score|   skill_codes|          lower|          upper|
    +---------------+------+---+----------+-----------------+-----+--------------+---------------+---------------+
    |        Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     [1, 2, 4]|        oh-lora|        OH-LORA|
    |     An Yujin  |female| 22|2003-09-01|            false| 90.1|        [1, 3]|     an yujin  |     AN YUJIN  |
    | Jang Wonyoung |female| 21|2004-08-31|             true| 83.1|        [1, 5]| jang wonyoung | JANG WONYOUNG |
    |     Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     [3, 6, 7]|     kim minjae|     KIM MINJAE|
    |    Lee   Minsu|  male| 25|2001-08-08|            false| 78.0|        [4, 8]|    lee   minsu|    LEE   MINSU|
    |           Gini|female| 22|2004-02-03|            false| 99.9|[1, 5, 10, 12]|           gini|           GINI|
    |        Genie  |  male| 40|1986-08-08|            false| 90.0|     [2, 3, 6]|        genie  |        GENIE  |
    |      Namoo Kim|  male| 35|1991-08-08|            false| 80.8|            []|      namoo kim|      NAMOO KIM|
    +---------------+------+---+----------+-----------------+-----+--------------+---------------+---------------+
    """

    # 4. F.substring()
    df_substring = df.withColumn("month",
                                 F.concat(F.substring(df["birthday"].cast("string"), 6, 2),
                                          F.lit("월")))
    df_substring.show()

    """
    결과:
    +---------------+------+---+----------+-----------------+-----+--------------+-----+
    |           name|gender|age|  birthday|used_as_character|score|   skill_codes|month|
    +---------------+------+---+----------+-----------------+-----+--------------+-----+
    |        Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     [1, 2, 4]| 10월|
    |     An Yujin  |female| 22|2003-09-01|            false| 90.1|        [1, 3]| 09월|
    | Jang Wonyoung |female| 21|2004-08-31|             true| 83.1|        [1, 5]| 08월|
    |     Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     [3, 6, 7]| 08월|
    |    Lee   Minsu|  male| 25|2001-08-08|            false| 78.0|        [4, 8]| 08월|
    |           Gini|female| 22|2004-02-03|            false| 99.9|[1, 5, 10, 12]| 02월|
    |        Genie  |  male| 40|1986-08-08|            false| 90.0|     [2, 3, 6]| 08월|
    |      Namoo Kim|  male| 35|1991-08-08|            false| 80.8|            []| 08월|
    +---------------+------+---+----------+-----------------+-----+--------------+-----+
    """


def example_array_map_functions(df):

    # 5. F.transform()
    avg_score = df.select(F.avg("score")).first()[0]
    score_std = df.select(F.stddev("score")).first()[0]
    print(f"score average = {avg_score}, std = {score_std}")

    def compute_skill_score(df):
        normalized_score = (df["score"] - avg_score) / score_std

        array_schema = ArrayType(IntegerType())
        df = df.withColumn("skill_codes",
                           F.from_json(F.col("skill_codes"), array_schema))

        return df.withColumn("normalized_score", normalized_score)

    df_transform = df.transform(compute_skill_score)
    df_transform.show()

    """
    결과:
    score average = 86.425, std = 6.848096711600135
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    |           name|gender|age|  birthday|used_as_character|score|   skill_codes|    normalized_score|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    |        Oh-LoRA|female| 22|2003-10-11|             true| 85.5|     [1, 2, 4]| -0.1350740269822884|
    |     An Yujin  |female| 22|2003-09-01|            false| 90.1|        [1, 3]|  0.5366454585512551|
    | Jang Wonyoung |female| 21|2004-08-31|             true| 83.1|        [1, 5]|-0.48553636726066024|
    |     Kim Minjae|  male| 30|1996-08-08|             true| 84.0|     [3, 6, 7]|-0.35411298965627025|
    |    Lee   Minsu|  male| 25|2001-08-08|            false| 78.0|        [4, 8]| -1.2302688403521977|
    |           Gini|female| 22|2004-02-03|            false| 99.9|[1, 5, 10, 12]|  1.9677000146879384|
    |        Genie  |  male| 40|1986-08-08|            false| 90.0|     [2, 3, 6]|  0.5220428610396572|
    |      Namoo Kim|  male| 35|1991-08-08|            false| 80.8|            []|  -0.821396110027432|
    +---------------+------+---+----------+-----------------+-----+--------------+--------------------+
    """

    # 6. F.explode()
    df_transform.select("name", F.explode("skill_codes")).limit(num=20).show()

    """
    결과:
    +---------------+---+
    |           name|col|
    +---------------+---+
    |        Oh-LoRA|  1|
    |        Oh-LoRA|  2|
    |        Oh-LoRA|  4|
    |     An Yujin  |  1|
    |     An Yujin  |  3|
    | Jang Wonyoung |  1|
    | Jang Wonyoung |  5|
    |     Kim Minjae|  3|
    |     Kim Minjae|  6|
    |     Kim Minjae|  7|
    |    Lee   Minsu|  4|
    |    Lee   Minsu|  8|
    |           Gini|  1|
    |           Gini|  5|
    |           Gini| 10|
    |           Gini| 12|
    |        Genie  |  2|
    |        Genie  |  3|
    |        Genie  |  6|
    +---------------+---+
    """


if __name__ == '__main__':
    spark = SparkSession.builder.appName("02_03_example").getOrCreate()
    df = spark.read.csv("02_03_example.csv", header=True, inferSchema=True)

    example_str_functions(df)
    example_array_map_functions(df)

