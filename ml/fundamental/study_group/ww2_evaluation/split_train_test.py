import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
#引入sklearn的iris测试数据集
iris = datasets.load_iris()

x = iris.data
y = iris.target

print(x.shape)
#(150, 4)
print(y.shape)
#(150)


#可以看到这里x这个特征数据集是个有150 条数据，4个特征的二维数组， y为一个一行150个数据的一维数组。可以看到这个数据集是有序的，lable 0的在最开始，然后1， 2， 那么需要对整个数据集进行shuffle，再分解。
#有2种方法能够进行分解这个数据集：

#将x, y合并为一个矩阵，然后对矩阵进行shuffle, 这样x,y 之间的对应关系仍然保持着
#使用np.concatenate方法进行矩阵合并时，必须保证矩阵保持同样的形状，比如纵向拼接，那么必须保证2个数据集有相同的行数，那么就只是将列合并起来， 所以先reshape y, 使其成为一个150行，1列的数组，y.reshape(-1, 1)， 中-1表示自行计算行数，列数为1.

print(y)
#[0 0 ...1 1 ..22]
print(y.reshape(-1, 1))
[[0]
 [0]
 ....
 [1]
 [1]
 ...
 ]
#使用np.concatenate 方法合并数组，axis=1表示纵向拼接。
temp_conca = np.concatenate((x, y.reshape(-1, 1)), axis=1)
print(temp_conca)
#调用np.random.shuffle会对数组进行重新洗牌，打乱之前的顺序。
np.random.shuffle(temp_conca)
print(temp_conca)


#对y的索引进行乱序，根据索引确定与X的对应关系，最后再通过乱序的索引进行赋值

shuffle_index = np.random.permutation(len(x))
#print(shuffle_index)
test_index = shuffle_index[:test_size]
train_index = shuffle_index[test_size:]

x_train=x[train_index]
y_train=y[train_index]
print(x)
print(train_index) 
print(x_train)
print("{} {}".format(x_train.shape, y_train.shape))

x_train=x[train_index] 
#这里可以看到一个二维数组，当只给第一项赋值的时候，会选取相对应的行然后取所有的列