## YARN内存和CPU资源配置
https://mapr.com/blog/best-practices-yarn-resource-management/
https://blog.csdn.net/u010708577/article/details/78979793
https://blog.csdn.net/lingbo229/article/details/80935459
http://crazyadmins.com/tag/tuning-yarn-to-get-maximum-performance/

[Yarn Tunning](https://docs.cloudera.com/documentation/enterprise/6/latest/topics/cdh_ig_yarn_tuning.html#concept_vbk_m43_fr)

* yarn.nodemanager.resource.cpu-vcores：yarn可用的总cpu， total cpu - 2

* yarn.nodemanager.resource.memory-mb：yarn可用的总RAM
* yarn.nodemanager.resource.detect-hardware-capabilities为true，且该配置还是默认值-1, YARN会自动计算可用物理内存。
* yarn.nodemanager.vmem-pmem-ratio，默认值为2.1。该值为可使用的虚拟内存除以物理内存，即YARN 中任务的单位物理内存相对应可使用的虚拟内存。例如，任务每分配1MB的物理内存，虚拟内存最大可使用2.1MB。
* yarn.nodemanager.resource.system-reserved-memory-mb, YARN保留的物理内存，给非YARN任务使用，该值一般不生效，只有当yarn.nodemanager.resource.detect-hardware-capabilities为true的状态才会启用，会根据系统的情况自动计算。

YARN分配给容器的相关配置可以通过如下配置项目调整：
* yarn.scheduler.minimum-allocation-mb：默认值1024MB，是每个容器请求被分配的最小内存。如果容器请求的内存资源小于该值，会以1024MB 进行分配；如果NodeManager可被分配的内存小于该值，则该NodeManager将会被ResouceManager给关闭。
* yarn.scheduler.maximum-allocation-mb：默认值8096MB，是每个容器请求被分配的最大内存。如果容器请求的资源超过该值，程序会抛出InvalidResourceRequestException的异常。
* yarn.scheduler.minimum-allocation-vcores：默认值1，是每个容器请求被分配的最少虚拟CPU 个数，低于此值的请求将被设置为此属性的值。此外，配置为虚拟内核少于此值的NodeManager将被ResouceManager关闭。
* yarn.scheduler.maximum-allocation-vcores：默认值4，是每个容器请求被分配的最大虚拟CPU个数，高于此值的请求将抛出InvalidResourceRequestException的异常。如果开发者所提交的作业需要处理的数据量较大，需要关注上面配置项

YARN还能对容器使用的硬件资源进行控制，通过如下的配置：
* yarn.nodemanager.resource.percentage-physical-cpu-limit：默认值100。一个节点内所有容器所能使用的物理CPU的占比，默认为100%。即如果一台机器有16核，CPU的使用率最大为1600%，且该比值为100%，则所有容器最多能使用的CPU资源为1600%，如果该比值为50%，则所有容器能使用的CPU资源为800%。
* yarn.nodemanager.linux-container-executor.cgroups.strict-resource-usage：默认值为false，表示开启CPU的共享模式。共享模式告诉系统容器除了能够使用被分配的CPU资源外，还能使用空闲的CPU资源。


[Spark tunning](https://docs.cloudera.com/documentation/enterprise/6/latest/topics/cdh_ig_running_spark_on_yarn.html#spark_on_yarn_config_apps)
仍然在CDH yarn中进行配置：
* spark.executor.cores: Number of processor cores to allocate on each executor. 
* spark.executor.memory: Maximum heap size to allocate to each executor. 
* spark.yarn.executor.memoryOverhead: spark.executor.memoryOverhead和spark.executor.memory的和不能超过yarn.scheduler.maximum-allocation-mb设置的值


Spark Driver端的配置如下：
Spark在Driver端的内存不会直接影响性能，但是在没有足够内存的情况下在driver端强制运行Spark任务需要调整。

spark.driver.memory---当hive运行在spark上时，driver端可用的最大Java堆内存。
spark.yarn.driver.memoryOverhead---每个driver可以额外从yarn请求的堆内存大小。这个参数加上spark.driver.memory就是yarn为driver端的JVM分配的总内存。
　　


## YARN



### 以下还整理了一些配置项用于hive调优：

```
hive.stats.fetch.column.stats=true

hive.optimize.index.filter=true

hive.optimize.reducededuplication.min.reducer=4

hive.optimize.reducededuplication=true

hive.merge.mapfiles=true

hive.merge.mapredfiles=false

hive.merge.smallfiles.avgsize=16000000

hive.merge.size.per.task=256000000

hive.merge.sparkfiles=true

hive.auto.convert.join=true

hive.auto.convert.join.noconditionaltask=true

hive.auto.convert.join.noconditionaltask.size=20M(might need to increase for Spark, 200M)

hive.optimize.bucketmapjoin.sortedmerge=false

hive.map.aggr.hash.percentmemory=0.5

hive.map.aggr=true

hive.optimize.sort.dynamic.partition=false

hive.stats.autogather=true

hive.stats.fetch.column.stats=true

hive.compute.query.using.stats=true

hive.limit.pushdown.memory.usage=0.4 (MR and Spark)

hive.optimize.index.filter=true

hive.exec.reducers.bytes.per.reducer=67108864

hive.smbjoin.cache.rows=10000

hive.fetch.task.conversion=more

hive.fetch.task.conversion.threshold=1073741824

hive.optimize.ppd=true

```