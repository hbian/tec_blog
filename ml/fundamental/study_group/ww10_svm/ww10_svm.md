## SVM
[入门支持向量机1：图文详解SVM原理与模型数学推导](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484477&idx=1&sn=226e099c1951b6c11b1e7fb6b7a092a3&chksm=eb932d8bdce4a49d0595b6c642fc2e5969fdc05a185f97a39cc1a896e24d56d8703541a28f9c&scene=21#wechat_redirect)
[入门支持向量机2:软间隔与sklearn中的SVM](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484512&idx=1&sn=7a6b75f312e92bbdecafdedf979ed929&chksm=eb932dd6dce4a4c0ae4ea087878ec7a5f5ccc0724a85aa93daff3d08c33ecf86a3d809e51a82&scene=21#wechat_redirect)
[入门支持向量机3：巧妙的Kernel Trick](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484546&idx=1&sn=33c6c5cb698b8835b2ee57dd8ea7c221&chksm=eb932d34dce4a4221f40f3daa26863a5fd05dcbcf74738d5423316c643e3ff930904d1a33fca&scene=21#wechat_redirect)
[入门支持向量机4：多项式核函数与RBF核函数代码实现及调参](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484572&idx=1&sn=fd6e86ce45167286fb6ba4089b7b29dd&chksm=eb932d2adce4a43c44d26e79d4968f395d7cc22a31d84aef7944b227e1843b3f0722a5e894ed&scene=21#wechat_redirect)
[入门支持向量机5：回归问题及系列回顾总结](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484596&idx=1&sn=7e93eb135d66c86238ccf516f0ae65ec&chksm=eb932d02dce4a41447a9cb34d627f435c760a5deb125a40d4c2a77f99e2187194d6bfbda4cbc&scene=21#wechat_redirect)

## 支撑向量机 SVM Support Vector Machine
支撑向量机，本质上就是个线性分类器，保证Margin最大

支撑向量机如何解决“不适定问题呢”？SVM要找到一条泛化性比较好的决策边界，就是这条直线要离两个分类都尽可能的远，我们认为这样的决策边界就是好的

将最优决策边界向上&下平移，在遇到第一个点时停下来，这个点被称为支撑向量Support Vector；支撑向量到决策边界的距离是d；这两条平移后的直线的间隔（2d）被称为最大间隔Margin。

支撑向量就是支撑着两条平移边界的点，我们只需要重点研究这几个支撑向量即可，这也是SVM名称的由来；Margin就是分界面可以移动的范围，范围越大表示容错能力越强。

所以我们可以看到，所谓的支撑向量机，最初就是一个线性分类器，只不过这个线性分类器不仅能把样本分对，可以最大化Margin。


### Soft Margin
在线性可分问题中，对于样本点来说，存在一根直线可以将样本点划分，我们称之为Hard Margin SVM；但是（同样线性不可分），有时候会出现不那么完美，样本点会有一些噪声或者异常点，并不能完全分开。即没有一条直线可以将样本分成两类。那么就提出了Soft Margin SVM。

Soft Margin SVM的思想也很朴素，就是在Hard Margin的基础上，将原来的约束条件放宽一些。增加容错性。


### SVM 演进

最初就是一个线性分类器，对其进行改进，使得Margin最大化，这就导出了Linear SVM，定义了Margin，将其数学表达式求出来，去优化这个函数。

Linear SVM也有一些问题，即在实际情况下不能完美地将各个数据点分开，在不满足限制条件的下就求不到数学解。为了解决线性可分的情况下存在异常点的问题，就提出了Soft Margin的思想，增加正则化项，提高容错性。

那么如何解决线性不可能问题呢？把原始空间的问题映射到高维空间，将线性不可分问题转换成线性可分问题，即将。这种想法非常好，但是高维数据做内积，计算量太大了。

为了解决这个问题，数学家提出了Kernel Trick核函数：。实际上我们从来不会去真正去求高维映射，而是直接用核函数来代替了，既相当于在高维空间进行操作，又解决了计算量大的问题。


### Sklearn 应用
[sklearn_hard_soft_svm](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww10_svm/sklearn_hard_soft_svm.py)
[sklearn_PolynomialKernelSVC](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww10_svm/sklearn_PolynomialKernelSVC.py)


###  SVM算法的优缺点

优点：
* 解决高维特征的分类问题和回归问题很有效,在特征维度大于样本数时依然有很好的效果。
* 仅仅使用一部分支持向量来做超平面的决策，无需依赖全部数据。
* 有大量的核函数可以使用，从而可以很灵活的来解决各种非线性的分类回归问题。
* 样本量不是海量数据的时候，分类准确率高，泛化能力强。

SVM算法的主要缺点有：
* 如果特征维度远远大于样本数，则SVM表现一般。
* SVM在样本量非常大，核函数映射维度非常高时，计算量过大，不太适合使用。
* 非线性问题的核函数的选择没有通用标准，难以选择一个合适的核函数。
* SVM对缺失数据敏感。

