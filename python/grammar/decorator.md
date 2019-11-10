## @property

本文是对廖雪峰大神的文章进行的自己总结[@property用法](https://www.liaoxuefeng.com/wiki/1016959663602400/1017502538658208#0)

@property 可以方便的设置一个只读的属性

```
class Student(object):

    @property
    def time(self):
        self._time = 100
        return self._time


s = Student()
print "s.time ={}" .format(s.time)
s.time = 2000
print "s.time ={}" .format(s.time)

```

可以看到读属性没有问题，一旦进行写时会raise AttributeError: can't set attribute
注意这里在方法里面写的时候是self._time ，但在外面使用时没有_, s.time直接获取属性

```
s.time =100
Traceback (most recent call last):
  File "test.py", line 26, in <module>
    s.time = 2000
AttributeError: can't set attribute
```

设置写属性, @time.setter 属性名加setter
```
class Student(object):

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        return self._time

s = Student()
s.time = 2000
print "s.time ={}" .format(s.time)
```
