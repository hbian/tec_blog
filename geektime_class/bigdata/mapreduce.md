## MapReduce
** MapReduce 既是编程模型又是计算框架 **
在 Map 阶段为每个数据块分配一个 Map 计算任务，然后将所有 map 输出的 Key 进行合并，相同的 Key 及其对应的 Value 发送给同一个 Reduce 任务去处理。


### MapReduce 作业启动和运行
如何为每个数据块分配一个 Map 计算任务，也就是代码是如何发送到数据块所在服务器的，发送后是如何启动的，启动以后如何知道自己需要计算的数据在文件什么位置

1. 大数据应用进程。这类进程是启动 MapReduce 程序的主入口，主要是指定 Map 和 Reduce 类、输入输出文件路径等，并提交作业给 Hadoop 集群，也就是下面提到的 JobTracker 进程。这是由用户启动的 MapReduce 程序进程， 可以理解为spark submit时启动的进程。

2. JobTracker 进程。这类进程根据要处理的输入数据量，命令下面提到的 TaskTracker 进程启动相应数量的Map和Reduce进程任务，并管理整个作业生命周期的任务调度和监控。这是 Hadoop 集群的常驻进程，需要注意的是，JobTracker 进程在整个 Hadoop 集群全局唯一.在CDH中针对每个应用的监控应该就是基于这个JobTracker.

3. TaskTracker 进程。这个进程负责启动和管理Map进程以及Reduce进程。因为需要每个数据块都有对应的 map 函数，TaskTracker进程通常和HDFS的DataNode进程启动在同一个服务器。也就是说，Hadoop 集群中绝大多数服务器同时运行DataNode进程和TaskTracker 进程。

JobTracker 进程和 TaskTracker 进程是主从关系，主服务器通常只有一台,从服务器可能有几百上千台，所有的从服务器听从主服务器的控制和调度安排。主服务器负责为应用程序分配服务器资源以及作业执行的调度，而具体的计算操作则在从服务器上完成。

具体来看，MapReduce的主服务器就是JobTracker，从服务器就是TaskTracker。HDFS 的主服务器是 NameNode，从服务器是 DataNode。Yarn、Spark等也都是这样的架构，这种一主多从的服务器架构也是绝大多数大数据系统的架构方案。

重复使用的架构方案叫作架构模式，一主多从可谓是大数据领域的最主要的架构模式。主服务器只有一台，掌控全局；从服务器很多台，负责具体的事情。这样很多台服务器可以有效组织起来，对外表现出一个统一又强大的计算能力。
![mapreduce_job_process](./mapreduce_job_process.png)

1. 应用进程 JobClient 将用户作业 JAR 包存储在 HDFS 中，将来这些 JAR 包会分发给 Hadoop 集群中的服务器执行 MapReduce 计算。
2. 应用程序提交 job 作业给 JobTracker。
3. JobTracker 根据作业调度策略创建 JobInProcess 树，每个作业都会有一个自己的 JobInProcess 树。
4. JobInProcess 根据输入数据分片数目（通常情况就是数据块的数目）和设置的 Reduce 数目创建相应数量的 TaskInProcess。
5. TaskTracker 进程和 JobTracker 进程进行定时通信。
6. 如果 TaskTracker 有空闲的计算资源（有空闲 CPU 核心），JobTracker 就会给它分配任务。分配任务的时候会根据 TaskTracker 的服务器名字匹配在同一台机器上的数据块计算任务给它，使启动的计算任务正好处理本机上的数据，以实现我们一开始就提到的“移动计算比移动数据更划算”。
7. TaskTracker 收到任务后根据任务类型（是 Map 还是 Reduce）和任务参数（作业 JAR 包路径、输入数据文件路径、要处理的数据在文件中的起始位置和偏移量、数据块多个备份的 DataNode 主机名等），启动相应的 Map 或者 Reduce 进程。
8. Map 或者 Reduce 进程启动后，检查本地是否有要执行任务的 JAR 包文件，如果没有，就去 HDFS 上下载，然后加载 Map 或者 Reduce 代码开始执行。
9. 如果是 Map进程，从HDFS读取数据(通常要读取的数据块正好存储在本机),如果是 Reduce进程，将结果数据写出到 HDFS。

### MapReduce 数据合并与连接
处于不同服务器的 map 输出的 ，如何把相同的 Key 聚合在一起发送给 Reduce 任务进行处理,在 map 输出与 reduce输入之间，MapReduce计算框架处理数据合并与连接操作，这个操作有个专门的词汇叫 shuffle. 分布式计算需要将不同服务器上的相关数据合并到一起进行下一步计算，这就是shuffle。
![shuffle](./shuffle.png)

每个 Map任务的计算结果都会写入到本地文件系统，等Map任务快要计算完成的时候，MapReduce 计算框架会启动 shuffle 过程，在 Map 任务进程调用一个 Partitioner 接口，对 Map 产生的每个 进行 Reduce 分区选择，然后通过 HTTP 通信发送给对应的 Reduce 进程。这样不管 Map 位于哪个服务器节点，相同的 Key 一定会被发送给相同的 Reduce 进程。Reduce 任务进程对收到的 进行排序和合并，相同的 Key 放在一起，组成一个 传递给 Reduce 执行。map 输出的 shuffle 到哪个 Reduce 进程是这里的关键，它是由 Partitioner 来实现，MapReduce 框架默认的 Partitioner 用 Key 的哈希值对 Reduce 任务数量取模，相同的 Key 一定会落在相同的 Reduce 任务 ID 上
需要对shuffle过程中出现数据倾斜如何处理加强处理，数据倾斜就是当某个key聚集了大量数据，shuffle到同一个reduce来汇总，会导致任务失败。严重的数据倾斜可能是数据本身的问题，需要做好预处理