## Summary
[数据降维1：主成分分析法思想及原理](
https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484343&idx=1&sn=6a7dd3b9979b306265da0747f15064e2&chksm=eb932a01dce4a317c6c344dde4b4e30c99e46fd06416508997043d17d2b4899a649b7cc570c5&scene=21#wechat_redirect)

[数据降维2：PCA算法的实现及使用](
https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484331&idx=1&sn=8e7b882d2e14e3c32d2a27669962b44b&chksm=eb932a1ddce4a30b65d82dcaf9b4f2967f14cd9f2bc532f9c8e186d5dd4e9ad3a5dbfa4027c6&scene=21#wechat_redirect)

[数据降维3：降维映射及PCA的实现与使用](
https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484370&idx=1&sn=fe01e5057f94c248ce69ef8766bffcb8&chksm=eb932a64dce4a3729c046346aa71a5ba2285e2f5237fe710bac805312db36379609fbd21430a&scene=21#wechat_redirect)

[数据降维之应用：降噪&人脸识别](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484382&idx=1&sn=d8d488b01935ca5e7dc05a9ee302cf03&chksm=eb932a68dce4a37e5ee4b576b56daba6bc2deee243a9a7c3e87ca56f5f602e00c6eb676a5f69&scene=21#wechat_redirect)

### 主成分分析法

PCA(Principal Component Analysis)即主成分分析方法，是一种使用最广泛的数据降维算法（非监督的机器学习方法）。
其最主要的用途在于“降维”，通过析取主成分显出的最大的个别差异，发现更便于人类理解的特征。也可以用来削减回归分析和聚类分析中变量的数目。

我们需要找到一种合理的方法，在减少需要分析的指标同时，尽量减少原指标包含信息的损失，以达到对所收集数据进行全面分析的目的。由于各变量之间存在一定的相关关系，因此可以考虑将关系紧密的变量变成尽可能少的新变量，使这些新变量是两两不相关的，那么就可以用较少的综合指标分别代表存在于各个变量中的各类信息。主成分分析与因子分析就属于这类降维算法。

PCA的主要思想是将n维特征映射到k维上，这k维是全新的正交特征也被称为主成分，是在原有n维特征的基础上重新构造出来的k维特征。我们要选择的就是让映射后样本间距最大的轴。

其过程分为两步：
1. 样本归0： 将样本进行均值归0（demean），即所有样本减去样本的均值。样本的分布没有改变，只是将坐标轴进行了移动。
2. 找到样本点映射后方差最大的单位向量，此时，我们就可以用搜索策略，使用梯度上升法来解决。在求极值的问题中，有梯度上升和梯度下降两个最优化方法。梯度上升用于求最大值，梯度下降用于求最小值。
3. 求解第一个主成分后，假设得到映射的轴为所表示的向量，需要先将数据集在第一个主成分上的分量去掉，然后在没有第一个主成分的基础上再寻找第二个主成分。

## sklearn pca
我们在使用sklearn中提高的PCA方法时，需要先初始化实例对象（此时可以传递主成分个数），fit操作得到主成分后进行降维映射操作pca.transform。在初始化实例对象时，也可以传入一个数字，表示主成分所解释的方差比例，即每个主成分对原始数据方差的重要程度。忽略对原始方差影响小的成分，在时间和准确度之间做一个权衡。

PCA算法提供了一个特殊的指标pca.explained_variance_ratio_（解释方差比例），我们可以使用这个指标找到某个数据集保持多少的精度：
```
pca.explained_variance_ratio_
# 输出：
array([ 0.14566817,  0.13735469])
```
上面就是主成分所解释的方差比例。对于现在的PCA算法来说，得到的是二维数据：0.14566817表示第一个轴能够解释14.56%数据的方差；0.13735469表示第二个轴能够解释13.73%数据的方差。PCA过程寻找主成分，就是找使得原数据的方差维持的最大。这个值就告诉我们，PCA最大维持了原来所有方差的百分比。对于这两个维度来说，[ 0.14566817, 0.13735469]涵盖了原数据的总方差的28%左右的信息，剩下72%的方差信息就丢失了，显然丢失的信息过多。

[sklearn_pca](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww9_pca/sklearn_pca.py)

## PCA能降噪
在实际的数据中不可避免地出现各种噪音，这些噪音的出现可能会对数据的准确性造成一定的影响。而主成分分析法还有一个用途就是降噪。PCA通过选取主成分将原有数据映射到低维数据再映射回高维数据的方式进行一定程度的降噪。

我们降噪，这就需要使用PCA中的一个方法：X_ori=pca.inverse_transform(X_pca)，将降维后的数据转换成与维度相同数据。要注意，还原后的数据，不等同于原数据！

这是因为在使用PCA降维时，已经丢失了部分的信息（忽略了解释方差比例）。因此在还原时，只能保证维度相同。会尽最大可能返回原始空间，但不会跟原来的数据一样。

这样一来一回之间，丢失掉的信息，就相当于降噪了。

```

from sklearn.decomposition import PCA

pca = PCA(n_components=1)
pca.fit(X)
X_reduction = pca.transform(X)
X_restore = pca.inverse_transform(X_reduction)
plt.scatter(X_restore[:,0], X_restore[:,1])
plt.show()
```