## Hive 文件格式以及压缩
Hive提供的格式有TEXT、SequenceFile、RCFile、ORC和Parquet等。
* SequenceFile是一个二进制key/value对结构的平面文件，在早期的Hadoop平台上被广泛用于MapReduce输出/输出格式，以及作为数据存储格式。

### PARQUET
源自于google Dremel系统，Parquet相当于GoogleDremel中的数据存储引擎。Apache Parquet 最初的设计动机是存储嵌套式数据，比如Protocolbuffer，thrift，json等，将这类数据存储成列式格式，以方便对其高效压缩和编码，且使用更少的IO操作取出需要的数据，这也是Parquet相比于ORC的优势，它能够透明地将Protobuf和thrift类型的数据进行列式存储，在Protobuf和thrift被广泛使用的今天，与parquet进行集成，是一件非容易和自然的事情。除了上述优势外，相比于ORC, Parquet没有太多其他可圈可点的地方，比如它不支持update操作（数据写成后不可修改），不支持ACID等。

Parquet is a column-oriented binary file format. The parquet is highly efficient for the types of large-scale queries. Parquet is especially good for queries scanning particular columns within a particular table. The Parquet table uses compression Snappy, gzip; currently Snappy by default.

spark天然支持parquet，并为其推荐的存储格式(默认存储为parquet)。

Hive中创建表时使用Parquet数据存储格式：

create table parquet_table(id int,name string) stored as parquet;

### ORC
ORC(OptimizedRow Columnar) 文件格式存储源自于RC（RecordColumnar File）这种存储格式，RC是一种列式存储引擎，对schema演化（修改schema需要重新生成数据）支持较差，而ORC是对RC改进，但它仍对schema演化支持较差，主要是在压缩编码，查询性能方面做了优化。RC/ORC最初是在Hive中得到使用，最后发展势头不错，独立成一个单独的项目。Hive 1.x版本对事务和update操作的支持，便是基于ORC实现的（其他存储格式暂不支持）。ORC发展到今天，已经具备一些非常高级的feature，比如支持update操作，支持ACID，支持struct，array复杂类型。你可以使用复杂类型构建一个类似于parquet的嵌套式数据架构，但当层数非常多时，写起来非常麻烦和复杂，而parquet提供的schema表达方式更容易表示出多级嵌套的数据类型。

Hive中创建表时使用ORC数据存储格式：

create table orc_table (id int,name string) stored as orc;

创建表时，指定ORC存储格式属性
orc.compress=NONE, ZLIB(Default), SNAPPY

### ORC vs PARQUET

https://zhuanlan.zhihu.com/p/141908285
Parquet 与 ORC 的不同点总结以下：

嵌套结构支持：Parquet 能够很完美的支持嵌套式结构，而在这一点上 ORC 支持的并不好，表达起来复杂且性能和空间都损耗较大。
更新与 ACID 支持：ORC 格式支持 update 操作与 ACID，而 Parquet 并不支持。
压缩与查询性能：在压缩空间与查询性能方面，Parquet 与 ORC 总体上相差不大。可能 ORC 要稍好于 Parquet。
查询引擎支持：这方面 Parquet 可能更有优势，支持 Hive、Impala、Presto 等各种查询引擎，而 ORC 与 Hive 接触的比较紧密，而与 Impala 适配的并不好。之前我们说 Impala 不支持 ORC，直到 CDH 6.1.x 版本也就是 Impala3.x 才开始以 experimental feature 支持 ORC 格式。
关于 Parquet 与 ORC，首先建议根据实际情况进行选择。另外，根据笔者的综合评估，如果不是一定要使用 ORC 的特性，还是建议选择 Parquet。

## 数据压缩
一般在hadoop集群上运行一个MapReduce会有以下步骤：
input-> Map-> shuffle -> reduce -> output
如果我们采用了数据压缩，在map阶段产生的数据大小就会减少，会减少磁盘的IO，同时还能够减少网络的IO。

经过简单的测试会发现，parquet和orc类型的表的查询效率明显优于textfile，sequencefile，parquet和orc之间差别不大。
现在看到的是parquet格式和snappy的压缩格式， 在建表语句中设置：
STORED AS PARQUET
TBLPROPERTIES ('PARQUET.COMPRESS'='SNAPPY')
在SQL中设置 set parquet.compression=SNAPPY 这个一定不能少，否则即使TBLPROPERTIES设置了也不会对数据进行压缩， 

```
set hive.exec.compress.intermediate=true --启用中间数据压缩
set hive.exec.compress.output=true; -- 启用最终数据输出压缩
set mapreduce.output.fileoutputformat.compress=true; --启用reduce输出压缩
set mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.SnappyCodec --设置reduce输出压缩格式
set mapreduce.map.output.compress=true; --启用map输入压缩
set mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.SnappyCodec；-- 设置map输出压缩格式
```
或者在hive-site.xml中设置相同配置

在查看表的压缩情况 desc formatted <table_name>,总会看到Compressed: No， 这个实际上的描述是不准确的。 
 The Compressed field is not a reliable indicator of whether the table contains compressed data. It typically always shows No, because the compression settings only apply during the session that loads data and are not stored persistently with the table metadata.


为了确认可以先获取一个hdfs文件，然后用parquet-tools进行检查
```
hdfs dfs -get /user/hive/warehouse/hive_table_test_parquet_snappy/000001_0 .

parquet-tools meta 000000_0
```
表的设计对于HiveSQL的性能也有一定的影响，但这里的实验只能说明有影响，并不能说明分区分桶表的性能一定比只分桶的表的性能差，因为基于不同业务和上层的计算逻辑，表现出来的性能差异也会不同

### Using Snappy with Spark HIVE
For most CDH components, by default Parquet data files are not compressed. Cloudera recommends enabling compression to reduce disk usage and increase read and write performance.

You do not need to specify configuration to read a compressed Parquet file. However, to write a compressed Parquet file, you must specify the compression type. The supported compression types, the compression default, and how you specify compression depends on the CDH component writing the files.

To set the compression type to use when writing data, configure the parquet.compression property:
set parquet.compression=GZIP;
INSERT OVERWRITE TABLE tinytable SELECT * FROM texttable;
The supported compression types are UNCOMPRESSED, GZIP, and SNAPPY.

To enable Snappy compression for Spark SQL when writing tables, specify the snappy codec in the spark.sql.parquet.compression.codec configuration:
sqlContext.setConf("spark.sql.parquet.compression.codec","snappy") 

## HIVE 小文件
小文件是如何产生的：
* 动态分区插入数据的时候，会产生大量的小文件，从而导致map数量的暴增
* 数据源本身就包含有大量的小文件
* reduce个数越多，生成的小文件也越多

小文件的危害:
* 从HIVE角度来看的话呢，小文件越多，map的个数也会越多，每一个map都会开启一个JVM虚拟机，每个虚拟机都要创建任务，执行任务，这些流程都会造成大量的资源浪费，严重影响性能
* 在HDFS中，每个小文件约占150byte，如果小文件过多则会占用大量的内存。这样namenode内存容量严重制约了集群的发展

从小文件的产生途径解决：
* 使用sequencefile作为表存储形式，要使用textfile，在一定程度上可以减少小文件
* 减少reduce的个数（减少生成分区数量）
* 少用动态分区，使用distribute by分区

对已经存在的小文件做出的解决方案：
* 使用Hadoop achieve把小文件进行归档
* 重建表，建表时减少reduce的数量
* 通过参数调节，设置map/reduce的数量

设置map输入合并小文件的相关参数:
```
//每个Map最大输入大小(这个值决定了合并后文件的数量)
set mapred.max.split.size=256000000;  
//一个节点上split的至少的大小(这个值决定了多个DataNode上的文件是否需要合并)
set mapred.min.split.size.per.node=100000000;
//一个交换机下split的至少的大小(这个值决定了多个交换机上的文件是否需要合并)  
set mapred.min.split.size.per.rack=100000000;
//执行Map前进行小文件合并
set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat;
```
关于这几个参数在cdh中的设置：
This property is a per job one and can be supplied as such (via code, via generic options -D, via client/gateway mapred-site.xml safety valve XML snippet).The properties in Cloudera Manager mostly apply to services and may not exhaustively cover all advanced properties.
If you'd like to apply a value to this property across all jobs, you can specify it under the YARN -> Configuration -> "MapReduce Client Advanced Configuration Snippet (Safety Valve) for mapred-site.xml" in property tags.

To indicate that the property value cannot be overridden by another , select the Final checkbox.
设置map输出和reduce输出进行合并的相关参数:
```
//设置map端输出进行合并，默认为true
set hive.merge.mapfiles = true
//设置reduce端输出进行合并，默认为false
set hive.merge.mapredfiles = true
//设置合并文件的大小
set hive.merge.size.per.task = 256*1000*1000
//当输出文件的平均大小小于该值时，启动一个独立的MapReduce任务进行文件merge。
set hive.merge.smallfiles.avgsize=16000000
```

设置表的存储格式为Sequencefile, 主要用于统计结果的SQL，reduce量结果比较小
在统计结果后再增加一个insert overwrite操作（普遍方法，特别是对于那些统计结果（reduce）产生的小文件效果特别好）此方法相当于启动一个独立的MapReduce任务进行文件merge。

