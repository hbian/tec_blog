## WW6的学习内容
* sklearn中的Pipeline
* 偏差与方差
* 模型正则化之L1正则、L2正则

[浅析多项式回归与sklearn中的Pipeline](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484400&idx=1&sn=3ca55d15e7ccd2d6234a5cf5c7abff73&chksm=eb932a46dce4a3509cfab261d80748b2a6eab43d09142a9838c7a4b0d9fb87772673d5494f0d&scene=21#wechat_redirect)

[ML/DL重要基础概念：偏差和方差](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484409&idx=1&sn=740b2a7b4201d7d2e0186e590e8e4a30&chksm=eb932a4fdce4a3593542dc91dda56ca5c92a673b56013d18fc502963bf8ab3e4626f90ec83fa&scene=21#wechat_redirect)

[模型正则化：L1正则、L2正则](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484437&idx=1&sn=40f4b448ed6b26b5e67690764a3f0cbb&chksm=eb932da3dce4a4b5820f1f8a6616edc08bd6700fc03055ed14a6eb4148d97c9fc299af94f3b1&scene=21#wechat_redirect)


## 多项式回归
多项式回归法，是为了对非线性数据进行处理。其实多项式回归在算法并没有什么新的地方，完全是使用线性回归的思路，关键在于为数据添加新的特征，而这些新的特征是原有的特征的多项式组合，采用这样的方式就能解决非线性问题。

这样的思路跟PCA这种降维思想刚好相反，而多项式回归则是升维，添加了新的特征之后，使得更好地拟合高维数据。
研究一个因变量与一个或多个自变量间多项式的回归分析方法，称为多项式回归（Polynomial Regression）。多项式回归是线性回归模型的一种，其回归函数关于回归系数是线性的。其中自变量x和因变量y之间的关系被建模为n次多项式。如果自变量只有一个时，称为一元多项式回归；如果自变量有多个时，称为多元多项式回归。

多项式回归的思路是：添加一个特征，即对于X中的每个数据进行平方。

### sklearn中的多项式回归
创建一个一元二次方程为原始数据，并增加一些噪音, 
```
import numpy as np
import matplotlib.pyplot as plt

x = np.random.uniform(-3, 3, size=100)
X = x.reshape(-1, 1)
y = 0.5 + x**2 + x + 2 + np.random.normal(0, 1, size=100)
plt.scatter(x, y)
plt.show()
```


多项式回归可以看作是对数据进行预处理，给数据添加新的特征，所以调用的库在preprocessing中：
```
from sklearn.preprocessing import PolynomialFeatures

# 这个degree表示我们使用多少次幂的多项式
poly = PolynomialFeatures(degree=2)    
poly.fit(X)
X2 = poly.transform(X)
X2.shape
# 查看数据
X2[:5,:]
```

X2的结果第一列常数项，可以看作是加入了一列x的0次方；第二列一次项系数（原来的样本X特征），第三列二次项系数（X平方前的特征）。

特征准备好之后进行训练：

```
from sklearn.linear_model import LinearRegression

reg = LinearRegression()
reg.fit(X2, y)
y_predict = reg.predict(X2)
plt.scatter(x, y)
plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
plt.show()

print(reg.coef_)
```


当数据维度是2维的，经过多项式预处理生成了6维数据。第一列很显然是0次项系数；第二列和第三列就是原本的X矩阵；第四列是第二列（原X的第一列）平方的结果；第五列是第二、三两列相乘的结果；第六列是第三列（原X的第二列）平方的结果。
过PolynomiaFeatures，将所有的可能组合，升维的方式呈指数型增长。这也会带来一定的问题。

## Pipeline
首先我们回顾多项式回归的过程：
1. 将原始数据通过PolynomialFeatures生成相应的多项式特征
2. 多项式数据可能还要进行特征归一化处理
3. 将数据送给线性回归
Pipeline就是将这些步骤都放在一起。参数传入一个列表，列表中的每个元素是管道中的一个步骤。每个元素是一个元组，元组的第一个元素是名字（字符串），第二个元素是实例化。
```
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

poly_reg = Pipeline([
    ('poly', PolynomialFeatures(degree=3)),
    ('std_scale', StandardScaler()),
    ('lin_reg', LinearRegression())
])  
poly_reg.fit(X, y)

y_predict = poly_reg.predict(X)

plt.scatter(x, y)
plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
plt.show()
```

## 偏差和方差
过拟合和欠拟合都会使训练好的机器学习模型在真实的数据中出现错误。我们可以将错误分为偏差（Bias）和方差（Variance）两类。下面就来看看偏差和方差的定义、产生原因以及二者之间如何权衡。

* 低偏差，低方差：这是训练的理想模型
* 低偏差，高方差：这是深度学习面临的最大问题，过拟合了。也就是模型太贴合训练数据了，导致其泛化（或通用）能力差，若遇到测试集，则准确度下降的厉害；
* 高偏差，低方差：这往往是训练的初始阶段；
* 高偏差，高方差：这是训练最糟糕的情况，准确度差，数据的离散程度也差。

模型误差 = 偏差 + 方差 + 不可避免的误差（噪音）。一般来说，随着模型复杂度的增加，方差会逐渐增大，偏差会逐渐减小。

偏差和方差通常是矛盾的。降低偏差，会提高方差；降低方差，会提高偏差。
这就需要在偏差和方差之间保持一个平衡。

我们要知道偏差和方差是无法完全避免的，只能尽量减少其影响。

在避免偏差时，需尽量选择正确的模型，一个非线性问题而我们一直用线性模型去解决，那无论如何，高偏差是无法避免的。
有了正确的模型，我们还要慎重选择数据集的大小，通常数据集越大越好，但大到数据集已经对整体所有数据有了一定的代表性后，再多的数据已经不能提升模型了，反而会带来计算量的增加。而训练数据太小一定是不好的，这会带来过拟合，模型复杂度太高，方差很大，不同数据集训练出来的模型变化非常大。
最后，要选择合适的模型复杂度，复杂度高的模型通常对训练数据有很好的拟合能力。
其实在机器学习领域，主要的挑战来自方差。处理高方差的手段有：
* 降低模型复杂度
* 减少数据维度；降噪
* 增加样本数
* 使用验证集

偏差衡量了模型的预测值与实际值之间的偏离关系，主要的原因可能是对问题本身的假设是不正确的，或者欠拟合。方差描述的是模型预测值的变化波动情况（或称之为离散情况），模型没有完全学习到问题的本质，通常原因可能是使用的模型太复杂，过拟合。

## 模型正则化：L1正则、L2正则
另外一个降低方差的重要方法：模型正则化

模型正则化（Regularization），对学习算法的修改，限制参数的大小，减少泛化误差而不是训练误差。我们在构造机器学习模型时，最终目的是让模型在面对新数据的时候，可以有很好的表现。当你用比较复杂的模型比如神经网络，去拟合数据时，很容易出现过拟合现象(训练集表现很好，测试集表现较差)，这会导致模型的泛化能力下降，这时候，我们就需要使用正则化，降低模型的复杂度。

正则化的策略包括：约束和惩罚被设计为编码特定类型的先验知识 偏好简单模型 其他形式的正则化，如：集成的方法，即结合多个假说解释训练数据

在实践中，过于复杂的模型不一定包含数据的真实的生成过程，甚至也不包括近似过程，这意味着控制模型的复杂程度不是一个很好的方法，或者说不能很好的找到合适的模型的方法。实践中发现的最好的拟合模型通常是一个适当正则化的大型模型。

### L1正则化
所谓的L1正则化，就是在目标函数中加了L1范数这一项。使用L1正则化的模型叫做LASSO回归。
以Pipeline的方式去封装一个LASSO回归, 在封装好了一个LASSO回归函数后，传入dregree参数和alpha参数，就可以验证LASSO回归的效果了
```
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

x = np.random.uniform(-3, 3, size=100)
X = x.reshape(-1, 1)
y = 0.5 + x**2 + x + 2 + np.random.normal(0, 1, size=100)
plt.scatter(x, y)
X_train, X_test, y_train, y_test = train_test_split(X,y)


def LassoRegression(degree,alpha):
    return Pipeline([
        ('poly',PolynomialFeatures(degree=degree)),
        ('std_scaler',StandardScaler()),
        ('lasso_reg',Lasso(alpha=alpha))
    ])

lasso_reg1 = LassoRegression(30,0.0001)
lasso_reg1.fit(X_train,y_train)
y1_predict=lasso_reg1.predict(X_test)
mean_squared_error(y_test,y1_predict)
```

我们保持degree参数不变，调整alpha参数，让其变大，也就是将L1正则项的比重放大，即让参数变小
alpha参数由之前的0.0001变为0.1， lasso_reg2 = LassoRegression(30,0.1)我们发现曲线更加的平滑了，相应的均方误差也变得更小了，说明结果更优了

如果继续放大alpha系数呢？lasso_reg3 = LassoRegression(30,10)，我们正则化得有些过了，变成一条直线了。
因此，我们需要找到合适的alpha系数，使正则化效果最好。


### L2正则化岭回归
LASSO是使用绝对值，岭回归是使用平方的办法

在sklearn中，包含了一个岭回归的方法：Ridge。下面我们以Pipeline的方式去封装一个岭回归的过程

```
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
# 需要传入一个多项式项数的参数degree以及一个alpha值
def ridgeregression(degree,alpha):
    return Pipeline([
        ("poly", PolynomialFeatures(degree=degree)),
        ("standard", StandardScaler()),
        ("ridge_reg", Ridge(alpha=alpha))   #alpha值就是正则化那一项的系数
    ])

ridge1_reg = ridgeregression(degree=30,alpha=0.0001)
ridge1_reg.fit(X_train,y_train)
y1_predict = ridge1_reg.predict(X_test)
mean_squared_error(y_test,y1_predict)
# 输出：1.00677921937119
plot_model(ridge1_reg)
```
如果我们调整系数，将其变大，意味着对参数的约束又变强了，曲线会更加光滑, 比如讲alpha由0.0001变为1，如果我们继续增大系数到100话，就会正则化得有些过了

LASSO回归和岭回归类似，取值过大反而会导致误差增加，拟合曲线为直线。但是LASSO更趋向于使得一部分的值为0，拟合曲线更趋向于直线，所以可以作为特征选择来使用，去除一些模型认为不需要的特征。LASSO可能会去除掉正确的特征，从而降低准确度，但如果特征特别大，使用LASSO可以使模型变小。

L1正则化就是在损失函数后边所加正则项为L1范数，加上L1范数容易得到稀疏解（0比较多），一般来说L1正则化较常使用。

L2正则化就是损失后边所加正则项为L2范数，加上L2正则相比于L1正则来说，得到的解比较平滑（不是稀疏），但是同样能够保证解中接近于0（但不是等于0，所以相对平滑）的维度比较多，降低模型的复杂度。