## HIVE SQL通用语法优化
https://zhuanlan.zhihu.com/p/174469951?utm_source=wechat_session
### 谓词下推
将过滤表达式尽可能移动至靠近数据源的位置，以使真正执行时能直接跳过无关的数据。
简单来说就是把where语句尽可能挪到最底层的位置，在最底层就把不需要的数据都过滤掉，然后让真正需要的数据参与运算，而不是留到最后才进行过滤。

比如说优化以下代码：
```
select t1.name,t2.age,t2.class,t2.income from t1 join t2 on t1.id=t2.id where t2.age>18
```

```
select t1.name,t2.age,t2.class,t2.income from t1 
join 
(select id,age,class,income from t2 where id>18) t2
on t1.id=t2.id 
```


### 多用子查询

基于谓词下推的思想，我们还可以做进一步的优化，即多用子查询，上面的代码可进一步优化成如下样子：

select t1.name,t2.age,t2.class,t2.income from
(select id,name from t1) t1
join
(select id,age,class,income from t2 where age>18) t2
on t1.id=t2.id
采用子查询后，尽管会增加job数但提前把数据完成了过滤，还提高了代码的可读性，尤其是当需要关联的表和条件成倍增加后，可读性将会非常重要

### 子查询的去重

当子查询的表中所需的字段存在重复值，那么对这些字段提前进行去重再进行关联同样会提高运算效率。还是以上面的代码为例：
```
select t1.name,t2.age,t2.class,t2.income from
(select id,name from t1) t1
join
(select id,age,class,income from t2 where age>18 group by id,age,class,income) t2
on t1.id=t2.id
```

### 过滤null值

当关联所用到的字段包含了太多null时，需要从业务的角度考虑这些为null的数据是否有存在的必要，如果不必要的话尽早过滤掉，避免影响关联的效率。

如果确实需要用到，则可用rand()把数据均匀分布在不同的reduce上，避免数据倾斜，详细可见第二部分，此处仅列出代码：
```
select 
n.*,
o.name
from 
nullidtable n 
full join 
bigtable o 
on nvl(n.id,rand())=o.id
```

### 不排序
SQL中进行排序是要消耗计算资源的，在Hive中这种资源消耗会更加明显。子查询里不要排序这一点就不多说了，子查询中排序是毫无意义的，同时在最后的结果步也尽可能少排序，排序这需求完全可以通过交互查询的UI或把结果数据导出进行替代解决。当然，如果进行查询时没有UI系统，或者不方便把数据导出，或者你就是想即时看到数据的排序情况，就当这条建议不存在就好，但在子查询里排序仍然还是毫无意义的。

### 分步

该原则主要目的是把大数据集拆成小数据集来运行。

#### 减少在select时用case when

有时出结果时需要用case when进行分类输出，如下面例子
```
select 
dt,
count(distinct case when id=1 then user_id else null end) as id_1_cnt,
count(distinct case when id=2 then user_id else null end) as id_2_cnt
from table_1
where dt between '20200511' and '20200915'
group by dt
```
但是实测发现case when的执行效率很低，当数据量太大的时候甚至会跑不出数，因此上面的代码可优化成如下形式：
```
select 
t1.dt,
t1.id_1_cnt,
t2.id_2_cnt
from
(select 
dt,
count(distinct user_id) as id_1_cnt
from table_1
where dt between '20200511' and '20200915' and id=1
group by dt) t1
left join
(select 
dt,
count(distinct user_id) as id_2_cnt
from table_1
where dt between '20200511' and '20200915' and id=2
group by dt) t2
on t1.dt=t2.dt
```
当数据量很大或者select时有太多的case when，采用上面的方式其执行效率会提高10倍以上。

#### 多用临时表

当需要建的表其逻辑非常复杂时，需要考虑用临时表的方式把中间逻辑分布执行，一来方便阅读、修改和维护，二来减少硬盘的开销(相较于建中间表的方式)

#### where+union all

当需要根据某字段分类汇总时发现运行速度很慢甚至跑不出结果，那么有可能是因为某一类型的数据样本量过大造成数据倾斜，此时可考虑通过where过滤+union all合并的方法分步统计和汇总来处理该问题。

优化前：
```
select 
age,
count(distinct id) as id_cnt
from age_table
group by age
```
优化后：
```
select 
age,
count(distinct id) as id_cnt
from age_table
where age<35
group by age
union all
select 
age,
count(distinct id) as id_cnt
from age_table
where age>=35
group by age
```
