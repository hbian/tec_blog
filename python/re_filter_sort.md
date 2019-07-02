## RE 
[] Used to indicate a set of characters. In a set:
Characters that are not within a range can be matched by complementing the set. If the first character of the set is '^', all the characters that are not in the set will be matched. For example, [^5] will match any character except '5'

例如[^\w]会匹配所有非字符串, 例如用re.sub替换字符串中所有标点符号和换行

```
>>> import re
>>> a="a,b-c:d"
>>> re.sub("[^\w]", " ", a)
'a b c d'
```

## Filter
filter函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
filter(function, iterable)
```
>>> a=[1,3,4,6,8]
>>> filter(lambda x: x>5 , a)
[6, 8]
```


## sort vs sorted

sort是对当前list排序，返回none，会修改当前list
sorted 对当前list排序后返回新的排过序的list

sort, sorted中key的用法，可以指定根据哪一个值排序，默认的话会是第一个
```
>>> a
[['b', 1], ['a', 2]]
>>> a.sort(key=lambda x: x[0])
>>> a
[['a', 2], ['b', 1]]
>

#不用key进行指定默认排序会按第一个
>>> a= [["b",1], ["a",2]]
>>> a
[['a', 2], ['b', 1]]
```
