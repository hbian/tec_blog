# Hive数据处理模式
Hive SQL语法多种多样，但从数据处理的角度来说，这些语法本质上可以被分成3种模式，即过滤模式、聚合模式和连接模式。
* 过滤模式，即对数据的过滤，从过滤的粒度来看，分为数据行过滤、数据列过滤、文件过滤和目录过滤4种方式。这4种过滤方式有显式关键字表示，例如where、having等，也有隐式过滤，例如列式文件、物化视图等。
* 聚合模式，即数据的聚合，数据聚合的同时也意味着在处理数据过程中存在Shuffle的过程。Shuffle过程应该是作为每一个Hive开发者需要特别注意的地方。
* 连接模式，即表连接的操作，这类操作分为两大类：有Shuffle的连接操作和无Shuffle的连接操作。这两个类型都有优缺点，但只要涉及表连接的都需要特别注意，因为表连接常常是程序性能的瓶颈点。

## 过滤模式
### where
where子句发生在Map端，Map端的任务在执行时会尽可能将计算逻辑发送到数据所在的机器中执行，这时候可以利用分布式计算的优点，多机同时执行过滤操作，快速过滤掉大量的数据。如果能够在Map端过滤掉大量的数据，就可以减少跨机器进行网络传输到Reducer端的数据量，从而提升Map后面环节的处理效率。通过where子句的过滤模式，启示我们对于一个作业应尽量将其放在前面环节进行数据过滤，对于一个由几个大的作业组成的任务，为了提升整体的效率，也应尽可能地让前面的环节过滤掉大量非必须的数据。例如，对于一个HiveSQL脚本，通常由多个作业组成，转换成MapReduce任务，表示为Map1-Reduce1-Map2-Reduce2…-MapN-ReduceN。如果能够在前面的Map或者Reduce中过滤掉大量的数据，就有利于减少后面的作业处理和传输的数据量，从而提高整体的作业性能。

### having
having子句过滤having 子句过滤发生在数据聚合后，在MapReduce 引擎中表示在Reduce 阶段进行having子句的条件过滤。从上面的代码中可以看到，having 子句所对应的过滤操作（Filter Operator）发生在ReduceOperator和Group By Operator两个操作之后，即在Reduce阶段进行分组聚合做数据过滤。

### distinct
distinct子句过滤distinct子句用于列投影中过滤重复的数据，在Hive中其实也是发生在Reduce阶段。从上面的信息可以看到，Hive的distinct去重会在Reduce阶段使用Group By Operator操作将其转化成分组聚合的方式，分组的列key._col0就是s_age列。也就是说，在Hive中上面的语句其实和下面的语句等价
```
select distinct s_age from a
##equal in hive
select s_age from a group by s_age
```

### 列过滤
在SQL中可以使用关键字select对字段时行过滤。但是Hive存的数据是在HDFS中，如果不使用特殊的数据存储格式，在进行列筛选时，通常需要先取整行的数据，再通过列的偏移量取得对应的列值，这个过程对于HiveSQL的使用者来说是透明的，从MapReduce的伪代码中可以看出存在这样的一个过程。

## 聚合模式
### distinct
在过滤模式时我们提到distinct的过滤，其实它也兼具了部分聚合的功能。在Hive中使用distinct的功能，如果开启hive.map.aggr=true配置，那么使用distinct子句的处理流程，会在前面流程中进行数据聚合，减少数据流转到下游后，下游处理程序处理的数据量
```
set hive.map.aggr=true;
select distinct s_age from a
```
在Map阶段，进行了数据局部聚合，在Reduce阶段进行数据全局聚合。

### count(列)、count(＊)、count(1)行计数聚合模式
在实际工作中，我们经常使用的就是行数的统计。在Hive中进行行数的统计有count(列)、count(*)和count(1)几种写法，这几种写法在实际执行有一定的差异，结果可能也不太一样。
* count(列)：如果列中有null 值，那么这一列不会被记入统计的行数。另外，Hive读取数据进行计算时，需要将字节流转化为对象的序列化和反序列化的操作。
* count(*) : 不会出现count(列)在行是null值的情况下，不计入行数的问题。另外，count(*)在进行数据统计时不会读取表中的数据，只会使用到HDFS 文件中每一行的行偏移量。该偏移量是数据写入HDFS文件时，HDFS添加的。
* count(1)和count(*)类似.

严格意义上来说，count(列)和count(*)、count(1)不等价，count(列)只是针对列的计数，另外两者则是针对表的计数，当列不为null 时， count(列)和另外两者一致，但是count(列)还会涉及字段的筛选，以及数据序列化和反序列化，所以count(*)和count(1)的性能会更占优。当然，在不同数据存储格式里，上面结论不一定成立。例如，在ORC文件中，count算子可以直接读取索引中的统计信息，三者最后的表现性能差异不大。

    