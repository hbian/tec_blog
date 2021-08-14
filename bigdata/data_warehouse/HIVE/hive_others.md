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

## Hive开窗函数
Function (arg1,..., argn) OVER ([PARTITION BY <...>] [ORDER BY <....>]
[<window_expression>])
Function (arg1,..., argn) 可以是下面的函数：


比如说这样的一个飞机行李销售数据：
```
desc dwd_accounting_ancillary_ticket_daily;
ticketnumber            string
cabin                   string                                      
fltnum                  string                                      
dt                      string                                      
         
select ticketnumber, cabin, fltnum from  dwd_accounting_ancillary_ticket_daily where dt='2020-06-01' limit 10;
OK
872-5281296376  R   GX8920
872-5281296377  R   GX8920
847-2495389144  Z   PN6322
826-2507283747  A   GS7840
872-5278191903  T   GX8920
872-2300731758  G   GX8854
872-5278394006  Z   GX8949
847-2413716909  G   PN6269
872-2132688199  T   GX8966
872-5272471535  R   GX8850
```
窗口聚合函数: Aggregate Functions, 比如：sum(...)、 max(...)、min(...)、avg(...)等.

```
select fltnum, cabin, count(*) over (partition by fltnum, cabin order) as cnt from dwd_accounting_ancillary_ticket_daily where dt='2020-06-03' order by fltnum, cabin limit 10;
PN6443  Q   4
PN6443  T   11
PN6443  U   3
PN6443  Z   1
PN6444  G   1
PN6445  Z   36
```
窗口排序函数: Sort Functions: 数据排序函数, 比如 ：rank(...)、row_number(...)等.
row_number: 根据具体的分组和排序，为每行数据生成一个起始值等于1的唯一序列数
```
select ticketnumber,fltnum,baseprice, row_number() over(order by baseprice desc) from ads_accounting_ancillary_resv_daily where dt='2020-06-03' limit 10;

826-5285398020  GS7567  320 1
826-2507373085  GS7627  320 2
826-5285398020  GS7567  320 3
826-5286892069  GS6619  320 4
826-2441004619  GS7895  320 5
886-2106000666  UQ2555  300 6
886-5278943191  UQ2583  300 7

```

rank: 对组中的数据进行排名，如果名次相同，则排名也相同，但是下一个名次的排名序号会出现不连续。比如查找具体条件的topN行
```
select ticketnumber,fltnum,baseprice, rank() over(order by baseprice desc) from ads_accounting_ancillary_resv_daily where dt='2020-06-03' limit 10;

826-5285398020  GS7567  320 1
826-2507373085  GS7627  320 1
826-5285398020  GS7567  320 1
826-5286892069  GS6619  320 1
826-2441004619  GS7895  320 1
886-2106000666  UQ2555  300 6
886-5278943191  UQ2583  300 6
886-2105992460  UQ2520  300 6
886-5285355943  UQ2522  300 6
872-5285677992  GX8966  260 10

```

dense_rank: 函数的功能与rank函数类似，dense_rank函数在生成序号时是连续的，而rank函数生成的序号有可能不连续。当出现名次相同时，则排名序号也相同。而下一个排名的序号与上一个排名序号是连续的
```
select ticketnumber,fltnum,baseprice, dense_rank() over(order by baseprice desc) from ads_accounting_ancillary_resv_daily where dt='2020-06-03' limit 10;

826-5285398020 GS7567  320 1
826-2507373085  GS7627  320 1
826-5285398020  GS7567  320 1
826-5286892069  GS6619  320 1
826-2441004619  GS7895  320 1
886-2106000666  UQ2555  300 2
886-5278943191  UQ2583  300 2
886-2105992460  UQ2520  300 2
886-5285355943  UQ2522  300 2
872-5285677992  GX8966  260 3

```

percent_rank
排名计算公式为：(current rank - 1)/(total number of rows - 1)
```
select fltnum,baseprice, percent_rank() over(order by baseprice desc) from ads_accounting_ancillary_resv_daily where dt='2020-06-03' limit 10;

GS7567  320 0.0
GS7627  320 0.0
GS7567  320 0.0
GS6619  320 0.0
GS7895  320 0.0
UQ2555  300 0.0199203187250996
UQ2583  300 0.0199203187250996
UQ2520  300 0.0199203187250996
UQ2522  300 0.0199203187250996
GX8966  260 0.035856573705179286


```


通过子查询获得行李价格最贵的几个航班
```
aken: 1.308 seconds, Fetched: 9 row(s)
hive> select ticketnumber,fltnum,baseprice,fare_rank from (select ticketnumber,fltnum,baseprice, dt, dense_rank() over(order by baseprice desc) fare_rank from ads_accounting_ancillary_resv_daily where dt='2020-06-03') tmp where  fare_rank <3;
826-2507373085  GS7627  320 1
826-5285398020  GS7567  320 1
826-5286892069  GS6619  320 1
826-2441004619  GS7895  320 1
826-5285398020  GS7567  320 1
886-5278943191  UQ2583  300 2
886-2105992460  UQ2520  300 2
886-5285355943  UQ2522  300 2
886-2106000666  UQ2555  300 2


```

Analytics Functions: 统计和比较函数, 比如：lead(...)、lag(...)、 first_value(...)等.
cume_dist
如果按升序排列，则统计：小于等于当前值的行数/总行数(number of rows ≤ current row)/(total number of rows）。如果是降序排列，则统计：大于等于当前值的行数/总行数。比如，统计小于等于当前工资的人数占总人数的比例 ，用于累计统计.
```
select fltnum,baseprice, cume_dist() over(order by baseprice) from ads_accounting_ancillary_resv_daily where dt='2020-06-03' limit 10;

GX7861  40  0.003968253968253968
GX8949  60  0.01984126984126984
GX8978  60  0.01984126984126984
GX8973  60  0.01984126984126984
GX8949  60  0.01984126984126984
UQ2520  75  0.047619047619047616
UQ2617  75  0.047619047619047616
UQ2618  75  0.047619047619047616
UQ2535  75  0.047619047619047616
UQ2516  75  0.047619047619047616
```

lead(value_expr[,offset[,default]])
用于统计窗口内往下第n行值。第一个参数为列名，第二个参数为往下第n行（可选，默认为1），第三个参数为默认值（当往下第n行为NULL时候，取默认值，如不指定，则为NULL.
NULL时候，取默认值，如不指定，则为NULL.

lag(value_expr[,offset[,default]])
与lead相反，用于统计窗口内往上第n行值。第一个参数为列名，第二个参数为往上第n行（可选，默认为1），第三个参数为默认值（当往上第n行为NULL时候，取默认值，如不指定，则为NULL.

first_value
取分组内排序后，截止到当前行，第一个值

last_value
取分组内排序后，截止到当前行，最后一个值

窗口规范，窗口规范支持的格式：
```
(ROW | RANGE) BETWEEN (UNBOUNDED | [num]) PRECEDING AND ([num] PRECEDING | CURRENT ROW | (UNBOUNDED | [num]) FOLLOWING)
(ROW | RANGE) BETWEEN CURRENT ROW AND (CURRENT ROW | (UNBOUNDED | [num]) FOLLOWING)
(ROW | RANGE) BETWEEN [num] PRECEDING AND (UNBOUNDED | [num]) FOLLOWING
```

当ORDER BY后面缺少窗口从句条件，窗口规范默认是
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

当ORDER BY和窗口从句都缺失，窗口规范默认是：
ROW BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING

unbounded preceding and unbouned following的意思针对当前所有记录的前一条、后一条记录，也就是表中的所有记录。
rows between 1 preceding and unbounded following
实际1在这里不是从第1条记录开始的意思，而是指当前记录的前一条记录。preceding前面的修饰符是告诉窗口函数执行时参考的记录数，如同unbounded就是告诉oracle不管当前记录是第几条，只要前面有多少条记录，都列入统计的范围。

rows between unbounded preceding and current row: 这个就可以看到从第一行到当前行的滚动记录

## Hive 去重处理
除重不做统计操作
* select 之中使用distinct 关键字，只能在最前面使用关键字，
如果是 select name ,distinct age from po 这样的使用方式就是会报错。
正确的使用方式：select distinct age,name from po;
这样的distinct方式，使用了之后，就是求name age 得特殊值，然后求出唯一性。

* 直接使用GROUP BY:
select a, b from test group by a,b

* 使用分组函数
select a, b from
(select a, b
row_number() over(partition by a,b) as row_id
from test
) t
where row_id=1;

```
对于 source, dest, depature_date做去重处理

SELECT Distinct 'ALL',  
    trim(split(ibe_cmd, ',')[1]), 
    trim(split(ibe_cmd, ',')[2]),
    trim(depature_date),
    current_timestamp()
FROM hnadata.dwd_ibean_comhu_av_analysis 

SELECT 'ALL',  
    trim(split(ibe_cmd, ',')[1]), 
    trim(split(ibe_cmd, ',')[2]),
    trim(depature_date),
    current_timestamp()
FROM hnadata.dwd_ibean_comhu_av_analysis
GROUP BY  
ibe_cmd,
depature_date

SELECT Distinct 'ALL',  
    trim(split(t.ibe_cmd, ',')[1]), 
    trim(split(t.ibe_cmd, ',')[2]),
    trim(t.depature_date),
    current_timestamp()
FROM(
SELECT ibe_cmd,
depature_date,
ROW_NUMBER() OVER (PARTITION BY ibe_cmd, depature_date) AS row_id
FROM hnadata.dwd_ibean_comhu_av_analysis
WHERE dt='$DB_DATE'
) t
WHERE t.row_id=1;
```

distinct和group by这两种方法在我司的hive环境一下执行计划和底层执行都是一样都是hash(key)。我看到有些博客上面说group by比distinct好，原因是distinct的reduce为1而group by是hash(key)。
分组函数除重缺点:1.跟每组的数据量有关系，比如a=1，b=1占绝大部分会分到一个reduce处理。2.使用两层查询耗费资源。优点:可以输出分组外的字段比如:c。这样就可以实现多字段的除重或者说多字段的唯一，比如:a，b在记录里面都唯一。


## Spark SQL读取Hive分区表出现Input path does not exist
相同的SQL在hive中执行没有任何问题，但在使用spark sql会出现
```
Caused by: org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: hdfs://cdhdata3.gauss.tz:8020/data/warehouse/pro/dws/accounting/air/resv/daily/dt=pn
```
从hdfs中看并没有这个partition，但是在hive中执行show partitions <table>，查看<table>表对应的所有分区,确实存在这个partition，只是分区对应的hdfs目录不存在了。
Spark SQL处理时，hive分区表数据会根据show partitions中的分区去加载，发现目录缺失就会出错了。需要执行删除partition的命令， 个人理解实际上也就是在hive的metadata中删除。
```
alter table  dws_accounting_air_resv_daily drop partition (dt='pn');
```


## 基于hive对时间的处理
"2020-07-28T16:58:26.728609019+08:00" 将一个带有时区的时间转换为标准的时间格式。
Hive自身并不带处理包含时区信息的函数，需要先对时区T等字段进行处理
regexp_replace(regexp_replace(logging_date, 'T', ' '), '\\\\+08:00', '')
利用regexp_replace，设置T和+08:00为空值，那么数据会转换为

"2020-07-28 16:58:26.728609019"

from_unixtime(unix_timestamp('<log_date>'+28800,'yyyy-MM-dd HH:mm:ss')通过对时间进行加小时的处理完成时区信息的转换，然后

把固定日期转换成时间戳:
select unix_timestamp('2020-05-29','yyyy-MM-dd')  --返回结果 1590681600

时间戳转换成固定日期:
select from_unixtime(1590729143,'yyyy-MM-dd HH:mm:ss') --返回结果 2020-05-29 13:12:23


## bash hive转义
shell语言也有转义字符，自身直接处理。
而hive语句在shell脚本中执行时，就需要先由shell转义后，再由hive处理。这个过程又造成二次转义。
以，注意hive语句在shell脚本执行时，转义字符需要翻倍。hive处理的是shell转义后的语句，必须转以后正确，才能执行， '\\\\+08:00'， 比如这里需要对+进行转义，那么需要4个\字符。
