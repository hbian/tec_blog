## *args 和 **kwargs

函数定义参数时，经常会看到这*args **kwargs这二种， *args会将接收到参数以tuple的方式传给函数，**kwargs则会以dict的形式传递

```
def arg_demo(*args):
    print args, type(args)

arg_demo(1, "a", {"b":1})

#print result
(1, 'a', {'b': 1}) <type 'tuple'>


def kwarg_demo(**kwargs):
    print kwargs, type(kwargs)

kwarg_demo(a=1, b=2, c="hello")
#print result
{'a': 1, 'c': 'hello', 'b': 2} <type 'dict'>

```

需要注意的是如果这二个同时存在，必须按顺序使用*args 然后 **kwargs