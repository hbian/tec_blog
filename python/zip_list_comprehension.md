## zip 和 dict
zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。

```
a= [{'a1':1}, {'a2':2}]
b=[{'b1':1}, {'b2': 2}]
 
zip(a,b) 
[({'a1': 1}, {'b1': 1}), ({'a2': 2}, {'b2': 2})]
```

如上示例所示不止2个list， 任何2个iterable的对象都可以迭代

给定下面2个list，希望将attributes和values组成一个dict的list
```
#input:
attributes = ['name', 'dob', 'gender']
values = [['jason', '2000-01-01', 'male'], 
['mike', '1999-01-01', 'male'],
['nancy', '2001-02-01', 'female']
]

#output:
[{'dob': '2000-01-01', 'gender': 'male', 'name': 'jason'}, {'dob': '1999-01-01', 'gender': 'male', 'name': 'mike'}, {'dob': '2001-02-01', 'gender': 'female', 'name': 'nancy'}]

#solution:
[dict(zip(attributes, v)) for v in values]
```
注意用dict将tuple转换为dict的时候，无法直接转换，要先变成list
```
>>>dict(("a", 1))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: dictionary update sequence element #0 has length 1; 2 is required
>>>dict([("a", 1)])
{'a': 1}
```