import numpy as np
import matplotlib.pyplot as plt

X = np.empty((100, 2))
X[:,0] = np.random.uniform(0., 100., size=100)
X[:,1] = 0.75 * X[:,0] + 3. + np.random.normal(0, 10., size=100)


from sklearn.decomposition import PCA

# 初始化实例对象，传入主成分个数
pca = PCA(n_components=1)
pca.fit(X)
print(pca.components_)
#使用transform方法将矩阵X进行降维。得到一个特征的数据集
X_reduction = pca.transform(X)
X_reduction.shape

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

digits = datasets.load_digits()
X = digits.data
y = digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=666)
#对原始数据集进行训练，看看识别的结果
knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_train)
knn_clf.score(X_test, y_test)


from sklearn.decomposition import PCA

#将原来的64维降为2维
pca = PCA(n_components=2)
pca.fit(X_train)
X_train_reduction = pca.transform(X_train) # 训练数据集降维结果
X_test_reduction = pca.transform(X_test) # 测试数据集降维结果




pca = PCA(n_components=X_train.shape[1])
pca.fit(X_train)
pca.explained_variance_ratio_
plt.plot([i for i in range(X_train.shape[1])], 
         [np.sum(pca.explained_variance_ratio_[:i+1]) for i in range(X_train.shape[1])])
plt.show()

#在sklearn中，实例化时传入一个数字，就表示保持的方差比例
pca = PCA(0.95)
pca.fit(X_train)
#可以看到28维数据就可以解释95%以上的方差。
pca.n_components_

#用28维，95%的降维在进行训练
X_train_reduction = pca.transform(X_train)
X_test_reduction = pca.transform(X_test)
knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train_reduction, y_train)
knn_clf.score(X_test_reduction, y_test)