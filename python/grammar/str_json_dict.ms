## From json string to dict
使用json.loads方法
```
>>> a ='{"a":1}'
>>> type(a)
<type 'str'>
>>> b = json.loads(a)
>>> type(b)
<type 'dict'>
```

## From dict to json string
使用json.dumps方法
```
>>> a ={"a":1}
>>> type(a)
<type 'dict'>
>>> b = json.dumps(a)
>>> type(b)
<type 'str'>

```
