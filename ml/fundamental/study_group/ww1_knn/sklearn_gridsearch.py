#!/usr/bin/env python
# coding: utf-8

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()

x = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(x, y)
print(X_train.shape)
knn_bef = KNeighborsClassifier(n_neighbors=2)
knn_bef.fit(X_train, y_train)
print("before grid search:{}".format(knn_bef.score(X_test, y_test)))

param_search = [
    {"weights":["uniform"],
     "n_neighbors":[i for i in range(1,11)]
    },
    {"weights":["distance"],
     "n_neighbors":[i for i in range(1,11)],
     "p":[i for i in range(1,6)]
    }
]
# 调用网格搜索方法
# 定义网格搜索的对象grid_search，其构造函数的第一个参数表示对哪一个分类器进行算法搜索，第二个参数表示网格搜索相应的参数
grid_search = GridSearchCV(knn_clf, param_search)
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
print(grid_search.best_score_)
print(grid_search.best_estimator_)

knn_clf = grid_search.best_estimator_
print("After grid search:{}".format(knn_clf.score(X_test, y_test)))
