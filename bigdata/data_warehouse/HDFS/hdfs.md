整个HDFS主要有3个组件：NameNode、DataNode和Client。下面对这3个组件做个简要介绍。Client主要有以下几个职能： 
* 与NameNode进行交互，获取文件位置信息和文件块信息。  
* 与DataNode进行交互，读写数据文件。
* 访问并管理HDFS集群。

## HDFS 优化
* Hive 作业生成的小文件，过多的小文件会加重NameNode 的负担，导致集群整体性能下降。
* 设置合理的HDFS文件块的大小，可以减轻NameNode的负担，增加数据本地化操作的概率，提升程序性能。
* 适当增大NameNode的Java堆，调整JVM的参数可以提升NameNode性能。
* 在集群进行扩容和缩容的情况时，需要调整NameNode 服务处理程序计数和NameNode 处理程序计数。
* 在HDFS写入大数据文件的时候，可以尝试启用写入后清理缓存，启用写入后立即对磁盘数据排队。
* 在HDFS有比较多的随机读，或者一次性需要读取大数据文件时，可以启用读取后清理缓存。
* 集群的单机性能较高，可以适当增大处理程序计数。
* HDFS在读取数据时会开启HDFS快速读取。


https://blog.csdn.net/mocas_wang/article/details/108026856

## HDFS命名空间管理
HDFS的命名空间包含目录、文件和块。在HDFS1.0架构中，在整个HDFS集群中只有一个命名空间，并且只有唯一一个NameNode，负责对这个命名空间进行管理。
HDFS使用的是传统的分级文件体系，因此用户可以像使用普通文件系统一样创建、删除目录和文件以及在目录间移动文件、重命名文件等。
HDFS2.0新特性federation联邦功能支持多个命名空间，并且允许在HDFS中同时存在多个NameNode。HDFS的HA模式就是基于多个NameNode的。