## Cloudera 配置
在安装有外部库时，需要在CDH spark 中配置Extra Python Path， 为了确认还可以在提交任务是也带上

```
PYSPARK_PYTHON=/data/soft/venv/bin/python  spark-submit --master yarn --deploy-mode client   --conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=/data/soft/venv/bin/python --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/data/soft/venv/bin/python /data/dev/spark/air_structured_streaming.py
```
