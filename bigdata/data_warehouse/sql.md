## Oracle WITH AS
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

## Oracle CASE WHEN
```
　　CASE search_expression

　　WHEN expression1 THEN result1

　　WHEN expression2 THEN result2

　　...

　　WHEN expressionN THEN resultN

　　ELSE default_result
```

## Oracle NULL
* 等价于没有任何值、是未知数
* NULL与0、空字符串、空格都不同
* NULL的处理使用NVL函数或者nvl2
* 比较时使用关键字用"is null"和"is not null"

NVL(eExpression1, eExpression2)


如果 eExpression1 的计算结果为 null 值，则 NVL( ) 返回 eExpression2。如果 eExpression1 的计算结果不是 null 值，则返回 eExpression1
eExpression1 和 eExpression2 可以是任意一种数据类型。如果 eExpression1 与 eExpression2 的结果皆为 null 值，则 NVL( ) 返回 NULL

## Oracle decode
Decode 其实和case类似都是经过条件判断后进行赋值，CASE语句在处理类似问题就显得非常灵活。当只是需要匹配少量数值时，用Decode更为简洁。
```
decode (expression, sch_1, res_1)
decode (expression, sch_1, res_1, sch_2, res_2)
decode (expression, sch_1, res_1, sch_2, res_2, ...., sch_n, res_n, default)
```
比较表达式和搜索字，如果匹配，返回结果；如果不匹配，返回default值；如果未定义default值，则返回空值。

## SQL 查询重复的行
```
select [every column], count(*)
from mytable
group by [every column]
having count(*) > 1;
```