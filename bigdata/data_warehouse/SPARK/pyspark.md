## Cloudera 配置
在安装有外部库时，需要在CDH spark 中配置Extra Python Path， 为了确认还可以在提交任务是也带上

```
PYSPARK_PYTHON=/data/soft/venv/bin/python  spark-submit --master yarn --deploy-mode client   --conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=/data/soft/venv/bin/python --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/data/soft/venv/bin/python /data/dev/spark/air_structured_streaming.py
```


# Run pyspark on cloudera cluster

In a CDH deployment, SPARK_HOME defaults to /usr/lib/spark in package installations and /opt/cloudera/parcels/CDH/lib/spark in parcel installations. In a Cloudera Manager deployment, the shells are also available from /usr/bin

```
# set below env var in /root/.bash_profile 
export JAVA_HOME=/usr/java/jdk1.8.0_181-cloudera
export SPARK_HOME=/data/cloudera/parcels/CDH/lib/spark/
export SPARK_LOCAL_HOSTNAME=localhost
export PYSPARK_PYTHON=/data/soft/venv/bin/python


# in crontab
0 16 * * * source /root/.bash_profile && /opt/cloudera/parcels/CDH/lib/spark/bin/spark-submit --jars /usr/share/java/mysql-connector-java.jar /data/dev/spark/ibean_sql.py > /tmp/ibean_sql.log

```

we have to set --jars /usr/share/java/mysql-connector-java.jar, otherwise we will get "java.lang.ClassNotFoundException: com.mysql.jdbc.Driver" error

# 使用filter优化map处理

在使用map进行处理的时候，有时候需要对想对应的数据进行预先的判定，比如这个处理msg时候先要确定在字符串中，否则无法提取相关信息.
```
def retrieve_nginx_data(msg):
    nginx_msg = msg[1]
    if "():" in nginx_msg:
        ng_filter = nginx_msg.split("():")[1]
        rule = ng_filter.split()[0]
        ip = ng_filter.split("client:")[1].split()[0].strip(',')
        url = ng_filter.split("request:")[1].split()[1]
        return ((msg[0][0], msg[0][1], rule, ip, url), 1)
```
这样处理的问题是当条件不满足的的时候，后面reduce的处理会遇到空值
```
  File "/data/yarn/nm/usercache/root/appcache/application_1571815376800_0011/container_1571815376800_0011_01_000003/pyspark.zip/pyspark/shuffle.py", line 236, in mergeValues
    for k, v in iterator:
TypeError: 'NoneType' object is not iterable
```
这种情况下最好的解决办法提取用filter处理, 在map中去掉条件
```
.filter(lambda x: "():" in x[1])

def retrieve_nginx_data(msg):
    nginx_msg = msg[1]
    ng_filter = nginx_msg.split("():")[1]
    rule = ng_filter.split()[0]
    ip = ng_filter.split("client:")[1].split()[0].strip(',')
    url = ng_filter.split("request:")[1].split()[1]
    return ((msg[0][0], msg[0][1], rule, ip, url), 1)
```