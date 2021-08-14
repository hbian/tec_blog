## YARN基本组成
YARN的基本结构由一个ResourceManager与多个NodeManager组成。ResourceManager负责对NodeManager所持有的资源进行统一管理和调度。当在处理一个作业时ResourceManager会在NodeManager所在节点创建一全权负责单个作业运行和监控的程序ApplicationMaster。

* ResouceManager（简称RM）资源管理器负责整个集群资源的调度，该组件由两部分构成：调度器（Scheduler）和ApplicationsMaster（简称ASM）。调度器会根据特定调度器实现调度算法，结合作业所在的队列资源容量，将资源按调度算法分配给每个任务。分配的资源将用容器（container）形式提供，容器是一个相对封闭独立的环境，已经将CPU、内存及任务运行所需环境条件封装在一起。通过容器可以很好地限定每个任务使用的资源量。YARN调度器目前在生产环境中被用得较多的有两种：能力调度器（CapacityScheduler）和公平调度器（Fair Scheduler）。
* ApplicationMaster（简称AM）每个提交到集群的作业（job）都会有一个与之对应的AM 来管理。它负责进行数据切分，并为当前应用程序向RM 去申请资源，当申请到资源时会和NodeManager 通信，启动容器并运行相应的任务。此外，AM还负责监控任务（task）的状态和执行的进度。
* NodeManage（简称NM）NodeManager负责管理集群中单个节点的资源和任务，每个节点对应一个NodeManager,NodeManager负责接收ApplicationMaster的请求启动容器，监控容器的运行状态，并监控当前节点状态及当前节点的资源使用情况和容器的运行情况，并定时回报给ResourceManager。

## YARN工作流程
YARN在工作时主要会经历3个步骤：
1. ResourceManager收集NodeManager反馈的资源信息，将这些资源分割成若干组，在YARN中以队列表示。
2. 当YARN接收用户提交的作业后，会尝试为作业创建一个代理ApplicationMaster。
3. 由ApplicationMaster将作业拆解成一个个任务（task），为每个任务申请运行所需的资源，并监控它们的运行。

YARN在处理任务时的工作流程,经历了以下几个步骤：
1. 客户端向YARN提交一个作业（Application）。
2. 作业提交后，RM根据从NM收集的资源信息，在有足够资源的节点分配一个容器，并与对应的NM进行通信，要求它在该容器中启动AM。
3. AM创建成功后向RM中的ASM注册自己，表示自己可以去管理一个作业（job）。
4. AM注册成功后，会对作业需要处理的数据进行切分，然后向RM申请资源，RM会根据给定的调度策略提供给请求的资源AM。
5. AM申请到资源成功后，会与集群中的NM通信，要求它启动任务。
6. NM接收到AM的要求后，根据作业提供的信息，启动对应的任务。
7. 启动后的每个任务会定时向AM提供自己的状态信息和执行的进度。
8. 作业运行完成后AM会向ASM注销和关闭自己。


