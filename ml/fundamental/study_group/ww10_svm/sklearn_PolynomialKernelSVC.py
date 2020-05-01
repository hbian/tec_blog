
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

X, y = datasets.make_moons(noise=0.20,random_state=123)

plt.scatter(X[y==0,0], X[y==0,1])
plt.scatter(X[y==1,0], X[y==1,1])
plt.show()



def plot_decision_boundary(model, axis):   
    #生成长宽分别为axis[1]-axis[0]， axis[3]-axis[2]的网状节点
    x0, x1 = np.meshgrid(
        np.linspace(axis[0], axis[1], int((axis[1]-axis[0])*100)).reshape(-1, 1),
        np.linspace(axis[2], axis[3], int((axis[3]-axis[2])*100)).reshape(-1, 1),
    )
    #np.c_是按行连接两个矩阵，就是把两矩阵左右相加，要求行数相等。
    #.ravel()会将数组打平，变为一个一维数组
    X_new = np.c_[x0.ravel(), x1.ravel()]
    y_predict = model.predict(X_new)
    zz = y_predict.reshape(x0.shape)
    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(['#EF9A9A','#FFF59D','#90CAF9'])
    plt.contourf(x0, x1, zz, linewidth=5, cmap=custom_cmap)

    


from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
def PolynomialKernelSVC(degree, C=1.0):
    return Pipeline([
        ("std_scaler", StandardScaler()),
        ("kernelSVC", SVC(kernel='poly',degree=degree,C=C))
    ])

poly_kernel_svc = PolynomialKernelSVC(degree=3)
poly_kernel_svc.fit(X, y)

plot_decision_boundary(poly_kernel_svc, axis=[-1.5, 2.5, -1.0, 1.5])
plt.scatter(X[y==0,0], X[y==0,1])
plt.scatter(X[y==1,0], X[y==1,1])
plt.show()


#我们再尝试着保持阶数degree不变，去调大参数C：
#通过肉眼观察可见，参数C越大，中间的“凸起”越尖锐。我们知道，参数C是正则化项的系数，C越大，越接近于Hard Margin；C越小，容错性越大。
poly_kernel_svc = PolynomialKernelSVC(degree=3,C=200)
poly_kernel_svc.fit(X, y)


#通过一些尝试发现，degree参数为偶数时，决策边界类似于双曲线的形式，而为奇数时，则是以直线为基础。大家可以使用网格搜索找到最佳参数。但是我们要注意，多项式阶数degree参数越大，则越容易出现过拟合。

poly_kernel_svc = PolynomialKernelSVC(degree=4)
poly_kernel_svc.fit(X, y)
plot_decision_boundary(poly_kernel_svc, axis=[-1.5, 2.5, -1.0, 1.5])
plt.show()