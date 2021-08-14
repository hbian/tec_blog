# Hive 性能调优实战

使用explain 查看HiveSql执行计划：
```
hive (hnadata)> explain select dt, count(*) from ads_accounting_ancillary_resv_daily group by dt;
OK
Explain
STAGE DEPENDENCIES:
  Stage-1 is a root stage
  Stage-0 depends on stages: Stage-1

STAGE PLANS:
  Stage: Stage-1
    Spark
      Edges:
        Reducer 2 <- Map 1 (GROUP, 1)
      DagName: root_20200615185154_18334dd6-96e4-4bea-8118-d52140d88d47:1
      Vertices:
        Map 1 
            Map Operator Tree:
                TableScan
                  alias: ads_accounting_ancillary_resv_daily
                  Statistics: Num rows: 11010 Data size: 2315522 Basic stats: COMPLETE Column stats: NONE
                  Select Operator
                    expressions: dt (type: string)
                    outputColumnNames: dt
                    Statistics: Num rows: 11010 Data size: 2315522 Basic stats: COMPLETE Column stats: NONE
                    Group By Operator
                      aggregations: count()
                      keys: dt (type: string)
                      mode: hash
                      outputColumnNames: _col0, _col1
                      Statistics: Num rows: 11010 Data size: 2315522 Basic stats: COMPLETE Column stats: NONE
                      Reduce Output Operator
                        key expressions: _col0 (type: string)
                        sort order: +
                        Map-reduce partition columns: _col0 (type: string)
                        Statistics: Num rows: 11010 Data size: 2315522 Basic stats: COMPLETE Column stats: NONE
                        value expressions: _col1 (type: bigint)
        Reducer 2 
            Execution mode: vectorized
            Reduce Operator Tree:
              Group By Operator
                aggregations: count(VALUE._col0)
                keys: KEY._col0 (type: string)
                mode: mergepartial
                outputColumnNames: _col0, _col1
                Statistics: Num rows: 5505 Data size: 1157761 Basic stats: COMPLETE Column stats: NONE
                File Output Operator
                  compressed: false
                  Statistics: Num rows: 5505 Data size: 1157761 Basic stats: COMPLETE Column stats: NONE
                  table:
                      input format: org.apache.hadoop.mapred.SequenceFileInputFormat
                      output format: org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat
                      serde: org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe

  Stage: Stage-0
    Fetch Operator
      limit: -1
      Processor Tree:
        ListSink

```


将SQL转化为MapReduce，例如SQL执行计划中的Select Operator就是对列的投影操作，转化成MapReduce 算子就是对一行的数据按一定的列分割符进行分割并取出该列。

总结，其实不仅仅是MapReduce在数据处理时将所有的数据简化成业务无关的键-值对模式，大部分的大数据数计算引擎在底层实现上也是如此，如Spark、Tez和Storm。在进行数据处理时先将计算发往数据所在的节点，将数据以键-值对作为输入，在本地处理后再以键-值对的形式发往远端的节点，这个过程通用叫法为Shuffle，远端的节点将接收的数据组织成键-值对的形式作为输入，处理后的数据，最终也以键-值对的形式输出。这些都会体现在执行计划上。

开启hive.vectorized.execution.enabled操作，默认是关闭状态，将一个普通的查询转化为向量化查询执行是一个Hive 特性。它大大减少了扫描、过滤器、聚合和连接等典型查询操作的CPU 使用。标准查询执行系统一次处理一行。矢量化查询执行可以一次性处理1024行的数据块，以减少底层操作系统处理数据时的指令和上下文切换。

查看hive当前配置：
```
set hive.exec.parallel;
# 打开hive的并行
set hive.exec.parallel=true


set hive.vectorized.execution.enabled = true;
set hive.vectorized.execution.reduce.enabled = true;
```


**通过对MapReduce的学习，能看懂执行计划，但执行计划仅能提供SQL的执行逻辑，却没有提供每个过程的一些量化统计信息，这对于调优的帮助有限,可以通过YARN提供的工具查看Job日志。查看YARN Job日志可以知晓MapReduce整个过程的量化数据信息，可以较好地定位整个程序的瓶颈位置。定位到出现瓶颈的位置后，尝试使用优化“三板斧”：利用别人已有的经验来改写SQL；给SQL语句用上Hint的语法；使用数据库开放的配置参数。**


能用简单的代码就不要用复杂的代码去编写，至于调优，要讲求适时优化，在发现并定位到性能瓶颈点才开始启动调优。当然也不是说开始写代码时随便写，除了代码要尽量简单，也要遵循一些原则,总结的代码优化原则：
* 理透需求原则，这是优化的根本
* 把握数据全链路原则，这是优化的脉络
* 坚持代码的简洁原则，这让优化更加简单: 不管是写SQL，还是用其他的语言写工程化项目，都需要尽量保持代码的简洁。一份简洁的代码，是逻辑思维清晰的体现，也是对业务较好理解的一种体现。一份简洁的代码，在后期的维护及工作交接时都能给予自己和别人极大的帮助。相反，一份读起来逻辑别扭、冗长复杂的代码，有更高的几率潜藏Bug，潜藏性能不友好的逻辑，甚至它是对真实需求的一种扭曲实现。这种案例，在实际开发中比比皆是。
* 没有瓶颈时谈论优化，是自寻烦恼。从接触代码开始，笔者对编码这份工作就有了极大的好感，对自己写的代码要求也比较高，尤其是对性能十分敏感，有时可以说是“偏执”。只要凭借以往经验验证的某些技术细节是性能不好的，那么在新的代码遇到类似情况就会极力避免，即使代价大一些。但技术在更新，业务要求在变化，线上环境也在变。技术在经过版本的更新后，某些有性能问题的用法可能变得没有问题；某些业务，之前为了避免引发性能问题而过早花大力气调优的地方，甚至可以直接舍弃；某些环境可能由于业务的调整发生巨变，则导致某些原本不耗费时间的处理环节其性能却急速下降，如线上环境数据激增。有优化意识是好的，但优化不区分对象而谈优化，容易一叶障目。

当业务人员提出一个需求时，我们需要知道相关的信息，大体可以分为以下3个方面。（1）业务数据准备理清支持这个业务的基础数据有哪些，输出的数据要求是什么，这些业务的数据以什么样的方式存储，其占用空间及元数据等信息如何等。要获取上述信息，除了日常要做好需求等相关文件的梳理工作以外，在技术层面，Hive还提供了一些工具可以获取到一些业务信息。例如，通过Hive 提供的交互命令来获取所要处理的数据信息；通过收集统计信息，查看Hive的metadata库对表的数据量和占用空间等信息。在这里有两种方式可以做到快速了解Hive的元数据信息。方式1：通过desc formatted。通过desc formatted tablename来查看表信息，可以获取到注释、字段的含义（comment）、创建者用户、数据存储地址、数据占用空间和数据量等信息，具体可看下面的案例。

下面将优化所要关注的问题分为两类：
* 影响项目整体落地的问题、重大性能问题；
* 不影响项目整体落地，但是影响部分功能。
第一种情况，在实际项目中，有经验的老工一般能够预知且提早介入，一般在项目设计阶段就已经规避。第二种情况，在具体实现上，由于所处的环节较为靠后，且和实际的业务有较强的关联，会根据实际情况而反复地调整。这种情况就需要在具体环境下，依据具体的业务要求进行调优，将优化放到有瓶颈点的地方去考虑和讨论，否则只是做更多的投入和产出不成正比的工作。

## 总结调优的一般性过程
首先，要明白所有的优化是相对的，例如程序运行需要2个小时，看似很慢，但如果需求的目标是3个小时，即可正常作业，无特别情况，可以不进行优化。优化的基本流程如下：第一，选择性能评估项及各自目标，常见的评估性能指标有程序的时延和吞吐量；第二，如果系统是由多个组件和服务构成，需要分组件和服务定义性能目标；第三，明确当前环境下各个组件的性能；第四，分析定位性能瓶颈；第五，优化产生性能瓶颈的程序或者系统；第六，性能监控和告警。上面的流程是优化的基本流程，前面三点可以结合各自的实际应用场景，结合运维意见及业务的要求自行设定.

* 分析定位性能瓶颈：在Hive 中最常见的是磁盘和网络I/O 的瓶颈，其次是内存会成为一个性能瓶颈。CPU一般比I/O资源相对富余。为什么是前面三点最有可能出现瓶颈？要解释这个问题，需要了解Hive 执行计划，以及计算引擎的基本原理，并借助作业监控工具优化产生性能瓶颈的程序或者系统。在Hive 中，优化方式可以归结为3点，即优化存储、优化执行过程和优化作业的调度。
* 性能监控和告警：建立性能监控和告警，在操作系统和硬件层面可以借助Linux或UNIX系统提供的系统工具，也可以借助一些开源的工具，例如Zabbix和Ganglia；可以记录服务器运行时的历史过程，也可以定制化监控很多细粒度指标。软件层面，大数据组件可以借助cloudera或者Ambari监控工具，或者借助开源工具Prometheus和Grafana定制监控大数据组件。作业层面借助YARN Timeline提供的查看作业信息的服务信息进行监控


有这样一个案例，在同步数据的讨论会议上，业务方说有些数据库表每日都有数据更新，怎么同步更新的数据？程序员A认为目前数据日志解析工具可以捕捉数据更新。程序员B认为还有一个比较简单的方法，可以用支持事务机制的表，只是这些表使用起来有特殊限制，需要升级系统环境。资历较老的程序员会问到每日更新的数据有多少，表数据总共有多少，这些数据从开始同步到最后的数据使用，可以支持多久的等待时间。业务方说数据每日更新增量1万以内，最大的表数据量不超过10万，整体数据量不到100MB，这些数据从同步到使用允许24小时的等待时间。程序员C 认为简单数据量总量不多，可以全量同步，不会对现有的系统造成太大的压力，也不会对同步作业造成多大压力，如果不需要历史数据，可以每日覆盖对应的表，如果需要历史数据，就采用表分区的方式，按日分区，每个分区同步当日所有的数据。比较3个程序员的方案，程序员A需要引入更多的同步组件，且解析工具的部署维护是一个问题，在数据库的日志格式变更后，同步又是一个问题，并且耗时长，后期维护难度较高。程序员B需要对生产环境的软件进行升级，需要评估软件是否对现有生产环境有影响，稳定情况如何。而程序员C解了业务的整体情况后，采用的就是一般的方式——全量同步。在业务要求范围内也能快速完成业务需求。很显然，程序员C的方案对程序员A和程序员B的方案来说都是一个极大的优化，而且从源头尽可能地掐断了因一个小需求引入众多操作所带来的性能问题。



