#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# 手写数字数据集，封装好的对象，可以理解为一个字段digits = datasets.load_digits()# 可以使用keys()方法来看一下数据集的详情digits.keys()
# 5620张图片，每张图片有64个像素点即特征（8*8整数像素图像），每个特征的取值范围是1～16（sklearn中的不全），对应的分类结果是10个数字print(digits.DESCR)
digits = datasets.load_digits()

x = digits.data
y = digits.target
#x[666] 是一个64 列的一维数组， reshape以后获得一个8*8的二维数组，方便后面的展示
print(x[666].reshape(8, 8))
#打印
plt.imshow(x[666].reshape(8, 8), cmap = matplotlib.cm.binary)
plt.show()


X_train, X_test, y_train, y_test = train_test_split(x, y)
knn_clf = KNeighborsClassifier(n_neighbors=3)
knn_clf.fit(X_train, y_train)
y_predict = knn_clf.predict(X_test)
#calculate the accuracy
print(sum(y_predict == y_test) / len(y_test))

from math import sqrt

def accuracy_score(y_true, y_predict):
    """计算y_true和y_predict之间的准确率"""
    assert y_true.shape[0] == y_predict.shape[0],"the size of y_true must be equal to the size of y_predict"
    return sum(y_true == y_predict) / len(y_true)

def score(self, X_test, y_test):
    """根据X_test进行预测, 给出预测的真值y_test，计算预测算法的准确度"""
    y_predict = self.predict(X_test)    
    return accuracy_score(y_test, y_predict)
knn_clf.score(X_test, y_test)