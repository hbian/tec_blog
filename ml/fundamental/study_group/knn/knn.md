## ML Study Group
首先想感谢木东居士和饼干组织并经营这个小组, 给了自己一个循序渐进而且能够和大家一起学习的机会,学习资料：

[W1_KNN学习](https://mp.weixin.qq.com/s/AG1CgLHBNA5Lpxg_Myo8IA)

[KNN算法简单实现](https://mp.weixin.qq.com/s?__biz=MzUyMjI4MzE0MQ==&mid=2247484679&idx=1&sn=aec5259ee503b9b127b79e2a9661205d&scene=21#wechat_redirect)

[机器学习-KNN算法](https://www.cnblogs.com/gemine/p/11130032.html)

## KNN
K nearest neighbor：K最邻近算法.

在处理分类问题时，可以这么理解，获取离该样本最近的K个最近距离的邻居的分类, 通过多数表决(投票法)来判断该样本的分类.

在处理回归问题时，获取离该样本最近的K个最近距离的邻居的标记值, 通过平均法，计算最近K个样本的标记均值作为预测结果

分类问题的算法流程可以梳理如下：

* 计算预测对象到训练集中对象距离
* 按距离进行排序，并提取最近的k个对象
* 统计这K个邻居的类别，取频率最高的为预测对象的类别


KNN特点：
*监督学习算法
*KNN 没有训练过程，是懒惰学习的代表(lazy learning), 此类学习技术在训练过程只是把样本保存起来。训练时间开销为0， 待收到测试样本时再进行处理。


### 距离
这个算法中的一个关键点就是求样本之间的距离，有如下几种常见距离

* 欧式距离 Euclidean Distance

多维空间中的各个点之间的绝对距离， 每个点在各自维度上的坐标相减， 差值平方后进行就和然后开方：

![欧式距离](http://dl2.iteye.com/upload/attachment/0098/4314/bb71ff05-fe7f-3045-bfc7-1bfad452af9f.png)

可以用勾股定理中的求直角边距离来模拟这个距离在二维时的应用。

* 明可夫斯基距离 Minkowski Distance

明氏距离是欧氏距离的推广，是对多个距离度量公式的概括性的表述。公式如下：

![明氏距离](http://dl2.iteye.com/upload/attachment/0098/4316/9567216c-ffd4-3d7f-a871-f8685a304cdd.png)

其实可以看到欧式距离和曼哈顿距离就是P=2 和 P=1时的情况

* 曼哈顿距离 Manhattan Distance
对距离进行简单估算，可以想象求从一个街区去另外个街区仅走车行道的距离

![曼哈顿距离](http://dl2.iteye.com/upload/attachment/0098/4318/87bb1b15-ee66-34ec-890e-f09a3f7aa1ab.png)

**以上的距离算法都必须保证各个特征必须在一个度量。比如说2个特征都是距离长度为cm， 这个时候我们可以用欧式距离。但是如果是一个人为样本，重量和身高作为特征，那么欧式距离就失效了**

皮尔逊相关系数，余弦相似度可以处理不同量级这个问题，这里记录下，以后再展开研究。

## KNN 简单实现
例子为通过给定的病例中肿瘤大小和发现时间二个特征，来对未知病例进行分类，良性或者恶性，流程如下：
* 首先对训练集进行绘图
* 计算预测点到训练集中所有点的距离
* 按距离进行排序并找到K个距离最近的点
* 获取这K个点的分类Label，通过most common获得比例最高的分类

代码实现如下 ：

[knn_poc](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/knn/knn_poc.py)


常规的机器学习流程：
选择机器学习算法 -> 机器学习算法.fit(x_train, y_train) -> 得到模型 -> 模型.predict(x_test)-> 输出结果.
kNN算法没有模型，模型其实就是训练数据集，可以在简单版本的KNN实现中看到fit方法仅仅是存储训练集，predict的过程就是求k近邻的过程。

综合前面的POC的代码:[仿照sklearn实现自己的knn](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/knn/knn_sk_like.py)

## kd树
K近邻法的重要步骤是对所有的实例点进行快速k近邻搜索。如果采用线性扫描（linear scan），要计算输入点与每一个点的距离，时间复杂度非常高。因此在查询操作时，使用kd树。

[KD树](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247483857&idx=3&sn=5a4573e5fe074241a45f6affb969448f&chksm=eb932867dce4a171ff2890ee6b326cfc234e1361948d673c30ea30110894435a63f780b0540e&token=932563280&lang=zh_CN&scene=21#wechat_redirect)

## KNN需要注意的几个问题

* 大数吞小数

在进行距离计算的时候，有时候某个特征的数值会特别的大，那么计算欧式距离的时候，其他的特征的值的影响就会非常的小被大数给覆盖掉了。所以我们很有必要进行特征的标准化或者叫做特征的归一化。个人觉得这并不是一个KNN独有的问题，很多算法都涉及到这个问题，可以利用sklearn的preprocessing.scale先进行标准化

* 怎么处理样本的重要性

利用权重值。我们在计算距离的时候可以针对不同的邻居使用不同的权重值，比如距离越近的邻居我们使用的权重值偏大，这个可以指定算法的weights参数来设置。

* 如何处理大数据量

一旦特征或者样本的数目特别的多，KNN的时间复杂度将会非常的高。解决方法是利用KD-Tree这种方式解决时间复杂度的问题，利用KD树可以将时间复杂度降到O(logD*N*N)。D是维度数，N是样本数。但是这样维度很多的话那么时间复杂度还是非常的高，所以可以利用类似哈希算法解决高维空间问题，只不过该算法得到的解是近似解，不是完全解。会损失精确率。

