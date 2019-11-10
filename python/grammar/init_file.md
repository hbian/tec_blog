## __init__ 文件用法

## 总结
Python 3.2以及之前版本以前主要是为了通过文件夹生成python的package， python3.3之后可以不再需要
[How_to_create_a_Python_Package_with___init__py](https://timothybramlett.com/How_to_create_a_Python_Package_with___init__py.html)
that is basically what __init__.py does! It allows you to treat a directory as if it was a python module. Then you can further define imports inside your __init__.py file to make imports more succinct, or you can just leave the file blank.


###  用法一: 简化代码调用
避免调用时写packagename.modulename这样的复杂调用， stackoverflow的例子
For convenience: the other users will not need to know your functions' exact location in your package hierarchy.
```
your_package/
  __init__.py
  file1.py/
  file2.py/
    ...
  fileN.py

# in __init__.py
from file1 import *
from file2 import *
...
from fileN import *

# in file1.py
def add():
    pass
```
then others can call add() by
```
from your_package import add

#without knowing file1, like
from your_package.file1 import add
```