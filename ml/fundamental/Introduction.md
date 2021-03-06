## 基本流程
1. 场景解析：先把业务逻辑想清楚，把业务场景进行抽象，然后将业务场景于算法进行匹配。以放爬虫为例， 了解爬虫来网站是要获取什么信息，我们是否清楚网站都有些什么样的请求，那么识别爬虫到底是一个分类还是一个聚类的问题呢，这涉及到了完全不同的算法和模型
2. 数据预处理：清洗数据，针对空值和乱码进行处理，比如ng日志中有些列就可能存在空值。
    * 数据的标准化(normalization):数据同趋化处理和无量纲化处理.
        *  数据同趋化是指：将数据按比例缩放，使其落入一个比较小的区间. 在某些评价指标的处理时会用到，去除数据的到单位限制，将其转为无量纲的纯数字， 便于不同单位的或量级的指标进行比较和加权。比较典型的处理办法之一就是归一化处理，将数据映射到[0,1]的区间
        * 归一化的好处： 
        - 提高模型的收敛速度: 如果一个模型只有x1 [1, 10] 和x2[1,1000]二个特征时，对其进行优化时会得到一个椭圆形，梯度下降时会沿着等高线方向走之字形， 这样迭代的很慢。如果将x1, x2进行归一化处理后，会得到一个圆形，迭代会快很多。
        - 提升模型的精度: 在多个指标共存的情况下，比如房间数和房间大小，是具有不同的量纲和数量级的。这时候如果用原始数据进行分析，那么数值较高的特征会更加突出，数值较低的的特征会被削弱。以航司爬虫LFS,RES,PAY为例，那么LFS,和RES就不是一个数量级的数据，如果不进行归一化处理，LFS的的特征会被明显放大。
        * 需要归一化的模型：有些模型在各个维度进行不均匀伸缩后，最优解与原来不等价，例如SVM（距离分界面远的也拉近了，支持向量变多？）。对于这样的模型，除非本来各维数据的分布范围就比较接近，否则必须进行标准化，以免模型参数被分布范围较大或较小的数据dominate。
        有些模型在各个维度进行不均匀伸缩后，最优解与原来等价，例如logistic regression（因为θ的大小本来就自学习出不同的feature的重要性吧？）。对于这样的模型，是否标准化理论上不会改变最优解。但是，由于实际求解往往使用迭代算法，如果目标函数的形状太“扁”，迭代算法可能收敛得很慢甚至不收敛。所以对于具有伸缩不变性的模型，最好也进行数据标准化。
    * 定性特征的转换：定性的特征无法在机器学习中直接使用，比如说男女，比如说nginx中的访问url。这时候可以使用哑编码将定性特征转化为定量的，比如说一个特征有N个值，那么就将其转化为N个特征，当特征为某个值m时，m这个特征取1， 其他特征取0. 哑编码的方式相比直接指定的方式，不用增加调参的工作，对于线性模型来说，使用哑编码后的特征可达到非线性的效果。

3. 特征工程： 数据和特征决定了机器学习的上限，算法和模型只是逼近这个上限而已。
    - 特征是否发散：如果一个特征不发散，例如方差接近于0，也就是说样本在这个特征上基本上没有差异，这个特征对于样本的区分并没有什么用
    - 特征与目标的相关性：这点比较显见，与目标相关性高的特征，应当优选选择。除方差法外，本文介绍的其他方法均从相关性考虑。
4. 模型训练：训练数据经过数据清洗和特征提取，然后进入算法训练模块生成模型。然后使用模型的预测组件可以对测试数据进行计算，获得预测结果
5. 模型评估.
6. 离线和在线服务
