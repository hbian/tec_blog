## 大数据软件性能优化
一般说来，大数据软件性能优化会涉及硬件、操作系统、大数据产品及其配置、应用程序开发和部署几个方面。当性能不能满足需求的时候，先看看各项性能指标是否合理，如果资源没有全面利用，那么可能是配置不合理或者大数据应用程序（包括 SQL 语句）需要优化；如果某项资源利用已经达到极限，那么就要具体来分析，是集群资源不足，需要增加新的硬件服务器，还是需要对某项硬件、操作系统或是JVM，甚至是对大数据产品源代码进行调优。

* SQL 语句优化。使用关系数据库的时候，SQL优化是数据库优化的重要手段，因为实现同样功能但是不同的 SQL 写法可能带来的性能差距是数量级的。我们知道在大数据分析时，由于数据量规模巨大，所以 SQL 语句写法引起的性能差距就更加巨大。典型的就是 Hive 的 MapJoin 语法，如果 join 的一张表比较小，比如只有几 MB，那么就可以用 MapJoin 进行连接，Hive 会将这张小表当作 Cache 数据全部加载到所有的 Map 任务中，在 Map 阶段完成 join 操作，无需 shuffle。

* 数据倾斜处理。数据倾斜是指当两张表进行join的时候,其中一张表join的某个字段值对应的数据行数特别多，那么在shuffle的时候，这个字段值（Key）对应的所有记录都会被 partition 到同一个 Reduce 任务，导致这个任务长时间无法完成。淘宝的产品经理曾经讲过一个案例，他想把用户日志和用户表通过用户 ID 进行 join，但是日志表有几亿条记录的用户 ID 是 null，Hive 把 null 当作一个字段值 shuffle 到同一个 Reduce，结果这个 Reduce 跑了两天也没跑完，SQL 当然也执行不完。像这种情况的数据倾斜，因为 null 字段没有意义，所以可以在 where 条件里加一个 userID != null 过滤掉就可以了。

* Spark 应用配置优化, 比如executor的个数

* 操作系统配置优化， 比如关闭transparent huge pages
```
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/ transparent_hugepage/defrag
```
