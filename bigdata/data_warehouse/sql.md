## Oracle
### Oracle WITH AS
 可以把WITH AS 的用法看成赋值的用法，以减少SQL语句的冗余。
 当我们在SQL语句中频繁的利用某一个Select查询语句作为数据源时，我们可以用WITH AS 的用法进行简写, 增加了SQL的易读性，如果构造了多个子查询，结构会更清晰；更重要的是："一次分析，多次使用"。
```
#Grammar
with 
    tempName1 as (select ....),
    tempName2 as (select ....)
select ...from  tempName 
```

* 子查询可重用相同或者前一个with查询块，通过select调用, with子句也只能被select调用
* 同级select前有多个查询定义，第一个用with，后面的不用with，并且用逗号分割
* 最后一个with查询块与下面的select调用之间不能用逗号分割，只通过右括号分离，with子句的查询必须括号括起
* 如果定义了with子句，而在查询中不使用，则会报ora-32035错误，只要后面有引用的即可，不一定在select调用，在后with查询块引用也是可以的
* 前面的with子句定义的查询在后面的with子句中可以使用，但是一个with子句内部不能嵌套with子句
* with查询的结果列有别名，引用时候必须使用别名或者*

### Oracle CASE WHEN
```
　　CASE search_expression

　　WHEN expression1 THEN result1

　　WHEN expression2 THEN result2

　　...

　　WHEN expressionN THEN resultN

　　ELSE default_result
```

### Oracle NULL
* 等价于没有任何值、是未知数
* NULL与0、空字符串、空格都不同
* NULL的处理使用NVL函数或者nvl2
* 比较时使用关键字用"is null"和"is not null"

NVL(eExpression1, eExpression2)


如果 eExpression1 的计算结果为 null 值，则 NVL( ) 返回 eExpression2。如果 eExpression1 的计算结果不是 null 值，则返回 eExpression1
eExpression1 和 eExpression2 可以是任意一种数据类型。如果 eExpression1 与 eExpression2 的结果皆为 null 值，则 NVL( ) 返回 NULL

### Oracle decode
Decode 其实和case类似都是经过条件判断后进行赋值，CASE语句在处理类似问题就显得非常灵活。当只是需要匹配少量数值时，用Decode更为简洁。
```
decode (expression, sch_1, res_1)
decode (expression, sch_1, res_1, sch_2, res_2)
decode (expression, sch_1, res_1, sch_2, res_2, ...., sch_n, res_n, default)
```
比较表达式和搜索字，如果匹配，返回结果；如果不匹配，返回default值；如果未定义default值，则返回空值。


## HIVE
### SQL 查询重复的行
```
select [every column], count(*)
from mytable
group by [every column]
having count(*) > 1;
```

### ROW_NUMBER OVER
ROW_NUMBER() OVER(PARTITION BY COLUMN ORDER BY COLUMN)

简单的说row_number()从1开始，为每一条分组(PARTITION BY COLUMN)记录返回一个数字， 

row_number() OVER (PARTITION BY COL1 ORDER BY COL2) 表示根据COL1分组，在分组内部根据 COL2排序，而此函数计算的值就表示每组内部排序后的顺序编号（组内连续的唯一的)
这个也就可以看出COL1 到底有多少重复数据，可以进行去重等操作

## Finding Duplicate Rows based on Multiple Columns

```
select pos, count(pos), book_date, count(book_date), resv_book_date, count(resv_book_date) from ticket_in_pos_and_bookdate GROUP BY pos, book_date, resv_book_date HAVING( count(pos) >1 and  count(book_date)>1 and count(resv_book_date) >1)
```


## 关于SQL JOIN和Uninon
https://developer.aliyun.com/article/37377


## in和exists、not in 和 not exists
IN 包含的值不应过多，IN本身这个操作消耗就比较高，如果IN里面是连续的数值，则可以用between代替，IN里面的字段如果是添加了索引，效率还是可以的，目前测试一万以内还是可以，但是超过了结果可能会有点爆炸。

exists以外层表为驱动表，先被访问，适合于外表小而内表大的情况。
in则是先执行子查询，适合外表大而内表小的情况，

一般情况是不推荐使用not in，因为效率非常低，

```
select * from table_a where table_a.id not in (select table_b.id from table_b)

select * from table_a left join table_b on table_a.id = table_b.id where table_b.id is null
```
语句2的效率是要高于语句1的，SQL的结果是获取到在table_a中存在但是table_b中不存在的数据，如果直接用not in是不走索引的，而且在table_b比较大的时候效率会非常低，实际工作中我试了一下直接not in，然后数据达到一万条的时候大概需要150S左右才能查出数据（感谢DBA和运维不杀之恩），我采取的方法是，先查出两个表的交集，这样得到的表会小很多，而且是用的in，效率会高很多，然后再用not in，最终的效果也是一样，但是时间只要2.56S，然后采取语句2的关联表来处理，时间缩短到了1.42S，基本上效率是比较高的，当然理想的是在1S内。

## 尽量少用or，同时尽量用union all 代替union

or两边的字段如果有不走索引的会导致整个的查询不走索引，从而导致效率低下，这时可以使用union all或者union，而两者的区别是union是将两个结果合并之后再进行唯一性的过滤操作，效率会比union all低很多，但是union all需要两个数据集没有重复的数据