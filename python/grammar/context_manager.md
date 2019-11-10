## Context manager
Python provides special syntax for this in the with statement, which automatically manages resources encapsulated within context manager types, or more generally performs startup and cleanup actions around a block of code. You should always use a with statement for resource management. 
简单来说，是为了简化 try, finally对问题的处理

```
f = open(filename)
try:
    # ...
finally:
    f.close()
```

Context managers work by calling __enter__() when the with context is entered, binding the return value to the target of as, and calling __exit__() when the context is exited. There’s some subtlety about handling exceptions during exit, but you can ignore it for simple use.

More subtly, __init__() is called when an object is created, but __enter__() is called when a with context is entered.
一个简单的implementation的例子
```
class ContextManager(): 
    def __init__(self): 
        print('init method called') 
          
    def __enter__(self): 
        print('enter method called') 
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        print('exit method called') 
  
  
with ContextManager() as manager: 
    print('with statement block') 
```
一般情况下不需要自己写这些__init__和__enter__函数

@contextmanager这个decorator接受一个generator，用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了, 一个mysql的例子 
```
from contextlib import contextmanager

@contextmanager
def mysql_manager(db_host, db_user, db_password, database):
    db_connection = MySQLdb.connect(db_host, db_user, db_password, db=database)
    yield db_connection
    logging.info("The mysql connection will be closed now.")
    db_connection.close()
```