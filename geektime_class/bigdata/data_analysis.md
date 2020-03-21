# 对大数据的认识
当我们谈论大数据的时候，我们究竟在谈什么？是谈 Hadoop、Spark 这样的大数据技术产品？还是谈大数据分析、大数据算法与推荐系统这样的大数据应用？其实这些都是大数据的工具和手段，大数据的核心就是数据本身。数据就是一座矿山，大数据技术产品、大数据分析与算法是挖掘机、采矿车，你学了大数据，每天开着矿车忙忙碌碌，那你只是一个矿工，可能每天面对一座金山却视而不见。数据比代码的地位要高得多，用途也大得多，做大数据的同学要意识到数据的重要性。数据的作用是无处不在的，不但能做统计分析、精准营销、智能推荐，还能做量化交易帮你自动赚钱，甚至能驱动公司运营，管理整个公司。

事实上，公司到了一定规模，产品功能越来越复杂，人员越来越多，不管用什么驱动，最后一定都是数据驱动。没有量化的数据，不足以凝聚团队的目标，甚至无法降低团队间的内耗。这个时候哪个部门能有效利用数据，能用数据说话，能用数据打动老板，哪个部门就能成为公司的驱动核心，在公司拥有更多话语权。我们学大数据，手里用的是技术，眼里要看到数据，要让数据为你所用。数据才是核心才是不可代替的，技术并不是。

数据，不管你用还是不用，它就在那里。但是它的规律与价值，你不去分析、挖掘、思考，它不会自己跳出来告诉你答案。顶尖的高手，总是能从看似不相干的事物之间找到其联系与规律，并加以利用，产生出化腐朽为神奇的功效。我们应该对数据保持敏感与好奇，不断将现实发生的事情与数据关联起来，去思考、去分析，用数据推断出来的结论指导现实的工作，再根据现实的反馈修正自己的方法与思维，顶尖高手就是在这样的训练中不断修炼出来的。

## 数据分析
数据分析中，有一种金字塔分析方法。它是说，任何一个问题，都可能有三到五个引起的原因，而每个原因，又可能有三到五个引起的子原因，由此延伸，组成一个金字塔状的结构。我们可以根据这个金字塔结构对数据进行分析，寻找引起问题的真正原因。

金字塔分析方法可以全面评估引起问题的各种原因，但是也可能会陷入到太过全面，无从下手或者分析代价太大的境况。所以要根据经验和分析，寻找主要原因链路。绝大多数互联网产品的主要原因链路就在转化漏斗图上，上面案例中，数据分析师的分析过程，基本就集中在转化漏斗上。
我曾经看过某独角兽互联网公司的数据运营指导文件，对于几个关键业务指标的异常必须要及时通知高管层，并在限定时间内分析异常原因。而指导分析的链路点，基本都在转化漏斗图上，只不过因为入口渠道众多，这样的分析链路也有很多条。这种金字塔方法不仅可以用于数据分析过程，在很多地方都适用，任何事情都可以归纳出一个中心点，然后几个分支点，每个分支点又有几个子分支。构建起这样一个金字塔，对于你要表达的核心观点，或者要学习知识，都可以有一个清晰的脉络，不管是和别人交流，还是自己思考学习，都很有帮助。


## 利用大数据增长用户数量
 增长模型的各个环节其实都离不开大数据的支持，具体是利用大数据分析和计算，增长用户的手段主要有：
 * 利用用户画像进行精准广告获客。比如微信朋友圈的广告，通过对用户微信数据的分析进行用户画像。投放广告的时候，可以精确使用用户标签进行广告投放，获取到有效的客户，即所谓的广告选人。
 * 通过用户分析挽回用户。我在前面说过，互联网产品的用户留存很难超过 40%，对于流失用户，可以通过短信、推送等手段进行挽回，比如根据用户注册信息，推送用户感兴趣的商品、折扣券、红包等信息，重新激活用户。留存用户由于某些原因也会再次流失或者沉默，通过用户价值分析和流失原因分析，也可以进一步采用各种运营策略挽回用户。
 * A/B 测试决定产品功能。新功能通过 A/B 测试进行数据分析，分析是否对用户留存、购买转化等关键指标有正向作用，以此决定是否上新功能。
 * 大数据反欺诈、反羊毛。互联网产品在拉新或提高留存的过程中，会有很多促销手段，但是这些促销手段会吸引来专业的“羊毛党”，他们会注册大量虚假账号，然后领取红包，使企业的促销资源无法投放到真正的用户手中。此时可以通过历史数据、用户点击行为分析等大数据技术，有效识别出“羊毛党”。
 * 用户生命周期管理。一个互联网产品的用户会经历获取、提升、成熟、衰退、离网几个阶段，用户在不同的生命周期阶段会有不同的诉求，通过数据分析对用户进行分类，可以有针对性的运营，进一步提升用户的留存和转化。


## 通过数据推动需求
引入业务数据监控，在提出一个新需求时，需要对价值进行预估：这个新功能可以有多少点击，可以提高多少留存、多少转化，对预期价值进行量化。产品和开发需要知道预期价值，如果对价值有疑惑，可以提出质疑，多方一起讨论，对需求进行完善。新功能上线后，对新功能的业务指标进行持续监控，检验是否达到当初的预期；如果没有，提出后续改进的措施。