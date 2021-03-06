## Summary
[决策树1：初识决策树](https://mp.weixin.qq.com/s/k_OjObExgsi4DaHMSGUUMA)

[特征选择中的相关概念](https://mp.weixin.qq.com/s/yFxysYAx2Fe--11kJ4M3tg)

[决策树3: 特征选择之寻找最优划分](https://mp.weixin.qq.com/s/lP5ZqfhDCd4Tt3IYpQm-Lg)

[决策树4：构建算法之ID3、C4.5](https://mp.weixin.qq.com/s/lP5ZqfhDCd4Tt3IYpQm-Lg)

[决策树5：剪枝与sklearn中的决策树](https://mp.weixin.qq.com/s/YzNH1DybIlBTcJsacAEQwA)

[决策树6：分类与回归树CART](https://mp.weixin.qq.com/s/XAJnl9HggdQ6-Rab9GJiVw)

## 决策树与条件概率
用决策树分类：从根节点开始，对实例的某一特征进行测试，根据测试结果将实例分配到其子节点，此时每个子节点对应着该特征的一个取值，如此递归的对实例进行测试并分配，直到到达叶节点，最后将实例分到叶节点的类中。 

决策树表示给定特征条件下，类的条件概率分布，这个条件概率分布表示在特征空间的划分上，将特征空间根据各个特征值不断进行划分，就将特征空间分为了多个不相交的单元，在每个单元定义了一个类的概率分布，这样，这条由根节点到达叶节点的路径就成了一个条件概率分布。

假设X表示特征的随机变量，Y表示类的随机变量，那么这个条件概率可以表示为P(Y|X)，其中X取值于给定划分下单元的集合，Y取值于类的集合。各叶结点（单元）上的条件概率往往偏向某一个类。根据输入的测试样本，由路径找到对应单元的各个类的条件概率，并将该输入测试样本分为条件概率最大的一类中，就可以完成对测试样本的分类。

## 决策树学习目标与本质 

学习目标: 根据给定的训练数据集构建一个决策模型，使它能够对实例进行正确的分类。

决策树学习本质: 从训练数据集中归纳出一组分类规则。与训练数据集不相矛盾的决策树（即能对训练数据进行正确分类的决策树）可能是0个或多个。我们需要找到一个与训练数据矛盾较小的决策树，同时具有很好的泛化能力。

从另一个角度看，决策树学习是由训练数据集估计条件概率模型。基于特征空间划分的类的条件概率模型有无穷多个。我们选择的条件概率模型应该不仅对训练数据有很好地拟合，而且对未知数据有很好地预测。


## 决策树的损失函数

决策树损失函数: 正则化的极大似然函数
正则化： 简单来说是防止过拟合，TODO:仍要仔细理解
极大似然函数: 利用已知的样本结果，反推最有可能（最大概率）导致这样结果的参数值

[极大似然估计法的理解指南](http://www.sohu.com/a/308694540_633698)

## 决策树的构建
决策树通常有三个步骤:
* 特征选择
* 决策树的生成
* 决策树的修剪

决策树学习的算法通常是一个递归地选择最优特征，并根据该特征对训练数据进行分割，使得对各个子数据集有一个最好的分类的过程。这一过程对应着对特征空间的划分，也对应着决策树的构建。

这一过程对应着对特征空间的划分，也对应着决策树的构建。
1. 开始：构建根节点，将所有训练数据都放在根节点，选择一个最优特征，按照这一特征将训练数据集分割成子集，使得各个子集有一个在当前条件下最好的分类。
2. 如果这些子集已经能够被基本正确分类，那么构建叶节点，并将这些子集分到所对应的叶子节点去。
3. 如果还有子集不能够被正确的分类，那么就对这些子集选择新的最优特征，继续对其进行分割，构建相应的节点，如此递归进行，直至所有训练数据子集被基本正确的分类，或者没有合适的特征为止。
4. 每个子集都被分到叶节点上，即都有了明确的类，这样就生成了一颗决策树。

以上方法就是决策树学习中的特征选择和决策树生成，这样生成的决策树可能对训练数据有很好的分类能力，但对未知的测试数据却未必有很好的分类能力，即可能发生过拟合现象。我们需要对已生成的树自下而上进行剪枝，将树变得更简单，从而使其具有更好的泛化能力。具体地，就是去掉过于细分的叶结点，使其回退到父结点，甚至更高的结点，然后将父结点或更高的结点改为新的叶结点，从而使得模型有较好的泛化能力。

决策树生成和决策树剪枝是个相对的过程，决策树生成旨在得到对于当前子数据集最好的分类效果(局部最优)，而决策树剪枝则是考虑全局最优，增强泛化能力。

### 特征选择
在构建决策树，进行特征选择划分时，究竟选择哪个特征更好些？

这就要求确定选择特征的准则。直观上，如果一个特征具有更好的分类能力，或者说，按照这一特征将训练数据集分割成子集，使得各个子集在当前条件下有最好的分类，那么就更应该选择这个特征。

因此特征选择要解决的核心问题就是：
* 每个节点在哪个维度上做划分？
* 某个维度在哪个值上做划分？

划分的依据是： 要让数据划分成两部分之后，系统整体的信息熵降低。


### 信息熵 条件熵 信息增益
信息熵表示随机变量的不确定度。对于一组数据来说，越随机、不确定性越高，信息熵越大；不确定性越低，信息熵越小.
假设有三组，每组为三类的信息，每组每类的概率为：
```
三组概率，根据公式计算信息熵H 分别为：
{1/3, 1/3, 1/3}：H=1.0986
{1/10, 2/10, 7/10}： H=0.8018
{1, 0, 0}：H=0
```
这里可以清晰的看到， 第一组，每种结果的概率的相同所以不确定性越高，信息熵越大
数据有70%的概率是落在第三类中，因此要比第一个式子更稳定；第三个式子，干脆只有一个类，因此熵最小为0（特别稳定）

条件熵是：定义为X给定条件下，Y的条件概率分布的熵对X的数学期望

信息增益就是：以某特征划分数据集前后的熵的差值

信息增益总是偏向于选择取值较多的属性。信息增益比在此基础上增加了一个罚项，解决了这个问题。


## 决策树的修剪
两个目的：降低复杂度，解决过拟合。
决策树是依据训练集进行构建的，为了尽可能正确地分类训练样本，结点划分过程将不断重复，有时会造成决策树分支过多。这就可能会把训练样本学的“太好”了，以至于把训练集自身的一些特点当作所有数据都具有的一般性质而导致过拟合。因此可主动去掉一些分支来降低过拟合风险。
决策树非常容易产生过拟合，实际所有非参数学习算法，都非常容易产生过拟合。

决策树的修剪主要分为两种：
* 预剪枝（Pre-Pruning）
* 后剪枝（Post-Pruning）

预剪枝是指在决策树生成过程中，对每个节点在划分前先进行估计，若当前节点的划分不能带来决策树泛化性能的提升，则停止划分并将当前节点标记为叶节点。
那么所谓的“决策树泛化性能”如何来判定呢？这就可以使用性能评估中的留出法，即预留一部分数据用作“验证集”以进行性能评估。

后剪枝是先从训练集生成一颗完整的决策树，然后自底向上地对非叶节点进行考察，若将该节点对应的子树完全替换为叶节点能带来决策树繁花性的提升，则将该子树替换为叶节点。

对比预剪枝和后剪枝，能够发现，后剪枝决策树通常比预剪枝决策树保留了更多的分支，一般情形下，后剪枝决策树的欠拟合风险小，泛华性能往往也要优于预剪枝决策树。但后剪枝过程是在构建完全决策树之后进行的，并且要自底向上的对树中的所有非叶结点进行逐一考察，因此其训练时间开销要比未剪枝决策树和预剪枝决策树都大得多。


## CART算法
Classification And Regression Tree。顾名思义，CART算法既可以用于创建分类树（Classification Tree），也可以用于创建回归树（Regression Tree）、模型树（Model Tree）

ID3中使用了信息增益选择特征，增益大优先选择。C4.5中，采用信息增益比选择特征，减少因特征值多导致信息增益大的问题。CART分类树算法使用基尼系数来代替信息增益比，基尼系数代表了模型的不纯度，基尼系数越小，不纯度越低，特征越好。这和信息增益（比）相反。


## 决策树优势

* 决策树易于理解和实现. 人们在通过解释后都有能力去理解决策树所表达的意义。
对于决策树，数据的准备往往是简单或者是不必要的 . 
* 其他的技术往往要求先把数据一般化，比如去掉多余的或者空白的属性。
* 能够同时处理数据型和常规型属性。其他的技术往往要求数据属性的单一。
* 是一个白盒模型如果给定一个观察的模型，那么根据所产生的决策树很容易推出相应的逻辑表达式。
* 易于通过静态测试来对模型进行评测。表示有可能测量该模型的可信度。
* 在相对短的时间内能够对大型数据源做出可行且效果良好的结果


## Sklearn决策树
部分sklearn决策树代码
[sklearn_dt](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/ww8_decision_tree/decision_tree.py)