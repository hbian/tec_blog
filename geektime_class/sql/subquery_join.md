##　子查询 Subquery

### 非关联子查询
子查询从数据表中查询了数据结果，如果这个数据结果只执行一次，然后这个数据结果作为主查询的条件进行执行，那么这样的子查询叫做非关联子查询。
我们以 NBA 球员数据表为例，假设我们想要知道哪个球员的身高最高，最高身高是多少，就可以采用子查询的方式：
```
SQL: SELECT player_name, height FROM player WHERE height = (SELECT max(height) FROM player)
```
通过SELECT max(height) FROM player可以得到最高身高这个数值，结果为 2.16，然后我们再通过player这个表，看谁具有这个身高，再进行输出，这样的子查询就是非关联子查询。

### 关联子查询
如果子查询的执行依赖于外部查询，通常情况下都是因为子查询中的表用到了外部的表，并进行了条件关联，因此每执行一次外部查询，子查询都要重新计算一次，这样的子查询就称之为关联子查询

比如我们想要查找每个球队中大于平均身高的球员有哪些，并显示他们的球员姓名、身高以及所在球队 ID. 首先我们需要统计球队的平均身高，
```
SELECT avg(height) FROM player AS b WHERE a.team_id = b.team_id
```
然后筛选身高大于这个数值的球员姓名、身高和球队 ID，即：
```

SELECT player_name, height, team_id FROM player AS a WHERE height > (SELECT avg(height) FROM player AS b WHERE a.team_id = b.team_id)
```

### EXISTS子查询
关联子查询通常也会和 EXISTS 一起来使用，EXISTS 子查询用来判断条件是否满足，满足的话为 True，不满足为 False。NOT EXISTS 就是不存在的意思, 同样可以用于子查询。
比如我们想要看出场过的球员都有哪些，并且显示他们的姓名、球员 ID 和球队 ID。在这个统计中，是否出场是通过 player_score 这张表中的球员出场表现来统计的，如果某个球员在 player_score 中有出场记录则代表他出场过，这里就使用到了 EXISTS 子查询，即
```
EXISTS (SELECT player_id FROM player_score WHERE player.player_id = player_score.player_id)
```
然后将它作为筛选的条件，实际上也是关联子查询，
```

SQL：SELECT player_id, team_id, player_name FROM player WHERE EXISTS (SELECT player_id FROM player_score WHERE player.player_id = player_score.player_id)
```
使用NOT EXISTS查询未出场的球员
```
SQL: SELECT player_id, team_id, player_name FROM player WHERE NOT EXISTS (SELECT player_id FROM player_score WHERE player.player_id = player_score.player_id)
```

### 集合比较子查询
* IN: 判断是否在集合中
* ANY: 需要与比较操作符一起使用，于子查询返回的任何值做比较
* ALL: 需要与比较操作符一起使用，于子查询返回的所有值做比较
ANY 和 ALL 都需要使用比较符，比较符包括了（>）（=）（<）（>=）（<=）和（<>）等。

还是出场球员，我们可以将EXISTS替换为IN
```
SELECT player_id, team_id, player_name FROM player WHERE player_id in (SELECT player_id FROM player_score WHERE player.player_id = player_score.player_id)
```

在IN和EXISTS可以获得相同结果的时候，
```
SELECT * FROM A WHERE cc IN (SELECT cc FROM B)
```
VS
```
SELECT * FROM A WHERE EXIST (SELECT cc FROM B WHERE B.cc=A.cc)
```

The Exists keyword evaluates true or false, but the IN keyword will compare all values in the corresponding subuery column.  If you are using the IN operator, the SQL engine will scan all records fetched from the inner query. On the other hand, if we are using EXISTS, the SQL engine will stop the scanning process as soon as it found a match.

The EXISTS subquery is used when we want to display all rows where we have a matching column in both tables.  In most cases, this type of subquery can be re-written with a standard join to improve performance.

**The EXISTS clause is much faster than IN when the subquery results is very large. Conversely, the IN clause is faster than EXISTS when the subquery results is very small.**

## Join
### 交叉连接 笛卡尔积 
笛卡尔乘积是一个数学运算。假设我有两个集合 X 和 Y，那么 X 和 Y 的笛卡尔积就是 X 和 Y 的所有可能组合，也就是第一个对象来自于 X，第二个对象来自于 Y 的所有可能
以下是两张表的笛卡尔积的结果，这是笛卡尔积的调用方式:
```
#SQL92
SQL: SELECT * FROM player, team
#SQL99
SQL: SELECT * FROM player CROSS JOIN team
```
笛卡尔积也称为交叉连接，英文是CROSS JOIN，它的作用就是可以把任意表进行连接，即使这两张表不相关
多张表交叉
```
SQL: SELECT * FROM t1 CROSS JOIN t2 CROSS JOIN t3
```
### 自然连接 等值连接 非等值连接 
SQL99自然连接是SQL92 中的等值连接，两张表的自然连接就是用两张表中都存在的列进行连接。我们也可以对多张表进行等值连接。
针对 player 表和 team 表都存在 team_id 这一列，我们可以用等值连接进行查询。

ON连接用来指定我们想要的连接条件，这里我们指定了连接条件是ON player.team_id = team.team_id，相当于是用 ON 进行了 team_id 字段的等值连接。

USING连接指定了具体的相同的字段名称，你需要在 USING 的括号 () 中填入要指定的同名字段。同时使用 JOIN USING 可以简化 JOIN ON 的等值连接，
```
#SQL92 等值连接
SELECT player_id, player.team_id, player_name, height, team_name FROM player, team WHERE player.team_id = team.team_id
#SQL99 NATURAL JOIN
SELECT player_id, team_id, player_name, height, team_name FROM player NATURAL JOIN team 
#SQL99 ON连接
SELECT player_id, player.team_id, player_name, height, team_name FROM player JOIN team ON player.team_id = team.team_id
#SQL99 USING 连接
SELECT player_id, team_id, player_name, height, team_name FROM player JOIN team USING(team_id)
```

当我们进行多表查询的时候，如果连接多个表的条件是等号时，就是等值连接，其他的运算符连接就是非等值查询。当然你也可以ON连接进行非等值连接，比如我们想要查询球员的身高等级，需要用 player 和 height_grades 两张表：
```
SQL99：SELECT p.player_name, p.height, h.height_level
FROM player as p JOIN height_grades as h
ON height BETWEEN h.height_lowest AND h.height_highest
```


### 外连接 自连接
除了查询满足条件的记录以外，外连接还可以查询某一方不满足条件的记录。两张表的外连接，会有一张是主表，另一张是从表。如果是多张表的外连接，那么第一张表是主表，即显示全部的行，而第剩下的表则显示对应连接的信息。在SQL92中采用（+）代表从表所在的位置，而且在SQL92中，只有左外连接和右外连接，没有全外连接。

左外连接，就是指左边的表是主表，需要显示左边表的全部行，而右侧的表是从表，（+）表示哪个是从表。

SQL99 的外连接包括了三种形式：左外连接：LEFT JOIN 或 LEFT OUTER JOIN右外连接：RIGHT JOIN 或 RIGHT OUTER JOIN全外连接：FULL JOIN 或 FULL OUTER JOIN我们在 SQL92 中讲解了左外连接、右外连接，在 SQL99 中还有全外连接。全外连接实际上就是左外连接和右外连接的结合。在这三种外连接中，我们一般省略 OUTER 不写。

```
SQL：SELECT * FROM player LEFT JOIN team on player.team_id = team.team_id

SQL：SELECT * FROM player RIGHT JOIN team on player.team_id = team.team_id

SQL：SELECT * FROM player FULL JOIN team ON player.team_id = team.team_id
```


自连接可以对多个表进行操作，也可以对同一个表进行操作。也就是说查询条件使用了当前表的字段。
我们想要查看比布雷克·格里芬高的球员都有谁，以及他们的对应身高：
```
#SQL92：
SELECT b.player_name, b.height FROM player as a , player as b WHERE a.player_name = '布雷克-格里芬' and a.height < b.height
#SQL99
SELECT b.player_name, b.height FROM player as a JOIN player as b ON a.player_name = '布雷克-格里芬' and a.height < b.height
```
如果不用自连接的话，需要采用两次 SQL 查询。首先需要查询布雷克·格里芬的身高。
```
SQL：SELECT height FROM player WHERE player_name = '布雷克-格里芬'
```
运行结果为 2.08。然后再查询比 2.08 高的球员都有谁，以及他们的对应身高：
```
SQL：SELECT player_name, height FROM player WHERE height > 2.08
```

在进行连接查询的时候，查询的顺序仍然是
查询顺序是：FROM > WHERE > GROUP BY > HAVING > SELECT 的字段 > DISTINCT > ORDER BY > LIMIT
先进行 CROSS JOIN 求笛卡尔积，然后进行条件筛选。
当有ON和WHERE时，执行的顺序会先进行ON连接，然后进行WHERE筛选。ON连接是一般连接表的方式，当我们得到数据之后，再会对数据行进行条件筛选

* 内连接：将多个表之间满足连接条件的数据行查询出来。它包括了等值连接、非等值连接和自连接。
* 外连接：会返回一个表中的所有记录，以及另一个表中匹配的行。它包括了左外连接、右外连接和全连接。
* 交叉连接：也称为笛卡尔积，返回左表中每一行与右表中每一行的组合。在 SQL99 中使用的 CROSS JOIN。

```
SELECT ...
FROM table1
    JOIN table2 ON table1和table2的连接条件
        JOIN table3 ON table2和table3的连接条件
```

Oracle 没有表别名 AS为了让 SQL 查询语句更简洁，我们经常会使用表别名 AS，不过在 Oracle 中是不存在 AS 的，使用表别名的时候，直接在表名后面写上表别名即可，比如 player p，而不是 player AS p。

使用自连接而不是子查询我们在查看比布雷克·格里芬高的球员都有谁的时候，可以使用子查询，也可以使用自连接。一般情况建议你使用自连接，因为在许多 DBMS 的处理过程中，对于自连接的处理速度要比子查询快得多。你可以这样理解：子查询实际上是通过未知表进行查询后的条件判断，而自连接是通过已知的自身数据表进行条件判断，因此在大部分 DBMS 中都对自连接处理进行了优化。

Oracle支持全外连接 FULL JOIN，而MySQL不支持，不过想要写全外连接的话，可以用 左外连接 UNION 右外连接，比如：
```
SELECT * FROM player LEFT JOIN team ON player.team_id = team.team_id
UNION
SELECT * FROM player RIGHT JOIN team ON player.team_id = team.team_id
```