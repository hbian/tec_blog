## Spark Structured Streaming
https://www.adaltas.com/en/2019/04/18/spark-streaming-data-pipelines-with-structured-streaming/

It is built on top of the existing Spark SQL engine and the Spark DataFrame. The Structured Streaming engine shares the same API as with the Spark SQL engine and is as easy to use. Spark Structured Streaming models streaming data as an infinite table. Its API allows the execution of long-running SQL queries on a stream abstracted as a table.

Internally, by default, Structured Streaming queries are processed using a micro-batch processing engine, which processes data streams as a series of small batch jobs thereby achieving end-to-end latencies as low as 100 milliseconds and exactly-once fault-tolerance guarantees. However, since Spark 2.3, we have introduced a new low-latency processing mode called Continuous Processing, which can achieve end-to-end latencies as low as 1 millisecond with at-least-once guarantees.

## pyspark_kafka_structured_streaming 示例

该示例将从kafka中应用structured_streaming的方式读取消息，从json消息中过滤和提前部分字段并打印
```
# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark import SparkContext


from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import from_json
from pyspark.sql.types import *

spark = SparkSession.builder.appName("SSKafka").getOrCreate()

#定义schema, 从json中提取的字段和类型
schema = StructType([StructField("message", StringType()), StructField("tags", ArrayType(StringType()))])

log_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka1.amcc.tz:9092").option("subscribe", "hello").load()\
     .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

#定义schema, 从json中提取的字段和类型
message = log_df.select(from_json("value", schema).alias("json"))

# Start running the query that prints the running counts to the console
query = message \
    .writeStream\
    .outputMode('append')\
    .format('console')\
    .option('truncate', False)\
    .option('numRows', 5)\
    .start()

query.awaitTermination()
```

kafka 消息如下
```
{"@timestamp":"2019-05-23T08:39:35.734Z","beat":{"hostname":"spark_test","input_type":"log","message":"2019-05-23 16:39:34.835 [grpc-default-executor-259] [] INFO  hello world","offset":14678666,"source":"/data/logs/spark_test.log","tags":["spark","kafka","uat"],"type":"log"}
``` 
