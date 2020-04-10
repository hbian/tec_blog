# 逻辑回归
WW6的学习内容: 逻辑回归：损失函数、梯度、决策边界

[数据科学家学习小组之机器学习第六周](https://mp.weixin.qq.com/s/Zsh0XalClcg2NlylBd4AJg)

[出场率No.1的逻辑回归算法，是怎样“炼成”的](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484074&idx=1&sn=25a66eedf3a9e7cb439e157309614f88&scene=21#wechat_redirect)

[逻辑回归的本质及其损失函数的推导、求解](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484100&idx=1&sn=50c9caf07c84135b467305685472f2cc&scene=21#wechat_redirect)

[逻辑回归代码实现与调用](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484105&idx=1&sn=7ad5725fc9a2bba86c96ff352924f19e&scene=21#wechat_redirect)

[逻辑回归的决策边界及多项式](https://mp.weixin.qq.com/s?__biz=MzI4MjkzNTUxMw==&mid=2247484138&idx=1&sn=8bbc9f2a4c17a95ea0f11bb2714c38eb&scene=21#wechat_redirect)

[sklearn中的逻辑回归中及正则化](https://mp.weixin.qq.com/s/BUDdj4najgR0QAHhtu8X9A)

## 逻辑回归
Logistic Regression, 是解决分类问题的，本质是求概率再分类,即预测样本发生的概率是多少, 由于概率是一个数，因此被叫做“逻辑回归”。

逻辑回归在分类结果的背后是隐藏变量的博弈，我们认为隐藏变量与特征是线性相关的，因此就可以对隐藏变量之差求概率（得到随机变量的累积分布函数），得到probit回归模型。为了使数学公式更为简单，使用sigmoid函数去近似，最终得到逻辑回归模型。

那么对于解决分类问题的逻辑回归来说，我们需要找到一个“联系函数”，将线性回归模型的预测值与真实标记联系起来。

将"概率"转换为"分类"的工具是"阶梯函数"：
```
p^ = f(x) 
y^ ={0 p^<0.5, 1 p^ >0.5
```

### 为什么要使用sigmoid函数作为假设？
TODO:这段话仍然要反复加深理解

因为线性回归模型的预测值为实数，而样本的类标记为（0,1），我们需要将分类任务的真实标记y与线性回归模型的预测值联系起来，也就是找到广义线性模型中的联系函数。如果选择单位阶跃函数的话，它是不连续的不可微。而如果选择sigmoid函数，它是连续的，而且能够将z转化为一个接近0或1的值。

## 决策边界
决策边界就是能够把样本正确分类的一条边界，主要有线性决策边界(linear decision boundaries)和非线性决策边界(non-linear decision boundaries)。

注意：决策边界是假设函数的属性，由参数决定，而不是由数据集的特征决定。


## SKlearn中的逻辑回归
这里主要是看看SKlearn，实现多项式项逻辑回归, 以及决策边界

[sklearn_logistic_regression](https://github.com/hbian/tec_blog/blob/master/ml/fundamental/study_group/knn/sklearn_logistic_regression.py)


TODO:  模型的正则化, L1，L2的正则仍需要单独学习


逻辑回归对问题划分层次，并利用非线性变换和线性模型的组合，将未知的复杂问题分解为已知的简单问题,理解好逻辑回归的细节,有助于掌握了数据建模的精髓. 逻辑回归: **将样本的特征和样本发生的概率联系起来**，