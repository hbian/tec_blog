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

## CDH manager installation

### Setup yum repo

首先下载以下rpm包
https://archive.cloudera.com/cm6/6.1.1/redhat7/yum/RPMS/x86_64/
cloudera-manager-daemons-6.1.1-853290.el7.x86_64.rpm  oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm
cloudera-manager-agent-6.1.1-853290.el7.x86_64.rpm  cloudera-manager-server-6.1.1-853290.el7.x86_64.rpm
https://archive.cloudera.com/cm6/6.1.1/
allkeys.asc
```
setup httpd service
yum -y install httpd createrepo

systemctl start httpd
systemctl enable httpd
然后进入到前面准备好的存放Cloudera Manager RPM包的目录cloudera-repos下：
cd /upload/cloudera-repos/
生成RPM元数据：
createrepo .

然后将cloudera-repos目录移动到httpd的html目录下：
mv cloudera-repos /var/www/html/
确保可以通过浏览器查看到这些RPM包：
img
接着在Cloudera Manager Server主机上创建cm6的repo文件（要把哪个节点作为Cloudera Manager Server节点，就在这个节点上创建repo文件）：
cd /etc/yum.repos.d
vim cloudera-manager.repo
添加如下内容：

[cloudera-manager]
name=Cloudera Manager 6.0.1
baseurl=http://cdh601/cloudera-repos/
gpgcheck=0
enabled=1
保存，退出,然后执行yum clean all && yum makecache命令：
```

### Setup parcel

```
下载CDH-6.1.1-1.cdh6.1.1.p0.875250-el7.parcel, manifest.json
https://archive.cloudera.com/cdh6/6.1.1/parcels/

需要手动用命令生成sha1,下载的无法直接使用而且需重新命名
sha1sum CDH-6.1.1-1.cdh6.1.1.p0.875250-el7.parcel | awk '{ print $1 }' > CDH-6.1.1-1.cdh6.1.1.p0.875250-el7.parcel.sha

manifest.json和.sha缺一不可，否则安装时无法找到parcel文件
```

### Update hostname
```
sudo hostnamectl set-hostname cdhmanager.amcc.tz

# ADD IP address and fully qualified domain name (FQDN) of each host in /etc/hosts
10.72.83.25 cdhmanager.amcc.tz cdhmanager


#Edit /etc/sysconfig/network with the FQDN of this host only
/etc/sysconfig/network
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


### jdk installation
```
sudo yum --nogpgcheck localinstall ./oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm -y
```

### mysql driver installation
```
tar xzvf mysql-connector-java-5.1.47.tar.gz
mkdir -p /usr/share/java/
cd mysql-connector-java-5.1.47
sudo cp mysql-connector-java-5.1.47-bin.jar /usr/share/java/mysql-connector-java.jar
```

### Install Cloudera Manager Server
```
sudo yum --nogpgcheck localinstall ./cloudera-manager-daemons-6.1.1-853290.el7.x86_64.rpm ./cloudera-manager-agent-6.1.1-853290.el7.x86_64.rpm ./cloudera-manager-server-6.1.1-853290.el7.x86_64.rpm -y
```

### Configure DB

```
create database cdhpro
GRANT ALL ON cdhpro.* TO 'cdhpro'@'%' IDENTIFIED BY 'cdhpro123456';

#Install mysql driver
tar xzvf mysql-connector-java-5.1.47.tar.gz
mkdir -p /usr/share/java/
cd mysql-connector-java-5.1.47
sudo cp mysql-connector-java-5.1.47-bin.jar /usr/share/java/mysql-connector-java.jar
```

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
hdfs dfs -mkdir /user/root
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


