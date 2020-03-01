#!/usr/bin/env python
# coding: utf-8

import numpy as np
from math import sqrt
from collections import Counter

class kNNClassifier:

    def __init__(self, k):
        assert k >=1 ," k must > 1"
        self.k = k
        self._x_train = None
        self._y_train = None
        
    def fit(self, X_train, Y_train):
        assert X_train.shape[0] == Y_train.shape[0], "the size of X_train must be equal to the size of y_train"
        assert self.k <= Y_train.shape[0], "the size of train data must be at least k"
        self._x_train = X_train
        self._y_train = Y_train
        
    def predict(self, x_predict):
        assert self._x_train is not None and self._y_train is not None, "must fit before predict!"
        assert x_predict.shape[1] == self._x_train.shape[1], "train and test data must have the same num of features"
        y_predict = [self._predict(x) for x in x_predict]
        return np.array(y_predict)
    
    def _predict(self, x):
         distances = [sqrt(np.sum((x_train - x) ** 2)) for x_train in self._x_train]
         nearest = np.argsort(distances)
         k_lables = [self._y_train[i] for i in nearest[:self.k]]
         result = Counter(k_lables).most_common(1)[0][0]
         return result

    def __repr__(self):
        return "kNN(k={})".format(self.k)

def train_test_split(X, y, test_ratio=0.2, seed=None):
    assert X.shape[0] == y.shape[0], "the size of X must be equal to the size of y"
    assert 0.0 <= test_ratio <= 1.0, "test_train must be valid"
    if seed:    # 是否使用随机种子，使随机结果相同，方便debug
        np.random.seed(seed)
    # permutation(n) 可直接生成一个随机排列的数组，含有n个元素
    shuffle_index = np.random.permutation(len(X))

    test_size = int(len(X) * test_ratio)
    test_index = shuffle_index[:test_size]
    train_index = shuffle_index[test_size:]
    X_train = X[train_index]
    X_test = X[test_index]
    y_train = y[train_index]
    y_test = y[test_index]

    return X_train, X_test, y_train, y_test   

#Test our sklearn like kNNClassifier
    
raw_data_X = [[3.393533211, 2.331273381],
              [3.110073483, 1.781539638],
              [1.343853454, 3.368312451],
              [3.582294121, 4.679917921],
              [2.280362211, 2.866990212],
              [7.423436752, 4.685324231],
              [5.745231231, 3.532131321],
              [9.172112222, 2.511113104],
              [7.927841231, 3.421455345],
              [7.939831414, 0.791631213]
             ]
raw_data_Y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
knn = kNNClassifier(k=6)
knn.fit(np.array(raw_data_X), np.array(raw_data_Y))
x_test = np.array([8.90933607318, 3.365731514])
y_predict = knn.predict(x_test.reshape(1, -1))
#print(y_predict)

#Use iris data test splitter
iris = datasets.load_iris()

iris_x = iris.data
iris_y = iris.target

X_train, X_test, y_train, y_test = train_test_split(iris_x, iris_y)
# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)

knn.fit(X_train, y_train)
y_predict=knn.predict(X_test)
print(y_predict)
print(y_test)