## CDH 6.0.1 的集群
* Apache Hadoop   3.0.0  
* Apache HBase    2.0.0
* Apache Hive   2.1.1
* Apache Parquet    1.9.0
* Apache Spark  2.2.0
* Apache Sqoop  1.4.7
* Apache ZooKeeper  3.4.5


## HIVE
### Hive metastore 
Provides metastore services when Hive is configured with a remote metastore.
Cloudera Manager treats the Hive Metastore Server as a required role for all Hive services. A remote metastore provides the following benefits:
* The Hive metastore database password and JDBC drivers do not need to be shared with every Hive client; only the Hive Metastore Server does. 
* Control activity on the Hive metastore database. To stop all activity on the database, stop the Hive Metastore Server. This makes it easy to back up and upgrade, which require all Hive activity to stop.

提供一个远程HIVE metastore的连接服务,并不是HIVE metastore数据库本身

### HiveServer2 
Enables remote clients to run Hive queries, and supports a Thrift API tailored for JDBC and ODBC clients, Kerberos authentication, and multi-client concurrency. 

### WebHCat 
HCatalog is a table and storage management layer for Hadoop that makes the same table information available to Hive, Pig, MapReduce, and Sqoop. Table definitions are maintained in the Hive metastore, which HCatalog requires. WebHCat allows you to access HCatalog using an HTTP (REST style) interface.


### Gateway
Because the Hive service does not have worker roles, another mechanism is needed to enable the propagation of client configurations to the other hosts in your cluster. In Cloudera Manager gateway roles fulfill this function. 

### Transaction (ACID) Support in Hive
The CDH distribution of Hive does not support transactions (HIVE-5317). Currently, transaction support in Hive is an experimental feature that only works with the ORC file format. Cloudera recommends using the Parquet file format, which works across many tools. Merge updates in Hive tables using existing functionality, including statements such as INSERT, INSERT OVERWRITE, and CREATE TABLE AS SELECT.

### Apache Parquet Tables with Hive in CDH

```
CREATE TABLE parquet_table_name (x INT, y STRING) STORED AS PARQUET;
```

* Set dfs.blocksize to 256 MB in HDFS Config, Default size is 128 MB
* To enhance performance on Parquet tables in Hive, see Enabling Query Vectorization.

To set the compression type to use when writing data, configure the parquet.compression property:
```
SET parquet.compression=GZIP;
INSERT OVERWRITE TABLE tinytable SELECT * FROM texttable;
```
The supported compression types are UNCOMPRESSED, GZIP, and SNAPPY.

### Hive on Spark Memory and Hardware Requirements
Memory:
* Minimum: 16 GB
* Recommended: 32 GB for larger data sizes
Individual executor heaps should be no larger than 16 GB so machines with more RAM can use multiple executors.

CPU:  
* Minimum: 4 cores
* Recommended: 8 cores for larger data sizes
Disk space requirements are driven by scratch space requirements for Spark spill.




