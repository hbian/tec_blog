## abstractmethod implement python interface

```
import abc

class AbstractBuilder:
    """
        The appplication builder interface
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def build(self, *args, **kwargs):
        pass
```

继承这个AbstractBuilder后，如果没有重写abc.abstractmethod 修饰过的方法，调用时会报错。

还有一种比较urgly不用abc.abstractmethod的写法
```
import inspect

    def build(self, *args, **kwargs):
        raise NotImplementedError("The {}.{} has not been implemented".format(self.__class__.__name__,
                     inspect.stack()[0][3]))

```