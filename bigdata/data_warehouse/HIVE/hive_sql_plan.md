##  HiveSQL执行计划
Hive提供的执行计划目前可以查看的信息有以下几种：
* 查看执行计划的基本信息，即explain
* 查看执行计划的扩展信息，即explain extended
* 查看SQL数据输入依赖的信息，即explain dependency
* 查看SQL操作相关权限的信息，即explain authorization
* 查看SQL的向量化描述信息，即explain vectorization。


在查询语句的SQL 前面加上关键字explain 是查看执行计划的基本方法。用explain打开的执行计划包含以下两部分：
* 作业的依赖关系图，即STAGE DEPENDENCIES
* 每个作业的详细信息，即STAGE PLANS

* MapReduce：表示当前任务执行所用的计算引擎是MapReduce。
* Map Opertaor Tree：表示当前描述的Map阶段执行的操作信息。
* Reduce Opertaor Tree：表示当前秒时的是Reduce阶段的操作信息。

Map操作树（MapOperator Tree）信息解读如下：
* TableScan：表示对关键字alias声明的结果集 
* Statistics：表示对当前阶段的统计信息。例如，当前处理的数据行和数据量，这两个都是预估值。
* Filter Operator：表示在之前操作（TableScan）的结果集上进行数据的过滤。
* predicate：表示filter Operator进行过滤时，所用的谓词，即s_age<30 and s_namelike '%红%'。
* Select Operator：表示在之前的结果集上对列进行投影，即筛选列。
* expressions：表示需要投影的列，即筛选的列。
* outputColNames：表示输出的列名。
* Group By Operator：表示在之前的结果集上分组聚合。
* aggreations：表示分组聚合使用的算法，这里是count(1)
* keys：表示分组的列，在该例子表示的是s_age。
* Reduce output Operator：表示当前描述的是对之前结果聚会后的输出信息，这里表示Map端聚合后的输出信息。
* key expressions/value expressions:MapReduce计算引擎，在Map阶段和Reduce阶段输出的都是键-值对的形式，这里key expression和value expressions分别描述的就是Map阶段输出的键（key）和值（value）所用的数据列。这里的例子key expressions指代的就是s_age列，value exporess 指代的就是count（1）列。
* sort order：表示输出是否进行排序，+表示正序，-表示倒序。
* Map-reduce partition columns：表示Map 阶段输出到Reduce 阶段的分区列，在Hive-SQL中，可以用distribute by指代分区的列。

Reduce阶段所涉及的关键词与Map阶段的关键词是一样的，字段表示含义也相同
* compressed：在File Output Operator中这个关键词表示文件输出的结果是否进行压缩，false表示不进行输出压缩。
* input format/out putformat：分别表示文件输入和输出的文件类型。
* serde：表示读取表数据的序列化和反序列化的方式。

explain dependency的使用场景有两个。场景一，快速排除。快速排除因为读取不到相应分区的数据而导致任务数据输出异常。例如，在一个以天分区的任务中，上游任务因为生产过程不可控因素出现异常或者空跑，导致下游任务引发异常。通过这种方式，可以快速查看SQL读取的分区是否出现异常。场景二，帮助理清表的输入，帮助理解程序的运行，特别是有助于理解有多重自查询，多表连接的依赖输入。