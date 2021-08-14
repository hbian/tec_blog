## Hive MetaStore的结构
https://www.jianshu.com/p/420ddb3bde7f 

DBS记录数据库的信息
```
字段  解释
DB_ID   数据库的编号,默认的数据库编号为1,如果创建其他数据库的时候,这个字段会自增,主键
DESC    对数据库进行一个简单的介绍
DB_LOCATION_URI 数据库的存放位置，默认是存放在hdfs://ip:9000/user/hive/warehouse，如果是其他数据库，就在后面添加目录,默认位置可以通过参数hive.metastore.warehouse.dir来设置
NAME    数据库的名称
OWNER_NAME  数据库所有者名称
OWNER_TYPE  数据库所有者的类型
DBS的DB_ID与DATABASE_PARAMS的DB_ID进行关联。
```

DATABASE_PARAMS DB_ID是一个主键，使得DBS与DATABASE_PARAMS关联。
```
字段  解释
DB_ID   数据库的编号
PARAM_KEY   参数名称
PARAM_VALUE 参数值
```
生产cdh上测试为空表

TBLS记录数据表的信息
```
字段  解释
TBL_ID  在hive中创建表的时候自动生成的一个id，用来表示，主键
CREATE_TIME 创建的数据表的时间，使用的是时间戳
DBS_ID  这个表是在那个数据库里面
LAST_ACCESS_TIME    最后一次访问的时间戳
OWNER   数据表的所有者
RETENTION   保留时间
SD_ID   标记物理存储信息的id
TBL_NAME    数据表的名称
TBL_TYPE    数据表的类型,MANAGED_TABLE, EXTERNAL_TABLE, VIRTUAL_VIEW, INDEX_TABLE
VIEW_EXPANDED_TEXT  展开视图文本，非视图为null
VIEW_ORIGINAL_TEXT  原始视图文本，非视图为null

select * from tbls where TBL_NAME='ods_ibean_commonhu_logs'


```

TBLS的SD_ID与SDS的SD_ID进行关联,TBLS的DB_ID与DBS的DB_ID进行关联,相关的thrift类为Table,StorageDescriptor。



TABLE_PARAMS: TABLE_PARAMS的TBL_ID与TBLS的TBL_ID的进行关联,TBL_ID与PARAM_KEY作为联合主键。

```
字段  解释
TBL_ID  数据的编号
PARAM_KEY   参数
PARAM_VALUE 参数的值
```
PARAM_KEY会有如下属性
```
COLUMN_STATS_ACCURATE   精确统计列
numFiles    文件数
numRows 行数
rawDataSize 原始数据大小
totalSize   当前大小
transient_lastDdlTime   最近一次操作的时间戳
```

SDS 此对象包含有关属于表的数据的物理存储的所有信息，数据表的存储描述。
TBLS的SD_ID与SDS的SD_ID进行关联，SDS的SERDE_ID与SERDES的SERDE_ID进行关联，SDS的CD_ID与CDS的CD_ID进行关联。相关的thrift表为StorageDescriptor。
```
字段  解释
SD_ID   主键
CD_ID   数据表编号
INPUT_FORMAT    数据输入格式
IS_COMPRESSED   是否对数据进行了压缩
IS_STOREDASSUBDIRECTORIES   是否进行存储在子目录
LOCATION    数据存放位置
NUM_BUCKETS 分桶的数量
OUTPUT_FORMAT   数据的输出格式
SERDE_ID    序列和反序列的信息
```

CDS 记录数据表的编号，仅有一个一个自增的序列，就是一个标识。
```
字段  解释
CD_ID   主键,记录数据表的编号
```

SERDES 记录序列化和反序列化信息
```
字段  解释
SERDE_ID    主键,记录序列化的编号
NAME    序列化和反序列化名称，默认为表名
SLIB    使用的是哪种序列化方式
```

SERDE_PARAMS SERDE_PARAMS的SERDE_ID与SERDES的SERDE_ID进行关联
```
字段  解释
SERDE_ID    主键,记录序列化的编号
PARAM_KEY   参数名称
PARAM_VALUE 参数的值
```

TAB_COL_STATS 数据表的列信息统计


Sort_COLS 记录要进行排序的列
生产cdh上测试为空表

COLUMNS_V2 用于描述列的信息 
```
字段  解释
CD_ID   表的编号
COMMENT 相关描述信息
COLUMN_NAME 列的名称
TYPE_NAME   类的类型
```

分区表PARTITIONS
```
字段  解释
PART_ID 分区的编号
CREATE_TIME 创建分区的时间
LAST_ACCESS_TIME    最近一次访问时间
PART_NAME   分区的名字
SD_ID   存储描述的id
TBL_ID  数据表的id
```

PARTITION_PARAMS
```
字段  解释
PART_ID 分区的编号
PARAM_KEY   参数
PARAM_VALUE 参数的值
```

PARTITION_KEYS
```
字段  解释
TBL_ID  数据表的编号
PKEY_COMMENT    分区字段的描述
PKEY_NAME   分区字段的名称
PKEY_TYPE   分区字段的类型
```

PARTITION_KEY_VALS
```
字段  解释
PART_ID 分区编号
PART_KEY_VAL    分区字段的值
```


###  Hive删除整个表
从元数据删除Hive的表需要得到五个ID.
TBL_ID：表ID
SD_ID ：序列化配置信息
CD_ID：字段信息ID
PART_ID：分区ID
SERDE_ID：序列化类ID

TBL_ID（56）和SD_ID（61，62，63，64）可以从TBLS表（存表的创建信息）得到，CD_ID（56）,SERDE_ID（64）可以从SDS表（表的压缩和格式文件存储的基本信息）得到，PART_ID（11，12，13）可以从PARTITIONS表（存储表分区的基本信息）中得到。

需要删除的partitions部分：
```
partition_key_vals, partition_params,partitions,partition_keys
```

需要删除的table:
```
table_params, tbls
```
删除完table信息后，hive表里面已经查不到该表了
还需要删除的其他元数据：
```
SERDE_PARAMS, serdes, SDS, COLUMNS_V2
```

```
delete from partition_params where part_id in (282141, 282162, 282809, 284022, 285229, 286441,287654,  288866,290073,291280,296651);

delete from partition_key_vals  where part_id in (282141, 282162, 282809, 284022, 285229, 286441,287654,  288866,290073,291280,296651);

delete from partitions where TBL_ID='133328'

delete from partition_keys where TBL_ID='133328'


delete from table_params where tbl_id='133328';
delete from tbls where tbl_id='133328';


delete from serdes where SERDE_ID='415411'
delete from SERDE_PARAMS where SERDE_ID='415411'

delete from SDS where SD_ID='415411'
delete from COLUMNS_V2 where cd_id='133328';
```