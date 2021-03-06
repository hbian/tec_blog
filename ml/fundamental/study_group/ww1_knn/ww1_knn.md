## KNN
[W1_KNN学习](https://mp.weixin.qq.com/s/AG1CgLHBNA5Lpxg_Myo8IA)

[KNN算法简单实现](https://mp.weixin.qq.com/s?__biz=MzUyMjI4MzE0MQ==&mid=2247484679&idx=1&sn=aec5259ee503b9b127b79e2a9661205d&scene=21#wechat_redirect)

[机器学习-KNN算法](https://www.cnblogs.com/gemine/p/11130032.html)

## kNN思想简介
K nearest neighbor：K最邻近算法. KNN的原理以及实现过程可描述如下：

在一个给定的类别已知的训练样本集中，已知样本集中每一个数据与所属分类的对应关系（标签）。在输入不含有标签的新样本后，将新的数据的每个特征与样本集中数据对应的特征进行比较，然后算法提取样本最相似的k个数据(最近邻)的分类标签。通过多数表决等方式进行预测。即选择k个最相似数据中出现次数最多的分类，作为新数据的分类。
在处理分类问题时，可以这么理解，获取离该样本最近的K个最近距离的邻居的分类, 通过多数表决(投票法)来判断该样本的分类.

这里可以看到K近邻法不具有显式的学习过程，而是利用训练数据集对特征向量空间进行划分，并作为其分类的“模型”。

## kNN算法流程
K近邻法使用的模型，实际上是特征空间的划分。模型由三个基本要素决定：
* 距离度量
* k值
* 分类决策规则

算法流程可以梳理如下：

1. 计算测试对象到训练集中每个对象的距离
2. 按照距离的远近排序
3. 选取与当前测试对象最近的k的训练对象，作为该测试对象的邻居
4. 统计这k个邻居的类别频次
5. k个邻居里频次最高的类别，即为测试对象的类别

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

[knn_poc](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww1_knn/knn_poc.py)


常规的机器学习流程：
选择机器学习算法 -> 机器学习算法.fit(x_train, y_train) -> 得到模型 -> 模型.predict(x_test)-> 输出结果.
kNN算法没有模型，模型其实就是训练数据集，可以在简单版本的KNN实现中看到fit方法仅仅是存储训练集，predict的过程就是求k近邻的过程。

综合前面的POC的代码:[仿照sklearn实现自己的knn](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww1_knn/knn_sk_like.py)


## KNN需要注意的几个问题

* 大数吞小数

在进行距离计算的时候，有时候某个特征的数值会特别的大，那么计算欧式距离的时候，其他的特征的值的影响就会非常的小被大数给覆盖掉了。所以我们很有必要进行特征的标准化或者叫做特征的归一化。个人觉得这并不是一个KNN独有的问题，很多算法都涉及到这个问题，可以利用sklearn的preprocessing.scale先进行标准化

* 怎么处理样本的重要性

利用权重值。我们在计算距离的时候可以针对不同的邻居使用不同的权重值，比如距离越近的邻居我们使用的权重值偏大，这个可以指定算法的weights参数来设置。

* 如何处理大数据量

一旦特征或者样本的数目特别的多，KNN的时间复杂度将会非常的高。解决方法是利用KD-Tree这种方式解决时间复杂度的问题，利用KD树可以将时间复杂度降到O(logD*N*N)。D是维度数，N是样本数。但是这样维度很多的话那么时间复杂度还是非常的高，所以可以利用类似哈希算法解决高维空间问题，只不过该算法得到的解是近似解，不是完全解。会损失精确率。

K近邻法的重要步骤是对所有的实例点进行快速k近邻搜索。如果采用线性扫描（linear scan），要计算输入点与每一个点的距离，时间复杂度非常高。因此在查询操作时，使用kd树。

[KD树](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247483857&idx=3&sn=5a4573e5fe074241a45f6affb969448f&chksm=eb932867dce4a171ff2890ee6b326cfc234e1361948d673c30ea30110894435a63f780b0540e&token=932563280&lang=zh_CN&scene=21#wechat_redirect)

KNN算法的时间复杂度为O(D*N*N)。其中D为维度数，N为样本总数。从时间复杂度上我们可以很清楚的就知道KNN非常不适合高维度的数据集，容易发生维度爆炸的情况。同时我们也发现了一个问题在关于K的选择上面，我们一般也要选择K的值应该尽量选择为奇数，并且不要是分类结果的偶数倍，否则会出现同票的情况。具体选择K的大小我们可以进行交叉验证.交叉验证指的是将训练数据集进一步分成训练数据和验证数据，选择在验证数据里面最好的超参数组合。参数一般分为模型参数和超级参数。模型参数是需要我们通过不断的调整模型和超参数训练得到的最佳参数。而超参数则是我们人为手动设定的值。像在KNN中超参数就是K的值。我们可以通过交叉验证的方式，选择一组最好的K值作为模型最终的K值。

## Summary
KNN 没有训练过程，是懒惰学习的代表(lazy learning), 此类学习技术在训练过程只是把样本保存起来。训练时间开销为0， 待收到测试样本时再进行处理, KNN是适合在低维度空间中使用.

## KNN题目
1. KNN算法原理，优缺点
KNN主要用于分类，通过计算测试集于训练集之间的距离，然后选择K个最近距离，通过多数票决定测试集的分类。
* 优点：没有学习过程，适合于多分类问题
* 缺点: 不适合于特征或者样本的数目特别的多的训练样本集。
当样本不平衡时，如其中一个类别的样本较大，可能会导致对新样本计算近邻时，大容量样本占大多数，影响分类效果。

2. KNN算法中如何计算距离，为什么用欧式不用曼哈顿？
KNN算法中主要使用欧式距离.
曼哈顿距离只计算水平或垂直距离，有维度的限制。另一方面，欧氏距离可用于任何空间的距离计算问题。因为，数据点可以存在于任何空间，欧氏距离是更可行的选择。

3. KNN中如何选取超参数K值？
K值最好选择奇数，避免同票的情况。通过交叉验证选取K值得最优解。

4. KNN算法时间度，高维数据如何处理
KNN算法的时间复杂度为O(D*N*N)。