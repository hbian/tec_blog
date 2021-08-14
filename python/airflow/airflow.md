## Quick start
```
#airflow needs a home, ~/airflow is the default,
export AIRFLOW_HOME=~/airflow
# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080 -D
```

## webserver
webserver 是一个守护进程，它接受 HTTP 请求，允许你通过 Python Flask Web 应用程序与 airflow 进行交互，webserver 提供以下功能：

* 中止、恢复、触发任务。
* 监控正在运行的任务，断点续跑任务。
* 执行 ad-hoc 命令或 SQL 语句来查询任务的状态，日志等详细信息。
* 配置连接，包括不限于数据库、ssh 的连接等。

webserver 守护进程使用 gunicorn 服务器（相当于 java 中的 tomcat ）处理并发请求，可通过修改{AIRFLOW_HOME}/airflow.cfg文件中 workers 的值来控制处理并发请求的进程数。
```
#In {AIRFLOW_HOME}/airflow.cfg, Number of workers to run the Gunicorn web server
workers = 4

# start the web server, default port is 8080, deamon mode
airflow webserver -p 8080 -D
```


## scheduler
scheduler是一个守护进程，它周期性地轮询任务的调度计划，以确定是否触发任务执行。
启动的 scheduler 守护进程：
```
airflow scheduler -D 
```

调度器 scheduler 会间隔性的去轮询元数据库（Metastore）已注册的 DAG（有向无环图，可理解为作业流）是否需要被执行。如果一个具体的 DAG 根据其调度计划需要被执行，scheduler 守护进程就会先在元数据库创建一个 DagRun 的实例，并触发 DAG 内部的具体 task（任务，可以这样理解：DAG 包含一个或多个task），触发其实并不是真正的去执行任务，而是推送 task 消息至消息队列（即 broker）中，每一个 task 消息都包含此 task 的 DAG ID，task ID，及具体需要被执行的函数。如果 task 是要执行 bash 脚本，那么 task 消息还会包含 bash 脚本的代码。

用户可能在 webserver 上来控制 DAG，比如手动触发一个 DAG 去执行。当用户这样做的时候，一个DagRun 的实例将在元数据库被创建，scheduler 使同 #1 一样的方法去触发 DAG 中具体的 task 。


## DAG && Task
DAG
DAG 意为有向无循环图，在 Airflow 中则定义了整个完整的作业。同一个 DAG 中的所有 Task 拥有相同的调度时间。
Task
Task 为 DAG 中具体的作业任务，它必须存在于某一个 DAG 之中。Task 在 DAG 中配置依赖关系，跨 DAG 的依赖是可行的，但是并不推荐。跨 DAG 依赖会导致 DAG 图的直观性降低，并给依赖管理带来麻烦。
DAG Run
当一个 DAG 满足它的调度时间，或者被外部触发时，就会产生一个 DAG Run。可以理解为由 DAG 实例化的实例。
Task Instance
当一个 Task 被调度启动时，就会产生一个 Task Instance。可以理解为由 Task 实例化的实例

### Test && debug dag
The dag default folder is  referenced in your airflow.cfg, the default one is
$AIRFLOW_HOME/dags, Put the test dag file in this folder
```
#Validate the code
python3 ./import_ods_debug.py
#List the dag
airflow list_dags
#list the tasks 
airflow list_tasks import_ods_debug
# prints the hierarchy of tasks 
airflow list_tasks import_ods_debug --tree
# Test one task
airflow test import_ods_debug ods_start 2020-03-16

新的dag刚加入时，默认是