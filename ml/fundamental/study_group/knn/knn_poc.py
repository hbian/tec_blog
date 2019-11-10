#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

# Trainning data
# raw_data_x是特征，raw_data_y是标签，0为良性，1为恶性
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
X_train = np.array(raw_data_X)
Y_train = np.array(raw_data_Y)

#首先汇出良性结果的图， 颜色为绿, label对图上画出的点进行标注
#先进行判断y为0时，然后取值x轴0的数值 X_train[Y_train==0,0]
plt.scatter(X_train[Y_train==0,0],X_train[Y_train==0,1], color='g', label = 'Good')
plt.scatter(X_train[Y_train==1,0],X_train[Y_train==1,1], color='r', label = 'Bad')

plt.xlabel('Tumor Size')
plt.ylabel('Time')
plt.axis([0,10,0,5])
#Display the label
plt.legend()
plt.show()



# Calculate distances
from math import sqrt
X_test = [8.90933607318, 3.365731514]
distance=[]
for x in X_train:
    d= sqrt(np.sum((x-X_test)**2))
    distance.append(d)
print(distance)

#Sort the K nearest neighbors
nearest = np.argsort(distance)
print(nearest[:k])

#Find the nearest k neighbors label
k = 6
k_lables = [Y_train[i] for i in nearest[:k]]
print(k_lables)

#Find the most common result
from collections import Counter
votes = Counter(k_lables)
votes.most_common()
print("test result: {}".format(votes.most_common()[0][1]))


#Implementation with sklearn
from sklearn.neighbors import KNeighborsClassifier
kNN_classifier = KNeighborsClassifier(n_neighbors=k)
kNN_classifier.fit(X_train, Y_train)
#reshape()成一个二维数组，第一个参数是1表示只有一个数据，第二个参数-1，numpy自动决定第二维度有多少
y_predict = kNN_classifier.predict(X_test.reshape(1,-1))
print(y_predict)