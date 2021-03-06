数据库中的索引，其实就是一种数据结构。好比一本书的目录，它可以帮我们快速进行特定值的定位与查找，从而加快数据查询的效率。
在数据表中的数据行数比较少的情况下，比如不到 1000 行，是不需要创建索引的。

当数据重复度大，比如高于 10% 的时候，也不需要对这个字段使用索引。我之前讲到过，如果是性别这个字段，就不需要对它创建索引。这是为什么呢？如果你想要在 100 万行数据中查找其中的 50 万行（比如性别为男的数据），一旦创建了索引，你需要先访问 50 万次索引，然后再访问 50 万次数据表，这样加起来的开销比不使用索引可能还要大。

索引的类型
从功能逻辑分类:
* 普通索引是基础的索引，没有任何约束，主要用于提高查询效率。
* 唯一索引就是在普通索引的基础上增加了数据唯一性的约束，在一张数据表里可以有多个唯一索引。
* 主键索引在唯一索引的基础上增加了不为空的约束，也就是 NOT NULL+UNIQUE，一张表里最多只有一个主键索引。
* 全文索引用的不多，MySQL自带的全文索引只支持英文。我们通常可以采用专门的全文搜索引擎，比如 ES(ElasticSearch) 和 Solr。

按照物理实现方式：
* 聚集索引： 聚集索引可以按照主键来排序存储数据，这样在查找行的时候非常有效。只有当表包含聚集索引时，表内的数据行才会按找索引列的值在磁盘上进行物理排序和存储。每一个表只能有一个聚集索引，因为数据行本身只能按一个顺序存储。举个例子，如果是一本汉语字典，我们想要查找“数”这个字，直接在书中找汉语拼音的位置即可，也就是拼音“shu”。这样找到了索引的位置，在它后面就是我们想要找的数据行。
* 非聚集索引：我们也把非聚集索引称为二级索引或者辅助索引。在数据库系统会有单独的存储空间存放非聚集索引，这些索引项是按照顺序存储的，但索引项指向的内容是随机存储的。也就是说系统会进行两次查找，第一次先找到索引，第二次找到索引对应的位置取出数据行。非聚集索引不会把索引指向的内容像聚集索引一样直接放到索引的后面，而是维护单独的索引表（只维护索引，不维护索引指向的数据），为数据检索提供方便。我们还以汉语字典为例，如果想要查找“数”字，那么按照部首查找的方式，先找到“数”字的偏旁部首，然后这个目录会告诉我们“数”字存放到第多少页，我们再去指定的页码找这个字。

聚集索引与非聚集索引的原理不同，在使用上也有一些区别：
* 聚集索引的叶子节点存储的就是我们的数据记录，非聚集索引的叶子节点存储的是数据位置。非聚集索引不会影响数据表的物理存储顺序。
* 一个表只能有一个聚集索引，因为只能有一种排序存储的方式，但可以有多个非聚集索引，也就是多个索引目录提供数据检索。
* 使用聚集索引的时候，数据的查询效率高，但如果对数据进行插入，删除，更新等操作，效率会比非聚集索引低。因为聚集索引是面向读取的设计，因为我们的数据会按照聚集索引的大小顺序写入到磁盘，因此聚集索引会存在存储顺序的问题。而我们更新，插入的内容往往都是随机的，这时如果我们还是用聚集索引，所有的记录就需要重新进行排序并重新写入到磁盘中，所以效率相比于非聚集索引可能会降低。
而非聚集索引只是存储索引，我们只需要更新这个索引即可，不需要对所有的记录重新排序。

索引还可以按照字段个数进行划分，分成单一索引和联合索引。索引列为一列时为单一索引；多个列组合在一起创建的索引叫做联合索引。创建联合索引时，我们需要注意创建时的顺序问题，因为联合索引 (x, y, z) 和 (z, y, x) 在使用的时候效率可能会存在差别。这里需要说明的是联合索引存在最左匹配原则，也就是按照最左优先的方式进行索引的匹配。比如刚才举例的 (x, y, z)，如果查询条件是 WHERE x=1 AND y=2 AND z=3，就可以匹配上联合索引；如果查询条件是 WHERE y=2，就无法匹配上联合索引。但是如果是仅查询WHERE x=1仍然会匹配到索引。但是SQL条件语句中的字段顺序不重要，因为在逻辑查询优化阶段会自动进行 查询重写，也就是说WHERE y=2 AND x=1 AND z=3，顺序不对，在sql进行逻辑优化后，仍会配上联合索引。
如果我们遇到了范围条件查询，比如（<）（<=）（>）（>=）和 between 等，那么范围列后的列就无法使用到索引了。

## Hash Index

键值 key 通过 Hash 映射找到桶 bucket。在这里桶（bucket）指的是一个能存储一条或多条记录的存储单位。一个桶的结构包含了一个内存指针数组，桶中的每行数据都会指向下一行，形成链表结构，当遇到 Hash 冲突时，会在桶中进行键值的查找。那么什么是 Hash 冲突呢？如果桶的空间小于输入的空间，不同的输入可能会映射到同一个桶中，这时就会产生 Hash 冲突，如果 Hash 冲突的量很大，就会影响读取的性能。通常 Hash 值的字节数比较少，简单的 4 个字节就够了。在 Hash 值相同的情况下，就会进一步比较桶（Bucket）中的键值，从而找到最终的数据行。

### Hash索引结构VS B+树
* Hash 索引不能进行范围查询，而 B+ 树可以。这是因为 Hash 索引指向的数据是无序的，而 B+ 树的叶子节点是个有序的链表。
* Hash 索引不支持联合索引的最左侧原则（即联合索引的部分索引无法使用），而 B+ 树可以。对于联合索引来说，Hash 索引在计算 Hash 值的时候是将索引键合并后再一起计算 Hash 值，所以不会针对每个索引单独计算 Hash 值。因此如果用到联合索引的一个或者几个索引时，联合索引无法被利用。
* Hash 索引不支持ORDER BY排序，因为Hash索引指向的数据是无序的，因此无法起到排序优化的作用，而 B+ 树索引数据是有序的，可以起到对该字段 ORDER BY 排序优化的作用。
* 也无法用 Hash 索引进行模糊查询，而 B+ 树使用 LIKE 进行模糊查询的时候，LIKE 后面前模糊查询（比如 % 开头）的话就可以起到优化作用。
* 对于等值查询来说，通常 Hash 索引的效率更高，不过也存在一种情况，就是索引列的重复值如果很多，效率就会降低。这是因为遇到Hash冲突时，需要遍历桶中的行指针来进行比较，找到查询的关键字，非常耗时。所以，Hash索引通常不会用到重复值多的列上，比如列为性别、年龄的情况等。

在键值型（Key-Value）数据库中，Redis 存储的核心就是 Hash 表。

## 需要创建索引的情况
* 字段的数值有唯一性的限制，比如用户名：索引本身可以起到约束的作用，比如唯一索引、主键索引都是可以起到唯一性约束的，因此在我们的数据表中，如果某个字段是唯一性的，就可以直接创建唯一性索引，或者主键索引。
* 频繁作为WHERE查询条件的字段，尤其在数据表大的情况下: 在数据量大的情况下，某个字段在 SQL 查询的 WHERE 条件中经常被使用到，那么就需要给这个字段创建索引了。创建普通索引就可以大幅提升数据查询的效率。
* 需要经常 GROUP BY 和 ORDER BY 的列: 索引就是让数据按照某种顺序进行存储或检索，因此当我们使用GROUP BY对数据进行分组查询，或者使用ORDER BY对数据进行排序的时候，就需要对分组或者排序的字段进行索引。
* 多个单列索引在多条件查询时只会生效一个索引（MySQL 会选择其中一个限制最严格的作为索引），所以在多条件联合查询的时候最好创建联合索引。
* UPDATE、DELETE 的 WHERE 条件列，一般也需要创建索引:对数据按照某个条件进行查询后再进行 UPDATE 或 DELETE 的操作，如果对WHERE字段创建了索引，就能大幅提升效率。原理是因为我们需要先根据 WHERE 条件列检索出来这条记录，然后再对它进行更新或删除。如果进行更新的时候，更新的字段是非索引字段，提升的效率会更明显，这是因为非索引字段更新不需要对索引进行维护。
* DISTINCT 字段需要创建索引
* 做多表JOIN连接操作时，创建索引需要注意以下的原则
    * 连接表的数量尽量不要超过 3 张，因为每增加一张表就相当于增加了一次嵌套的循环，数量级增长会非常快，严重影响查询的效率。
    * 对 WHERE 条件创建索引，因为WHERE才是对数据条件的过滤。如果在数据量非常大的情况下，没有 WHERE 条件过滤是非常可怕的。
    * 对用于连接的字段创建索引，并且该字段在多张表中的类型必须一致。比如 user_id 在 product_comment 表和 user 表中都为 int(11) 类型，而不能一个为 int 另一个为 varchar 类型。

## 不需要创建索引的情况
* WHERE 条件（包括 GROUP BY、ORDER BY）里用不到的字段不需要创建索引，索引的价值是快速定位，如果起不到定位的字段通常是不需要创建索引的。
* 如果表记录太少，比如少于 1000 个，那么是不需要创建索引的。
* 字段中如果有大量重复数据，也不用创建索引，比如性别字段。
* 频繁更新的字段不一定要创建索引。因为更新数据的时候，也需要更新索引，如果索引太多，在更新索引的时候也会造成负担，从而影响效率。

## 索引失效的情况
* 如果索引进行了表达式计算，则会失效。 例如：
```
EXPLAIN SELECT comment_id, user_id, comment_text FROM product_comment WHERE comment_id+1 = 900001


+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
| id | select_type | table           | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra       |
+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
|  1 | SIMPLE      | product_comment | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 996663 |   100.00 | Using where |
+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
```
如果对索引进行了表达式计算，索引就失效了。这是因为我们需要把索引字段的取值都取出来，然后依次进行表达式的计算来进行条件判断，因此采用的就是全表扫描的方式，运行时间也会慢很多，最终运行时间为 2.538 秒。
* 如果对索引使用函数，也会造成失效: 例如使用SUBSTRING
```
EXPLAIN SELECT comment_id, user_id, comment_text FROM product_comment WHERE SUBSTRING(comment_text, 1,3)='abc'

+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
| id | select_type | table           | partitions | type | possible_keys | key  | key_len | ref  | rows   | filtered | Extra       |
+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
|  1 | SIMPLE      | product_comment | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 996663 |   100.00 | Using where |
+----+-------------+-----------------+------------+------+---------------+------+---------+------+--------+----------+-------------+
```
用Like进行改写后
```
SELECT comment_id, user_id, comment_text FROM product_comment WHERE comment_text LIKE 'abc%'


+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
| id | select_type | table           | partitions | type  | possible_keys | key          | key_len | ref  | rows | filtered | Extra                 |
+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
|  1 | SIMPLE      | product_comment | NULL       | range | comment_text  | comment_text | 767     | NULL |  213 |   100.00 | Using index condition |
+----+-------------+-----------------+------------+-------+---------------+--------------+---------+------+------+----------+-----------------------+
```

* 在 WHERE 子句中，如果在 OR 前的条件列进行了索引，而在 OR 后的条件列没有进行索引，那么索引会失效。比如下面的 SQL 语句，comment_id 是主键，而 comment_text 没有进行索引，因为 OR 的含义就是两个只要满足一个即可，因此只有一个条件列进行了索引是没有意义的，只要有条件列没有进行索引，就会进行全表扫描，因此索引的条件列也会失效
* 当我们使用 LIKE 进行模糊查询的时候，后面不能是 %
* 索引列尽量设置为NOT NULL约束: MySQL官方文档建议我们尽量将数据表的字段设置为 NOT NULL 约束，这样做的好处是可以更好地使用索引，节省空间，甚至加速SQL 的运行。判断索引列是否为NOT NULL，往往需要走全表扫描，因此我们最好在设计数据表的时候就将字段设置为 NOT NULL 约束比如你可以将 INT 类型的字段，默认值设置为 0。将字符类型的默认值设置为空字符串 ('')。
* 我们在使用联合索引的时候要注意最左原则最左原则也就是需要从左到右的使用索引中的字段，一条 SQL 语句可以只使用联合索引的一部分，但是需要从最左侧开始，否则就会失效。

针对date的优化，保证字段index生效
```
#Index not used due to date func

SELECT comment_id, comment_text, comment_time FROM product_comment WHERE DATE(comment_time) >= '2018-10-01 10:00:00' AND DATE(comment_time) <= '2018-10-02 10:00:00'
#Use index
SELECT comment_id, comment_text, comment_time FROM product_comment WHERE comment_time BETWEEN DATE('2018-10-01 10:00:00') AND DATE('2018-10-02 10:00:00')
```

回表指的就是数据库根据索引找到了数据行之后，还需要通过主键再次到数据表中读取数据的情况。我们可以通过宽索引将 SELECT 中需要用到的列（主键列可以除外）都设置在宽索引中，这样就避免了回表扫描的情况，从而提升 SQL 查询效率。回表指的就是数据库根据索引找到了数据行之后，还需要通过主键再次到数据表中读取数据的情况。

三星索引具体指的是：
* 在WHERE条件语句中，找到所有等值谓词中的条件列，将它们作为索引片中的开始列；
* 将 GROUP BY 和 ORDER BY 中的列加入到索引中；
* 将 SELECT 字段中剩余的列加入到索引片中。

首先，如果我们要通过索引查找符合条件的记录，就需要将 WHERE 子句中的等值谓词列加入到索引片中，这样索引的过滤能力越强，最终扫描的数据行就越少。另外，如果我们要对数据记录分组或者排序，都需要重新扫描数据记录。为了避免进行 file sort 排序，可以把 GROUP BY 和 ORDER BY 中涉及到的列加入到索引中，因为创建了索引就会按照索引的顺序来存储数据，这样再对这些数据按照某个字段进行分组或者排序的时候，就会提升效率。最后，我们取数据的时候，可能会存在回表情况。回表就是通过索引找到了数据行，但是还需要通过主键的方式在数据表中查找完成的记录。这是因为 SELECT 所需的字段并不都保存在索引中，因此我们可以将 SELECT 中的字段都保存在索引中避免回表的情况，从而提升查询效率。

这样的三星索引也会有如下的问题
* 采用三星索引会让索引片变宽，这样每个页能够存储的索引数据就会变少，从而增加了页加载的数量。
* 从另一个角度来看，如果数据量很大，比如有 1000 万行数据，过多索引所需要的磁盘空间可能会成为一个问题，对缓冲池所需空间的压力也会增加。增加了索引维护的成本。
* 如果我们为所有的查询语句都设计理想的三星索引，就会让数据表中的索引个数过多，这样索引维护的成本也会增加。举个例子，当我们添加一条记录的时候，就需要在每一个索引上都添加相应的行（存储对应的主键值），假设添加一行记录的时间成本是 10ms（磁盘随机读取一个页的时间），那么如果我们创建了10个索引，添加一条记录的时间就可能变成 0.1s，如果是添加 10 条记录呢？就会花费近 1s 的时间。从索引维护的成本来看消耗还是很高的。当然对于数据库来说，数据的更新不一定马上回写到磁盘上，但即使不及时将脏页进行回写，也会造成缓冲池中的空间占用过多，脏页过多的情况。


### 索引设置的建议
* 一张表的索引个数不宜过多，否则一条记录的增加和修改，会因为过多的索引造成额外的负担。针对这个情况，当你需要新建索引的时候，首先考虑在原有的索引片上增加索引，也就是采用复合索引的方式，而不是新建一个新的索引。另外我们可以定期检查索引的使用情况，对于很少使用到的索引可以及时删除，从而减少索引数量。
* 在索引片中，我们也需要控制索引列的数量，通常情况下我们将WHERE里的条件列添加到索引中，而 SELECT 中的非条件列则不需要添加。除非 SELECT 中的非条件列数少，并且该字段会经常使用到。
* 另外单列索引和复合索引的长度也需要控制，在 MySQL InnoDB 中，系统默认单个索引长度最大为767bytes，如果单列索引长度超过了这个限制，就会取前缀索引，也就是取前 255 字符。这实际上也是告诉我们，字符列会占用较大的空间，在数据表设计的时候，尽量采用数值类型替代字符类型，尽量避免用字符类型做主键，同时针对字符字段最好只建前缀索引。
