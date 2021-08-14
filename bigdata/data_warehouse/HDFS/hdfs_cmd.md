## 查看根目录下文件大小
 sudo -u hdfs hdfs dfs -du -h /

## 查看根目录下文件
sudo -u hdfs hadoop dfs -ls -h /
 
## 删除目录
sudo -u hdfs hadoop dfs -rm -r -skipTrash /folder_name

## Spark staging 目录清理
 /user/root/.sparkStaging/ 会生成job相关的文件，没有被自动清理
 sudo -u hdfs hdfs dfs -rm -r -skipTrash /user/root/.sparkStaging/*

## spark 日志清理
在spark main中打Enable Event Log Cleaner

清空spark任务执行历史记录 hadoop dfs -ls /user/spark/applicationHistory hadoop dfs -rm -r -skipTrash /user/spark/applicationHistory


# HDFS副本集配置
dfs.replication这个集群默认是3副本，如果非重要数据可以设置为2，节约存储空间。


# hbase 在region server配置中默认最大化压缩七天一次, hbase.hregion.majorcompaction， 改为1days