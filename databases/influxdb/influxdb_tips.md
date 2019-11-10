## 查看tag key中values的个数
查看tag key中values的个数， 因tag会被进行index，所以key中的值太多会严重影响系统的读写
```
> SHOW TAG Values CARDINALITY from nginx_access with key = "agent";
name: nginx_access
count
-----
17000
> SHOW TAG Values CARDINALITY from nginx_access with key = "url";
name: nginx_access
count
-----
54032
> SHOW TAG Values CARDINALITY from nginx_access with key = "referrer";
name: nginx_access
count
-----
53650
> SHOW TAG Values CARDINALITY from nginx_access with key = "method";
name: nginx_access
count
-----
6
> SHOW TAG Values CARDINALITY from nginx_access with key = "response_code";
name: nginx_access
count
-----
15

```


## 重复数据
A point is uniquely identified by the measurement name, tag set, and timestamp. If you submit a new point with the same measurement, tag set, and timestamp as an existing point, the field set becomes the union of the old field set and the new field set, where any ties go to the new field set.
一条数据是由measurement name, tag set, and timestamp这3个维度决定的，如果同一timestamp提交2条相同measurement， tag的数据，即使filed不同，第二条的filed也会覆盖前一条.