## CDH hive on spark
```
#最重要是set
#Default Execution Engine
hive.execution.engine=spark
Spark On YARN Service: Spark

```

## Hive 值为NULL
当hive值中NULL，而预期应该是有其他数值时候，请检查数据结构是否正确，比如定义该列值为int，但写入的数值为string， 这样会导致写入失败，hive写入时没有报错而是自动填充了null

## HIVE 优化
https://blog.csdn.net/qq_36753550/article/details/82825207
set hive.exec.dynamic.partition.mode=nonstrict; （它的默认值是strick，即不允许分区列全部是动态的）

### 避免一些不必要的MR作业
在hive中，我们可以进行优化，让一些语句避免执行MR作业，从而加快效率，这些参数就是hive.fetch.task.conversion，在hive-site.xml中可以设置下面属性：
```
<property>
  <name>hive.fetch.task.conversion</name>
  <value>more</value>
```
默认值为minimal,在不设置该参数的情况下，查询某一字段会执行mapreduce程序，当设置参数后，就不会走mapreduce程序了

###  数据压缩和存储格式
压缩方式 Snappy比较好， 和其他压缩方式比较: 压缩后大，压缩速度快，可以分割
在ORCFile或者Parquet之间选择，暂时使用的ORC
ORCFile: 数据按行分块，每块按照列存储。压缩快，快速列存取。效率比rcfile高，是rcfile的改良版本。
```
#在建表语句末尾添加：
tblproperties ("orc.compression"="snappy")
```
## 内部表, 外部表 AND 临时表
* 创建表时：创建内部表时，会将数据移动到数据仓库指向的路径；若创建外部表，仅记录数据所在的路径， 不对数据的位置做任何改变。

* 删除表时：在删除表的时候，内部表的元数据和数据会被一起删除，而外部表只删除元数据，不删除数据。这样外部表相对来说更加安全些，数据组织也更加灵活，方便共享源数据

* 临时表：临时分析，在关闭hive客户端后，临时表就会消失。主要用于存储不重要中间结果集，不重要的表。
 

```
#Internal table
create table int_table(
empno int,
ename string,
job string,
mgr int,
hiredate string,
sal double,
comm double,
deptno int
)
row format delimited fields terminated by '\t' 
LOCATION '/user/hive/warehouse/hadoop.db/int_table';

#External table

create EXTERNAL table ext_table(
deptno int,
dname string,
loc string
)
row format delimited fields terminated by '\t' ;
load data local inpath '/opt/datas/dept.txt' into table ext_table;


create TEMPORARY table tmp_table(  
deptno int,  
dname string,
loc string
)
row format delimited  fields terminated by '\t';
 
load data local inpath '/opt/datas/dept.txt' into table tmp_table;

```


### 分区表

普通的表：select * from logs where date = '20171209'，执行流程：对全表的数据进行查询，然后才过滤操作。

分区表：select * from logs where date = '20171209'，执行流程：直接加载对应文件路径下的数据。适用于大数据量，可以通过分区快速定位需要查询的数据，分区表的作用主要是提高了查询检索的效率 。

```
#Create 分区表
DROP TABLE IF EXISTS ods_rresv;
CREATE EXTERNAL TABLE ods_rresv (
`AIRLINE` STRING,
`id` INT,
`code` STRING,
`channeltype` STRING,
`reserveandholddate` STRING
) COMMENT '订单表'
PARTITIONED BY (`dt` string)
row format delimited fields terminated by '\t'
location '/data/warehouse/pro/hnadata/tdpreport/ods/ods_rresv/'
;
load data inpath '/data/origin_data/pro/hnadata/tdpreport/9h/rresv/2019-12-01'  into table hnadata.ods_rresv partition(dt='2019-12-01');

hdfs dfs -ls /data/warehouse/pro/hnadata/tdpreport/ods/ods_rresv
drwxr-xr-x   - root supergroup          0 2019-11-22 14:20 /data/warehouse/pro/hnadata/tdpreport/ods/ods_rresv/dt=2019-11-08
drwxr-xr-x   - root supergroup          0 2019-11-28 11:06 /data/warehouse/pro/hnadata/tdpreport/ods/ods_rresv/dt=2019-11-26
drwxr-xr-x   - root supergroup          0 2019-11-28 10:56 /data/warehouse/pro/hnadata/tdpreport/ods/ods_rresv/dt=2019-11-27

```

创建二级分区并且加载数据
```
create table part2_tab(  
empno int,  
ename string,
job string,  
mgr int,
hiredate string,  
sal double,  
comm double,  
deptno int
)partitioned by (`datetime` string,hour string)
row format delimited  fields terminated by '\t';
 
load data local inpath '/opt/datas/emp.txt' into table part2_tab partition(`datetime`='20171209',hour='01');
 
load data local inpath '/opt/datas/emp.txt' into table part2_tab partition(`datetime`='20171209',hour='02');
/user/hive/warehouse/hadoop.db/emp_part2/datetime=20171209/hour=01
/user/hive/warehouse/hadoop.db/emp_part2/datetime=20171209/hour=02
```

手动创建目录/user/hive/warehouse/hadoop.db/emp_part2/datetime=20171209/hour=03，然后put上数据，表select查询是查询不到的。然后，使用alter将路径添加到原数据库mysql数据库中。
```
alter table emp_part2 add partition(`datetime`='20171209',hour='03');
```


## 桶表

[Hive桶表](https://www.jianshu.com/p/50b662e57d40)
我们知道分区和分桶都是对数据的细分管理，如果两者结合使用，肯定是有层级和先后顺序的。实际也是如此，我们的数据是先分区管理，对每个分区的数据我们可以使用分桶进行管理。也就是说分区分桶表，其中的分桶必然在最末端的分区中。

```
create external table if not exists part_bk_users(
f1 string,
f2 string,
f3 string
)
partitioned by(contry string,city string)
clustered by(f1) into 5 buckets
row format delimited fields terminated by'\t';
```

```
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.enforce.bucketing = true;
```

## Hive表的修改
https://blog.csdn.net/xueyao0201/article/details/79387647

## HIVE SQL 优化
* where条件优化
优化前（关系数据库不用考虑会自动优化）：
select m.cid,u.id from order m join customer u on( m.cid =u.id )where m.dt='20180808';
优化后(where条件在map端执行而不是在reduce端执行）：
select m.cid,u.id from （select * from order where dt='20180818'） m join customer u on( m.cid =u.id);

* union优化
尽量不要使用union （union 去掉重复的记录）而是使用 union all 然后在用group by 去重

* count distinct优化
不要使用count (distinct   cloumn) ,使用子查询
select count(1) from (select id from tablename group by id) tmp;
 
* 用in 来代替join
如果需要根据一个表的字段来约束另为一个表，尽量用in来代替join .
select id,name from tb1  a join tb2 b on(a.id = b.id);
 select id,name from tb1 where id in(select id from tb2); in 要比join 快

* 消灭子查询内的 group by 、 COUNT(DISTINCT)，MAX，MIN。 可以减少job的数量。

