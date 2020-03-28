## Redis
Redis 快的原因:
* Redis 是基于内存的数据库，这样可以避免磁盘 I/O.
* Redis 数据结构结构简单，Redis 采用 Key-Value 方式进行存储，也就是使用 Hash 结构进行操作，数据的操作复杂度为 O(1)。
* Redis采用单进程单线程模型，这样做的好处就是避免了上下文切换和不必要的线程之间引起的资源竞争。
* Redis 采用了多路 I/O 复用技术。这里的多路指的是多个socket网络连接，复用指的是复用同一个线程。采用多路 I/O 复用技术的好处是可以在同一个线程中处理多个 I/O 请求，尽量减少网络 I/O 的消耗，提升使用效率。

## Redis的数据类型
* 字符串类型是对应的结构是key-value。设置某个键的值，使用方法为set key value，比如我们想要给 name 这个键设置值为 zhangfei，可以写成set name zhangfei。如果想要取某个键的值，可以使用get key，比如想取 name 的值，写成 get name 即可。
* 哈希（hash）提供了字段和字段值的映射，对应的结构是key-field-value。如果我们想要设置某个键的哈希值，可以使用hset key field value，如果想要给 user1 设置 username 为 zhangfei，age 为 28
```
hset user1 username zhangfei
hset user1 age 28

#设置多个值
#hmset key field value [field value...]
Hmset user1 username zhangfei age 28

```
* 字符串列表（list）的底层是一个双向链表结构，所以我们可以向列表的两端添加元素，时间复杂度都为 O(1)，同时我们也可以获取列表中的某个片段。
如果想要向列表左侧增加元素可以使用：LPUSH key value [...]，同样，我们也可以使用RPUSH key value [...]向列表右侧添加元素
```
LPUSH heroList zhangfei guanyu liubei
```
如果我们想要获取列表中某一片段的内容，使用LRANGE key start stop即可，比如我们想要获取 heroList 从 0 到 4 位置的数据，写成LRANGE heroList 0 4即可
* 字符串集合（set）是字符串类型的无序集合，与列表（list）的区别在于集合中的元素是无序的，同时元素不能重复。如果想要在集合中添加元素，可以使用SADD key member [...]，比如我们给 heroSet 集合添加 zhangfei、guanyu、liubei、dianwei 和 lvbu 这五个元素，可以写成
```
#add
SADD heroSet zhangfei guanyu liubei dianwei lvbu
#Remove
SREM heroSet liubei lvbu
#Get all members
SMEMBERS heroSet
#Check member in set
SISMEMBER key member 
```
* 有序字符串集合（SortedSet，简称 ZSET）理解成集合的升级版。实际上 ZSET 是在集合的基础上增加了一个分数属性，这个属性在添加修改元素的时候可以被指定。每次指定后，ZSET 都会按照分数来进行自动排序，也就是说我们在给集合 key 添加 member 的时候，可以指定 score。
```
#Add new member 
ZADD key score member [...]
#Remove member
ZREM key member [member …]
#Get member score
ZSCORE key member
```
我们也可以获取某个范围的元素列表。如果想要分数从小到大进行排序，使用ZRANGE key start stop [WITHSCORES]，如果分数从大到小进行排序，使用ZREVRANGE key start stop [WITHSCORES]。需要注意的是，WITHSCORES 是个可选项，如果使用 WITHSCORES 会将分数一同显示出来

## Redis连接池机制
连接池机制基于直接连接的弊端，Redis 提供了连接池的机制，这个机制可以让我们事先创建好多个连接，将其放到连接池中，当我们需要进行 Redis 操作的时候就直接从连接池中获取，完成之后也不会直接释放掉连接，而是将它返回到连接池中。连接池机制可以避免频繁创建和释放连接，提升整体的性能。
连接池机制的原理在连接池的实例中会有两个 list，保存的是_available_connections和_in_use_connections，它们分别代表连接池中可以使用的连接集合和正在使用的连接集合。当我们想要创建连接的时候，可以从_available_connections中获取一个连接进行使用，并将其放到_in_use_connections中。如果没有可用的连接，才会创建一个新连接，再将其放到_in_use_connections中。如果连接使用完毕，会从_in_use_connections中删除，添加到_available_connections中，供后续使用。