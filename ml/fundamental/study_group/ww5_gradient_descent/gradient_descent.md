# WW5 梯度下降

* [WW5 梯度下降](https://mp.weixin.qq.com/s/UN3p9ArkkGkFOOGIUc_BYw)
* [梯度下降](https://mp.weixin.qq.com/s/44p8anqiiQV6XYGqH5u-Ug)
* [手动实现梯度下降](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247483985&idx=1&sn=759dc972a7dc1bd01af53b68619c01c8&scene=21#wechat_redirect)
* [线性回归中的梯度下降](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484001&idx=1&sn=9e7a22277acf5049fd1d945bfe4229db&scene=21#wechat_redirect)
* [速度更快的随机梯度下降法](https://mp.weixin.qq.com/s/OUslRwKGpS29gncsiyAPyg)
* [梯度下降番外：非常有用的调试方式及总结](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484074&idx=2&sn=6ec6cc66c9b865b7f304604172e11b2b&chksm=eb932b1cdce4a20a0b4dbd471d586501b998c4e69237baebf2ebecac4a54c4d379d09583c5c8&scene=21#wechat_redirect)
## 梯度下降

机器学习就是需找一种函数f(x)并进行优化，且这种函数能够做预测、分类、生成等工作。

那么其实可以总结出关于"如何找到函数f(x)"的方法的三步：

1. 定义一个函数集合（define a function set）
2. 判断函数的好坏（goodness of a function）
3. 选择最好的函数（pick the best one）

选取最好的函数，如果结合线性回归的话就是使得损失函数最小化，那么现在机器学习最最核心的方法就是梯度下降。

梯度下降(Gradient Descent, GD)不是一个机器学习算法，而是一种基于搜索的最优化方法。梯度下降(Gradient Descent, GD)优化算法，其作用是用来对原始模型的损失函数进行优化，以便寻找到最优的参数，使得损失函数的值最小。
梯度下降从损失值出发，去更新参数，且要大幅降低计算次数, 抓住了参数与损失值之间的导数，也就是能够计算梯度（gradient），通过导数告诉我们此时此刻某参数应该朝什么方向，以怎样的速度运动，能安全高效降低损失值，朝最小损失值靠拢。


### 梯度
多元函数的导数(derivative)就是梯度(gradient)，分别对每个变量进行微分，然后用逗号分割开，梯度是用括号包括起来，说明梯度其实一个向量.
在单变量的函数中，梯度其实就是函数的微分，代表着函数在某个给定点的切线的斜率. 在多变量函数中，梯度是一个向量，向量有方向，梯度的方向就指出了函数在给定点的上升最快的方向.
梯度指向误差值增加最快的方向，导数为0（梯度为0向量）的点，就是优化问题的解。我们沿着梯度的反方向进行线性搜索，从而减少误差值。每次搜索的步长为某个特定的数值，直到梯度与0向量非常接近为止.

梯度下降就是从群山中山顶找一条最短的路走到山谷最低的地方。


### 布长和初始点
布长\eta对应的是步伐的长度，在学术上，我们称之为"学习率"(learning rate)，是模型训练时的一个很重要的超参数，能直接影响算法的正确性和效率
* 首先，学习率不能太大。并且从直观上来说，如果学习率太大，那么有可能会"迈过"最低点，从而发生"摇摆"的现象（不收敛），无法得到最低点
* 其次，学习率又不能太小。如果太小，会导致每次迭代时，参数几乎不变化，收敛学习速度变慢，使得算法的效率降低，需要很长时间才能达到最低点。

从理论上，它只能保证达到局部最低点，而非全局最低点。在很多复杂函数中有很多极小值点，我们使用梯度下降法只能得到局部最优解，而不能得到全局最优解。那么对应的解决方案如下：首先随机产生多个初始参数集，即多组；然后分别对每个初始参数集使用梯度下降法，直到函数值收敛于某个值；最后从这些值中找出最小值，这个找到的最小值被当作函数的最小值。当然这种方式不一定能找到全局最优解，但是起码能找到较好的。

对于梯度下降来说，初始点的位置，也是一个超参数。


在梯度下降之前需要使用归一化

## 随机梯度下降 stochastic gradient descent

批量梯度下降法，每一次计算过程，都要将样本中所有信息进行批量计算。但是显然如果样本量很大的话，计算梯度就比较耗时。基于这个问题，改进的方案就是随机梯度下降法。即每次迭代随机选取一个样本来对参数进行更新。使得训练速度加快。

批量搜索，那么每次都是沿着一个方向前进，但是随机梯度下降法由于不能保证随机选择的方向是损失函数减小的方向，更不能保证一定是减小速度最快的方向，所以搜索路径就会呈现曲线的态势，即随机梯度下降有着不可预知性。

但实验结论告诉我们，通过随机梯度下降法，依然能够达到最小值的附近（用精度换速度）。

随机梯度下降法的过程中，学习率的取值很重要，这是因为如果学习率一直取一个固定值，所以可能会导致点已经取到最小值附近了，但是固定的步长导致点的取值又跳去了这个点的范围。因此我们希望在随机梯度下降法中，学习率是逐渐递减的


## 批量梯度下降法 VS 随机梯度下降法SGD
批量梯度下降法BGD(Batch Gradient Descent)。
* 优点：全局最优解；易于并行实现；
* 缺点：当样本数据很多时，计算量开销大，计算速度慢。

针对于上述缺点，其实有一种更好的方法：随机梯度下降法SGD（stochastic gradient descent），随机梯度下降是每次迭代使用一个样本来对参数进行更新。
* 优点：计算速度快；
* 缺点：收敛性能不好

批量梯度下降法每次对所有样本都看一遍，缺点是慢，缺点是稳定。随机梯度下降法每次随机看一个，优点是快，缺点是不稳定。
其实还有一种中和二者优缺点的方法小批量梯度下降法 MBGD（Mini-Batch Gradient Descent）：在每次更新时用b个样本，其实批量的梯度下降就是一种折中的方法，用一些小样本来近似全部。优点：减少了计算的开销量，降低了随机性。
在机器学习领域，随机具有非常大的意义，因为计算速度很快。对于复杂的损失函数来说，随机可以跳出局部最优解，并且有更快的速度。