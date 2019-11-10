https://www.cloudera.com/documentation/enterprise/6/6.1/topics/installation.html

因公司内网无法访问互联网，本文主要概述如何进行离线安装。

## Cluster Server Sizing and role assignments

[host_role_assignments](https://www.cloudera.com/documentation/enterprise/6/6.1/topics/cm_ig_host_allocations.html#host_role_assignments)
一个CDH cluster大致包括如下4种roles:

Master hosts: run Hadoop master processes such as the HDFS NameNode and YARN Resource Manager.
Utility hosts: run other cluster processes that are not master processes such as Cloudera Manager and the Hive Metastore.
Gateway hosts: are client access points for launching jobs in the cluster. The number of gateway hosts required varies depending on the type and size of the workloads.
Worker hosts: primarily run DataNodes and other distributed processes such as Impalad.

针对我们需要的3 - 10 Worker Hosts without High Availability， 主要会运行spark, hdfs, 后期可能会考虑添加的有hbase， kafka，大致可以如下安排
One master Host: (4C, 4G, 50G) 
NameNode
YARN ResourceManager
JobHistory Server
ZooKeeper
Spark History Server

One host for all Utility and Gateway roles: (4C, 4G, 20G)
Secondary NameNode
Cloudera Manager
Cloudera Manager Management Service
Gateway configuration

3 - 10 Worker Hosts: (8C, 16G, 20G)
DataNode
NodeManager

## CDH Server installation
安装主要分为以下几个步骤
* 安装cdh server 服务器， 配置数据库， 配置parcels
* 安装cdh其他服务器，安装agent,安装parcel，加入集群


### Update hostname
```
sudo hostnamectl set-hostname cdhmanager.amcc.tz

# ADD IP address and fully qualified domain name (FQDN) of each host in /etc/hosts
10.72.83.25 cdhmanager.amcc.tz cdhmanager


#Edit /etc/sysconfig/network with the FQDN of this host only
vim /etc/sysconfig/network
HOSTNAME=cdhmanager.amcc.tz
```

### System optimisation
```
echo never > /sys/kernel/mm/transparent_hugepage/defrag

echo never > /sys/kernel/mm/transparent_hugepage/enabled


echo 1 > /proc/sys/vm/swappiness
sysctl vm.swappiness=1

vim /etc/sysctl.conf
vm.swappiness=1


#Disable the tuned Service
systemctl start tuned
tuned-adm off
tuned-adm list
systemctl stop tuned
systemctl disable tuned

sudo sysctl -w vm.swappiness=1

```


### package installation
```
#Download rpm package
#https://archive.cloudera.com/cm6/6.0.1/redhat7/yum/RPMS/x86_64/
oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm
cloudera-manager-agent-6.0.1-610811.el7.x86_64.rpm
cloudera-manager-daemons-6.0.1-610811.el7.x86_64.rpm

#install jdk
sudo yum --nogpgcheck localinstall ./oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm -y

#install mysql driver
tar xzvf mysql-connector-java-5.1.47.tar.gz
mkdir -p /usr/share/java/
cd mysql-connector-java-5.1.47
sudo cp mysql-connector-java-5.1.47-bin.jar /usr/share/java/mysql-connector-java.jar

### Install Cloudera Manager Server
sudo yum --nogpgcheck localinstall ./cloudera-manager-daemons-6.0.1-610811.el7.x86_64.rpm ./cloudera-manager-agent-6.0.1-610811.el7.x86_64.rpm ./cloudera-manager-server-6.1.1-853290.el7.x86_64.rpm -y
```

### Configure DB

```
create database cdhpro
GRANT ALL ON gauss.* TO 'gauss'@'%' IDENTIFIED BY 'gauss123456';

#Setup database from cdh manager server
/opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h 10.72.84.99 gauss gauss gauss123456
```

### start cloudera-scm-server 和 cloudera-scm-agent
首先cloudera-scm这个用户和组必须建立， 然后上一步中的的配置写在
```
#Check db.properties
cat /etc/cloudera-scm-server/db.properties

#Check log folder owner
[root@cdhmanager tmp]# ll /var/log/|grep cloudera-scm
drwxr-x---  2 cloudera-scm cloudera-scm    204 Jul 17 11:22 cloudera-scm-agent
drwxr-x---  2 cloudera-scm cloudera-scm   4096 Nov  3 05:21 cloudera-scm-server

#start service
sudo systemctl start cloudera-scm-server
tail -f /var/log/cloudera-scm-server/cloudera-scm-server.log
#wait for msg 
2019-11-06 17:40:26,692 INFO WebServerImpl:com.cloudera.server.cmf.WebServerImpl: Started Jetty server.
```

server 启动后， 修改/etc/cloudera-scm-agent/config.ini中
server_host=cdhmanager.gauss.tz， 然后systemctl start cloudera-scm-agent


### Setup parcel
http://10.72.83.167:7180 admin/admin 选择好cdh版本号，开始配置parcel
```
mkdir -p /data/cdh/parcels
下载CDH-6.1.1-1.cdh6.1.1.p0.875250-el7.parcel, manifest.json
https://archive.cloudera.com/cdh6/6.1.1/parcels/

需要手动用命令生成sha1,下载的无法直接使用而且需重新命名
sha1sum CDH-6.0.1-1.cdh6.0.1.p0.590678-el7.parcel | awk '{ print $1 }' >CDH-6.0.1-1.cdh6.0.1.p0.590678-el7.parcel.sha

manifest.json和.sha缺一不可，否则安装时无法找到parcel文件


#在网页中配置parcel文件夹/data/cdh/parcels，如果parcels文件夹找不到查看
/var/log/cloudera-scm-agent/cloudera-scm-agent.log， cloudera-scm-agent负责部分parcels文件的处理

#类似报错可以忽略
[06/Nov/2019 18:36:31 +0000] 19380 MainThread parcel       ERROR    Exception while reading parcel: CDH-6.0.1-1.cdh6.0.1.p0.590678-el7.parcel
Traceback (most recent call last):
  File "/opt/cloudera/cm-agent/lib/python2.7/site-packages/cmf/parcel.py", line 114, in refresh
    fd = open(manifest)

#注意修改文件夹位置后，需要重启cloudera-scm-agent 和 cloudera-scm-server
```


## CDH node installation
server节点安装好后首先安装master节点.
Node 节点重复上面server安装中的Update hostname和 system optimisation步骤，
在package installation中， 安装除了server以外的package，这样提前安装好cloudera-scm-agent，这样在加入node到cluster时可以直接添加避免通过local repo的形式安装agent.

agent安装好后， 加入host to cluster 
http://10.72.83.167:7180/cmf/add-hosts-wizard
然后install parcels


## HIVE
Create a seperated database for hive with latin1 as character set.


### Spark

Spark Shell 刚刚启动时报一个permission problem with an HDFS directory under /user:

```
ERROR spark.SparkContext: Error initializing SparkContext.
org.apache.hadoop.security.AccessControlException: Permission denied:
user=<varname>user_id</varname>, access=WRITE, inode="/user":hdfs:supergroup:drwxr-xr-x
at org.apache.hadoop.hdfs.server.namenode.FSPermissionChecker.check(FSPermissionChecker.java:400)
```

解决办法
```
#新建这个user的路径
sudo -u hdfs hdfs dfs -mkdir /user/root
sudo -u hdfs hadoop fs -chown root /user/root
```

### TIPS
1.manifest.json和.sha缺一不可，否则安装时无法找到parcel文件, 如果一直找不到查看scm server日志
2. 新host 安装agent时DNS反向解析PTR localhost：
```
using localhost as scm server hostname  
BEGIN which python  
/usr/bin/python  
END (0)  
BEGIN python -c 'import socket; import sys; s = socket.socket(socket.AF_INET); s.settimeout(5.0); s.connect((sys.argv[1], int(sys.argv[2]))); s.close();' localhost 7182  
Traceback (most recent call last):  
File "<string>", line 1, in <module>  
File "<string>", line 1, in connect  
socket.error: [Errno 111] Connection refused  
END (1)  
could not contact scm server at localhost:7182, giving up  
``` 
位置原因导致DNS反向解析错误，不能正确解析Cloudera Manager Server主机名。解决方案是 mv /usr/bin/host /usr/bin/host.bak  
3. 在install parcels时如果卡在distributed,需要检查所有host中是否配置了所有节点的host ip
```


